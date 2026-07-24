"""API 输入模型；把不可信请求挡在应用服务边界之外。"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class QueryOptions(BaseModel):
    top_k: int | None = Field(default=None, ge=1, le=20)
    include_debug: bool = False
    stream: bool = False


class QueryRequest(BaseModel):
    knowledge_base_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=2, max_length=2000)
    filters: dict[str, Any] = Field(default_factory=dict)
    options: QueryOptions = Field(default_factory=QueryOptions)


class FeedbackRequest(BaseModel):
    query_id: str
    rating: Literal["positive", "negative"]
    reason_codes: list[str] = Field(default_factory=list)
    comment: str = Field(default="", max_length=2000)
    expected_answer: str | None = None
    created_by: str = Field(default="anonymous", max_length=100)

