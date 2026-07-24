"""不安装 LlamaIndex 也能验证防腐层的字段映射。"""

from dataclasses import dataclass, field
from pathlib import Path

from app.ingestion.parsers_llama import _documents_to_blocks


@dataclass
class FakeLlamaDocument:
    text: str
    metadata: dict = field(default_factory=dict)

    def get_content(self) -> str:
        return self.text


def test_llama_document_is_mapped_to_domain_block():
    documents = [FakeLlamaDocument("  企业知识正文  ", {"title": "制度章节", "internal": "不要透传"})]
    blocks = _documents_to_blocks(
        documents,
        Path("policy.pdf"),
        locator_factory=lambda metadata, index: {"page_start": index, "page_end": index},
    )

    assert blocks[0].text == "企业知识正文"
    assert blocks[0].title == "制度章节"
    assert blocks[0].section_path == ["制度章节"]
    assert blocks[0].locator == {"page_start": 1, "page_end": 1}
    assert "internal" not in blocks[0].locator

