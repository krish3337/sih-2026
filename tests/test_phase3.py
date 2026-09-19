"""Phase 3 smoke test — data loading, embedding, and retrieval end-to-end."""

import sys
sys.stdout.reconfigure(encoding="utf-8")

# ── 1. Create stores via config (the ONLY place that imports impl/) ──────
from ai_core.config import (
    create_embedder,
    create_vector_store,
    create_graph_store,
    create_standards_repository,
    CONFIDENCE_THRESHOLD,
)

print("Creating stores …")
embedder = create_embedder()
vector_store = create_vector_store()
graph_store = create_graph_store()
repo = create_standards_repository()
print(f"  Embedder model dim: {embedder.embedding_dim}")

# ── 2. Load data into stores via data_loader ─────────────────────────────
from ai_core.data_loader import load_all

summary = load_all(
    vector_store=vector_store,
    graph_store=graph_store,
    embedder=embedder,
)
print(f"  Summary: {summary}")

# ── 3. Retriever test ────────────────────────────────────────────────────
from ai_core.retriever import Retriever

retriever = Retriever(
    vector_store=vector_store,
    standards_repo=repo,
    embedder=embedder,
    confidence_threshold=CONFIDENCE_THRESHOLD,
)

test_queries = [
    ("stainless steel welded pipes for general service", "IS 17876"),
    ("steel tubes for belt conveyor idlers", "IS 9295"),
    ("spiral welded steel pipe above 457mm", "IS 5504"),
    ("silica flour for foundries", "IS 3339"),
    ("something completely unrelated like quantum computing chips", None),
]

print("=" * 60)
print("  RETRIEVAL TESTS")
print("=" * 60)

all_passed = True
for query, expected_base_id in test_queries:
    results = retriever.retrieve_candidates(query, top_k=3)
    top = results[0] if results else None

    if expected_base_id is None:
        # Expect low confidence
        status = "✓" if top and top["low_confidence"] else "✗"
        print(f"\n  Query: \"{query}\"")
        print(f"  Expected: low_confidence=True")
        print(f"  Got:      top={top['base_id'] if top else 'None'}, "
              f"score={top['score'] if top else 'N/A'}, "
              f"low_confidence={top['low_confidence'] if top else 'N/A'}")
        print(f"  {status}")
        if status == "✗":
            all_passed = False
    else:
        match = top and top["base_id"] == expected_base_id
        status = "✓" if match else "✗"
        print(f"\n  Query: \"{query}\"")
        print(f"  Expected: {expected_base_id}")
        print(f"  Got:      {top['base_id'] if top else 'None'} "
              f"(score={top['score'] if top else 'N/A'}, "
              f"low_confidence={top['low_confidence'] if top else 'N/A'})")
        print(f"  {status}")
        if not match:
            all_passed = False
            # Show top 3 for debugging
            for i, r in enumerate(results):
                print(f"    #{i+1}: {r['base_id']} (score={r['score']})")

print("\n" + "=" * 60)
if all_passed:
    print("  PHASE 3 SMOKE TEST: ALL PASSED")
else:
    print("  PHASE 3 SMOKE TEST: SOME FAILURES (review above)")
print("=" * 60)
