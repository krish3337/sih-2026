"""
data_loader.py — Load verified JSON data into the interface stores.

Reads data/standards.json and data/relations.json, populates the
StandardsRepository, GraphStore, and VectorStore instances passed in.

This module receives *already-constructed* store instances (created by
config.py) and fills them with data.  It depends only on the interface
types, never on concrete impl/ classes.
"""

import json
import os
from typing import List

import numpy as np

from ai_core.interfaces.vector_store import VectorStore
from ai_core.interfaces.graph_store import GraphStore
from ai_core.embedder import Embedder


# ── Paths ────────────────────────────────────────────────────────────────────
DATA_DIR = "data"
STANDARDS_PATH = os.path.join(DATA_DIR, "standards.json")
RELATIONS_PATH = os.path.join(DATA_DIR, "relations.json")


def load_graph(graph_store: GraphStore, relations_path: str = RELATIONS_PATH) -> int:
    """Load cross-reference edges into the GraphStore.

    Parameters
    ----------
    graph_store : GraphStore
        Interface instance to populate.
    relations_path : str
        Path to relations.json.

    Returns
    -------
    int
        Number of relation records processed.
    """
    with open(relations_path, "r", encoding="utf-8") as fh:
        relations: List[dict] = json.load(fh)

    for rel in relations:
        graph_store.add_edge(
            from_id=rel["from_standard_id"],
            to_id=rel["to_standard_id"],
            relation_type=rel["relation_type"],
        )

    return len(relations)


def load_vectors(
    vector_store: VectorStore,
    embedder: Embedder,
    standards_path: str = STANDARDS_PATH,
) -> int:
    """Embed scope descriptions and load into the VectorStore.

    Each standard's ``scope_description`` is embedded and keyed by
    ``base_id`` — the same normalised ID used in relations.json for
    graph matching.

    Parameters
    ----------
    vector_store : VectorStore
        Interface instance to populate.
    embedder : Embedder
        Embedding utility for encoding scope texts.
    standards_path : str
        Path to standards.json.

    Returns
    -------
    int
        Number of standards embedded.
    """
    with open(standards_path, "r", encoding="utf-8") as fh:
        standards: List[dict] = json.load(fh)

    ids: List[str] = []
    texts: List[str] = []

    for std in standards:
        base_id = std.get("base_id", "")
        scope = std.get("scope_description", "")

        if not base_id or not scope or scope == "N/A":
            continue

        ids.append(base_id)
        # Combine title + scope for richer embedding context
        title = std.get("title", "")
        combined = f"{title}. {scope}" if title and title != "N/A" else scope
        texts.append(combined)

    if not texts:
        return 0

    print(f"  Embedding {len(texts)} scope descriptions …")
    embeddings: np.ndarray = embedder.embed_texts(texts)
    vector_store.add(ids, embeddings)

    return len(ids)


def load_all(
    vector_store: VectorStore,
    graph_store: GraphStore,
    embedder: Embedder,
    standards_path: str = STANDARDS_PATH,
    relations_path: str = RELATIONS_PATH,
) -> dict:
    """One-call loader: populate all stores from data files.

    Parameters
    ----------
    vector_store : VectorStore
        Interface instance for embeddings.
    graph_store : GraphStore
        Interface instance for cross-reference graph.
    embedder : Embedder
        Embedding utility.
    standards_path : str
        Path to standards.json.
    relations_path : str
        Path to relations.json.

    Returns
    -------
    dict
        Summary counts: ``{"standards_embedded", "relations_loaded"}``.
    """
    print("Loading data …")

    n_relations = load_graph(graph_store, relations_path)
    print(f"  Graph:   {n_relations} relation records → {graph_store.edge_count} unique edges")

    n_embedded = load_vectors(vector_store, embedder, standards_path)
    print(f"  Vectors: {n_embedded} scope descriptions embedded")

    print("  Done.\n")

    return {
        "standards_embedded": n_embedded,
        "relations_loaded": n_relations,
    }
