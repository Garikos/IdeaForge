"""Agent status API endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import AGENT_REGISTRY, settings
from ...models.agent import AgentRun
from ...models.database import get_session
from ...schemas.agent import AgentInfo, AgentRunStatus

router = APIRouter(tags=["agents"])


@router.get("/agents", response_model=list[AgentInfo])
async def list_agents():
    """List all available agents with their status."""
    agents = []
    for agent_id, info in AGENT_REGISTRY.items():
        key_field = info.get("requires_key")
        has_key = True
        if key_field:
            has_key = bool(getattr(settings, key_field, ""))

        agents.append(
            AgentInfo(
                id=agent_id,
                name=info["name"],
                category=info["category"],
                cost=info["cost"],
                description=info["description"],
                limits=info["limits"],
                requires_key=key_field,
                enabled=info["enabled_default"],
                has_api_key=has_key,
            )
        )
    return agents


@router.get("/agents/runs/{run_id}", response_model=list[AgentRunStatus])
async def get_agent_runs(
    run_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get agent run statuses for a specific research run."""
    result = await session.execute(
        select(AgentRun)
        .where(AgentRun.research_run_id == run_id)
        .order_by(AgentRun.created_at)
    )
    runs = result.scalars().all()
    return [
        AgentRunStatus(
            agent_name=r.agent_name,
            status=r.status.value,
            duration_seconds=r.duration_seconds,
            result_summary=r.result_summary,
            error_message=r.error_message,
        )
        for r in runs
    ]
