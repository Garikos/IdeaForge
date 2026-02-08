"""Research service — orchestrates the full research pipeline."""

from __future__ import annotations

import asyncio
import threading
from typing import Any

import structlog

from ..agents.coordinator import coordinator
from ..api.ws.events import research_cancelled
from ..api.ws.manager import ws_manager
from ..models.idea import BusinessIdea, IdeaStatus

logger = structlog.get_logger()

# Active research runs: run_id -> (asyncio.Task, threading.Event)
_active_runs: dict[str, tuple[asyncio.Task, threading.Event]] = {}


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

    cancel_event = threading.Event()

    # Store this task so it can be cancelled
    current_task = asyncio.current_task()
    if current_task:
        _active_runs[run_id] = (current_task, cancel_event)

    try:
        # Run the research crew (blocking, so wrap in thread)
        ideas = await coordinator.run_research(
            run_id=run_id,
            query=query,
            sources=sources,
            llm_provider=llm_provider,
            cancel_event=cancel_event,
        )

        logger.info("Research pipeline completed", run_id=run_id, ideas_count=len(ideas))

        # In a full setup, we'd save to DB here.
        # For now, broadcast results via WebSocket.
        await ws_manager.broadcast("research", {
            "type": "research_results",
            "run_id": run_id,
            "ideas": ideas,
        })

    except asyncio.CancelledError:
        logger.info("Research pipeline cancelled", run_id=run_id)
        await ws_manager.broadcast("research", research_cancelled(run_id))

    except Exception as e:
        logger.error("Research pipeline failed", run_id=run_id, error=str(e))
        await ws_manager.broadcast("research", {
            "type": "research_failed",
            "run_id": run_id,
            "error": str(e),
        })

    finally:
        _active_runs.pop(run_id, None)


async def cancel_research(run_id: str) -> bool:
    """Cancel a running research pipeline.

    Returns True if the run was found and cancelled.
    """
    entry = _active_runs.get(run_id)
    if not entry:
        return False

    task, cancel_event = entry
    # Signal the crew thread to stop
    cancel_event.set()
    # Cancel the async task
    task.cancel()

    logger.info("Research cancelled by user", run_id=run_id)
    return True
