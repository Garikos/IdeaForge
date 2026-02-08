"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import api_router
from .api.ws.manager import ws_manager
from .config import settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown lifecycle."""
    logger.info("Starting IdeaForge", debug=settings.debug)
    yield
    logger.info("Shutting down IdeaForge")
    await ws_manager.disconnect_all()


app = FastAPI(
    title=settings.app_name,
    description="Мульти-агентная платформа для поиска бизнес-идей",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}
