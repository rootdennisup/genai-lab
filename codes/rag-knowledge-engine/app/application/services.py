"""上传索引和问答用例。

应用层只编排“先做什么、失败后如何更新状态”，算法细节留在 ingestion/retrieval，
持久化细节留在 infrastructure。这正是模块化单体最关键的分层方式。
"""

from __future__ import annotations

import hashlib
import re
import time
import uuid
from pathlib import Path
from typing import Any

from app.core.config import Settings
from app.domain.models import DocumentStatus, RetrievedChunk
from app.infrastructure.database import SQLiteRepository
from app.ingestion.chunker import chunk_blocks
from app.ingestion.parsers import parse_document
from app.retrieval.engine import hybrid_search


SUPPORTED_TYPES = {".pdf": "pdf", ".docx": "docx", ".xlsx": "xlsx", ".md": "md", ".markdown": "md"}


class IngestionService:
    def __init__(self, repository: SQLiteRepository, settings: Settings) -> None:
        self.repository, self.settings = repository, settings

    def ingest(self, file_name: str, content: bytes, knowledge_base_id: str,
               name: str | None, metadata: dict[str, Any]) -> dict[str, Any]:
        suffix = Path(file_name).suffix.lower()
        if suffix not in SUPPORTED_TYPES:
            raise ValueError("UNSUPPORTED_FILE_TYPE: 仅支持 PDF、DOCX、XLSX、Markdown")
        if not content:
            raise ValueError("EMPTY_FILE: 上传文件不能为空")
        if len(content) > self.settings.max_upload_mb * 1024 * 1024:
            raise ValueError(f"FILE_TOO_LARGE: 文件不能超过 {self.settings.max_upload_mb} MB")

        document_id = str(uuid.uuid4())
        checksum = hashlib.sha256(content).hexdigest()
        self.settings.object_store_path.mkdir(parents=True, exist_ok=True)
        # 存储名只使用服务端 UUID 和白名单扩展名，避免目录穿越与文件名覆盖。
        storage_path = self.settings.object_store_path / f"{document_id}{suffix}"
        storage_path.write_bytes(content)
        document = {"id": document_id, "knowledge_base_id": knowledge_base_id,
                    "name": name or Path(file_name).stem, "file_name": Path(file_name).name,
                    "file_type": SUPPORTED_TYPES[suffix], "storage_uri": str(storage_path),
                    "checksum": checksum, "status": DocumentStatus.UPLOADED, "metadata": metadata}
        self.repository.create_document(document)
        return self.index(document_id)

    def index(self, document_id: str) -> dict[str, Any]:
        document = self.repository.get_document(document_id)
        if not document:
            raise LookupError("DOCUMENT_NOT_FOUND")
        self.repository.update_document_status(document_id, DocumentStatus.PROCESSING)
        try:
            blocks = parse_document(Path(document["storage_uri"]), document["file_type"])
            chunks = chunk_blocks(blocks, document_id, document["knowledge_base_id"], document["metadata"],
                                  self.settings.chunk_size, self.settings.chunk_overlap)
            if not chunks:
                raise ValueError("DOCUMENT_PARSE_FAILED: 文档没有可索引文本")
            self.repository.replace_chunks(document_id, chunks)
            self.repository.update_document_status(document_id, DocumentStatus.READY)
        except Exception as exc:
            self.repository.update_document_status(document_id, DocumentStatus.FAILED, str(exc))
            raise
        result = self.repository.get_document(document_id) or document
        result["chunk_count"] = len(chunks)
        return result


class QueryService:
    def __init__(self, repository: SQLiteRepository, settings: Settings) -> None:
        self.repository, self.settings = repository, settings

    @staticmethod
    def _normalize(question: str) -> str:
        return re.sub(r"\s+", " ", question).strip()

    def answer(self, knowledge_base_id: str, question: str, filters: dict[str, Any],
               top_k: int | None, include_debug: bool) -> dict[str, Any]:
        started = time.perf_counter()
        query_id = str(uuid.uuid4())
        normalized = self._normalize(question)
        retrieval_started = time.perf_counter()
        chunks = self.repository.list_chunks(knowledge_base_id, filters)
        ranked = hybrid_search(normalized, chunks, self.settings.keyword_top_k,
                               self.settings.vector_top_k, self.settings.rrf_k)
        retrieval_ms = round((time.perf_counter() - retrieval_started) * 1000, 2)
        limit = min(max(top_k or self.settings.context_top_k, 1), 20)
        selected = ranked[:limit]

        # 多层拒答的第一版：无候选、最高重排相关度不足，或完全没有词项/向量证据。
        enough = bool(selected and selected[0].rerank_score >= self.settings.min_evidence_score
                      and (selected[0].keyword_score > 0 or selected[0].vector_score >= 0.20))
        if enough:
            answer, citations = self._extractive_answer(selected)
            refused, refusal_reason = False, None
        else:
            answer = "当前知识库中没有找到足够信息回答该问题。请补充更具体的关键词，或确认相关文档已上传并完成索引。"
            citations, refused, refusal_reason = [], True, "insufficient_evidence"

        total_ms = round((time.perf_counter() - started) * 1000, 2)
        latency = {"retrieval": retrieval_ms, "rerank": 0.0, "generation": 0.0, "total": total_ms}
        debug = {"candidate_count": len(ranked), "context_chunk_ids": [item.chunk.id for item in selected],
                 "results": [self._debug_item(item) for item in ranked[:20]]}
        response = {"query_id": query_id, "answer": answer, "refused": refused,
                    "refusal_reason": refusal_reason, "citations": citations,
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "latency_ms": latency}
        self.repository.save_query_log({**response, "knowledge_base_id": knowledge_base_id,
                                        "question": question, "normalized_query": normalized,
                                        "filters": filters, "debug": debug})
        if include_debug:
            response["debug"] = debug
        return response

    def _extractive_answer(self, selected: list[RetrievedChunk]) -> tuple[str, list[dict[str, Any]]]:
        """默认抽取证据原文，杜绝未配置 LLM 时凭空生成企业事实。"""
        citations, paragraphs = [], []
        for number, item in enumerate(selected[:3], 1):
            chunk = item.chunk
            document = self.repository.get_document(chunk.document_id) or {}
            citation_id = f"S{number}"
            quote = chunk.content[:360]
            paragraphs.append(f"{quote} [{citation_id}]")
            citations.append({"citation_id": citation_id, "chunk_id": chunk.id,
                              "document_id": chunk.document_id, "file_name": document.get("file_name", ""),
                              "title": chunk.title, **chunk.source_locator, "quote": quote})
        return "\n\n".join(paragraphs), citations

    @staticmethod
    def _debug_item(item: RetrievedChunk) -> dict[str, Any]:
        return {"chunk_id": item.chunk.id, "document_id": item.chunk.document_id,
                "title": item.chunk.title, "keyword_score": round(item.keyword_score, 6),
                "vector_score": round(item.vector_score, 6), "fusion_score": round(item.fusion_score, 6),
                "rerank_score": round(item.rerank_score, 6), "preview": item.chunk.content[:160]}

