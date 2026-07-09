from uuid import uuid4

from fastapi import APIRouter

from app.conversation.models import ChatRequest, ChatResponse
from app.llm_runtime.client import LLMClient
from app.prompt_engine.builder import PromptBuilder

router = APIRouter(prefix="/api/chat", tags=["chat"])

# MVP 阶段先直接实例化服务对象，后续可以升级为 FastAPI 依赖注入
prompt_builder = PromptBuilder()
llm_client = LLMClient()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """聊天 API：接收用户输入，构建 Prompt，调用大模型并返回回复。"""
    chat_id = request.chat_id or str(uuid4())

    # 将业务输入转换成大模型需要的 messages 结构
    messages = prompt_builder.build_chat_messages(
        user_message=request.message,
        persona=request.persona,
    )

    # 通过统一的 LLM Runtime 调用模型，避免 API 层直接依赖具体厂商
    llm_response = await llm_client.chat(messages)

    return ChatResponse(
        chat_id=chat_id,
        reply=llm_response.content,
        model=llm_response.model,
    )