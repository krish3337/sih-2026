"""
embedder.py — Multilingual embedding utility for scope texts and queries.

Uses sentence-transformers with a multilingual model to satisfy the
English + Hindi requirement.  The model choice is configurable; the
default (multilingual-e5-large) handles both languages without a
separate translation step.

This module is a standalone utility — not behind an interface — since
embedding is always local inference, not an infrastructure-swappable
concern like storage or LLM provider.
"""

from typing import List

import numpy as np


class Embedder:
    """Wraps a sentence-transformer model for encoding texts and queries."""

    def __init__(
        self,
        model_name: str = "intfloat/multilingual-e5-large",
    ) -> None:
        """Load the embedding model.

        Parameters
        ----------
        model_name : str
            HuggingFace model identifier.  Tested options:
            - ``"intfloat/multilingual-e5-large"``  (~1.1 GB, recommended)
            - ``"BAAI/bge-m3"``                     (~2.3 GB, heavier)
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required for embedding. "
                "Install with:  pip install sentence-transformers"
            ) from exc

        self._model_name = model_name
        self._model = SentenceTransformer(model_name)

    # ── Public API ───────────────────────────────────────────────────────

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embed document texts (standard scope descriptions).

        Returns a 2-D array of shape ``(len(texts), embedding_dim)``.
        """
        prefixed = self._prefix_passages(texts)
        embeddings = self._model.encode(
            prefixed,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > 20,
        )
        return np.asarray(embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single search query.

        Returns a 1-D array of shape ``(embedding_dim,)``.
        """
        prefixed = self._prefix_query(query)
        embedding = self._model.encode(
            prefixed,
            normalize_embeddings=True,
        )
        return np.asarray(embedding, dtype=np.float32)

    # ── Model-specific prefixing ─────────────────────────────────────────
    # E5 models require "query: " / "passage: " prefixes to distinguish
    # asymmetric retrieval roles.  BGE-M3 and most other models do not.

    def _prefix_passages(self, texts: List[str]) -> List[str]:
        if self._is_e5:
            return [f"passage: {t}" for t in texts]
        return texts

    def _prefix_query(self, query: str) -> str:
        if self._is_e5:
            return f"query: {query}"
        return query

    @property
    def _is_e5(self) -> bool:
        return "e5" in self._model_name.lower()

    @property
    def embedding_dim(self) -> int:
        """Dimensionality of the model's output vectors."""
        return self._model.get_sentence_embedding_dimension()
