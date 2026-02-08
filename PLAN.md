# IdeaForge: Мульти-агентная платформа для поиска бизнес-идей

## Контекст

Собираем сервис, который помогает найти актуальные и высокодоходные бизнес-идеи с помощью AI-агентов. Агенты анализируют множество бесплатных источников данных, выдают выжимку с анализом, помогают выбрать лучшие идеи и создать бизнес-план. Всё в едином веб-интерфейсе на русском языке, где каждый агент имеет свою роль и может взаимодействовать с другими.

**Scope первой итерации:** Фаза 1 (фундамент) + Фаза 2 (агенты-исследователи)
**LLM:** Groq (бесплатно, 14K req/day) + Gemini Flash (бесплатно) + Ollama (локально) + OpenAI/Anthropic/DeepSeek (опционально)
**Бюджет:** $0 для разработки и MVP. Все источники данных и LLM бесплатные.
**Язык интерфейса:** Русский

---

## Стратегия LLM: нулевой бюджет

Система поддерживает переключение между провайдерами. Каждый агент может использовать свой LLM.

### Бесплатные LLM-провайдеры (приоритетные)

| Провайдер | Модели | Лимиты бесплатного тарифа | Tool Calling |
|-----------|--------|--------------------------|--------------|
| **Groq** | Llama 3.1 70B, Mixtral 8x7B | 14,400 req/день, без карты | Да |
| **Google Gemini** | Gemini 2.5 Flash, Flash-Lite | 250-1000 req/день | Да |
| **Ollama** (локально) | Llama 3.1, Qwen 2.5, Mistral | Безлимит | Да |
| **OpenRouter** | DeepSeek V3 free, Llama 3.1 | 50 req/день | Да |
| **Cloudflare Workers AI** | Llama 3.2, Mistral 7B | 100K req/день | Частично |
| **Cerebras** | Llama 3.1 всех размеров | 30 RPM, 1M tokens/день | Да |

### Стратегия распределения

```python
# В config.py — LLM Registry
LLM_PROVIDERS = {
    "groq": {                          # По умолчанию для разработки
        "model": "groq/llama-3.1-70b-versatile",
        "cost": "free",
        "speed": "ultra-fast",
    },
    "gemini": {                        # Запасной бесплатный
        "model": "gemini/gemini-2.5-flash",
        "cost": "free",
        "speed": "fast",
    },
    "ollama": {                        # Локальный, без лимитов
        "model": "ollama/llama3.1",
        "base_url": "http://localhost:11434",
        "cost": "free",
        "speed": "medium",
    },
    "deepseek": {                      # Ультра-дешёвый для продакшена
        "model": "deepseek/deepseek-chat",
        "cost": "$0.028/1M tokens",
    },
    "openai": {                        # Премиум для сложных задач
        "model": "openai/gpt-4o-mini",
        "cost": "$0.15/1M tokens",
    },
    "anthropic": {                     # Премиум альтернатива
        "model": "anthropic/claude-haiku-4-5",
        "cost": "$1/1M tokens",
    },
}
```

В UI — настройка: какой LLM использовать для каждого типа агента. По умолчанию — Groq (бесплатно и быстро).

---

## Архитектура

```
┌─────────────────────────────────┐
│   Next.js Frontend (RU)          │
│   TailwindCSS + Shadcn/ui        │
│   Zustand + TanStack Query       │
└───────────────┬─────────────────┘
                │ WebSocket + REST
┌───────────────▼─────────────────┐
│   FastAPI Backend                │
│   Coordinator (оркестратор)      │
│   LLM Registry (переключатель)  │
└───────────────┬─────────────────┘
           ┌────┴─────────────┐
      ┌────▼────┐     ┌──────▼──────┐
      │ CrewAI  │     │ SharedMemory│
      │ Crews   │     │ (ChromaDB)  │
      └────┬────┘     └─────────────┘
           │
    ┌──────┼──────────────────────────────────────┐
    │      │                                       │
    ▼      ▼           ▼          ▼          ▼     ▼
 Google  Reddit    YouTube   HackerNews  GitHub  News
(Trends) (PRAW)  (Data API) (Firebase)  (API)  (GNews)
  FREE    FREE      FREE      FREE      FREE    FREE
```

---

## Полный реестр агентов-исследователей (все бесплатные)

### Категория 1: Поисковые тренды

| # | Агент | Источник | API | Стоимость | Что даёт |
|---|-------|----------|-----|-----------|----------|
| 1 | **Google Trends Agent** | Google Trends | TrendsPyG (библиотека) | $0 | Растущие поисковые запросы, сезонность, гео-интерес |
| 2 | **Google Search Agent** | Google Search | Serper API | $0 (2500 free) | Топ результаты, People Also Ask, связанные запросы |
| 3 | **Wikipedia Trends Agent** | Wikipedia | Pageviews API | $0 | Популярность тем по просмотрам страниц |

### Категория 2: Социальные платформы

| # | Агент | Источник | API | Стоимость | Что даёт |
|---|-------|----------|-----|-----------|----------|
| 4 | **Reddit Agent** | Reddit | PRAW (OAuth) | $0 | Pain points, бизнес-идеи из сообществ, sentiment |
| 5 | **Hacker News Agent** | Hacker News | Firebase API | $0 | Тех-тренды, стартап-обсуждения, реакция комьюнити |
| 6 | **DEV.to Agent** | DEV.to | Forem API | $0 | Тренды разработчиков, популярные технологии |
| 7 | **Bluesky Agent** | Bluesky | AT Protocol | $0 | Социальные тренды, обсуждения |
| 8 | **Mastodon Agent** | Mastodon | Public API | $0 | Тренды децентрализованных соцсетей |

### Категория 3: Контент и видео

| # | Агент | Источник | API | Стоимость | Что даёт |
|---|-------|----------|-----|-----------|----------|
| 9 | **YouTube Agent** | YouTube | Data API v3 | $0 | Популярные видео, engagement, растущие каналы |

### Категория 4: Технологии и стартапы

| # | Агент | Источник | API | Стоимость | Что даёт |
|---|-------|----------|-----|-----------|----------|
| 10 | **GitHub Trending Agent** | GitHub | REST API | $0 | Растущие репозитории, языки, технологии |
| 11 | **npm/PyPI Trends Agent** | npm + PyPI | Registry APIs | $0 | Популярные библиотеки, рост загрузок |

### Категория 5: Новости и медиа

| # | Агент | Источник | API | Стоимость | Что даёт |
|---|-------|----------|-----|-----------|----------|
| 12 | **News Agent** | GNews.io | REST API | $0 (100 req/day) | Новости из 60K+ источников |

### Категория 6: Экономика и данные

| # | Агент | Источник | API | Стоимость | Что даёт |
|---|-------|----------|-----|-----------|----------|
| 13 | **Economic Data Agent** | BLS + World Bank | REST APIs | $0 | Рынок труда, зарплаты, экономические показатели |

### Категория 7: Анализ

| # | Агент | Источник | Инструмент | Стоимость | Что даёт |
|---|-------|----------|------------|-----------|----------|
| 14 | **Sentiment Agent** | VADER | Локальная библиотека | $0 | Анализ тональности текстов |
| 15 | **Research Synthesizer** | LLM | Groq / Gemini | $0 | Объединение всех данных в единый рейтинг |

**Итого: 15 бесплатных агентов + 5 платных (доступны по желанию)**

Все агенты включаются/выключаются через UI (чекбоксы). Пользователь выбирает какие источники использовать для каждого исследования.

---

## Платные агенты (подключаются при необходимости)

Архитектура TOOL_REGISTRY позволяет добавить любой источник без изменения кода crew. Достаточно создать новый tool-файл и зарегистрировать его.

### Платные источники данных

| # | Агент | Источник | API | Стоимость | Что даёт | Когда подключать |
|---|-------|----------|-----|-----------|----------|-----------------|
| P1 | **Twitter/X Agent** | Twitter/X | API v2 (tweepy) | $200/мес (Basic) | Тренды, хэштеги, sentiment соцсетей | Когда нужен широкий социальный охват |
| P2 | **Crunchbase Agent** | Crunchbase | REST API | $29-99/мес | Стартапы, фандинг, инвесторы, раунды | Для конкурентного анализа стартапов |
| P3 | **SimilarWeb Agent** | SimilarWeb | REST API | $125+/мес | Трафик сайтов, конкуренты, каналы | Для оценки размера рынка |
| P4 | **Premium News Agent** | NewsAPI Pro | REST API | $449/мес | Полный архив новостей, commercial use | Для продакшена с новостным анализом |
| P5 | **Product Hunt Agent** | Product Hunt | GraphQL API | $0-custom | Запуски стартапов, тренды продуктов | Для анализа новых продуктов |

### Платные LLM (уже встроены в LLM Registry)

| Провайдер | Модель | Стоимость | Когда подключать |
|-----------|--------|-----------|-----------------|
| **DeepSeek** | DeepSeek V3.2 | $0.028/1M tokens (~$1-2/мес) | Первый шаг при масштабировании |
| **OpenAI** | GPT-4o-mini | $0.15/1M tokens (~$5-10/мес) | Лучшее качество tool calling |
| **OpenAI** | GPT-4o | $2.5/1M tokens (~$20-50/мес) | Сложные задачи анализа |
| **Anthropic** | Claude Haiku 4.5 | $1/1M tokens (~$5/мес) | Лучшее качество рассуждений |
| **Anthropic** | Claude Sonnet 4.5 | $3/1M tokens (~$30/мес) | Премиум-анализ бизнес-планов |

### Архитектура переключения (уже заложена)

```python
# Переключение происходит через UI или .env без изменения кода:

# 1. В UI: Settings → LLM Provider → выбрать из списка
# 2. В .env: LLM_PROVIDER=groq → deepseek → openai → anthropic
# 3. Per-agent: каждый агент может использовать свой LLM

# Для добавления нового платного источника:
# 1. Создать src/ideaforge/agents/tools/twitter_tool.py
# 2. Добавить в TOOL_REGISTRY["twitter"] = TwitterResearchTool
# 3. В UI появится новый чекбокс "Twitter/X" с пометкой "$"
# 4. Никакой другой код менять не нужно
```

В UI агенты с пометкой "$" (платные) визуально отделены от бесплатных. При попытке включить платный агент без API-ключа — показываем инструкцию по получению ключа и стоимость.

---

## Фаза 0: Сохранение плана

Первым делом при начале реализации — сохранить этот план в корень проекта:
- `PLAN.md` — копия этого плана в `/Users/Garikos/Workplace/2026/freeJob/PLAN.md`

---

## Фаза 1: Фундамент

### 1.1 Настройка окружения и монорепо

**Действия:**
- Обновить Node.js до v20 через nvm
- Установить pnpm (менеджер пакетов для монорепо)
- Установить uv (быстрый Python-менеджер от Astral)
- Инициализировать git-репозиторий

**Создать файлы:**
- `package.json` — корневой workspace config
- `pnpm-workspace.yaml` — определение workspace (apps/*, packages/*)
- `turbo.json` — Turborepo pipeline (dev, build, lint)
- `docker-compose.yml` — PostgreSQL 16 + ChromaDB для локальной разработки
- `.env.example` — шаблон переменных окружения (все API-ключи опциональны кроме Groq)
- `.gitignore` — Python, Node, IDE, OS, .env

### 1.2 Backend (FastAPI)

**Путь:** `apps/api/`

**Создать:**
- `pyproject.toml` — зависимости:
  - Фреймворк: fastapi, uvicorn[standard], websockets
  - БД: sqlalchemy[asyncio], asyncpg, alembic
  - Агенты: crewai[tools]
  - Вектор: chromadb
  - Данные: praw, google-api-python-client, httpx
  - Тренды: trendspyg (Google Trends)
  - Анализ: vaderSentiment
  - Конфиг: pydantic-settings, python-dotenv
  - Логи: structlog
- `src/ideaforge/main.py` — FastAPI app с CORS, lifespan, WebSocket
- `src/ideaforge/config.py` — Pydantic Settings + LLM Registry (все провайдеры)
- `src/ideaforge/models/database.py` — AsyncEngine + AsyncSession + Base
- `src/ideaforge/models/idea.py` — BusinessIdea model
- `src/ideaforge/models/agent.py` — AgentRun model
- `src/ideaforge/schemas/` — Pydantic request/response схемы
- `src/ideaforge/api/router.py` — главный роутер
- `src/ideaforge/api/v1/research.py` — эндпоинты исследования
- `src/ideaforge/api/v1/agents.py` — эндпоинты статуса агентов
- `src/ideaforge/api/v1/settings.py` — эндпоинты настроек (LLM provider, активные агенты)
- `src/ideaforge/api/ws/manager.py` — WebSocket менеджер
- `src/ideaforge/api/ws/events.py` — типы событий

**LLM Registry (ключевая деталь):**
```python
# src/ideaforge/core/llm_registry.py
# Фабрика LLM для CrewAI — создаёт нужный LLM по имени провайдера
# Поддержка: groq (default), gemini, ollama, openrouter,
#            cloudflare, cerebras, deepseek, openai, anthropic
# Каждый агент может использовать свой LLM
# UI позволяет переключать через /api/v1/settings/llm
```

### 1.3 Frontend (Next.js)

**Путь:** `apps/web/`

**Создать через:** `pnpm create next-app web --typescript --tailwind --eslint --app --src-dir`

**Дополнительные зависимости:** zustand, @tanstack/react-query, shadcn/ui

**Создать:**
- `src/app/layout.tsx` — корневой layout с providers, навигация на русском
- `src/app/page.tsx` — главная страница / dashboard
- `src/app/(dashboard)/research/page.tsx` — страница исследований
- `src/app/(dashboard)/agents/page.tsx` — обзор агентов
- `src/app/(dashboard)/settings/page.tsx` — настройки (LLM, активные агенты)
- `src/components/ui/` — Shadcn компоненты
- `src/components/agents/AgentCard.tsx` — карточка агента (статус, прогресс, лог)
- `src/components/agents/AgentActivityFeed.tsx` — лента активности
- `src/components/research/ResearchForm.tsx` — форма с выбором источников (чекбоксы по категориям)
- `src/components/research/IdeaCard.tsx` — карточка найденной идеи
- `src/components/settings/LlmSelector.tsx` — выбор LLM провайдера
- `src/components/settings/AgentToggle.tsx` — вкл/выкл каждого агента
- `src/lib/api.ts` — API-клиент
- `src/lib/websocket.ts` — WebSocket клиент с автореконнектом
- `src/lib/i18n/ru.ts` — русские строки интерфейса
- `src/lib/stores/agentStore.ts` — Zustand store для агентов
- `src/lib/stores/researchStore.ts` — Zustand store для результатов
- `src/lib/stores/settingsStore.ts` — Zustand store для настроек

### 1.4 Инфраструктура агентов

**Создать:**
- `src/ideaforge/agents/coordinator.py` — центральный оркестратор
  - Метод `run_research(query, sources, llm_config)` — запускает выбранные crews
  - Метод `get_available_agents()` — список всех агентов с их статусом
  - WebSocket broadcast при каждом изменении
- `src/ideaforge/agents/config/agents.yaml` — YAML-определения всех 15 агентов
- `src/ideaforge/agents/config/tasks.yaml` — YAML-определения задач
- `src/ideaforge/core/llm_registry.py` — фабрика LLM (Groq/Gemini/Ollama/etc.)
- `src/ideaforge/core/events.py` — Event Bus для коммуникации между агентами
- `src/ideaforge/core/memory.py` — SharedMemory через ChromaDB
- `src/ideaforge/services/vector_service.py` — CRUD для ChromaDB

### 1.5 База данных

**Alembic миграции:** таблицы `business_ideas`, `agent_runs`, `settings`

**Модель BusinessIdea:**
- id, title, summary, source (какой агент нашёл), source_url
- business_potential, market_size_score, competition_score, sentiment_score, composite_score
- status (discovered → analyzed → planned → selected → in_progress)
- raw_data (JSON), analysis_data (JSON)
- created_at, updated_at

### Проверка Фазы 1

```bash
# 1. docker compose up -d (PostgreSQL + ChromaDB)
# 2. cd apps/api && uv run uvicorn src.ideaforge.main:app --reload
# 3. cd apps/web && pnpm dev
# Ожидаемый результат:
#   - http://localhost:8000/docs — Swagger UI
#   - http://localhost:3000 — Dashboard на русском
#   - WebSocket подключение работает
#   - Страница настроек показывает все LLM провайдеры и агентов
```

---

## Фаза 2: Агенты-исследователи

### 2.1 Google Trends Tool (бесплатно — TrendsPyG)

**Файл:** `src/ideaforge/agents/tools/google_trends.py`

- `GoogleTrendsTool(BaseTool)` — через библиотеку TrendsPyG (бесплатная)
  - interest_over_time(keyword) — интерес к запросу за период
  - trending_searches(region) — актуальные тренды по стране
  - related_queries(keyword) — связанные запросы (rising & top)
  - suggestions(keyword) — автодополнение для генерации идей
- Возвращает: trending keywords, рост, гео-данные

**Стоимость:** $0 (неофициальная библиотека, работает через scraping)

### 2.2 Google Search Tool (бесплатный лимит — Serper)

**Файл:** `src/ideaforge/agents/tools/google_search.py`

- `GoogleSearchTool(BaseTool)` — через Serper API
  - organic results + People Also Ask + related searches
- **Стоимость:** $0 (2500 бесплатных запросов, потом $0.30/1K)

### 2.3 Reddit Tool (бесплатно — PRAW)

**Файл:** `src/ideaforge/agents/tools/reddit_tool.py`

- `RedditResearchTool(BaseTool)` — через PRAW (OAuth)
- Целевые сабреддиты: r/Entrepreneur, r/SideProject, r/startups, r/SaaS, r/BusinessIdeas, r/passive_income, r/indiehackers
- Данные: title, score, upvote_ratio, num_comments, top_comments

**Стоимость:** $0 (60 req/min)

### 2.4 Hacker News Tool (бесплатно — Firebase API)

**Файл:** `src/ideaforge/agents/tools/hackernews_tool.py`

- `HackerNewsResearchTool(BaseTool)` — через Firebase REST API
  - `https://hacker-news.firebaseio.com/v0/`
  - topstories, newstories, beststories, askstories, showstories
  - Для каждой истории: title, score, descendants (комментарии), url
  - Комментарии для анализа sentiment
- **Ключевое:** HN отлично показывает тех-тренды и отношение разработчиков к бизнес-идеям

**Стоимость:** $0 (без лимитов!)

### 2.5 YouTube Tool (бесплатно — Data API v3)

**Файл:** `src/ideaforge/agents/tools/youtube_tool.py`

- `YouTubeResearchTool(BaseTool)` — через google-api-python-client
  - search().list() + videos().list() для статистики
  - Данные: title, channel, views, likes, comments, published_at

**Стоимость:** $0 (10K units/день)

### 2.6 GitHub Trending Tool (бесплатно)

**Файл:** `src/ideaforge/agents/tools/github_tool.py`

- `GitHubTrendingTool(BaseTool)` — через GitHub REST API
  - Trending repositories по языкам и темам
  - Stars, forks, описание, topics
  - Рост звёзд за неделю/месяц
- **Ценность:** Показывает какие технологии набирают обороты → инструменты/SaaS вокруг них

**Стоимость:** $0 (5000 req/час с auth, 60 req/час без)

### 2.7 DEV.to Tool (бесплатно — Forem API)

**Файл:** `src/ideaforge/agents/tools/devto_tool.py`

- `DevToResearchTool(BaseTool)` — через Forem API
  - GET /articles?top=7 — популярные статьи за неделю
  - GET /articles?tag=startup,business,ai
  - Данные: title, tags, positive_reactions_count, comments_count, reading_time

**Стоимость:** $0

### 2.8 News Tool (бесплатно — GNews API)

**Файл:** `src/ideaforge/agents/tools/news_tool.py`

- `NewsResearchTool(BaseTool)` — через GNews.io API
  - GET /search?q=query&lang=en&max=10
  - Данные: title, description, source, published_at, url
  - Категории: business, technology, science

**Стоимость:** $0 (100 запросов/день)

### 2.9 Wikipedia Trends Tool (бесплатно — Pageviews API)

**Файл:** `src/ideaforge/agents/tools/wikipedia_tool.py`

- `WikipediaTrendsTool(BaseTool)` — через Wikimedia Pageviews API
  - pageviews/top/{project}/{access}/{year}/{month}/{day} — самые просматриваемые
  - pageviews/per-article — просмотры конкретной темы за период
- **Ценность:** Рост просмотров страницы = рост общественного интереса к теме

**Стоимость:** $0 (без лимитов)

### 2.10 Bluesky Tool (бесплатно — AT Protocol)

**Файл:** `src/ideaforge/agents/tools/bluesky_tool.py`

- `BlueskyResearchTool(BaseTool)` — через AT Protocol API
  - Поиск постов по запросу
  - Trending хэштеги
  - Данные: text, likes, reposts, replies

**Стоимость:** $0

### 2.11 npm/PyPI Trends Tool (бесплатно)

**Файл:** `src/ideaforge/agents/tools/package_trends_tool.py`

- `PackageTrendsTool(BaseTool)` — через npm registry + PyPI APIs
  - npm: downloads/point/last-month/{package} — загрузки пакета
  - PyPI: https://pypistats.org/api/ — статистика Python-пакетов
- **Ценность:** Рост загрузок = рост экосистемы → возможности для инструментов

**Стоимость:** $0

### 2.12 Economic Data Tool (бесплатно — BLS + World Bank)

**Файл:** `src/ideaforge/agents/tools/economic_tool.py`

- `EconomicDataTool(BaseTool)` — агрегатор:
  - BLS API: рынок труда, зарплаты, инфляция (500 req/день)
  - World Bank API: ВВП, рост, показатели по странам (без лимитов)
- **Ценность:** Макроэкономический контекст для оценки рынка

**Стоимость:** $0

### 2.13 Sentiment Analysis Tool (бесплатно — VADER)

**Файл:** `src/ideaforge/agents/tools/sentiment.py`

- `SentimentAnalysisTool(BaseTool)` — VADER для тональности
- Работает локально, идеально для коротких текстов (комментарии, посты)

**Стоимость:** $0

### 2.14 Research Crew (сборка)

**Файл:** `src/ideaforge/agents/crews/research_crew.py`

Динамическая сборка crew на основе выбранных пользователем источников:

```python
class ResearchCrew:
    """
    Создаёт crew из выбранных агентов.
    Пользователь в UI выбирает чекбоксами какие источники включить.
    """

    # Реестр всех доступных tools
    TOOL_REGISTRY = {
        "google_trends": GoogleTrendsTool,
        "google_search": GoogleSearchTool,
        "reddit": RedditResearchTool,
        "hackernews": HackerNewsResearchTool,
        "youtube": YouTubeResearchTool,
        "github": GitHubTrendingTool,
        "devto": DevToResearchTool,
        "news": NewsResearchTool,
        "wikipedia": WikipediaTrendsTool,
        "bluesky": BlueskyResearchTool,
        "packages": PackageTrendsTool,
        "economic": EconomicDataTool,
    }

    def build_crew(self, query, selected_sources, llm_config):
        # 1. Создать агентов только для выбранных источников
        # 2. Всегда добавить Synthesizer последним
        # 3. Каждый агент использует LLM из llm_config
        # 4. Запустить crew и вернуть результат
```

**Пайплайн:**
```
Выбранные агенты (параллельно собирают данные)
    │         │          │         │
    Google    Reddit   HackerNews  YouTube  ...
    │         │          │         │
    └─────────┴──────────┴─────────┘
                    │
            Synthesizer Agent
            (объединяет всё в рейтинг)
                    │
            JSON: 5-15 бизнес-идей
            с оценкой по каждому
```

### 2.15 Research Service

**Файл:** `src/ideaforge/services/research_service.py`

- Получает от UI: query + список включённых источников + LLM config
- Собирает ResearchCrew динамически из выбранных источников
- Запускает через asyncio.to_thread
- Парсит результат → BusinessIdea модели
- Сохраняет в PostgreSQL + ChromaDB
- WebSocket broadcast на каждом этапе

### 2.16 API Endpoints

**Файл:** `src/ideaforge/api/v1/research.py`

- `POST /api/v1/research` — запуск (query, sources[], llm_provider)
- `GET /api/v1/research/{run_id}` — статус и результаты
- `GET /api/v1/ideas` — все найденные идеи (sort, filter, paginate)
- `GET /api/v1/ideas/{id}` — детали идеи

**Файл:** `src/ideaforge/api/v1/settings.py`

- `GET /api/v1/settings/agents` — список всех агентов с их статусом (вкл/выкл)
- `PUT /api/v1/settings/agents` — обновить какие агенты активны
- `GET /api/v1/settings/llm` — текущий LLM провайдер и доступные
- `PUT /api/v1/settings/llm` — сменить LLM провайдер
- `GET /api/v1/settings/llm/test` — проверить подключение к LLM

**WebSocket:** `ws://localhost:8000/api/v1/ws/{channel}`
- "research" — события исследования
- "agents" — статусы агентов

### 2.17 Frontend: страница исследований

**Файл:** `apps/web/src/app/(dashboard)/research/page.tsx`

- Текстовое поле запроса на русском
- **Выбор источников по категориям** (чекбоксы с toggle-группами):
  - Поисковые тренды: Google Trends, Google Search, Wikipedia
  - Социальные: Reddit, HackerNews, DEV.to, Bluesky
  - Контент: YouTube
  - Технологии: GitHub, npm/PyPI
  - Новости: GNews
  - Экономика: BLS/World Bank
  - Быстрые пресеты: "Все", "Тех-фокус", "Бизнес-фокус", "Минимум (быстро)"
- Кнопка "Начать исследование"
- Лента активности агентов в реальном времени
- Карточки результатов: название, описание, источники, оценка

### 2.18 Frontend: страница настроек

**Файл:** `apps/web/src/app/(dashboard)/settings/page.tsx`

- **Секция "LLM Провайдер":**
  - Выпадающий список провайдеров с индикатором "бесплатно/платно"
  - Кнопка "Проверить подключение"
  - Поля для API-ключей (если нужны)
- **Секция "Агенты":**
  - Список всех 15 агентов с toggle on/off
  - Группировка по категориям
  - Для каждого: описание, статус, лимиты API

### Проверка Фазы 2

```bash
# 1. Установить Groq API key (бесплатный, без карты):
#    Регистрация на console.groq.com → получить ключ → добавить в .env
# 2. Запустить backend и frontend
# 3. Через UI: выбрать 3-4 источника, ввести запрос
# 4. Наблюдать работу агентов в реальном времени
# 5. Получить список ранжированных бизнес-идей
# 6. Поменять LLM на Gemini Flash, повторить — сравнить результаты
# 7. API тест:
curl -X POST http://localhost:8000/api/v1/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "AI инструменты для малого бизнеса 2026",
    "sources": ["google_trends", "reddit", "hackernews", "youtube", "github"],
    "llm_provider": "groq"
  }'
```

---

## Структура проекта

```
freeJob/
├── package.json
├── pnpm-workspace.yaml
├── turbo.json
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── apps/
│   ├── web/                              # Next.js frontend
│   │   ├── package.json
│   │   ├── next.config.js
│   │   ├── tailwind.config.ts
│   │   └── src/
│   │       ├── app/
│   │       │   ├── layout.tsx
│   │       │   ├── page.tsx
│   │       │   └── (dashboard)/
│   │       │       ├── research/page.tsx
│   │       │       ├── agents/page.tsx
│   │       │       └── settings/page.tsx
│   │       ├── components/
│   │       │   ├── ui/                   # Shadcn
│   │       │   ├── agents/
│   │       │   │   ├── AgentCard.tsx
│   │       │   │   └── AgentActivityFeed.tsx
│   │       │   ├── research/
│   │       │   │   ├── ResearchForm.tsx
│   │       │   │   ├── SourceSelector.tsx # Выбор источников по категориям
│   │       │   │   └── IdeaCard.tsx
│   │       │   └── settings/
│   │       │       ├── LlmSelector.tsx
│   │       │       └── AgentToggle.tsx
│   │       ├── lib/
│   │       │   ├── api.ts
│   │       │   ├── websocket.ts
│   │       │   ├── i18n/ru.ts
│   │       │   └── stores/
│   │       │       ├── agentStore.ts
│   │       │       ├── researchStore.ts
│   │       │       └── settingsStore.ts
│   │       └── types/
│   │           ├── agent.ts
│   │           ├── research.ts
│   │           └── settings.ts
│   │
│   └── api/                              # Python FastAPI backend
│       ├── pyproject.toml
│       ├── alembic.ini
│       ├── alembic/
│       └── src/ideaforge/
│           ├── __init__.py
│           ├── main.py
│           ├── config.py
│           ├── models/
│           │   ├── database.py
│           │   ├── idea.py
│           │   └── agent.py
│           ├── schemas/
│           │   ├── research.py
│           │   ├── agent.py
│           │   └── settings.py
│           ├── api/
│           │   ├── router.py
│           │   ├── v1/
│           │   │   ├── research.py
│           │   │   ├── agents.py
│           │   │   └── settings.py
│           │   └── ws/
│           │       ├── manager.py
│           │       └── events.py
│           ├── agents/
│           │   ├── coordinator.py
│           │   ├── config/
│           │   │   ├── agents.yaml
│           │   │   └── tasks.yaml
│           │   ├── crews/
│           │   │   └── research_crew.py   # Динамическая сборка из выбранных
│           │   ├── tools/
│           │   │   ├── __init__.py         # TOOL_REGISTRY
│           │   │   ├── google_trends.py    # TrendsPyG — бесплатно
│           │   │   ├── google_search.py    # Serper — 2500 free
│           │   │   ├── reddit_tool.py      # PRAW — бесплатно
│           │   │   ├── hackernews_tool.py  # Firebase API — бесплатно, без лимитов
│           │   │   ├── youtube_tool.py     # Data API v3 — бесплатно
│           │   │   ├── github_tool.py      # REST API — бесплатно
│           │   │   ├── devto_tool.py       # Forem API — бесплатно
│           │   │   ├── news_tool.py        # GNews — 100 req/day free
│           │   │   ├── wikipedia_tool.py   # Pageviews API — бесплатно
│           │   │   ├── bluesky_tool.py     # AT Protocol — бесплатно
│           │   │   ├── package_trends.py   # npm + PyPI — бесплатно
│           │   │   ├── economic_tool.py    # BLS + World Bank — бесплатно
│           │   │   └── sentiment.py        # VADER — бесплатно, локально
│           │   └── callbacks/
│           │       └── ws_callback.py
│           ├── services/
│           │   ├── research_service.py
│           │   └── vector_service.py
│           └── core/
│               ├── llm_registry.py         # Фабрика LLM (Groq/Gemini/Ollama/...)
│               ├── events.py
│               ├── memory.py
│               └── logging.py
```

---

## Будущие фазы (после Фазы 1+2)

- **Фаза 3:** Агенты-аналитики (глубокий анализ трендов, рынка, конкуренции, скоринг)
- **Фаза 4:** Бизнес-планирование (генерация плана, финмодель, оценка рисков)
- **Фаза 5:** Поддержка исполнения (задачи, ресурсы, прогресс, коллаборация)
- **Фаза 6:** Полировка (UI/UX, мониторинг, деплой, масштабирование)

---

## Стоимость

### MVP (бесплатный тариф) — $0/мес

| Компонент | Стоимость |
|-----------|-----------|
| LLM (Groq / Gemini / Ollama) | $0 |
| 12 источников данных | $0 |
| VADER sentiment | $0 |
| PostgreSQL + ChromaDB (Docker) | $0 |
| **Итого MVP** | **$0** |

### Рост (когда нужно больше) — $1-55/мес

| Апгрейд | Стоимость | Что даёт |
|----------|-----------|----------|
| DeepSeek V3.2 LLM | +$1-2/мес | Лучше качество анализа |
| GPT-4o-mini LLM | +$5-10/мес | Надёжный tool calling |
| Claude Haiku 4.5 | +$5/мес | Глубокие рассуждения |
| Serper (сверх 2500) | +$5/мес | Больше Google-запросов |

### Масштаб (полный охват) — $250-500/мес

| Апгрейд | Стоимость | Что даёт |
|----------|-----------|----------|
| Twitter/X API | +$200/мес | Социальный охват |
| Crunchbase | +$29-99/мес | Данные стартапов |
| SimilarWeb | +$125/мес | Трафик конкурентов |
| GPT-4o / Claude Sonnet | +$20-50/мес | Премиум-анализ |

**Путь миграции:** $0 → $1-2 → $10-20 → $250+ — каждый шаг через переключатель в UI, без изменения кода.
