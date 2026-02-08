"""Sentiment analysis tool using VADER."""

from __future__ import annotations

from crewai.tools import BaseTool


class SentimentAnalysisTool(BaseTool):
    name: str = "sentiment_analysis"
    description: str = (
        "Analyze the sentiment (positive/negative/neutral) of given text. "
        "Works locally without API calls. Good for short texts like comments and posts."
    )

    def _run(self, text: str) -> str:
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

            analyzer = SentimentIntensityAnalyzer()

            # Handle multiple texts separated by newlines
            lines = [line.strip() for line in text.split("\n") if line.strip()]

            if not lines:
                return "No text provided for sentiment analysis"

            overall_scores = {"neg": 0.0, "neu": 0.0, "pos": 0.0, "compound": 0.0}
            results = []

            for line in lines[:20]:  # Limit to 20 texts
                scores = analyzer.polarity_scores(line)
                for key in overall_scores:
                    overall_scores[key] += scores[key]

                label = "positive" if scores["compound"] >= 0.05 else "negative" if scores["compound"] <= -0.05 else "neutral"
                results.append(f"  [{label}] ({scores['compound']:+.3f}) {line[:100]}")

            count = len(results)
            avg_compound = overall_scores["compound"] / count

            overall_label = "positive" if avg_compound >= 0.05 else "negative" if avg_compound <= -0.05 else "neutral"

            summary = (
                f"Sentiment Analysis ({count} texts):\n"
                f"Overall: {overall_label} (compound: {avg_compound:+.3f})\n"
                f"Avg scores — pos: {overall_scores['pos']/count:.3f}, "
                f"neu: {overall_scores['neu']/count:.3f}, "
                f"neg: {overall_scores['neg']/count:.3f}\n\n"
                f"Details:\n" + "\n".join(results)
            )

            return summary

        except ImportError:
            return "Sentiment tool: vaderSentiment not installed"
        except Exception as e:
            return f"Sentiment analysis error: {str(e)}"
