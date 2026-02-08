"""CrewAI callback that broadcasts events via WebSocket."""

from __future__ import annotations

from typing import Any

import structlog

logger = structlog.get_logger()


class WebSocketCallback:
    """Callback handler for CrewAI that forwards events to WebSocket."""

    def __init__(self, run_id: str, on_event: Any = None):
        self.run_id = run_id
        self.on_event = on_event

    def on_task_start(self, task: Any):
        logger.info("Task started", run_id=self.run_id, task=str(task)[:100])

    def on_task_end(self, task: Any, output: Any):
        logger.info("Task completed", run_id=self.run_id, output=str(output)[:200])
