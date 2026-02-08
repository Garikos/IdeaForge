"""Google Trends research tool using pytrends."""

from __future__ import annotations

from crewai.tools import BaseTool


class GoogleTrendsTool(BaseTool):
    name: str = "google_trends_research"
    description: str = (
        "Research Google Trends data: trending searches, interest over time, "
        "related queries, and geographic interest for a given keyword."
    )

    def _run(self, query: str) -> str:
        try:
            from pytrends.request import TrendReq

            pytrends = TrendReq(hl="en-US", tz=360)

            results = []

            # Trending searches (global)
            try:
                trending = pytrends.trending_searches(pn="united_states")
                top_trending = trending.head(10).values.tolist()
                results.append(f"Top trending searches (US): {[t[0] for t in top_trending]}")
            except Exception:
                results.append("Trending searches: unavailable")

            # Interest over time
            try:
                pytrends.build_payload([query], timeframe="today 3-m")
                iot = pytrends.interest_over_time()
                if not iot.empty:
                    avg_interest = iot[query].mean()
                    max_interest = iot[query].max()
                    recent = iot[query].tail(7).mean()
                    results.append(
                        f"Interest for '{query}': avg={avg_interest:.0f}, "
                        f"max={max_interest:.0f}, last_7_days_avg={recent:.0f}"
                    )
            except Exception:
                results.append(f"Interest over time for '{query}': unavailable")

            # Related queries
            try:
                related = pytrends.related_queries()
                if query in related and related[query]["rising"] is not None:
                    rising = related[query]["rising"].head(10)
                    rising_list = rising["query"].tolist()
                    results.append(f"Rising related queries: {rising_list}")
                if query in related and related[query]["top"] is not None:
                    top = related[query]["top"].head(10)
                    top_list = top["query"].tolist()
                    results.append(f"Top related queries: {top_list}")
            except Exception:
                results.append("Related queries: unavailable")

            # Suggestions
            try:
                suggestions = pytrends.suggestions(keyword=query)
                if suggestions:
                    titles = [s["title"] for s in suggestions[:10]]
                    results.append(f"Suggestions: {titles}")
            except Exception:
                pass

            return "\n".join(results) if results else f"No trend data found for '{query}'"

        except ImportError:
            return "Google Trends tool: pytrends library not installed"
        except Exception as e:
            return f"Google Trends error: {str(e)}"
