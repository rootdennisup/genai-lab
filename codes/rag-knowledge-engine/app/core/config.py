"""集中管理应用配置。

教学提示：把检索参数放到配置而不是散落在算法代码中，后续才能使用评估集
系统地调优，而不是凭感觉反复修改魔法数字。
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class Settings:
    """只包含 MVP 所需配置；所有相对路径均相对于项目根目录解析。"""

    app_env: str = os.getenv("APP_ENV", "development")
    database_path: Path = PROJECT_ROOT / os.getenv("DATABASE_PATH", "data/rag.db")
    object_store_path: Path = PROJECT_ROOT / os.getenv("OBJECT_STORE_PATH", "data/uploads")
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "20"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "80"))
    keyword_top_k: int = int(os.getenv("KEYWORD_TOP_K", "20"))
    vector_top_k: int = int(os.getenv("VECTOR_TOP_K", "20"))
    context_top_k: int = int(os.getenv("CONTEXT_TOP_K", "6"))
    rrf_k: int = int(os.getenv("RRF_K", "60"))
    # 0.18 是本地轻量 Rerank 的保守起点，最终必须用正/负评估集重新标定。
    min_evidence_score: float = float(os.getenv("MIN_EVIDENCE_SCORE", "0.18"))


@lru_cache
def get_settings() -> Settings:
    """缓存不可变配置，确保同一进程内各模块看到一致的参数。"""

    return Settings()
