import pytest
import numpy as np
from typing import List, Dict

from ai_core.interfaces.embedder import Embedder
from ai_core.interfaces.vector_store import VectorStore
from ai_core.interfaces.llm_client import LLMClient
from ai_core.errors import EmbedderMismatchError

class FakeEmbedder(Embedder):
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return np.zeros((len(texts), 3), dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        return np.zeros(3, dtype=np.float32)

    @property
    def dimension(self) -> int:
        return 3

    @property
    def model_id(self) -> str:
        return "fake-embedder"

    @property
    def confidence_threshold(self) -> float:
        return 0.5

class FakeLLMClient(LLMClient):
    def extract(self, prompt: str) -> Dict:
        return {
            "product_type": "pipe",
            "material_grade": None,
            "product_form": None,
            "application": None,
            "explicit_standard_numbers": ["IS 123"],
            "detected_language": "English"
        }

    def generate(self, prompt: str) -> str:
        return "This is a fake synthesized response based on context."

def test_embedder_contract():
    embedder = FakeEmbedder()
    res = embedder.embed_texts(["test"])
    assert res.shape == (1, 3)
    query = embedder.embed_query("test")
    assert query.shape == (3,)

def test_vector_store_contract():
    from ai_core.impl.in_memory_vector_store import InMemoryVectorStore
    store = InMemoryVectorStore()
    store.configure_embedder("fake-embedder", 3)
    store.add(["id1"], np.array([[1, 0, 0]], dtype=np.float32))
    res = store.search(np.array([1, 0, 0], dtype=np.float32))
    assert len(res) == 1
    assert res[0][0] == "id1"
    
def test_vector_store_safety():
    from ai_core.impl.in_memory_vector_store import InMemoryVectorStore
    store = InMemoryVectorStore()
    store.configure_embedder("fake-embedder", 3)
    with pytest.raises(EmbedderMismatchError):
        store.configure_embedder("other", 3)
    with pytest.raises(EmbedderMismatchError):
        store.add(["id2"], np.array([[1, 0]], dtype=np.float32))

@pytest.mark.slow
@pytest.mark.needs_api_key
def test_real_llm_contract():
    pass
