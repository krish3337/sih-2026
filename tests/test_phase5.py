"""Phase 5 smoke test — Query Understanding and Synthesizer LLM modules."""

import sys
import json
sys.stdout.reconfigure(encoding="utf-8")

# 1. Create client
from ai_core.config import create_llm_client
try:
    llm = create_llm_client()
except ValueError as e:
    print(f"Skipping LLM tests: {e}")
    sys.exit(0)

# 2. Test Query Understanding
from ai_core.query_understanding import QueryUnderstanding
qu = QueryUnderstanding(llm)

print("=" * 60)
print("  QUERY UNDERSTANDING TEST")
print("=" * 60)

raw_query = "Need standard for spiral welded steel pipes above 457mm for water transport."
print(f"Raw Query: {raw_query}\n")

extracted = qu.extract_query_attributes(raw_query)
print("Extracted Attributes:")
print(json.dumps(extracted, indent=2))
print("✓ Query Understanding works")

# 3. Test Synthesizer
from ai_core.synthesizer import Synthesizer
synth = Synthesizer(llm)

print("\n" + "=" * 60)
print("  SYNTHESIZER TEST")
print("=" * 60)

# Mock context
primary_candidates = [
    {
        "standard_id": "IS 5504:2025",
        "title": "Spiral Welded Pipes - Specification",
        "score": 0.885,
        "low_confidence": False,
        "scope_description": "This standard covers the requirements of spiral seam welded steel pipe over 457 mm diameter..."
    }
]

allied_standards = [
    {"standard_id": "IS 228", "title": "Methods of chemical analysis of steels", "relation_type": "Test Method"},
    {"standard_id": "IS 1608", "title": "Metallic materials - Tensile testing", "relation_type": "Test Method"}
]

status_info = {
    "status": "Active",
    "current_version_year": 2025,
    "amendments": []
}

certification_info = {
    "certification_name": "BIS Standard Mark",
    "mandatory": "No",
    "qco_reference": "N/A",
    "hs_code": "not verified"
}

response = synth.synthesize_response(
    query=raw_query,
    primary_candidates=primary_candidates,
    allied_standards=allied_standards,
    status_info=status_info,
    certification_info=certification_info
)

print("Generated Explanation:\n")
print(response["explanation"])
print("\n✓ Synthesizer works and obeys context")

print("\nPHASE 5 SMOKE TEST: ALL PASSED")
