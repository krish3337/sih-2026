"""
retriever.py — Semantic retrieval of candidate standards.

Embeds the query, searches the VectorStore, and returns ranked
candidates with a low-confidence flag when the top score falls below
the configured threshold.

Depends only on the VectorStore interface and the Embedder utility —
never on a concrete impl/ class.
"""

from typing import Dict, List

from ai_core.interfaces.vector_store import VectorStore
from ai_core.interfaces.standards_repository import StandardsRepository
from ai_core.interfaces.embedder import Embedder


class Retriever:
    """Semantic retrieval of candidate standards from the VectorStore."""

    def __init__(
        self,
        vector_store: VectorStore,
        standards_repo: StandardsRepository,
        embedder: Embedder,
        confidence_threshold: float = None,
    ) -> None:
        """
        Parameters
        ----------
        vector_store : VectorStore
            Populated vector store to search against.
        standards_repo : StandardsRepository
            For enriching results with standard metadata.
        embedder : Embedder
            For encoding the query text.
        confidence_threshold : float
            Minimum top-score to consider a match confident.
            Below this, results are flagged ``low_confidence: True``.
        """
        self._vector_store = vector_store
        self._repo = standards_repo
        self._embedder = embedder
        self._threshold = confidence_threshold if confidence_threshold is not None else embedder.confidence_threshold

    def retrieve_candidates(
        self,
        retrieval_query: str,
        top_k: int = 5,
    ) -> List[Dict]:
        """Retrieve the top-k candidate standards for a query.

        Parameters
        ----------
        retrieval_query : str
            Clean query string (from query_understanding, not raw user
            input).
        top_k : int
            Number of candidates to return.

        Returns
        -------
        list[dict]
            Each dict contains:
            - ``base_id``: normalised standard ID
            - ``standard_id``: full standard ID (e.g. "IS 5504:2025")
            - ``title``: standard title
            - ``scope_description``: scope text (evidence snippet)
            - ``score``: cosine similarity score (float, 0–1)
            - ``low_confidence``: bool, True if this result's score
              is below the confidence threshold
            - ``status``: standard status
            - ``current_version_year``: edition year

            Sorted descending by score.
        """
        # Embed the query
        query_embedding = self._embedder.embed_query(retrieval_query)

        # Search the vector store
        raw_results = self._vector_store.search(query_embedding, top_k=top_k)

        if not raw_results:
            return []

        # Determine confidence flag based on the top score
        top_score = raw_results[0][1]
        is_low_confidence = top_score < self._threshold

        # Enrich each result with metadata from the repository
        candidates = []
        for base_id, score in raw_results:
            record = self._repo.get(base_id)

            candidate: Dict = {
                "base_id": base_id,
                "standard_id": record["standard_id"] if record else base_id,
                "title": record.get("title", "N/A") if record else "N/A",
                "scope_description": (
                    record.get("scope_description", "N/A") if record else "N/A"
                ),
                "score": round(score, 4),
                "low_confidence": is_low_confidence,
                "status": record.get("status", "N/A") if record else "N/A",
                "current_version_year": (
                    record.get("current_version_year", "N/A")
                    if record else "N/A"
                ),
            }
            candidates.append(candidate)

        return candidates

    @property
    def confidence_threshold(self) -> float:
        """Current confidence threshold."""
        return self._threshold

    @confidence_threshold.setter
    def confidence_threshold(self, value: float) -> None:
        """Update the confidence threshold at runtime."""
        self._threshold = value
