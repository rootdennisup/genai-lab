"""不依赖第三方 RAG 框架的 Hybrid Search 实现。

本地哈希向量不是生产级语义模型，它的价值是让数据链路完全离线可运行，并清楚展示
EmbeddingProvider 的边界。接入真实模型时只需替换 ``embed`` 的实现。
"""

from __future__ import annotations

import hashlib
import math
from collections import Counter, defaultdict

from app.domain.models import Chunk, RetrievedChunk


def _terms(text: str) -> list[str]:
    from app.ingestion.chunker import tokenize
    return tokenize(text)


class HashEmbedding:
    dimension = 256
    model_name = "local-hash-embedding"

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        for term in _terms(text):
            digest = hashlib.blake2b(term.encode("utf-8"), digest_size=8).digest()
            index = int.from_bytes(digest, "big") % self.dimension
            sign = 1.0 if digest[0] & 1 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=False))


def hybrid_search(question: str, chunks: list[Chunk], keyword_top_k: int,
                  vector_top_k: int, rrf_k: int) -> list[RetrievedChunk]:
    if not chunks:
        return []
    query_terms = _terms(question)
    query_counts = Counter(query_terms)
    document_terms = [Counter(_terms(chunk.content + " " + chunk.title)) for chunk in chunks]
    document_frequency = Counter(term for counts in document_terms for term in counts)
    average_length = sum(sum(counts.values()) for counts in document_terms) / len(chunks)

    keyword_scores: list[tuple[int, float]] = []
    for index, counts in enumerate(document_terms):
        length = sum(counts.values())
        score = 0.0
        for term in query_counts:
            frequency = counts[term]
            if not frequency:
                continue
            # 标准 BM25 的 IDF + 长度归一化；标题已加入待检索文本。
            idf = math.log(1 + (len(chunks) - document_frequency[term] + 0.5) /
                           (document_frequency[term] + 0.5))
            score += idf * frequency * 2.2 / (frequency + 1.2 * (0.25 + 0.75 * length / average_length))
        keyword_scores.append((index, score))
    keyword_ranked = sorted(keyword_scores, key=lambda item: item[1], reverse=True)[:keyword_top_k]

    query_vector = HashEmbedding().embed(question)
    vector_ranked = sorted(enumerate(_cosine(query_vector, chunk.vector) for chunk in chunks),
                           key=lambda item: item[1], reverse=True)[:vector_top_k]

    results: dict[int, RetrievedChunk] = {}
    for rank, (index, score) in enumerate(keyword_ranked, 1):
        if score <= 0:
            continue
        item = results.setdefault(index, RetrievedChunk(chunk=chunks[index]))
        item.keyword_score = score
        item.fusion_score += 1 / (rrf_k + rank)
    for rank, (index, score) in enumerate(vector_ranked, 1):
        if score <= 0:
            continue
        item = results.setdefault(index, RetrievedChunk(chunk=chunks[index]))
        item.vector_score = score
        item.fusion_score += 1 / (rrf_k + rank)

    query_set = set(query_terms)
    for item in results.values():
        content_set = set(_terms(item.chunk.content + " " + item.chunk.title))
        coverage = len(query_set & content_set) / max(1, len(query_set))
        # 本地 Rerank 综合词项覆盖、向量相似度与融合分；可降级且保留各阶段得分。
        item.rerank_score = 0.55 * coverage + 0.30 * max(0.0, item.vector_score) + 0.15 * min(1.0, item.keyword_score)
    return sorted(results.values(), key=lambda item: (item.rerank_score, item.fusion_score), reverse=True)

