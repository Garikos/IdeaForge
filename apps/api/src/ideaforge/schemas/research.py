"""Research request/response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500, description="Поисковый запрос")
    sources: list[str] = Field(
        default=["google_trends", "hackernews", "github"],
        description="Список источников для исследования",
    )
    llm_provider: str = Field(default="groq", description="LLM провайдер")


class ResearchRunResponse(BaseModel):
    run_id: str
    status: str
    query: str
    sources: list[str]
    llm_provider: str
    created_at: datetime


class IdeaResponse(BaseModel):
    id: int
    title: str
    summary: str
    source: str
    source_url: str | None = None
    business_potential: float | None = None
    market_size_score: float | None = None
    competition_score: float | None = None
    sentiment_score: float | None = None
    composite_score: float | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class IdeaListResponse(BaseModel):
    items: list[IdeaResponse]
    total: int
