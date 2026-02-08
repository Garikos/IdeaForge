"""Google Search research tool via Serper API."""

from __future__ import annotations

import httpx
from crewai.tools import BaseTool

from ...config import settings


class GoogleSearchTool(BaseTool):
    name: str = "google_search_research"
    description: str = (
        "Search Google for a query and return organic results, "
        "People Also Ask questions, and related searches."
    )

    def _run(self, query: str) -> str:
        if not settings.serper_api_key:
            return "Google Search tool: SERPER_API_KEY not configured"

        try:
            resp = httpx.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": settings.serper_api_key,
                    "Content-Type": "application/json",
                },
                json={"q": query, "num": 10},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            results = []

            # Organic results
            for item in data.get("organic", [])[:10]:
                results.append(
                    f"- {item.get('title', 'No title')}\n"
                    f"  URL: {item.get('link', '')}\n"
                    f"  Snippet: {item.get('snippet', '')}"
                )

            # People Also Ask
            paa = data.get("peopleAlsoAsk", [])
            if paa:
                questions = [q.get("question", "") for q in paa[:5]]
                results.append(f"\nPeople Also Ask: {questions}")

            # Related searches
            related = data.get("relatedSearches", [])
            if related:
                queries = [r.get("query", "") for r in related[:5]]
                results.append(f"\nRelated searches: {queries}")

            return "\n".join(results) if results else f"No results for '{query}'"

        except Exception as e:
            return f"Google Search error: {str(e)}"
