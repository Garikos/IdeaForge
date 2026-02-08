"""Event Bus for inter-agent communication."""

from __future__ import annotations

import asyncio
from typing import Any, Callable, Coroutine

import structlog

logger = structlog.get_logger()

EventHandler = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class EventBus:
    """Simple pub/sub event bus for agent communication."""

    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler):
        if event_type in self._handlers:
            self._handlers[event_type] = [
                h for h in self._handlers[event_type] if h != handler
            ]

    async def publish(self, event_type: str, data: dict[str, Any]):
        logger.debug("Event published", event_type=event_type)
        handlers = self._handlers.get(event_type, []) + self._handlers.get("*", [])
        for handler in handlers:
            try:
                await handler(data)
            except Exception as e:
                logger.error("Event handler error", event_type=event_type, error=str(e))


# Global event bus instance
event_bus = EventBus()
