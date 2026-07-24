"""RAG 核心领域对象。

这些对象刻意不引用 Web 框架或 SQLite，使解析器、检索器和模型供应商都可以替换。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class DocumentStatus(StrEnum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


@dataclass(slots=True)
class ParsedBlock:
    """解析后的结构块；locator 保存页码、章节、工作表行号等定位信息。"""

    text: str
    title: str = ""
    section_path: list[str] = field(default_factory=list)
    locator: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Chunk:
    id: str
    document_id: str
    knowledge_base_id: str
    sequence: int
    content: str
    content_hash: str
    token_count: int
    title: str
    section_path: list[str]
    source_locator: dict[str, Any]
    metadata: dict[str, Any]
    vector: list[float]


@dataclass(slots=True)
class RetrievedChunk:
    chunk: Chunk
    keyword_score: float = 0.0
    vector_score: float = 0.0
    fusion_score: float = 0.0
    rerank_score: float = 0.0

