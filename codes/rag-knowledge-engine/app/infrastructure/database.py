"""SQLite 元数据仓库。

MVP 把 Chunk 正文、向量和问答轨迹放在同一数据库中，便于学习和调试。
生产环境可分别替换为 PostgreSQL、OpenSearch 与 Qdrant，而不改变应用服务流程。
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator

from app.domain.models import Chunk


class SQLiteRepository:
    def __init__(self, path: Path) -> None:
        self.path = path

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY, knowledge_base_id TEXT NOT NULL, name TEXT NOT NULL,
                    file_name TEXT NOT NULL, file_type TEXT NOT NULL, storage_uri TEXT NOT NULL,
                    checksum TEXT NOT NULL, status TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 1,
                    metadata_json TEXT NOT NULL, error_message TEXT,
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_documents_kb ON documents(knowledge_base_id);
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY, document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                    knowledge_base_id TEXT NOT NULL, sequence INTEGER NOT NULL, content TEXT NOT NULL,
                    content_hash TEXT NOT NULL, token_count INTEGER NOT NULL, title TEXT NOT NULL,
                    section_path_json TEXT NOT NULL, locator_json TEXT NOT NULL,
                    metadata_json TEXT NOT NULL, vector_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_chunks_kb ON chunks(knowledge_base_id);
                CREATE TABLE IF NOT EXISTS query_logs (
                    query_id TEXT PRIMARY KEY, knowledge_base_id TEXT NOT NULL, question TEXT NOT NULL,
                    normalized_query TEXT NOT NULL, filters_json TEXT NOT NULL, debug_json TEXT NOT NULL,
                    answer TEXT NOT NULL, citations_json TEXT NOT NULL, refused INTEGER NOT NULL,
                    refusal_reason TEXT, latency_json TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS feedback (
                    id TEXT PRIMARY KEY, query_id TEXT NOT NULL REFERENCES query_logs(query_id),
                    rating TEXT NOT NULL, reason_codes_json TEXT NOT NULL, comment TEXT NOT NULL,
                    expected_answer TEXT, created_by TEXT NOT NULL, created_at TEXT NOT NULL
                );
                """
            )

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat()

    def create_document(self, document: dict[str, Any]) -> None:
        now = self._now()
        with self.connect() as db:
            db.execute(
                """INSERT INTO documents
                (id, knowledge_base_id, name, file_name, file_type, storage_uri, checksum,
                 status, metadata_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (document["id"], document["knowledge_base_id"], document["name"],
                 document["file_name"], document["file_type"], document["storage_uri"],
                 document["checksum"], document["status"], json.dumps(document["metadata"], ensure_ascii=False),
                 now, now),
            )

    def update_document_status(self, document_id: str, status: str, error: str | None = None) -> None:
        with self.connect() as db:
            db.execute("UPDATE documents SET status=?, error_message=?, updated_at=? WHERE id=?",
                       (status, error, self._now(), document_id))

    def get_document(self, document_id: str) -> dict[str, Any] | None:
        with self.connect() as db:
            row = db.execute("SELECT * FROM documents WHERE id=?", (document_id,)).fetchone()
        return self._document_dict(row) if row else None

    def list_documents(self, knowledge_base_id: str | None = None) -> list[dict[str, Any]]:
        sql, params = "SELECT * FROM documents", ()
        if knowledge_base_id:
            sql, params = sql + " WHERE knowledge_base_id=?", (knowledge_base_id,)
        with self.connect() as db:
            rows = db.execute(sql + " ORDER BY created_at DESC", params).fetchall()
        return [self._document_dict(row) for row in rows]

    @staticmethod
    def _document_dict(row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        result["metadata"] = json.loads(result.pop("metadata_json"))
        return result

    def replace_chunks(self, document_id: str, chunks: list[Chunk]) -> None:
        """先删后写让重建索引保持幂等，不会产生重复 Chunk。"""
        with self.connect() as db:
            db.execute("DELETE FROM chunks WHERE document_id=?", (document_id,))
            db.executemany(
                """INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [(c.id, c.document_id, c.knowledge_base_id, c.sequence, c.content,
                  c.content_hash, c.token_count, c.title,
                  json.dumps(c.section_path, ensure_ascii=False),
                  json.dumps(c.source_locator, ensure_ascii=False),
                  json.dumps(c.metadata, ensure_ascii=False), json.dumps(c.vector)) for c in chunks],
            )

    def list_chunks(self, knowledge_base_id: str, filters: dict[str, Any] | None = None) -> list[Chunk]:
        with self.connect() as db:
            rows = db.execute("SELECT * FROM chunks WHERE knowledge_base_id=?", (knowledge_base_id,)).fetchall()
        chunks = [self._chunk(row) for row in rows]
        # 教学版在内存中过滤；生产版必须把权限条件下推到搜索引擎/向量库查询中。
        if filters:
            chunks = [c for c in chunks if all(self._matches(c.metadata.get(k), v) for k, v in filters.items())]
        return chunks

    @staticmethod
    def _matches(actual: Any, expected: Any) -> bool:
        if isinstance(expected, list):
            return actual in expected or (isinstance(actual, list) and bool(set(actual) & set(expected)))
        return actual == expected

    @staticmethod
    def _chunk(row: sqlite3.Row) -> Chunk:
        return Chunk(id=row["id"], document_id=row["document_id"],
                     knowledge_base_id=row["knowledge_base_id"], sequence=row["sequence"],
                     content=row["content"], content_hash=row["content_hash"],
                     token_count=row["token_count"], title=row["title"],
                     section_path=json.loads(row["section_path_json"]),
                     source_locator=json.loads(row["locator_json"]),
                     metadata=json.loads(row["metadata_json"]), vector=json.loads(row["vector_json"]))

    def delete_document(self, document_id: str) -> dict[str, Any] | None:
        document = self.get_document(document_id)
        if document:
            with self.connect() as db:
                db.execute("DELETE FROM documents WHERE id=?", (document_id,))
        return document

    def save_query_log(self, log: dict[str, Any]) -> None:
        with self.connect() as db:
            db.execute("""INSERT INTO query_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (log["query_id"], log["knowledge_base_id"], log["question"], log["normalized_query"],
                        json.dumps(log["filters"], ensure_ascii=False), json.dumps(log["debug"], ensure_ascii=False),
                        log["answer"], json.dumps(log["citations"], ensure_ascii=False), int(log["refused"]),
                        log.get("refusal_reason"), json.dumps(log["latency_ms"]), self._now()))

    def query_exists(self, query_id: str) -> bool:
        with self.connect() as db:
            return db.execute("SELECT 1 FROM query_logs WHERE query_id=?", (query_id,)).fetchone() is not None

    def save_feedback(self, feedback: dict[str, Any]) -> None:
        with self.connect() as db:
            db.execute("INSERT INTO feedback VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (feedback["id"], feedback["query_id"], feedback["rating"],
                        json.dumps(feedback["reason_codes"], ensure_ascii=False), feedback["comment"],
                        feedback.get("expected_answer"), feedback["created_by"], self._now()))
