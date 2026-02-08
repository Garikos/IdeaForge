"""Wikipedia Trends research tool via Wikimedia Pageviews API."""

from __future__ import annotations

from datetime import datetime, timedelta

import httpx
from crewai.tools import BaseTool


class WikipediaTrendsTool(BaseTool):
    name: str = "wikipedia_trends_research"
    description: str = (
        "Track public interest in topics through Wikipedia pageview trends. "
        "Rising pageviews indicate growing public awareness."
    )

    def _run(self, query: str) -> str:
        try:
            client = httpx.Client(
                timeout=15,
                headers={"User-Agent": "IdeaForge/0.1 (research tool)"},
            )
            results = []

            # Get top viewed pages (most recent available day)
            today = datetime.now()
            for days_back in range(1, 5):
                date = today - timedelta(days=days_back)
                date_str = date.strftime("%Y/%m/%d")
                try:
                    resp = client.get(
                        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/"
                        f"top/en.wikipedia/all-access/{date_str}"
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        articles = data.get("items", [{}])[0].get("articles", [])
                        query_lower = query.lower()
                        relevant = [
                            a for a in articles[:200]
                            if query_lower in a.get("article", "").lower().replace("_", " ")
                        ]
                        if relevant:
                            for a in relevant[:5]:
                                results.append(
                                    f"- {a['article'].replace('_', ' ')}: "
                                    f"{a['views']:,} views on {date_str}"
                                )
                        break
                except Exception:
                    continue

            # Get pageviews for specific article matching query
            article_name = query.replace(" ", "_")
            end = datetime.now()
            start = end - timedelta(days=30)
            try:
                resp = client.get(
                    f"https://wikimedia.org/api/rest_v1/metrics/pageviews/"
                    f"per-article/en.wikipedia/all-access/all-agents/"
                    f"{article_name}/daily/"
                    f"{start.strftime('%Y%m%d')}/{end.strftime('%Y%m%d')}"
                )
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("items", [])
                    if items:
                        views = [i["views"] for i in items]
                        avg = sum(views) / len(views)
                        first_week = sum(views[:7]) / 7 if len(views) >= 7 else avg
                        last_week = sum(views[-7:]) / 7 if len(views) >= 7 else avg
                        trend = "rising" if last_week > first_week * 1.1 else "stable" if last_week > first_week * 0.9 else "declining"
                        results.append(
                            f"\nPageviews for '{query}' (30 days):\n"
                            f"  Average: {avg:,.0f}/day | Trend: {trend}\n"
                            f"  First week avg: {first_week:,.0f} | Last week avg: {last_week:,.0f}"
                        )
            except Exception:
                pass

            client.close()
            return "\n".join(results) if results else f"No Wikipedia data for '{query}'"

        except Exception as e:
            return f"Wikipedia error: {str(e)}"
