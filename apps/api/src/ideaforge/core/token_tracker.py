"""Token usage tracker for research runs."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    llm_calls: int = 0


class TokenTracker:
    """Thread-safe token accumulator for a single research run."""

    def __init__(
        self,
        run_id: str,
        provider: str,
        tpm_limit: int | None = None,
        on_update: Callable[[dict[str, Any]], None] | None = None,
    ):
        self.run_id = run_id
        self.provider = provider
        self.tpm_limit = tpm_limit
        self._usage = TokenUsage()
        self._lock = threading.Lock()
        self._on_update = on_update

    def record(self, prompt_tokens: int, completion_tokens: int) -> None:
        """Record tokens from a single LLM call."""
        with self._lock:
            self._usage.prompt_tokens += prompt_tokens
            self._usage.completion_tokens += completion_tokens
            self._usage.total_tokens += prompt_tokens + completion_tokens
            self._usage.llm_calls += 1

        if self._on_update:
            try:
                self._on_update(self.snapshot())
            except Exception:
                pass

    def snapshot(self) -> dict[str, Any]:
        """Return current token usage as a dict for WS broadcasting."""
        with self._lock:
            return {
                "type": "token_usage",
                "run_id": self.run_id,
                "provider": self.provider,
                "prompt_tokens": self._usage.prompt_tokens,
                "completion_tokens": self._usage.completion_tokens,
                "total_tokens": self._usage.total_tokens,
                "llm_calls": self._usage.llm_calls,
                "tpm_limit": self.tpm_limit,
            }
