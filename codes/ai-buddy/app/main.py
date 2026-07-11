from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router
from app.common.logger import logger, setup_logger
from app.infra.config import settings

setup_logger()

# FastAPI 应用入口
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

logger.info("AI-Buddy app initialized app_name={} llm_mode={}", settings.app_name, settings.llm_mode)

# 注册聊天相关 API 路由
app.include_router(chat_router)

# 挂载静态页面目录，用来放简易聊天页面
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def index() -> FileResponse:
    """浏览器访问根路径时，返回简易聊天页面。"""
    logger.info("Serving chat page")
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """健康检查接口，用于确认服务是否正常启动。"""
    logger.debug("Health check requested")
    return {"status": "ok"}
