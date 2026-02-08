"""Application configuration with Pydantic Settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- App ---
    app_name: str = "IdeaForge"
    debug: bool = False

    # --- Database ---
    database_url: str = "postgresql+asyncpg://ideaforge:ideaforge_dev@localhost:5432/ideaforge"

    # --- ChromaDB ---
    chroma_host: str = "localhost"
    chroma_port: int = 8100

    # --- Default LLM Provider ---
    llm_provider: str = "groq"

    # --- Free LLM API Keys ---
    groq_api_key: str = ""
    gemini_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    openrouter_api_key: str = ""
    cerebras_api_key: str = ""

    # --- Paid LLM API Keys (optional) ---
    deepseek_api_key: str = ""
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # --- Data Source API Keys ---
    serper_api_key: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "IdeaForge/0.1"
    youtube_api_key: str = ""
    github_token: str = ""
    gnews_api_key: str = ""
    bluesky_handle: str = ""
    bluesky_app_password: str = ""


# LLM provider configurations
LLM_PROVIDERS: dict[str, dict] = {
    "groq": {
        "model": "groq/llama-3.1-70b-versatile",
        "cost": "free",
        "speed": "ultra-fast",
        "requires_key": "groq_api_key",
        "description": "Groq — Llama 3.1 70B (бесплатно, 14K req/день)",
    },
    "gemini": {
        "model": "gemini/gemini-2.5-flash",
        "cost": "free",
        "speed": "fast",
        "requires_key": "gemini_api_key",
        "description": "Google Gemini 2.5 Flash (бесплатно, 250-1000 req/день)",
    },
    "ollama": {
        "model": "ollama/llama3.1",
        "base_url": "http://localhost:11434",
        "cost": "free",
        "speed": "medium",
        "requires_key": None,
        "description": "Ollama — локальная модель (бесплатно, без лимитов)",
    },
    "openrouter": {
        "model": "openrouter/deepseek/deepseek-chat-v3-0324:free",
        "cost": "free",
        "speed": "fast",
        "requires_key": "openrouter_api_key",
        "description": "OpenRouter — DeepSeek V3 free (50 req/день)",
    },
    "cerebras": {
        "model": "cerebras/llama-3.1-70b",
        "cost": "free",
        "speed": "ultra-fast",
        "requires_key": "cerebras_api_key",
        "description": "Cerebras — Llama 3.1 70B (бесплатно, 30 RPM)",
    },
    "deepseek": {
        "model": "deepseek/deepseek-chat",
        "cost": "$0.028/1M tokens",
        "speed": "fast",
        "requires_key": "deepseek_api_key",
        "description": "DeepSeek V3 ($0.028/1M tokens)",
    },
    "openai": {
        "model": "openai/gpt-4o-mini",
        "cost": "$0.15/1M tokens",
        "speed": "fast",
        "requires_key": "openai_api_key",
        "description": "OpenAI GPT-4o-mini ($0.15/1M tokens)",
    },
    "anthropic": {
        "model": "anthropic/claude-haiku-4-5",
        "cost": "$1/1M tokens",
        "speed": "fast",
        "requires_key": "anthropic_api_key",
        "description": "Anthropic Claude Haiku 4.5 ($1/1M tokens)",
    },
}

# Agent definitions with their data source metadata
AGENT_REGISTRY: dict[str, dict] = {
    "google_trends": {
        "name": "Google Trends",
        "category": "search_trends",
        "cost": "free",
        "description": "Растущие поисковые запросы, сезонность, гео-интерес",
        "limits": "Без лимитов (scraping)",
        "requires_key": None,
        "enabled_default": True,
    },
    "google_search": {
        "name": "Google Search",
        "category": "search_trends",
        "cost": "free",
        "description": "Топ результаты, People Also Ask, связанные запросы",
        "limits": "2500 бесплатных запросов",
        "requires_key": "serper_api_key",
        "enabled_default": True,
    },
    "wikipedia": {
        "name": "Wikipedia Trends",
        "category": "search_trends",
        "cost": "free",
        "description": "Популярность тем по просмотрам страниц",
        "limits": "Без лимитов",
        "requires_key": None,
        "enabled_default": False,
    },
    "reddit": {
        "name": "Reddit",
        "category": "social",
        "cost": "free",
        "description": "Pain points, бизнес-идеи из сообществ",
        "limits": "60 req/min",
        "requires_key": "reddit_client_id",
        "enabled_default": True,
    },
    "hackernews": {
        "name": "Hacker News",
        "category": "social",
        "cost": "free",
        "description": "Тех-тренды, стартап-обсуждения",
        "limits": "Без лимитов",
        "requires_key": None,
        "enabled_default": True,
    },
    "devto": {
        "name": "DEV.to",
        "category": "social",
        "cost": "free",
        "description": "Тренды разработчиков, популярные технологии",
        "limits": "Без лимитов",
        "requires_key": None,
        "enabled_default": False,
    },
    "bluesky": {
        "name": "Bluesky",
        "category": "social",
        "cost": "free",
        "description": "Социальные тренды, обсуждения",
        "limits": "Без лимитов",
        "requires_key": "bluesky_handle",
        "enabled_default": False,
    },
    "youtube": {
        "name": "YouTube",
        "category": "content",
        "cost": "free",
        "description": "Популярные видео, engagement, растущие каналы",
        "limits": "10K units/день",
        "requires_key": "youtube_api_key",
        "enabled_default": True,
    },
    "github": {
        "name": "GitHub Trending",
        "category": "tech",
        "cost": "free",
        "description": "Растущие репозитории, языки, технологии",
        "limits": "5000 req/час (auth) / 60 req/час (без)",
        "requires_key": None,
        "enabled_default": True,
    },
    "packages": {
        "name": "npm/PyPI Trends",
        "category": "tech",
        "cost": "free",
        "description": "Популярные библиотеки, рост загрузок",
        "limits": "Без лимитов",
        "requires_key": None,
        "enabled_default": False,
    },
    "news": {
        "name": "GNews",
        "category": "news",
        "cost": "free",
        "description": "Новости из 60K+ источников",
        "limits": "100 req/день",
        "requires_key": "gnews_api_key",
        "enabled_default": False,
    },
    "economic": {
        "name": "Economic Data",
        "category": "economy",
        "cost": "free",
        "description": "Рынок труда, зарплаты, экономические показатели",
        "limits": "500 req/день (BLS)",
        "requires_key": None,
        "enabled_default": False,
    },
}

settings = Settings()
