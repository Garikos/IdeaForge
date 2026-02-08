"""Main API router."""

from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .v1.agents import router as agents_router
from .v1.research import router as research_router
from .v1.settings import router as settings_router
from .ws.manager import ws_manager

api_router = APIRouter()

# REST API v1
api_router.include_router(research_router, prefix="/v1")
api_router.include_router(agents_router, prefix="/v1")
api_router.include_router(settings_router, prefix="/v1")


# WebSocket endpoint
@api_router.websocket("/v1/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            # Keep connection alive, listen for pings
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)
