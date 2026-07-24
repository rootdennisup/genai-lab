from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import app


def test_markdown_upload_query_and_refusal(tmp_path: Path):
    """用一条正样本和一条负样本验证完整链路及拒答边界。"""
    settings = Settings(database_path=tmp_path / "rag.db", object_store_path=tmp_path / "uploads",
                        min_evidence_score=0.18)
    with TestClient(app) as client:
        # lifespan 已完成默认装配；测试改用临时仓库以避免污染本地开发数据。
        from app.application.services import IngestionService, QueryService
        from app.infrastructure.database import SQLiteRepository
        repository = SQLiteRepository(settings.database_path)
        repository.initialize()
        app.state.settings = settings
        app.state.repository = repository
        app.state.ingestion = IngestionService(repository, settings)
        app.state.query = QueryService(repository, settings)

        upload = client.post("/api/v1/documents", data={"knowledge_base_id": "hr"},
                             files={"file": ("leave.md", "# 年假\n员工每年享有十天带薪年假。", "text/markdown")})
        assert upload.status_code == 201
        answer = client.post("/api/v1/query", json={"knowledge_base_id": "hr", "question": "员工年假有多少天？"})
        assert answer.status_code == 200
        assert answer.json()["refused"] is False
        assert answer.json()["citations"][0]["file_name"] == "leave.md"

        refused = client.post("/api/v1/query", json={"knowledge_base_id": "hr", "question": "火星基地预算金额？"})
        assert refused.json()["refused"] is True

