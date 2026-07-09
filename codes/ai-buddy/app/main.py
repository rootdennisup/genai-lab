from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.infra.config import settings

# FastAPI 应用入口，uvicorn 通过 app.main:app 加载这个对象
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

# 注册聊天相关 API 路由
app.include_router(chat_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """健康检查接口，用于确认服务是否正常启动。"""
    return {"status": "ok"}