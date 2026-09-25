"""
run_demo.py — Command-line interface for the Project K AI Pipeline (Phase 7).

Accepts --text or --pdf arguments and runs the full recommendation flow.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import time

# Create stores/clients
from ai_core.config import (
    create_embedder,
    create_vector_store,
    create_graph_store,
    create_standards_repository,
    create_llm_client,
)

# Load data
from ai_core.data_loader import load_all

# Components
from ai_core.query_understanding import QueryUnderstanding
from ai_core.retriever import Retriever
from ai_core.graph_expansion import GraphExpander
from ai_core.metadata_check import MetadataChecker
from ai_core.certification_check import CertificationChecker
from ai_core.synthesizer import Synthesizer
from ai_core.pdf_input import PDFInput
from ai_core.pipeline import RecommendationPipeline


def init_pipeline() -> RecommendationPipeline:
    """Initialises all stores, loads data, and wires the pipeline."""
    print("Initialising pipeline modules (this may take a moment for embedding) ...")
    
    embedder = create_embedder()
    vector_store = create_vector_store()
    graph_store = create_graph_store()
    repo = create_standards_repository()
    
    try:
        llm = create_llm_client()
    except ValueError as exc:
        print(f"\nERROR: {exc}")
        sys.exit(1)

    # Load JSON data into in-memory stores
    load_all(vector_store, graph_store, embedder)
    
    # Instantiate modules
    qu = QueryUnderstanding(llm)
    retriever = Retriever(vector_store, repo, embedder)
    expander = GraphExpander(graph_store, repo)
    meta = MetadataChecker(repo)
    cert = CertificationChecker(repo)
    synth = Synthesizer(llm)
    pdf_in = PDFInput()
    
    # Wire the pipeline
    return RecommendationPipeline(
        query_understanding=qu,
        retriever=retriever,
        graph_expander=expander,
        metadata_checker=meta,
        certification_checker=cert,
        synthesizer=synth,
        pdf_input=pdf_in
    )


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    
    parser = argparse.ArgumentParser(description="Project K: Indian Standards Recommendation AI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Raw query text (e.g., procurement requirement)")
    group.add_argument("--pdf", type=str, help="Path to a PDF document to analyze")
    
    args = parser.parse_args()

    pipeline = init_pipeline()
    
    print("\n" + "="*60)
    print("  RUNNING PIPELINE")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    try:
        if args.text:
            print(f"Processing Query: '{args.text}'\n")
            result = pipeline.recommend(args.text)
        elif args.pdf:
            print(f"Processing PDF: '{args.pdf}'\n")
            result = pipeline.recommend_from_pdf(args.pdf)
            
        elapsed = time.time() - start_time
        
        print("--- SYNTHESIZED EXPLANATION ---\n")
        print(result["explanation"])
        print("\n" + "-"*31)
        print(f"Pipeline completed in {elapsed:.2f}s")
        
    except Exception as exc:
        print(f"\nERROR running pipeline: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
