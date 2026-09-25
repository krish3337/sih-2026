from typing import List
import numpy as np

from ai_core.interfaces.embedder import Embedder

class E5Embedder(Embedder):
    """Wraps a sentence-transformer model (multilingual-e5-large) for encoding texts and queries."""

    def __init__(self, model_name: str = "intfloat/multilingual-e5-large") -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required for embedding. "
                "Install with:  pip install sentence-transformers"
            ) from exc

        self._model_name = model_name
        self._model = SentenceTransformer(model_name)

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        prefixed = [f"passage: {t}" for t in texts]
        embeddings = self._model.encode(
            prefixed,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > 20,
        )
        return np.asarray(embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        prefixed = f"query: {query}"
        embedding = self._model.encode(
            prefixed,
            normalize_embeddings=True,
        )
        return np.asarray(embedding, dtype=np.float32)

    @property
    def dimension(self) -> int:
        return self._model.get_sentence_embedding_dimension()
        
    @property
    def model_id(self) -> str:
        return self._model_name
        
    @property
    def confidence_threshold(self) -> float:
        # UNCALIBRATED default for e5
        return 0.80
