"""结构优先、长度兜底的 Chunk 切分器。"""

from __future__ import annotations

import hashlib
import re
import uuid

from app.domain.models import Chunk, ParsedBlock
from app.retrieval.engine import HashEmbedding


def tokenize(text: str) -> list[str]:
    """用于教学版检索的轻量 tokenizer：中文按字/双字，英文按单词。"""
    text = text.lower()
    words = re.findall(r"[a-z0-9_]+", text)
    chinese = re.findall(r"[\u4e00-\u9fff]", text)
    return words + chinese + ["".join(chinese[i:i + 2]) for i in range(max(0, len(chinese) - 1))]


def chunk_blocks(blocks: list[ParsedBlock], document_id: str, knowledge_base_id: str,
                 metadata: dict, chunk_size: int, overlap: int) -> list[Chunk]:
    """按近似 token 数切分，并给每块生成可重建的稳定 ID。"""
    chunks: list[Chunk] = []
    embedder = HashEmbedding()
    # 不依赖具体模型 tokenizer 时，以“约 2 个字符≈1 token”做保守估算。
    # 直接截取原文，避免在中文字符之间人为插入空格、破坏引用摘录。
    window_size = max(1, chunk_size * 2)
    step = max(1, (chunk_size - overlap) * 2)
    for block in blocks:
        if not block.text.strip():
            continue
        for start in range(0, len(block.text), step):
            content = block.text[start:start + window_size].strip()
            if not content:
                continue
            digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
            # UUID5 基于文档、位置和内容生成；相同版本重建时 ID 不漂移。
            chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{document_id}:{start}:{digest}"))
            chunks.append(Chunk(id=chunk_id, document_id=document_id,
                                knowledge_base_id=knowledge_base_id, sequence=len(chunks),
                                content=content, content_hash=digest,
                                token_count=max(1, len(content) // 2), title=block.title,
                                section_path=block.section_path,
                                source_locator=block.locator, metadata=metadata,
                                vector=embedder.embed(content)))
            if start + window_size >= len(block.text):
                break
    return chunks
