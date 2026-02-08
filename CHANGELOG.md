# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.3.0] - 2026-02-08

### Added
- **Rate limit handling** — automatic retry with backoff on 429 errors via litellm (`num_retries=3`, `timeout=120`)
- **Token usage tracking** — `TokenTracker` module with thread-safe counting and real-time WS broadcasting
- **Token usage widget** — real-time progress bar with three states: green (<70%), yellow (70-100%), red (>100% TPM)
- **Research cancellation** — "Остановить" button to cancel running research; uses `asyncio.Task.cancel()` + `threading.Event` for dual-layer cancellation
- `POST /research/{run_id}/cancel` API endpoint
- `rate_limits` configuration for all LLM providers (TPM, RPM, RPD)
- `token_usage` and `research_cancelled` WebSocket events
- `litellm.success_callback` integration for intercepting token usage from all LLM calls

### Fixed
- **Groq model decommissioned** — `llama-3.1-70b-versatile` replaced with `llama-3.3-70b-versatile`

## [0.2.0] - 2026-02-08

### Fixed
- **Research pipeline crash** — `output_json=True` replaced with Pydantic `BusinessIdeaItem` model (CrewAI 0.100+ API change)
- **Async callback deadlock** — `asyncio.run()` inside `asyncio.to_thread()` replaced with `asyncio.run_coroutine_threadsafe()` for thread-safe WS event broadcasting
- **Missing litellm dependency** — added `litellm>=1.50.0` to `pyproject.toml` (required by CrewAI for LLM provider routing)

### Added
- Manual agent event emission in `research_crew.py` — sends `agent_started`/`agent_completed` events for each agent before and after crew kickoff
- WebSocket connection status tracking — `onConnection()` callback and `connected` getter in `WebSocketClient`
- `AgentActivityFeed` component improvements:
  - Live elapsed timer during research
  - WebSocket connection indicator (green/red dot)
  - Pulsing animation for running agents
  - Error display block with details
  - Status icons and color-coded badges per agent state
- Full WebSocket event handling on research page — individual handlers for `research_started`, `agent_started`, `agent_completed`, `agent_failed`, `research_completed`, `research_failed`, `research_results`

### Changed
- `AgentActivityFeed` now accepts `researchStartTime`, `wsConnected`, and `error` props
- Research page tracks WS connection state and research start time

## [0.1.0] - 2026-02-08

### Added
- Initial project scaffold — monorepo with pnpm + Turborepo
- **Backend** (FastAPI):
  - REST API (`/api/v1/`) with endpoints: research, agents, ideas, settings
  - WebSocket real-time events (`/api/v1/ws/{channel}`)
  - 12 free data source agent tools (Google Trends, Reddit, Hacker News, GitHub, Wikipedia, StackOverflow, etc.)
  - Sentiment analysis agent (VADER)
  - Research synthesizer agent
  - CrewAI-based dynamic crew assembly (`ResearchCrew`)
  - LLM Registry with 8 providers (Groq, Gemini, Ollama, OpenRouter, Cerebras, DeepSeek, OpenAI, Anthropic)
  - SQLAlchemy async models (business_ideas, agent_runs)
  - Alembic migrations (async PostgreSQL via asyncpg)
  - Configuration via pydantic-settings + .env
- **Frontend** (Next.js 15 / React 19):
  - Dashboard layout with sidebar navigation
  - Research page with form, agent activity feed, idea cards
  - Ideas page with list view
  - Agents page with enable/disable toggles
  - Settings page (LLM provider selection, API keys)
  - Zustand state management
  - WebSocket client with auto-reconnect
  - Russian language UI
- GitHub repository: https://github.com/Garikos/IdeaForge
