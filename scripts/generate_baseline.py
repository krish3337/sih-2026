import os
import sys
import json
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.config import (
    create_embedder,
    create_vector_store,
    create_graph_store,
    create_standards_repository,
    create_llm_client,
)
from ai_core.data_loader import load_all
from ai_core.query_understanding import QueryUnderstanding
from ai_core.retriever import Retriever
from ai_core.graph_expansion import GraphExpander
from ai_core.metadata_check import MetadataChecker
from ai_core.certification_check import CertificationChecker

def generate_baseline():
    sys.stdout.reconfigure(encoding="utf-8")
    load_dotenv()
    
    print("Initializing components...")
    embedder = create_embedder()
    vector_store = create_vector_store()
    graph_store = create_graph_store()
    repo = create_standards_repository()
    
    try:
        llm = create_llm_client()
        qu = QueryUnderstanding(llm)
        has_llm = True
    except Exception as e:
        print(f"Failed to initialize LLM: {e}")
        qu = None
        has_llm = False

    load_all(vector_store, graph_store, embedder)
    
    retriever = Retriever(vector_store, repo, embedder)
    expander = GraphExpander(graph_store, repo)
    meta = MetadataChecker(repo)
    cert = CertificationChecker(repo)

    with open("data/test_queries.json", "r", encoding="utf-8") as f:
        test_queries = json.load(f)

    baseline_data = []

    for i, tq in enumerate(test_queries):
        raw_query = tq.get("input_text", "")
        print(f"Processing query {i+1}/{len(test_queries)}: {raw_query}")
        
        if has_llm:
            try:
                qu_result = qu.extract_query_attributes(raw_query)
                retrieval_query = qu_result.get("retrieval_query", raw_query)
            except Exception as e:
                print(f"LLM extraction failed: {e}. Using raw query.")
                retrieval_query = raw_query
        else:
            retrieval_query = raw_query

        candidates = retriever.retrieve_candidates(retrieval_query, top_k=5)
        # Round scores to 6 decimals
        for c in candidates:
            c["score"] = round(c["score"], 6)
            
        top_candidate = candidates[0] if candidates else None
        
        allied_standards = []
        status_info = {}
        cert_info = {}

        if top_candidate:
            base_id = top_candidate["base_id"]
            full_id = top_candidate["standard_id"]

            allied_standards = expander.get_allied_standards(base_id, max_hops=1)
            status_info = meta.check_status(base_id) or {}
            cert_info = cert.get_certification_requirements(full_id) or {}

        baseline_data.append({
            "original_query": raw_query,
            "retrieval_query": retrieval_query,
            "retriever_candidates": candidates,
            "graph_expansion": allied_standards,
            "metadata": status_info,
            "certification": cert_info
        })

    os.makedirs("tests/baseline", exist_ok=True)
    with open("tests/baseline/deterministic_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(baseline_data, f, indent=2)
    print("Baseline saved to tests/baseline/deterministic_snapshot.json")

if __name__ == "__main__":
    generate_baseline()
