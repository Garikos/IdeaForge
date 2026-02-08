"""BusinessIdea model."""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class IdeaStatus(str, enum.Enum):
    discovered = "discovered"
    analyzed = "analyzed"
    planned = "planned"
    selected = "selected"
    in_progress = "in_progress"


class BusinessIdea(Base):
    __tablename__ = "business_ideas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(2000))

    business_potential: Mapped[float | None] = mapped_column(Float)
    market_size_score: Mapped[float | None] = mapped_column(Float)
    competition_score: Mapped[float | None] = mapped_column(Float)
    sentiment_score: Mapped[float | None] = mapped_column(Float)
    composite_score: Mapped[float | None] = mapped_column(Float)

    status: Mapped[IdeaStatus] = mapped_column(
        Enum(IdeaStatus), default=IdeaStatus.discovered
    )
    raw_data: Mapped[dict | None] = mapped_column(JSONB)
    analysis_data: Mapped[dict | None] = mapped_column(JSONB)

    research_run_id: Mapped[str | None] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
