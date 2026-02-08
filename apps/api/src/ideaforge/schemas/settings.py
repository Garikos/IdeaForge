"""Settings schemas."""

from __future__ import annotations

from pydantic import BaseModel


class LlmProviderInfo(BaseModel):
    id: str
    model: str
    cost: str
    speed: str
    description: str
    has_api_key: bool
    is_active: bool


class LlmSettingsResponse(BaseModel):
    current_provider: str
    providers: list[LlmProviderInfo]


class LlmUpdateRequest(BaseModel):
    provider: str


class AgentToggleRequest(BaseModel):
    agents: dict[str, bool]
