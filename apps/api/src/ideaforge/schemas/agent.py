"""Agent schemas."""

from __future__ import annotations

from pydantic import BaseModel


class AgentInfo(BaseModel):
    id: str
    name: str
    category: str
    cost: str
    description: str
    limits: str
    requires_key: str | None
    enabled: bool
    has_api_key: bool


class AgentRunStatus(BaseModel):
    agent_name: str
    status: str
    duration_seconds: float | None = None
    result_summary: str | None = None
    error_message: str | None = None
