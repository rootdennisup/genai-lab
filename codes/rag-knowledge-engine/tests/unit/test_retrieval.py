from app.domain.models import Chunk
from app.retrieval.engine import HashEmbedding, hybrid_search


def make_chunk(chunk_id: str, text: str) -> Chunk:
    return Chunk(id=chunk_id, document_id="doc", knowledge_base_id="kb", sequence=0,
                 content=text, content_hash=chunk_id, token_count=10, title="制度",
                 section_path=[], source_locator={}, metadata={}, vector=HashEmbedding().embed(text))


def test_hybrid_search_puts_matching_chunk_first():
    chunks = [make_chunk("leave", "员工每年享有十天带薪年假"), make_chunk("food", "食堂午餐供应时间为十二点")]
    results = hybrid_search("员工有多少天年假", chunks, 20, 20, 60)
    assert results[0].chunk.id == "leave"
    assert results[0].keyword_score > 0

