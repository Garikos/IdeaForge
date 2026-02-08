"""Settings API endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from ...config import AGENT_REGISTRY, LLM_PROVIDERS, settings
from ...schemas.settings import (
    AgentToggleRequest,
    LlmProviderInfo,
    LlmSettingsResponse,
    LlmUpdateRequest,
)

router = APIRouter(tags=["settings"])

# In-memory state (will be persisted to DB in later phases)
_active_agents: dict[str, bool] = {
    agent_id: info["enabled_default"]
    for agent_id, info in AGENT_REGISTRY.items()
}
_current_llm: str = settings.llm_provider


@router.get("/settings/llm", response_model=LlmSettingsResponse)
async def get_llm_settings():
    """Get current LLM provider and available providers."""
    providers = []
    for provider_id, info in LLM_PROVIDERS.items():
        key_field = info.get("requires_key")
        has_key = True
        if key_field:
            has_key = bool(getattr(settings, key_field, ""))

        providers.append(
            LlmProviderInfo(
                id=provider_id,
                model=info["model"],
                cost=info["cost"],
                speed=info["speed"],
                description=info["description"],
                has_api_key=has_key,
                is_active=(provider_id == _current_llm),
            )
        )
    return LlmSettingsResponse(
        current_provider=_current_llm,
        providers=providers,
    )


@router.put("/settings/llm")
async def update_llm_provider(req: LlmUpdateRequest):
    """Change the active LLM provider."""
    global _current_llm
    if req.provider not in LLM_PROVIDERS:
        return {"error": f"Unknown provider: {req.provider}"}
    _current_llm = req.provider
    return {"status": "ok", "provider": _current_llm}


@router.get("/settings/agents")
async def get_agent_settings():
    """Get which agents are enabled/disabled."""
    return _active_agents


@router.put("/settings/agents")
async def update_agent_settings(req: AgentToggleRequest):
    """Toggle agents on/off."""
    for agent_id, enabled in req.agents.items():
        if agent_id in _active_agents:
            _active_agents[agent_id] = enabled
    return _active_agents


def get_active_agents() -> list[str]:
    """Helper: return list of currently enabled agent IDs."""
    return [aid for aid, enabled in _active_agents.items() if enabled]


def get_current_llm() -> str:
    """Helper: return current LLM provider ID."""
    return _current_llm
