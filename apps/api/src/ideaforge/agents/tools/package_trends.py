"""npm/PyPI package trends research tool."""

from __future__ import annotations

import httpx
from crewai.tools import BaseTool


class PackageTrendsTool(BaseTool):
    name: str = "package_trends_research"
    description: str = (
        "Analyze npm and PyPI package download trends to identify "
        "growing ecosystems and technology adoption patterns."
    )

    def _run(self, query: str) -> str:
        try:
            client = httpx.Client(timeout=15)
            results = []
            keywords = query.lower().split()

            # npm search
            try:
                resp = client.get(
                    f"https://registry.npmjs.org/-/v1/search",
                    params={"text": query, "size": 5},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    results.append("=== npm Packages ===")
                    for pkg in data.get("objects", []):
                        p = pkg.get("package", {})
                        name = p.get("name", "")
                        # Get download stats
                        dl_resp = client.get(
                            f"https://api.npmjs.org/downloads/point/last-month/{name}"
                        )
                        downloads = "N/A"
                        if dl_resp.status_code == 200:
                            downloads = f"{dl_resp.json().get('downloads', 0):,}"

                        results.append(
                            f"- {name}: {p.get('description', '')[:150]}\n"
                            f"  Downloads (last month): {downloads}\n"
                            f"  Version: {p.get('version', 'N/A')} | "
                            f"Keywords: {p.get('keywords', [])[:5]}"
                        )
            except Exception:
                results.append("npm search: unavailable")

            # PyPI search
            try:
                for keyword in keywords[:3]:
                    resp = client.get(
                        f"https://pypi.org/pypi/{keyword}/json"
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        info = data.get("info", {})
                        results.append(
                            f"\n=== PyPI: {info.get('name', keyword)} ===\n"
                            f"  Summary: {info.get('summary', 'N/A')}\n"
                            f"  Version: {info.get('version', 'N/A')}\n"
                            f"  URL: {info.get('project_url', '')}"
                        )

                        # Try to get download stats from pypistats
                        stats_resp = client.get(
                            f"https://pypistats.org/api/packages/{keyword}/recent"
                        )
                        if stats_resp.status_code == 200:
                            stats = stats_resp.json().get("data", {})
                            results.append(
                                f"  Downloads (last month): {stats.get('last_month', 'N/A'):,}"
                            )
            except Exception:
                pass

            client.close()
            return "\n".join(results) if results else f"No package data for '{query}'"

        except Exception as e:
            return f"Package trends error: {str(e)}"
