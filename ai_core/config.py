"""
config.py — Wiring: create concrete implementations and expose them as
interface types.

This is the ONLY module that imports from src/impl/.  Every other
pipeline module depends solely on the interfaces.
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)

from ai_core.interfaces.vector_store import VectorStore
from ai_core.interfaces.graph_store import GraphStore
from ai_core.interfaces.standards_repository import StandardsRepository
from ai_core.interfaces.llm_client import LLMClient
from ai_core.interfaces.embedder import Embedder

# ── Concrete impl imports (ONLY place in the codebase) ───────────────────
from ai_core.impl.in_memory_vector_store import InMemoryVectorStore
from ai_core.impl.in_memory_graph_store import InMemoryGraphStore
from ai_core.impl.in_memory_standards_repository import InMemoryStandardsRepository
from ai_core.impl.gemini_client import GeminiClient
from ai_core.impl.groq_client import GroqClient
from ai_core.impl.e5_embedder import E5Embedder


# ── Configuration constants ──────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
STANDARDS_PATH = os.path.join(DATA_DIR, "standards.json")
CERTIFICATION_PATH = os.path.join(DATA_DIR, "certification_rules.json")
RELATIONS_PATH = os.path.join(DATA_DIR, "relations.json")

# ── Registries ───────────────────────────────────────────────────────────
EMBEDDER_REGISTRY = {
    "e5": lambda: E5Embedder(model_name="intfloat/multilingual-e5-large"),
}

LLM_REGISTRY = {
    "gemini": lambda: GeminiClient(model_name="gemini-3.6-flash"),
    "groq": lambda: GroqClient(model_name=os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")),
}

# ── Factory functions ────────────────────────────────────────────────────

def create_embedder() -> Embedder:
    """Create the embedding model."""
    backend = os.environ.get("EMBEDDER_BACKEND", "e5")
    if backend == "fake":
        import numpy as np
        class FakeEmbedder(Embedder):
            model_id = "fake-model"
            confidence_threshold = 0.5
            
            @property
            def dimension(self) -> int:
                return 3
                
            def embed_query(self, query: str):
                return np.array([0.1, 0.2, 0.3])
                
            def embed_texts(self, texts):
                return np.array([[0.1, 0.2, 0.3] for _ in texts])
        return FakeEmbedder()
        
    if backend not in EMBEDDER_REGISTRY:
        raise ValueError(f"Unknown Embedder backend '{backend}'. Valid options: {list(EMBEDDER_REGISTRY.keys())}")
    return EMBEDDER_REGISTRY[backend]()


def create_vector_store() -> VectorStore:
    """Create an empty VectorStore (populated later by data_loader)."""
    return InMemoryVectorStore()


def create_graph_store() -> GraphStore:
    """Create an empty GraphStore (populated later by data_loader)."""
    return InMemoryGraphStore()


def create_standards_repository() -> StandardsRepository:
    """Create a StandardsRepository pre-loaded from JSON files."""
    return InMemoryStandardsRepository(
        standards_path=STANDARDS_PATH,
        certification_path=CERTIFICATION_PATH,
    )


def create_llm_client() -> LLMClient:
    """Create an LLMClient."""
    backend = os.environ.get("LLM_BACKEND", "gemini")
    if backend == "fake":
        class FakeLLMClient(LLMClient):
            def extract(self, prompt: str) -> dict:
                return {
                    "product_type": "steel pipe",
                    "material_grade": None,
                    "product_form": "pipe",
                    "application": "general",
                    "explicit_standard_numbers": [],
                    "detected_language": "en"
                }
            def generate(self, prompt: str) -> str:
                return "This is a mock AI explanation for testing purposes."
        return FakeLLMClient()
        
    if backend not in LLM_REGISTRY:
        raise ValueError(f"Unknown LLM backend '{backend}'. Valid options: {list(LLM_REGISTRY.keys())}")
    return LLM_REGISTRY[backend]()

