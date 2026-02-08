"""Shared memory via ChromaDB for agent collaboration."""

from __future__ import annotations

from typing import Any

import chromadb
import structlog

from ..config import settings

logger = structlog.get_logger()

_client: chromadb.HttpClient | None = None


def get_chroma_client() -> chromadb.HttpClient:
    global _client
    if _client is None:
        _client = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
        )
    return _client


class SharedMemory:
    """Shared memory for agents to store and retrieve research findings."""

    COLLECTION_NAME = "research_findings"

    def __init__(self):
        try:
            self._client = get_chroma_client()
            self._collection = self._client.get_or_create_collection(
                name=self.COLLECTION_NAME,
            )
        except Exception as e:
            logger.warning("ChromaDB not available, using in-memory fallback", error=str(e))
            self._client = None
            self._collection = None
            self._fallback: list[dict] = []

    def store(self, doc_id: str, text: str, metadata: dict[str, Any] | None = None):
        if self._collection is not None:
            self._collection.upsert(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata or {}],
            )
        else:
            self._fallback.append({"id": doc_id, "text": text, "metadata": metadata or {}})

    def search(self, query: str, n_results: int = 5) -> list[dict]:
        if self._collection is not None:
            results = self._collection.query(
                query_texts=[query],
                n_results=n_results,
            )
            items = []
            for i, doc_id in enumerate(results["ids"][0]):
                items.append({
                    "id": doc_id,
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                })
            return items
        # Fallback: simple text search
        return [
            item for item in self._fallback
            if query.lower() in item["text"].lower()
        ][:n_results]
