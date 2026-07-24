"""文档、问答与反馈 API。路由仅做协议转换，不包含检索算法。"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from app.api.schemas import FeedbackRequest, QueryRequest


router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health(request: Request) -> dict:
    return {"status": "ok", "environment": request.app.state.settings.app_env}


@router.post("/documents", status_code=201)
async def upload_document(request: Request, file: UploadFile = File(...),
                          knowledge_base_id: str = Form("default"), name: str | None = Form(None),
                          metadata: str = Form("{}")) -> dict:
    try:
        parsed_metadata = json.loads(metadata)
        if not isinstance(parsed_metadata, dict):
            raise ValueError
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(422, "metadata 必须是 JSON 对象") from exc
    content = await file.read(request.app.state.settings.max_upload_mb * 1024 * 1024 + 1)
    try:
        return request.app.state.ingestion.ingest(file.filename or "", content, knowledge_base_id,
                                                  name, parsed_metadata)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/documents")
def list_documents(request: Request, knowledge_base_id: str | None = None) -> list[dict]:
    return request.app.state.repository.list_documents(knowledge_base_id)


@router.get("/documents/{document_id}")
def get_document(document_id: str, request: Request) -> dict:
    document = request.app.state.repository.get_document(document_id)
    if not document:
        raise HTTPException(404, "DOCUMENT_NOT_FOUND")
    return document


@router.post("/documents/{document_id}/index")
def rebuild_document(document_id: str, request: Request) -> dict:
    try:
        return request.app.state.ingestion.index(document_id)
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(422, f"DOCUMENT_PARSE_FAILED: {exc}") from exc


@router.delete("/documents/{document_id}", status_code=204)
def delete_document(document_id: str, request: Request) -> None:
    document = request.app.state.repository.delete_document(document_id)
    if not document:
        raise HTTPException(404, "DOCUMENT_NOT_FOUND")
    # storage_uri 来自服务端数据库且指向随机文件名；只删除这一明确文件，不递归删除目录。
    Path(document["storage_uri"]).unlink(missing_ok=True)


@router.post("/query")
def query(payload: QueryRequest, request: Request) -> dict:
    if payload.options.stream:
        raise HTTPException(400, "MVP 暂未实现流式响应，请设置 stream=false")
    return request.app.state.query.answer(payload.knowledge_base_id, payload.question, payload.filters,
                                          payload.options.top_k, payload.options.include_debug)


@router.post("/feedback", status_code=201)
def submit_feedback(payload: FeedbackRequest, request: Request) -> dict:
    if not request.app.state.repository.query_exists(payload.query_id):
        raise HTTPException(404, "QUERY_NOT_FOUND")
    feedback = {"id": str(uuid.uuid4()), **payload.model_dump()}
    request.app.state.repository.save_feedback(feedback)
    return {"feedback_id": feedback["id"], "status": "accepted"}

