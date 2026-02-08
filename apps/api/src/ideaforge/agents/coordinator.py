"""Central coordinator — orchestrates research crews and manages agent lifecycle."""

from __future__ import annotations

import asyncio
import threading
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
from ..config import AGENT_REGISTRY, LLM_PROVIDERS
from ..core.token_tracker import TokenTracker

logger = structlog.get_logger()


def _make_callback(loop: asyncio.AbstractEventLoop, coro_fn):
    """Create a thread-safe callback that schedules a coroutine on the event loop."""
    def callback(*args):
        future = asyncio.run_coroutine_threadsafe(coro_fn(*args), loop)
        try:
            future.result(timeout=5)
        except Exception as e:
            logger.warning("Callback failed", error=str(e))
    return callback


class Coordinator:
    """Central orchestrator for research operations."""

    async def run_research(
        self,
        run_id: str,
        query: str,
        sources: list[str],
        llm_provider: str,
        cancel_event: threading.Event | None = None,
    ) -> list[dict[str, Any]]:
        """Run a research pipeline with selected sources."""
        logger.info("Starting research", run_id=run_id, query=query, sources=sources)

        # Broadcast start event
        await ws_manager.broadcast(
            "research",
            research_started(run_id, query, sources),
        )

        try:
            from .crews.research_crew import ResearchCrew

            # Capture current event loop for thread-safe callbacks
            loop = asyncio.get_running_loop()

            async def on_start(name):
                await ws_manager.broadcast("research", agent_started(run_id, name))

            async def on_complete(name, summary):
                await ws_manager.broadcast("research", agent_completed(run_id, name, summary))

            async def on_error(name, error):
                await ws_manager.broadcast("research", agent_failed(run_id, name, error))

            async def on_token_update(snapshot: dict):
                await ws_manager.broadcast("research", snapshot)

            # Get rate limit info for the provider
            provider_config = LLM_PROVIDERS.get(llm_provider, {})
            rate_limits = provider_config.get("rate_limits")
            tpm_limit = rate_limits.get("tpm") if rate_limits else None

            # Create token tracker with WS callback
            tracker = TokenTracker(
                run_id=run_id,
                provider=llm_provider,
                tpm_limit=tpm_limit,
                on_update=_make_callback(loop, on_token_update),
            )

            crew = ResearchCrew()
            results = await asyncio.to_thread(
                crew.run,
                query=query,
                selected_sources=sources,
                llm_provider=llm_provider,
                run_id=run_id,
                on_agent_start=_make_callback(loop, on_start),
                on_agent_complete=_make_callback(loop, on_complete),
                on_agent_error=_make_callback(loop, on_error),
                token_tracker=tracker,
                cancel_event=cancel_event,
            )

            # Broadcast final token usage + completion
            await ws_manager.broadcast("research", tracker.snapshot())
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
