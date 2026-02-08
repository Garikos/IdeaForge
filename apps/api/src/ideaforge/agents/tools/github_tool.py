"""GitHub Trending research tool via REST API."""

from __future__ import annotations

import httpx
from crewai.tools import BaseTool

from ...config import settings


class GitHubTrendingTool(BaseTool):
    name: str = "github_trending_research"
    description: str = (
        "Find trending GitHub repositories, growing technologies, "
        "and open-source ecosystem opportunities."
    )

    def _run(self, query: str) -> str:
        try:
            headers = {"Accept": "application/vnd.github.v3+json"}
            if settings.github_token:
                headers["Authorization"] = f"token {settings.github_token}"

            client = httpx.Client(timeout=15, headers=headers)
            results = []

            # Search repositories
            resp = client.get(
                "https://api.github.com/search/repositories",
                params={
                    "q": f"{query} stars:>100",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 10,
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for repo in data.get("items", []):
                results.append(
                    f"- {repo['full_name']}: {repo.get('description', 'No description')}\n"
                    f"  Stars: {repo['stargazers_count']} | Forks: {repo['forks_count']} | "
                    f"Language: {repo.get('language', 'N/A')}\n"
                    f"  Topics: {repo.get('topics', [])}\n"
                    f"  URL: {repo['html_url']}\n"
                    f"  Created: {repo['created_at']} | Updated: {repo['updated_at']}"
                )

            # Search for recently created repos (trending potential)
            resp2 = client.get(
                "https://api.github.com/search/repositories",
                params={
                    "q": f"{query} created:>2025-01-01",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 5,
                },
            )
            if resp2.status_code == 200:
                new_repos = resp2.json().get("items", [])
                if new_repos:
                    results.append("\n--- Recently Created (Rising) ---")
                    for repo in new_repos:
                        results.append(
                            f"- {repo['full_name']}: {repo.get('description', '')}\n"
                            f"  Stars: {repo['stargazers_count']} | "
                            f"Created: {repo['created_at']}"
                        )

            client.close()
            return "\n\n".join(results) if results else f"No GitHub results for '{query}'"

        except Exception as e:
            return f"GitHub error: {str(e)}"
