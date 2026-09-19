"""
adapter.py — Convert docs/IS_Standards_MERGED.xlsx into pipeline-ready JSON.

Outputs (all written to data/):
    standards.json            Standards + merged Amendments
    relations.json            Cross-reference edges (graph)
    certification_rules.json  Certification records keyed by standard_id
    test_queries.json         Gold test queries (passthrough for evaluation)

Run:
    python adapter.py
"""

import json
import os
import re
import sys

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl is required.  Install with:  pip install openpyxl")
    sys.exit(1)


# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(PROJECT_ROOT, "docs", "IS_Standards_MERGED.xlsx")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")


# ── ID normalisation ────────────────────────────────────────────────────────
def normalise_standard_id(raw: str) -> str:
    """Extract a clean base standard ID for matching / graph purposes.

    Examples
    --------
    "IS 5504:2025"                             → "IS 5504"
    "IS 1608 (Part 1):2022/ISO 6892-1:2019"   → "IS 1608"
    "IS 1956 (various parts)"                  → "IS 1956"
    "IS 228"                                   → "IS 228"
    "ISO 6892-1:2019"                          → "ISO 6892-1"  (non-IS ref)

    Placeholder values ("N/A", "not verified") are returned unchanged.
    """
    if not raw or not isinstance(raw, str):
        return str(raw) if raw is not None else "N/A"

    stripped = raw.strip()
    if stripped.upper() in ("N/A", "NOT VERIFIED"):
        return stripped

    # Try IS pattern first:  IS <digits>
    m = re.match(r"(IS\s+\d+)", stripped)
    if m:
        return m.group(1)

    # Fallback for ISO / other prefixed IDs:  PREFIX <alphanumeric+hyphens>
    m = re.match(r"(ISO\s+[\d\-]+)", stripped)
    if m:
        return m.group(1)

    # Last resort: return as-is
    return stripped


# ── Excel reader ─────────────────────────────────────────────────────────────
def read_tab(wb, tab_name, header_row=3):
    """Read a worksheet tab and return (list[dict], list[str warnings]).

    Layout convention in the workbook:
        Row 1 — tab title
        Row 2 — notes / instructions
        Row 3 — column headers
        Row 4+ — data rows
    """
    ws = wb[tab_name]
    header_cells = list(ws.iter_rows(min_row=header_row, max_row=header_row))[0]
    headers = [cell.value for cell in header_cells]

    rows = []
    warnings = []

    for row_idx, row in enumerate(
        ws.iter_rows(min_row=header_row + 1, max_row=ws.max_row),
        start=header_row + 1,
    ):
        values = [cell.value for cell in row]

        # Skip completely empty rows
        if all(v is None for v in values):
            continue

        record = {}
        for header, value in zip(headers, values):
            if header is None:
                continue
            # Preserve meaningful placeholders; flag truly blank cells
            if value is None:
                warnings.append(
                    f"[{tab_name}] Row {row_idx}, column '{header}': "
                    f"cell is blank (expected a value or 'N/A')"
                )
                value = "N/A"
            elif isinstance(value, str):
                value = value.strip()
            record[header] = value

        rows.append(record)

    return rows, warnings


# ── Builders ─────────────────────────────────────────────────────────────────
def build_standards(standards_rows, amendments_rows):
    """Merge Standards + Amendments → list of standard records."""

    # Group real amendments (amendment_number ≠ 0) by standard_id
    amendments_by_sid = {}
    for amd in amendments_rows:
        sid = amd.get("standard_id", "")
        amd_num = amd.get("amendment_number", 0)

        # amendment_number == 0 means "no amendment issued" — skip it
        if amd_num == 0 or str(amd_num) == "0":
            continue

        amendments_by_sid.setdefault(sid, []).append({
            "amendment_id": amd.get("amendment_id"),
            "amendment_number": amd_num,
            "date_issued": amd.get("date_issued", "N/A"),
            "summary_of_change": amd.get("summary_of_change", "N/A"),
        })

    standards = []
    for std in standards_rows:
        sid = std.get("standard_id", "")
        standards.append({
            "standard_id": sid,
            "base_id": normalise_standard_id(sid),
            "title": std.get("title", "N/A"),
            "part_number": std.get("part_number", "N/A"),
            "scope_description": std.get("scope_description", "N/A"),
            "status": std.get("status", "N/A"),
            "superseded_by": std.get("superseded_by", "N/A"),
            "superseding_is": std.get("superseding_is", "N/A"),
            "current_version_year": std.get("current_version_year", "N/A"),
            "technical_committee": std.get("technical_committee", "N/A"),
            "product_keywords": std.get("product_keywords", "N/A"),
            "amendments": amendments_by_sid.get(sid, []),
        })

    return standards


def build_relations(cross_ref_rows):
    """Cross_References → list of relation edges.

    Both from_standard_id and to_standard_id are normalised to base IDs
    for graph traversal.  The full original target string is preserved
    in target_detail so no information is lost.

    Reference-only targets (no full record in the Standards tab) are
    included as valid edges — the graph does not require a full standards
    record to exist.
    """
    relations = []
    warnings = []

    for cr in cross_ref_rows:
        source_raw = cr.get("source_standard_id", "")
        target_raw = cr.get("target_standard_id", "")
        ref_type = cr.get("reference_type", "N/A")

        if not source_raw or not target_raw:
            warnings.append(
                f"Skipped cross-ref {cr.get('ref_id', '??')}: "
                f"missing source or target ID"
            )
            continue

        relations.append({
            "ref_id": cr.get("ref_id"),
            "from_standard_id": normalise_standard_id(source_raw),
            "to_standard_id": normalise_standard_id(target_raw),
            "relation_type": ref_type,
            "target_detail": target_raw,
        })

    return relations, warnings


def build_certifications(cert_rows):
    """Certifications → dict keyed by standard_id."""
    certs = {}

    for cert in cert_rows:
        sid = cert.get("standard_id", "")
        certs[sid] = {
            "certification_id": cert.get("certification_id"),
            "certification_name": cert.get("certification_name", "N/A"),
            "mandatory": cert.get("mandatory", "N/A"),
            "qco_reference": cert.get("qco_reference", "N/A"),
            "hs_code": cert.get("hs_code", "N/A"),
        }

    return certs


# ── Helpers ──────────────────────────────────────────────────────────────────
def write_json(filename, data):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    print(f"  ✓ Wrote {path}")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    # Ensure unicode output works on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if not os.path.exists(EXCEL_PATH):
        print(f"ERROR: Excel file not found at '{EXCEL_PATH}'")
        print("       Run this script from the project root (SIH DEMO/).")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Reading {EXCEL_PATH} …")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    all_warnings = []

    # ── Standards + Amendments ───────────────────────────────────────────
    standards_rows, w = read_tab(wb, "Standards")
    all_warnings.extend(w)
    amendments_rows, w = read_tab(wb, "Amendments")
    all_warnings.extend(w)
    standards_json = build_standards(standards_rows, amendments_rows)

    # ── Cross References ─────────────────────────────────────────────────
    cross_ref_rows, w = read_tab(wb, "Cross_References")
    all_warnings.extend(w)
    relations_json, w = build_relations(cross_ref_rows)
    all_warnings.extend(w)

    # ── Certifications ───────────────────────────────────────────────────
    cert_rows, w = read_tab(wb, "Certifications")
    all_warnings.extend(w)
    cert_json = build_certifications(cert_rows)

    # ── Test Queries (passthrough) ───────────────────────────────────────
    test_query_rows, w = read_tab(wb, "Test_Queries")
    all_warnings.extend(w)

    # ── Write outputs ────────────────────────────────────────────────────
    print()
    write_json("standards.json", standards_json)
    write_json("relations.json", relations_json)
    write_json("certification_rules.json", cert_json)
    write_json("test_queries.json", test_query_rows)

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("  CONVERSION SUMMARY")
    print("=" * 50)

    print(f"  Standards:        {len(standards_json)}")

    with_amd = sum(1 for s in standards_json if s["amendments"])
    total_amd = sum(len(s["amendments"]) for s in standards_json)
    print(f"  Amendments:       {total_amd} real amendment(s) across "
          f"{with_amd} standard(s)")

    print(f"  Relations:        {len(relations_json)}")
    rel_types = {}
    for r in relations_json:
        rt = r["relation_type"]
        rel_types[rt] = rel_types.get(rt, 0) + 1
    for rt, count in sorted(rel_types.items()):
        print(f"      {rt}: {count}")

    print(f"  Certifications:   {len(cert_json)}")
    print(f"  Test Queries:     {len(test_query_rows)}")

    # Reference-only standards (in relations but not in standards.json)
    known_base_ids = {s["base_id"] for s in standards_json}
    ref_only = set()
    for r in relations_json:
        if r["to_standard_id"] not in known_base_ids:
            ref_only.add(r["to_standard_id"])
    print(f"  Reference-only targets (no full record): {len(ref_only)}")
    if ref_only:
        for rid in sorted(ref_only):
            print(f"      → {rid}")

    # Warnings
    if all_warnings:
        print(f"\n{'=' * 50}")
        print(f"  WARNINGS ({len(all_warnings)})")
        print(f"{'=' * 50}")
        for w in all_warnings:
            print(f"  ⚠  {w}")
    else:
        print("\n  No parse warnings — all rows processed cleanly.")

    print()


if __name__ == "__main__":
    main()
