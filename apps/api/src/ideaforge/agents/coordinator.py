"""Central coordinator — orchestrates research crews and manages agent lifecycle."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import structlog

from ..api.ws.events import (
    agent_completed,
    agent_failed,
    agent_started,
    research_completed,
    research_failed,
    research_started,
)
from ..api.ws.manager import ws_manager
from ..config import AGENT_REGISTRY
from ..core.events import event_bus

logger = structlog.get_logger()


class Coordinator:
    """Central orchestrator for research operations."""

    async def run_research(
        self,
        run_id: str,
        query: str,
        sources: list[str],
        llm_provider: str,
    ) -> list[dict[str, Any]]:
        """Run a research pipeline with selected sources.

        Args:
            run_id: Unique identifier for this research run.
            query: User's research query.
            sources: List of source IDs to use.
            llm_provider: LLM provider to use.

        Returns:
            List of discovered business ideas.
        """
        logger.info("Starting research", run_id=run_id, query=query, sources=sources)

        # Broadcast start event
        await ws_manager.broadcast(
            "research",
            research_started(run_id, query, sources),
        )

        try:
            # Import here to avoid circular imports
            from .crews.research_crew import ResearchCrew

            crew = ResearchCrew()
            results = await asyncio.to_thread(
                crew.run,
                query=query,
                selected_sources=sources,
                llm_provider=llm_provider,
                run_id=run_id,
                on_agent_start=lambda name: asyncio.run(
                    ws_manager.broadcast("research", agent_started(run_id, name))
                ),
                on_agent_complete=lambda name, summary: asyncio.run(
                    ws_manager.broadcast("research", agent_completed(run_id, name, summary))
                ),
                on_agent_error=lambda name, error: asyncio.run(
                    ws_manager.broadcast("research", agent_failed(run_id, name, error))
                ),
            )

            await ws_manager.broadcast(
                "research",
                research_completed(run_id, len(results)),
            )

            return results

        except Exception as e:
            logger.error("Research failed", run_id=run_id, error=str(e))
            await ws_manager.broadcast(
                "research",
                research_failed(run_id, str(e)),
            )
            raise

    def get_available_agents(self) -> list[dict]:
        """Return all registered agents with their metadata."""
        return [
            {"id": agent_id, **info}
            for agent_id, info in AGENT_REGISTRY.items()
        ]


coordinator = Coordinator()
