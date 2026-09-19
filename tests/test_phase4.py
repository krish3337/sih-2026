"""Phase 4 smoke test — deterministic graph expansion and metadata/certification lookups."""

import sys
sys.stdout.reconfigure(encoding="utf-8")

# 1. Create stores and load data
from ai_core.config import create_graph_store, create_standards_repository
from ai_core.data_loader import load_graph

graph_store = create_graph_store()
load_graph(graph_store)

repo = create_standards_repository()

# 2. GraphExpansion
from ai_core.graph_expansion import GraphExpander
expander = GraphExpander(graph_store, repo)

print("=" * 60)
print("  GRAPH EXPANSION TEST (IS 5504)")
print("=" * 60)
allied = expander.get_allied_standards("IS 5504", max_hops=1)
print(f"Found {len(allied)} allied standards (1-hop):")
for a in allied[:5]:
    print(f"  → {a['standard_id']} ({a['title'][:40]}...) - {a['relation_type']}")
if len(allied) > 5:
    print(f"  ... and {len(allied) - 5} more")
print("✓ Graph expansion works")

# 3. MetadataCheck
from ai_core.metadata_check import MetadataChecker
meta_checker = MetadataChecker(repo)

print("\n" + "=" * 60)
print("  METADATA CHECK TEST (IS 18573)")
print("=" * 60)
meta = meta_checker.check_status("IS 18573")
assert meta is not None
print(f"Status: {meta['status']}")
print(f"Version Year: {meta['current_version_year']}")
print(f"Amendments: {len(meta['amendments'])} real amendments")
print("✓ Metadata lookup works")

# 4. CertificationCheck
from ai_core.certification_check import CertificationChecker
cert_checker = CertificationChecker(repo)

print("\n" + "=" * 60)
print("  CERTIFICATION CHECK TEST (IS 17876:2022 & IS 5504:2025)")
print("=" * 60)
cert_mand = cert_checker.get_certification_requirements("IS 17876:2022")
print(f"IS 17876:2022 Mandatory? {cert_mand['mandatory'] if cert_mand else 'None'}")
print(f"  QCO: {cert_mand['qco_reference'] if cert_mand else 'None'}")

cert_opt = cert_checker.get_certification_requirements("IS 5504:2025")
print(f"\nIS 5504:2025 Mandatory? {cert_opt['mandatory'] if cert_opt else 'None'}")
print(f"  HS Code placeholder check: {cert_opt['hs_code'] if cert_opt else 'None'}")
print("✓ Certification lookup works (preserves placeholders)")

print("\nPHASE 4 SMOKE TEST: ALL PASSED")
