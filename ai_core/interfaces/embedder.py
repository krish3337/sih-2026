from abc import ABC, abstractmethod
from typing import List
import numpy as np

class Embedder(ABC):
    """Abstract interface for embedding texts and queries."""
    
    @abstractmethod
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embed document texts.
        
        Returns a 2-D array of shape (len(texts), embedding_dim).
        """
        pass
        
    @abstractmethod
    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single search query.
        
        Returns a 1-D array of shape (embedding_dim,).
        """
        pass
        
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Dimensionality of the model's output vectors."""
        pass
        
    @property
    @abstractmethod
    def model_id(self) -> str:
        """Identifier of the embedding model."""
        pass
        
    @property
    @abstractmethod
    def confidence_threshold(self) -> float:
        """UNCALIBRATED: The recommended confidence threshold for this embedder."""
        pass
