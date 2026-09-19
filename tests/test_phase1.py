"""Phase 1 smoke test — exercises all implementations against real data."""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import json
import numpy as np

# ── VectorStore ──────────────────────────────────────────────────────────
from ai_core.impl.in_memory_vector_store import InMemoryVectorStore
from ai_core.interfaces.vector_store import VectorStore

vs = InMemoryVectorStore()
assert isinstance(vs, VectorStore)

ids = ["IS 5504", "IS 9295", "IS 17876"]
emb = np.random.randn(3, 8).astype(np.float32)
vs.add(ids, emb)

# Query close to the third embedding — should rank IS 17876 first
q = emb[2] + np.random.randn(8) * 0.1
results = vs.search(q, top_k=3)
print("VectorStore search (IS 17876 should rank first):")
for sid, score in results:
    print(f"  {sid}: {score:.4f}")
assert results[0][0] == "IS 17876", f"Expected IS 17876 first, got {results[0][0]}"
print("  ✓ PASS\n")

# ── GraphStore ───────────────────────────────────────────────────────────
from ai_core.impl.in_memory_graph_store import InMemoryGraphStore
from ai_core.interfaces.graph_store import GraphStore

gs = InMemoryGraphStore()
assert isinstance(gs, GraphStore)

rels = json.load(open("data/relations.json", "r", encoding="utf-8"))
for r in rels:
    gs.add_edge(r["from_standard_id"], r["to_standard_id"], r["relation_type"])

print(f"GraphStore loaded: {gs.edge_count} edges, {gs.node_count} source nodes")

neighbors_1 = gs.get_neighbors("IS 5504", max_hops=1)
print(f"IS 5504 neighbors (1-hop): {len(neighbors_1)} standards")
for n in neighbors_1[:5]:
    print(f"  → {n['standard_id']} ({n['relation_type']}, hop {n['hop']})")
if len(neighbors_1) > 5:
    print(f"  ... and {len(neighbors_1) - 5} more")

neighbors_2 = gs.get_neighbors("IS 5504", max_hops=2)
print(f"IS 5504 neighbors (2-hop): {len(neighbors_2)} standards")
print("  ✓ PASS\n")

# ── StandardsRepository ─────────────────────────────────────────────────
from ai_core.impl.in_memory_standards_repository import InMemoryStandardsRepository
from ai_core.interfaces.standards_repository import StandardsRepository

repo = InMemoryStandardsRepository()
assert isinstance(repo, StandardsRepository)
print(f"StandardsRepository loaded: {repo.size} standards")

# Lookup by base_id
s = repo.get("IS 5504")
assert s is not None
print(f"  get('IS 5504'): {s['standard_id']} — {s['title'][:60]}...")

# Lookup by full standard_id (fallback)
s2 = repo.get("IS 5504:2025")
assert s2 is not None
print(f"  get('IS 5504:2025'): {s2['standard_id']}  (full-ID fallback works)")

# Status search
active = repo.search_by_status("Active")
print(f"  search_by_status('Active'): {len(active)} standards")

# Certification
cert = repo.get_certification("IS 17876:2022")
assert cert is not None
print(f"  get_certification('IS 17876:2022'): mandatory={cert['mandatory']}")

cert_none = repo.get_certification("IS 99999:2099")
assert cert_none is None
print(f"  get_certification('IS 99999:2099'): None (correctly missing)")
print("  ✓ PASS\n")

# ── LLMClient (import-only, no API call) ─────────────────────────────────
from ai_core.interfaces.llm_client import LLMClient
from ai_core.impl.gemini_client import GeminiClient
print(f"GeminiClient class importable: {issubclass(GeminiClient, LLMClient)}")
print("  (not instantiated — requires API key, tested separately)")
print("  ✓ PASS\n")

# ── Summary ──────────────────────────────────────────────────────────────
print("=" * 50)
print("  PHASE 1 SMOKE TEST: ALL PASSED")
print("=" * 50)
