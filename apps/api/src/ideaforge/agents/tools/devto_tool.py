"""DEV.to research tool via Forem API."""

from __future__ import annotations

import httpx
from crewai.tools import BaseTool


class DevToResearchTool(BaseTool):
    name: str = "devto_research"
    description: str = (
        "Research DEV.to for developer trends, popular technologies, "
        "and startup-related articles."
    )

    def _run(self, query: str) -> str:
        try:
            client = httpx.Client(timeout=15)
            results = []

            # Search articles by tag/query
            resp = client.get(
                "https://dev.to/api/articles",
                params={"tag": query.replace(" ", ","), "top": 7, "per_page": 10},
            )

            if resp.status_code != 200:
                # Fallback: search by page
                resp = client.get(
                    "https://dev.to/api/articles",
                    params={"page": 1, "per_page": 15, "top": 30},
                )

            if resp.status_code == 200:
                articles = resp.json()
                query_lower = query.lower()

                for article in articles:
                    title = article.get("title", "")
                    tags = article.get("tag_list", [])

                    # Filter by relevance
                    if (
                        query_lower in title.lower()
                        or any(query_lower in t.lower() for t in tags)
                        or not query_lower  # Show all if no specific filter
                    ):
                        results.append(
                            f"- {title}\n"
                            f"  Tags: {tags}\n"
                            f"  Reactions: {article.get('positive_reactions_count', 0)} | "
                            f"Comments: {article.get('comments_count', 0)} | "
                            f"Reading time: {article.get('reading_time_minutes', 0)} min\n"
                            f"  URL: {article.get('url', '')}\n"
                            f"  Published: {article.get('published_at', '')}"
                        )

            client.close()
            return "\n\n".join(results[:10]) if results else f"No DEV.to results for '{query}'"

        except Exception as e:
            return f"DEV.to error: {str(e)}"
