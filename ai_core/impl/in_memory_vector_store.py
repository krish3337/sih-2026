"""
InMemoryVectorStore — brute-force cosine similarity over numpy arrays.

Sufficient and simplest at the current 11-standard dataset scale.
Implements the VectorStore interface; swappable to FAISS / ChromaDB
for the scaled version without changing any pipeline code.
"""

from typing import List, Tuple

import numpy as np

from ai_core.interfaces.vector_store import VectorStore


class InMemoryVectorStore(VectorStore):
    """Brute-force cosine similarity search over in-memory embeddings."""

    def __init__(self) -> None:
        self._ids: List[str] = []
        self._embeddings: np.ndarray | None = None

    # ── VectorStore interface ────────────────────────────────────────────

    def add(self, ids: List[str], embeddings: np.ndarray) -> None:
        """Store *ids* and their corresponding *embeddings*.

        Normalises embeddings to unit vectors at load time so search()
        can use dot product instead of full cosine computation.
        """
        if embeddings.ndim != 2:
            raise ValueError(
                f"embeddings must be 2-D (got {embeddings.ndim}-D)"
            )
        if len(ids) != embeddings.shape[0]:
            raise ValueError(
                f"len(ids)={len(ids)} != embeddings rows={embeddings.shape[0]}"
            )

        # L2-normalise so dot product == cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)  # guard against zero vectors
        normalised = embeddings / norms

        if self._embeddings is None:
            self._ids = list(ids)
            self._embeddings = normalised
        else:
            self._ids.extend(ids)
            self._embeddings = np.vstack([self._embeddings, normalised])

    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """Return the *top_k* closest IDs by cosine similarity.

        Returns an empty list if the store is empty.
        """
        if self._embeddings is None or len(self._ids) == 0:
            return []

        # Normalise the query vector
        query = query_embedding.flatten()
        norm = np.linalg.norm(query)
        if norm == 0:
            return []
        query = query / norm

        # Cosine similarity via dot product (embeddings already unit-normed)
        scores = self._embeddings @ query  # shape: (n_standards,)

        # Top-k indices, descending
        k = min(top_k, len(self._ids))
        top_indices = np.argsort(scores)[::-1][:k]

        return [
            (self._ids[i], float(scores[i]))
            for i in top_indices
        ]

    # ── Utility ──────────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        """Number of stored embeddings."""
        return len(self._ids)
