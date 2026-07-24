"""FastAPI 应用装配入口。运行：``uvicorn app.main:app --reload``。"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.application.services import IngestionService, QueryService
from app.core.config import PROJECT_ROOT, get_settings
from app.infrastructure.database import SQLiteRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    repository = SQLiteRepository(settings.database_path)
    repository.initialize()
    app.state.settings = settings
    app.state.repository = repository
    app.state.ingestion = IngestionService(repository, settings)
    app.state.query = QueryService(repository, settings)
    yield


app = FastAPI(title="RAG Knowledge Engine", version="0.1.0", lifespan=lifespan)
app.include_router(router)
static_dir = PROJECT_ROOT / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.exception_handler(Exception)
async def unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    """统一兜底结构；不向客户端泄露本地路径、密钥或堆栈。"""
    trace_id = request.headers.get("x-trace-id", str(uuid.uuid4()))
    return JSONResponse(status_code=500, content={"error": {"code": "INTERNAL_ERROR",
        "message": "服务处理失败，请使用 trace_id 查询日志", "details": {}, "trace_id": trace_id}})
