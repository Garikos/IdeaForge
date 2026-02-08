"""Research service — orchestrates the full research pipeline."""

from __future__ import annotations

import asyncio
from typing import Any

import structlog

from ..agents.coordinator import coordinator
from ..api.ws.manager import ws_manager
from ..models.idea import BusinessIdea, IdeaStatus

logger = structlog.get_logger()


async def run_research_pipeline(
    run_id: str,
    query: str,
    sources: list[str],
    llm_provider: str,
) -> None:
    """Full research pipeline: run agents -> parse results -> save to DB.

    Runs as a background task from the API endpoint.
    """
    logger.info("Research pipeline started", run_id=run_id, query=query)

    try:
        # Run the research crew (blocking, so wrap in thread)
        ideas = await coordinator.run_research(
            run_id=run_id,
            query=query,
            sources=sources,
            llm_provider=llm_provider,
        )

        logger.info("Research pipeline completed", run_id=run_id, ideas_count=len(ideas))

        # In a full setup, we'd save to DB here.
        # For now, broadcast results via WebSocket.
        await ws_manager.broadcast("research", {
            "type": "research_results",
            "run_id": run_id,
            "ideas": ideas,
        })

    except Exception as e:
        logger.error("Research pipeline failed", run_id=run_id, error=str(e))
        await ws_manager.broadcast("research", {
            "type": "research_failed",
            "run_id": run_id,
            "error": str(e),
        })
