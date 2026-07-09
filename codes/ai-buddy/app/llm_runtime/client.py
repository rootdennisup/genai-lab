import httpx

from app.infra.config import qwen_settings, settings
from app.llm_runtime.models import LLMMessage, LLMResponse


class LLMClient:
    """统一的大模型调用入口，业务层只依赖这个类。"""
    
    async def chat(self, messages: list[LLMMessage]) -> LLMResponse:
        # mock 模式用于先跑通本地 API 链路
        if settings.llm_mode == "mock":
            return await self._mock_chat(messages)

        # qwen 模式用于真实调用百炼 Qwen
        if settings.llm_mode == "qwen":
            return await self._qwen_chat(messages)

        raise ValueError(f"Unsupported llm mode: {settings.llm_mode}")

    async def _mock_chat(self, messages: list[LLMMessage]) -> LLMResponse:
        user_message = messages[-1].content

        return LLMResponse(
            content=f"我已经收到你的消息：{user_message}\n\n这是 mock 回复，用来先跑通 AI-Buddy 的聊天链路。",
            model="mock-model",
        )

    async def _qwen_chat(self, messages: list[LLMMessage]) -> LLMResponse:
        if not qwen_settings.api_key:
            raise ValueError("QWEN_API_KEY is missing")

        if not qwen_settings.base_url:
            raise ValueError("QWEN_BASE_URL is missing")

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
                qwen_settings.base_url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        # 这里按 OpenAI-compatible 格式解析。
        # 如果你接入的百炼 Qwen 返回格式不同，只需要改这一小段。
        content = data["choices"][0]["message"]["content"]

        return LLMResponse(
            content=content,
            model=qwen_settings.model,
        )