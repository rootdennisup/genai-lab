import json
import httpx

from app.common.logger import logger
from app.infra.config import qwen_settings, settings
from app.llm_runtime.models import LLMMessage, LLMResponse
from app.llm_runtime.retry import SoftFailureError, RetryConfig, retry_async


class LLMClient:
    """统一的大模型调用入口，业务层只依赖这个类。"""
    
    async def chat(self, messages: list[LLMMessage]) -> LLMResponse:
        """非流式聊天入口：用于测试。"""
        logger.info("LLM chat started mode={} message_count={}", settings.llm_mode, len(messages))
        # mock 模式用于先跑通本地 API 链路
        if settings.llm_mode == "mock":
            return await self._mock_chat(messages)

        # qwen 模式用于真实调用百炼 Qwen
        if settings.llm_mode == "qwen":
            return await self._qwen_chat(messages)

        raise ValueError(f"Unsupported llm mode: {settings.llm_mode}")
    
    
    async def stream_chat(self, messages: list[LLMMessage]):
        """流式聊天入口：逐段产出模型生成的文本。"""
        logger.info("LLM stream chat started mode={} message_count={}", settings.llm_mode, len(messages))
        if settings.llm_mode == "mock":
            async for chunk in self._mock_stream_chat(messages):
                yield chunk
            return

        if settings.llm_mode == "qwen":
            async for chunk in self._qwen_stream_chat(messages):
                yield chunk
            return

        raise ValueError(f"Unsupported llm mode: {settings.llm_mode}")
    

    async def _mock_chat(self, messages: list[LLMMessage]) -> LLMResponse:
        user_message = messages[-1].content
        logger.info("Mock chat invoked user_message_length={}", len(user_message))

        return LLMResponse(
            content=f"我已经收到你的消息：{user_message}\n\n这是 mock 回复，用来先跑通 AI-Buddy 的聊天链路。",
            model="mock-model",
        )
        
    async def _mock_stream_chat(self, messages: list[LLMMessage]):
        user_message = messages[-1].content
        logger.info("Mock stream chat invoked user_message_length={}", len(user_message))
        chunks = [
            "我已经收到你的消息：",
            user_message,
            "\n\n",
            "这是 mock 流式回复，用来测试 AI-Buddy 的流式链路。",
        ]

        for chunk in chunks:
            yield chunk

    async def _qwen_chat(self, messages: list[LLMMessage]) -> LLMResponse:
        if not qwen_settings.api_key:
            logger.error("Qwen API key is missing")
            raise ValueError("QWEN_API_KEY is missing")

        if not qwen_settings.base_url:
            logger.error("Qwen base URL is missing")
            raise ValueError("QWEN_BASE_URL is missing")

        async def operation() -> LLMResponse:
            logger.info("Qwen non-stream request started model={}", qwen_settings.model)
            payload = {
                "model": qwen_settings.model,
                "messages": [
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                    for message in messages
                ],
                "temperature": 0.7,
            }

            headers = {
                "Authorization": f"Bearer {qwen_settings.api_key}",
                "Content-Type": "application/json",
            }

            async with httpx.AsyncClient(timeout=qwen_settings.timeout) as client:
                response = await client.post(
                    qwen_settings.chat_completions_url,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                logger.info("Qwen non-stream response received status_code={}", response.status_code)

            choices = data.get("choices") or []

            if not choices:
                logger.warning("Qwen non-stream soft failure: choices is empty")
                raise SoftFailureError("Qwen response choices is empty")

            message = choices[0].get("message") or {}
            content = message.get("content")

            if not content or not content.strip():
                logger.warning("Qwen non-stream soft failure: content is empty")
                raise SoftFailureError("Qwen response content is empty")

            logger.info("Qwen non-stream content parsed content_length={}", len(content))
            return LLMResponse(
                content=content,
                model=qwen_settings.model,
            )

        return await retry_async(
            operation,
            RetryConfig(
                max_attempts=3,
                base_delay=0.8,
                max_delay=6.0,
            ),
        )
    
        
    async def _qwen_stream_chat(self, messages: list[LLMMessage]):
        if not qwen_settings.api_key:
            logger.error("Qwen API key is missing")
            raise ValueError("QWEN_API_KEY is missing")

        if not qwen_settings.base_url:
            logger.error("Qwen base URL is missing")
            raise ValueError("QWEN_BASE_URL is missing")

        logger.info("Qwen stream request started model={}", qwen_settings.model)
        payload = {
            "model": qwen_settings.model,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ],
            "temperature": 0.7,
            "stream": True,
        }

        headers = {
            "Authorization": f"Bearer {qwen_settings.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=qwen_settings.timeout) as client:
            async with client.stream(
                "POST",
                qwen_settings.chat_completions_url,
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                logger.info("Qwen stream response connected status_code={}", response.status_code)

                async for line in response.aiter_lines():
                    if not line:
                        continue

                    if not line.startswith("data: "):
                        continue

                    data = line.removeprefix("data: ").strip()

                    if data == "[DONE]":
                        break

                    try:
                        chunk_data = json.loads(data)
                    except json.JSONDecodeError:
                        logger.warning("Qwen stream chunk JSON decode failed")
                        continue

                    choices = chunk_data.get("choices") or []

                    # 有些流式 chunk 只携带 usage / metadata，不携带正文 token
                    if not choices:
                        logger.debug("Qwen stream chunk skipped because choices is empty")
                        continue

                    choice = choices[0]
                    delta = choice.get("delta") or {}
                    content = delta.get("content")

                    if content:
                        yield content

                logger.info("Qwen stream response finished")
