"""Research API endpoints."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from ...models.database import get_session
from ...models.idea import BusinessIdea
from ...schemas.research import (
    IdeaListResponse,
    IdeaResponse,
    ResearchRequest,
    ResearchRunResponse,
)

router = APIRouter(tags=["research"])


@router.post("/research", response_model=ResearchRunResponse)
async def start_research(
    req: ResearchRequest,
    background_tasks: BackgroundTasks,
):
    """Start a new research run."""
    run_id = str(uuid.uuid4())[:8]

    # Import here to avoid circular imports
    from ...services.research_service import run_research_pipeline

    background_tasks.add_task(
        run_research_pipeline,
        run_id=run_id,
        query=req.query,
        sources=req.sources,
        llm_provider=req.llm_provider,
    )

    return ResearchRunResponse(
        run_id=run_id,
        status="started",
        query=req.query,
        sources=req.sources,
        llm_provider=req.llm_provider,
        created_at=datetime.now(timezone.utc),
    )


@router.get("/ideas", response_model=IdeaListResponse)
async def list_ideas(
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "composite_score",
    session: AsyncSession = Depends(get_session),
):
    """List all discovered business ideas."""
    order_col = getattr(BusinessIdea, sort_by, BusinessIdea.composite_score)
    query = (
        select(BusinessIdea)
        .order_by(order_col.desc().nullslast())
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(query)
    items = result.scalars().all()

    count_result = await session.execute(select(sa_func.count(BusinessIdea.id)))
    total = count_result.scalar() or 0

    return IdeaListResponse(
        items=[IdeaResponse.model_validate(i) for i in items],
        total=total,
    )


@router.get("/ideas/{idea_id}", response_model=IdeaResponse)
async def get_idea(
    idea_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific business idea."""
    result = await session.execute(
        select(BusinessIdea).where(BusinessIdea.id == idea_id)
    )
    idea = result.scalar_one()
    return IdeaResponse.model_validate(idea)
