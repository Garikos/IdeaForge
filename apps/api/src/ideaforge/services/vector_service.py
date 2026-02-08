"""Vector store service — CRUD operations for ChromaDB."""

from __future__ import annotations

from typing import Any

import structlog

from ..core.memory import SharedMemory

logger = structlog.get_logger()


class VectorService:
    """Service layer for ChromaDB vector operations."""

    def __init__(self):
        self._memory = SharedMemory()

    def store_finding(self, doc_id: str, text: str, metadata: dict[str, Any] | None = None):
        """Store a research finding in the vector database."""
        self._memory.store(doc_id, text, metadata)
        logger.debug("Stored finding", doc_id=doc_id)

    def search_similar(self, query: str, n_results: int = 5) -> list[dict]:
        """Search for similar findings."""
        return self._memory.search(query, n_results)

    def store_idea(self, idea_id: str, title: str, summary: str, source: str):
        """Store a business idea for semantic search."""
        text = f"{title}. {summary}"
        metadata = {"source": source, "type": "business_idea"}
        self._memory.store(f"idea_{idea_id}", text, metadata)


vector_service = VectorService()
