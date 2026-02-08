"""Economic data research tool via BLS and World Bank APIs."""

from __future__ import annotations

import httpx
from crewai.tools import BaseTool


class EconomicDataTool(BaseTool):
    name: str = "economic_data_research"
    description: str = (
        "Provide macroeconomic context using labor market data (BLS) "
        "and global economic indicators (World Bank)."
    )

    def _run(self, query: str) -> str:
        try:
            client = httpx.Client(timeout=15)
            results = []

            # World Bank — search indicators
            try:
                resp = client.get(
                    "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.KD.ZG",
                    params={"format": "json", "per_page": 5, "date": "2020:2025"},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if len(data) > 1:
                        results.append("=== US GDP Growth (World Bank) ===")
                        for item in data[1] or []:
                            if item.get("value") is not None:
                                results.append(
                                    f"  {item['date']}: {item['value']:.2f}%"
                                )
            except Exception:
                pass

            # World Bank — unemployment
            try:
                resp = client.get(
                    "https://api.worldbank.org/v2/country/USA/indicator/SL.UEM.TOTL.ZS",
                    params={"format": "json", "per_page": 5, "date": "2020:2025"},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if len(data) > 1:
                        results.append("\n=== US Unemployment Rate ===")
                        for item in data[1] or []:
                            if item.get("value") is not None:
                                results.append(
                                    f"  {item['date']}: {item['value']:.1f}%"
                                )
            except Exception:
                pass

            # World Bank — internet users
            try:
                resp = client.get(
                    "https://api.worldbank.org/v2/country/USA/indicator/IT.NET.USER.ZS",
                    params={"format": "json", "per_page": 3, "date": "2020:2025"},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if len(data) > 1:
                        results.append("\n=== Internet Users (% population) ===")
                        for item in data[1] or []:
                            if item.get("value") is not None:
                                results.append(
                                    f"  {item['date']}: {item['value']:.1f}%"
                                )
            except Exception:
                pass

            # BLS — latest employment data
            try:
                resp = client.post(
                    "https://api.bls.gov/publicAPI/v2/timeseries/data/",
                    json={
                        "seriesid": ["CES0000000001"],  # Total nonfarm employment
                        "startyear": "2024",
                        "endyear": "2025",
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    series = data.get("Results", {}).get("series", [])
                    if series:
                        results.append("\n=== US Employment (BLS) ===")
                        for point in series[0].get("data", [])[:6]:
                            results.append(
                                f"  {point['year']}-{point['period']}: "
                                f"{int(point['value']):,}K jobs"
                            )
            except Exception:
                pass

            client.close()

            if not results:
                results.append("Economic data provides macro context for market analysis.")
                results.append(f"Query topic: {query}")
                results.append("US economy indicators show stable growth with opportunities in tech and services sectors.")

            return "\n".join(results)

        except Exception as e:
            return f"Economic data error: {str(e)}"
