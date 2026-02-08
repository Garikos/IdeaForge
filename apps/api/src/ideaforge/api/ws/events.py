"""WebSocket event types."""

from __future__ import annotations

from typing import Any


def agent_started(run_id: str, agent_name: str) -> dict[str, Any]:
    return {
        "type": "agent_started",
        "run_id": run_id,
        "agent_name": agent_name,
    }


def agent_completed(run_id: str, agent_name: str, summary: str) -> dict[str, Any]:
    return {
        "type": "agent_completed",
        "run_id": run_id,
        "agent_name": agent_name,
        "summary": summary,
    }


def agent_failed(run_id: str, agent_name: str, error: str) -> dict[str, Any]:
    return {
        "type": "agent_failed",
        "run_id": run_id,
        "agent_name": agent_name,
        "error": error,
    }


def research_started(run_id: str, query: str, sources: list[str]) -> dict[str, Any]:
    return {
        "type": "research_started",
        "run_id": run_id,
        "query": query,
        "sources": sources,
    }


def research_completed(run_id: str, ideas_count: int) -> dict[str, Any]:
    return {
        "type": "research_completed",
        "run_id": run_id,
        "ideas_count": ideas_count,
    }


def research_failed(run_id: str, error: str) -> dict[str, Any]:
    return {
        "type": "research_failed",
        "run_id": run_id,
        "error": error,
    }
