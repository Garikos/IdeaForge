"""Research Crew — dynamically assembles agents from user-selected sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import yaml
import structlog
from crewai import Agent, Crew, Task, Process

from ...core.llm_registry import get_llm
from ..tools import TOOL_REGISTRY, SentimentAnalysisTool

logger = structlog.get_logger()

CONFIG_DIR = Path(__file__).parent.parent / "config"


def _load_yaml(filename: str) -> dict:
    with open(CONFIG_DIR / filename, "r") as f:
        return yaml.safe_load(f)


class ResearchCrew:
    """Dynamically builds a CrewAI crew from user-selected data sources."""

    def run(
        self,
        query: str,
        selected_sources: list[str],
        llm_provider: str = "groq",
        run_id: str = "",
        on_agent_start: Callable | None = None,
        on_agent_complete: Callable | None = None,
        on_agent_error: Callable | None = None,
    ) -> list[dict[str, Any]]:
        """Build and run a research crew.

        Args:
            query: The research query from the user.
            selected_sources: List of source IDs to include.
            llm_provider: Which LLM provider to use.
            run_id: Unique run identifier.
            on_agent_start: Callback when an agent starts.
            on_agent_complete: Callback when an agent finishes.
            on_agent_error: Callback when an agent fails.

        Returns:
            List of business ideas as dicts.
        """
        agents_config = _load_yaml("agents.yaml")
        tasks_config = _load_yaml("tasks.yaml")
        llm = get_llm(llm_provider)

        agents: list[Agent] = []
        tasks: list[Task] = []

        # Create research agents for each selected source
        for source_id in selected_sources:
            tool_class = TOOL_REGISTRY.get(source_id)
            if not tool_class:
                logger.warning("Unknown source", source_id=source_id)
                continue

            # Find matching agent config
            agent_key = f"{source_id}_researcher"
            agent_cfg = agents_config.get(agent_key)
            if not agent_cfg:
                # Fallback: use a generic researcher config
                agent_cfg = {
                    "role": f"{source_id.replace('_', ' ').title()} Researcher",
                    "goal": f"Research {source_id} for data about {{query}}",
                    "backstory": f"You are an expert at using {source_id} to find business opportunities.",
                    "verbose": True,
                }

            tool_instance = tool_class()
            agent = Agent(
                role=agent_cfg["role"],
                goal=agent_cfg["goal"].format(query=query),
                backstory=agent_cfg["backstory"],
                tools=[tool_instance],
                llm=llm,
                verbose=agent_cfg.get("verbose", True),
            )
            agents.append(agent)

            task_cfg = tasks_config.get("research_source_task", {})
            task = Task(
                description=task_cfg.get("description", "Research {query}").format(query=query),
                expected_output=task_cfg.get("expected_output", "Research findings"),
                agent=agent,
            )
            tasks.append(task)

        if not agents:
            logger.error("No agents created", selected_sources=selected_sources)
            return []

        # Add sentiment analyst
        sentiment_cfg = agents_config.get("sentiment_analyst", {})
        sentiment_agent = Agent(
            role=sentiment_cfg.get("role", "Sentiment Analyst"),
            goal=sentiment_cfg.get("goal", "Analyze sentiment").format(query=query),
            backstory=sentiment_cfg.get("backstory", "You analyze text sentiment."),
            tools=[SentimentAnalysisTool()],
            llm=llm,
            verbose=True,
        )
        agents.append(sentiment_agent)
        tasks.append(Task(
            description=f"Analyze the sentiment of all research findings about '{query}'.",
            expected_output="Sentiment analysis summary with scores.",
            agent=sentiment_agent,
        ))

        # Add synthesizer as final agent
        synth_cfg = agents_config.get("research_synthesizer", {})
        synthesizer = Agent(
            role=synth_cfg.get("role", "Research Synthesizer"),
            goal=synth_cfg.get("goal", "Synthesize findings").format(query=query),
            backstory=synth_cfg.get("backstory", "You synthesize research into business ideas."),
            llm=llm,
            verbose=True,
        )
        agents.append(synthesizer)

        synth_task_cfg = tasks_config.get("synthesize_task", {})
        synth_task = Task(
            description=synth_task_cfg.get("description", "Synthesize findings for {query}").format(query=query),
            expected_output=synth_task_cfg.get("expected_output", "JSON array of business ideas"),
            agent=synthesizer,
            output_json=True,
        )
        tasks.append(synth_task)

        # Build and run crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

        logger.info(
            "Running research crew",
            run_id=run_id,
            num_agents=len(agents),
            sources=selected_sources,
        )

        result = crew.kickoff()

        # Parse result into list of ideas
        return self._parse_results(result, run_id)

    def _parse_results(self, result: Any, run_id: str) -> list[dict]:
        """Parse crew output into structured business ideas."""
        try:
            raw = str(result)

            # Try to extract JSON from the output
            # Look for JSON array in the text
            start = raw.find("[")
            end = raw.rfind("]") + 1

            if start >= 0 and end > start:
                json_str = raw[start:end]
                ideas = json.loads(json_str)
                if isinstance(ideas, list):
                    # Add composite_score if not present
                    for idea in ideas:
                        if "composite_score" not in idea:
                            scores = [
                                idea.get("business_potential", 0) or 0,
                                idea.get("market_size_score", 0) or 0,
                                1 - (idea.get("competition_score", 0) or 0),  # Invert: less competition = better
                                idea.get("sentiment_score", 0) or 0,
                            ]
                            idea["composite_score"] = sum(scores) / len(scores) if scores else 0
                        idea["research_run_id"] = run_id
                    return sorted(ideas, key=lambda x: x.get("composite_score", 0), reverse=True)

            logger.warning("Could not parse JSON from crew output", raw=raw[:500])
            return [
                {
                    "title": "Research completed",
                    "summary": raw[:1000],
                    "source": "synthesizer",
                    "composite_score": 0.5,
                    "research_run_id": run_id,
                }
            ]

        except Exception as e:
            logger.error("Error parsing results", error=str(e))
            return []
