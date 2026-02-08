"""WebSocket connection manager."""

from __future__ import annotations

import json
from typing import Any

from fastapi import WebSocket
import structlog

logger = structlog.get_logger()


class ConnectionManager:
    """Manages WebSocket connections grouped by channels."""

    def __init__(self):
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self._connections:
            self._connections[channel] = []
        self._connections[channel].append(websocket)
        logger.info("WebSocket connected", channel=channel)

    def disconnect(self, websocket: WebSocket, channel: str):
        if channel in self._connections:
            self._connections[channel] = [
                ws for ws in self._connections[channel] if ws != websocket
            ]
            logger.info("WebSocket disconnected", channel=channel)

    async def broadcast(self, channel: str, data: dict[str, Any]):
        if channel not in self._connections:
            return
        message = json.dumps(data, ensure_ascii=False, default=str)
        dead: list[WebSocket] = []
        for ws in self._connections[channel]:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._connections[channel].remove(ws)

    async def disconnect_all(self):
        for channel, connections in self._connections.items():
            for ws in connections:
                try:
                    await ws.close()
                except Exception:
                    pass
        self._connections.clear()


ws_manager = ConnectionManager()
