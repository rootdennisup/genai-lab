from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.common.logger import logger
from app.conversation.models import ChatRequest, ChatResponse
from app.llm_runtime.client import LLMClient
from app.prompt_engine.builder import PromptBuilder

router = APIRouter(prefix="/api/chat", tags=["chat"])

# MVP 阶段先直接实例化服务对象，后续可以升级为 FastAPI 依赖注入
prompt_builder = PromptBuilder()
llm_client = LLMClient()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """普通聊天 API：等模型完整生成后，一次性返回 JSON。"""
    
    chat_id = request.chat_id or str(uuid4())
    logger.info(
        "Chat request received chat_id={} user_id={} message_length={} persona_set={}",
        chat_id,
        request.user_id,
        len(request.message),
        bool(request.persona),
    )

    # 将业务输入转换成大模型需要的 messages 结构
    messages = prompt_builder.build_chat_messages(
        user_message=request.message,
        persona=request.persona,
    )

    # 通过统一的 LLM Runtime 调用模型，避免 API 层直接依赖具体厂商
    llm_response = await llm_client.chat(messages)
    logger.info(
        "Chat response generated chat_id={} model={} reply_length={}",
        chat_id,
        llm_response.model,
        len(llm_response.content),
    )

    return ChatResponse(
        chat_id=chat_id,
        reply=llm_response.content,
        model=llm_response.model,
    )
    

@router.post("/stream")
async def stream_chat(request: ChatRequest) -> StreamingResponse:
    """流式聊天 API：边生成边返回文本。"""
    logger.info(
        "Stream chat request received chat_id={} user_id={} message_length={} persona_set={}",
        request.chat_id,
        request.user_id,
        len(request.message),
        bool(request.persona),
    )
    messages = prompt_builder.build_chat_messages(
        user_message=request.message,
        persona=request.persona,
    )

    return StreamingResponse(
        llm_client.stream_chat(messages),
        media_type="text/plain; charset=utf-8",
    )
    

## 1.项目根目录运行：uvicorn app.main:app --reload
## 2.浏览器访问：http://127.0.0.1:8000/docs
## 3.浏览器页面流式对话：http://127.0.0.1:8000/
