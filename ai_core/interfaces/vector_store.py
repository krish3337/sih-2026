"""
VectorStore interface — abstract contract for embedding-based retrieval.

Pipeline modules depend on this interface, never on a concrete implementation.
Wiring (which impl to use) happens only in config.py.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np


class VectorStore(ABC):
    """Store and search dense vector embeddings keyed by standard ID."""

    @abstractmethod
    def add(self, ids: List[str], embeddings: np.ndarray) -> None:
        """Add embeddings to the store.

        Parameters
        ----------
        ids : list[str]
            Standard base_ids corresponding to each row of *embeddings*.
        embeddings : np.ndarray
            2-D array of shape ``(len(ids), embedding_dim)``.
        """

    @abstractmethod
    def search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """Return the *top_k* closest IDs by similarity score.

        Parameters
        ----------
        query_embedding : np.ndarray
            1-D array of shape ``(embedding_dim,)``.
        top_k : int
            Number of results to return.

        Returns
        -------
        list[tuple[str, float]]
            ``(standard_base_id, similarity_score)`` pairs, sorted
            descending by score.
        """
