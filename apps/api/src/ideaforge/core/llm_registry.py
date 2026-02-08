"""LLM Registry — factory for creating LLM instances for CrewAI agents."""

from __future__ import annotations

import os

from crewai import LLM

from ..config import LLM_PROVIDERS, settings


def get_llm(provider: str | None = None) -> LLM:
    """Create a CrewAI LLM instance for the given provider.

    Args:
        provider: LLM provider ID (groq, gemini, ollama, etc.).
                  Defaults to settings.llm_provider.

    Returns:
        Configured LLM instance ready for CrewAI agents.
    """
    provider = provider or settings.llm_provider
    config = LLM_PROVIDERS.get(provider)
    if not config:
        raise ValueError(f"Unknown LLM provider: {provider}")

    model = config["model"]
    kwargs: dict = {}

    # Set API key in environment for litellm (used by CrewAI)
    key_field = config.get("requires_key")
    if key_field:
        api_key = getattr(settings, key_field, "")
        if api_key:
            _set_provider_env(provider, api_key)

    # Ollama needs base_url
    if "base_url" in config:
        kwargs["base_url"] = config["base_url"]

    return LLM(model=model, **kwargs)


def _set_provider_env(provider: str, api_key: str):
    """Set the appropriate environment variable for litellm."""
    env_map = {
        "groq": "GROQ_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "cerebras": "CEREBRAS_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    env_var = env_map.get(provider)
    if env_var:
        os.environ[env_var] = api_key


def get_available_providers() -> list[dict]:
    """Return list of all providers with their availability status."""
    result = []
    for pid, config in LLM_PROVIDERS.items():
        key_field = config.get("requires_key")
        available = True
        if key_field:
            available = bool(getattr(settings, key_field, ""))

        result.append({
            "id": pid,
            "model": config["model"],
            "cost": config["cost"],
            "speed": config["speed"],
            "available": available,
        })
    return result
