"""
config.py — Wiring: create concrete implementations and expose them as
interface types.

This is the ONLY module that imports from src/impl/.  Every other
pipeline module depends solely on the interfaces.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from ai_core.interfaces.vector_store import VectorStore
from ai_core.interfaces.graph_store import GraphStore
from ai_core.interfaces.standards_repository import StandardsRepository
from ai_core.interfaces.llm_client import LLMClient
from ai_core.embedder import Embedder

# ── Concrete impl imports (ONLY place in the codebase) ───────────────────
from ai_core.impl.in_memory_vector_store import InMemoryVectorStore
from ai_core.impl.in_memory_graph_store import InMemoryGraphStore
from ai_core.impl.in_memory_standards_repository import InMemoryStandardsRepository
from ai_core.impl.gemini_client import GeminiClient


# ── Configuration constants ──────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
STANDARDS_PATH = os.path.join(DATA_DIR, "standards.json")
CERTIFICATION_PATH = os.path.join(DATA_DIR, "certification_rules.json")
RELATIONS_PATH = os.path.join(DATA_DIR, "relations.json")

EMBEDDING_MODEL = "intfloat/multilingual-e5-large"
GEMINI_MODEL = "gemini-3.6-flash"
CONFIDENCE_THRESHOLD = 0.80


# ── Factory functions ────────────────────────────────────────────────────

def create_embedder() -> Embedder:
    """Create the embedding model."""
    return Embedder(model_name=EMBEDDING_MODEL)


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
    """Create an LLMClient (requires GEMINI_API_KEY env var)."""
    return GeminiClient(model_name=GEMINI_MODEL)
