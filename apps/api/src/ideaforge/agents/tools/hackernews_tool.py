"""Hacker News research tool via Firebase API (free, no limits)."""

from __future__ import annotations

import httpx
from crewai.tools import BaseTool

HN_API = "https://hacker-news.firebaseio.com/v0"


class HackerNewsResearchTool(BaseTool):
    name: str = "hackernews_research"
    description: str = (
        "Research Hacker News for tech trends, startup discussions, "
        "and developer sentiment. Uses Firebase API (free, unlimited)."
    )

    def _run(self, query: str) -> str:
        try:
            client = httpx.Client(timeout=15)
            results = []
            query_lower = query.lower()

            # Get top and best stories
            for story_type in ["topstories", "beststories", "showstories"]:
                try:
                    resp = client.get(f"{HN_API}/{story_type}.json")
                    story_ids = resp.json()[:50]  # Check top 50

                    for sid in story_ids:
                        try:
                            item_resp = client.get(f"{HN_API}/item/{sid}.json")
                            item = item_resp.json()
                            if not item or "title" not in item:
                                continue

                            title = item.get("title", "")
                            if query_lower in title.lower() or any(
                                word in title.lower() for word in query_lower.split()
                            ):
                                # Get a few top comments
                                comments = []
                                for kid in item.get("kids", [])[:3]:
                                    try:
                                        c_resp = client.get(f"{HN_API}/item/{kid}.json")
                                        c = c_resp.json()
                                        if c and "text" in c:
                                            comments.append(c["text"][:200])
                                    except Exception:
                                        continue

                                results.append(
                                    f"[{story_type}] {title}\n"
                                    f"  Score: {item.get('score', 0)} | "
                                    f"Comments: {item.get('descendants', 0)}\n"
                                    f"  URL: {item.get('url', f'https://news.ycombinator.com/item?id={sid}')}\n"
                                    f"  HN: https://news.ycombinator.com/item?id={sid}\n"
                                    f"  Sample comments: {comments[:2]}"
                                )

                                if len(results) >= 10:
                                    break
                        except Exception:
                            continue

                    if len(results) >= 10:
                        break
                except Exception:
                    continue

            client.close()
            return "\n\n".join(results) if results else f"No HN results for '{query}'"

        except Exception as e:
            return f"Hacker News error: {str(e)}"
