"""News research tool via GNews API."""

from __future__ import annotations

import httpx
from crewai.tools import BaseTool

from ...config import settings


class NewsResearchTool(BaseTool):
    name: str = "news_research"
    description: str = (
        "Search recent news articles from 60K+ sources about business topics."
    )

    def _run(self, query: str) -> str:
        if not settings.gnews_api_key:
            return "News tool: GNEWS_API_KEY not configured"

        try:
            client = httpx.Client(timeout=15)

            resp = client.get(
                "https://gnews.io/api/v4/search",
                params={
                    "q": query,
                    "lang": "en",
                    "max": 10,
                    "apikey": settings.gnews_api_key,
                },
            )
            resp.raise_for_status()
            data = resp.json()

            results = []
            for article in data.get("articles", []):
                results.append(
                    f"- {article.get('title', 'No title')}\n"
                    f"  Source: {article.get('source', {}).get('name', 'Unknown')}\n"
                    f"  Description: {article.get('description', '')[:200]}\n"
                    f"  URL: {article.get('url', '')}\n"
                    f"  Published: {article.get('publishedAt', '')}"
                )

            client.close()
            return "\n\n".join(results) if results else f"No news for '{query}'"

        except Exception as e:
            return f"News error: {str(e)}"
