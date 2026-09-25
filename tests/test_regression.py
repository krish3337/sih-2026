import json
import os
import pytest

from scripts.generate_baseline import generate_baseline
from ai_core.config import (
    create_embedder,
    create_vector_store,
    create_graph_store,
    create_standards_repository,
    create_llm_client
)
from ai_core.data_loader import load_all
from ai_core.retriever import Retriever
from ai_core.graph_expansion import GraphExpander

@pytest.mark.slow
def test_deterministic_regression():
    """
    Re-runs the retrieval and graph expansion over the test queries
    and asserts that the results exactly match the saved baseline snapshot.
    """
    baseline_path = os.path.join(os.path.dirname(__file__), "baseline", "deterministic_snapshot.json")
    if not os.path.exists(baseline_path):
        pytest.skip("No baseline snapshot found. Generate it first using scripts/generate_baseline.py")
        
    with open(baseline_path, "r", encoding="utf-8") as f:
        baseline_data = json.load(f)
        
    # We must use the real embedder to get the real scores
    os.environ["EMBEDDER_BACKEND"] = "e5"
    
    embedder = create_embedder()
    vector_store = create_vector_store()
    graph_store = create_graph_store()
    repo = create_standards_repository()
    
    load_all(vector_store, graph_store, embedder)
    
    retriever = Retriever(vector_store, repo, embedder)
    expander = GraphExpander(graph_store, repo)
    
    for snapshot in baseline_data:
        retrieval_query = snapshot["retrieval_query"]
        
        # Test 1: Retrieve Candidates
        candidates = retriever.retrieve_candidates(retrieval_query, top_k=5)
        for c in candidates:
            c["score"] = round(c["score"], 6)
            
        assert len(candidates) == len(snapshot["retriever_candidates"])
        for i, c in enumerate(candidates):
            assert c["standard_id"] == snapshot["retriever_candidates"][i]["standard_id"], f"Mismatch in candidate IDs for query: {retrieval_query}"
            # Compare scores with slight tolerance for float precision
            assert abs(c["score"] - snapshot["retriever_candidates"][i]["score"]) < 1e-5, f"Mismatch in score for candidate {c['standard_id']}"
            
        # Test 2: Graph Expansion
        if candidates:
            base_id = candidates[0]["base_id"]
            allied = expander.get_allied_standards(base_id, max_hops=1)
            assert allied == snapshot["graph_expansion"], f"Mismatch in graph expansion for {base_id}"
