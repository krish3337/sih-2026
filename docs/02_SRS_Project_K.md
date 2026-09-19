# Software Requirements Specification — Project K

---

## 1. Functional Requirements

| ID | Requirement | Testable acceptance criteria |
|---|---|---|
| FR-1 | System shall accept a free-text product description or specification as input | Input string of at least 1 word is accepted and passed to the pipeline |
| FR-2 | System shall accept a PDF file as input | Given a valid PDF path, text is successfully extracted |
| FR-3 | System shall distinguish short PDFs (product specs) from long PDFs (tender documents) and handle each appropriately | Long PDFs (>~1000 words) trigger technical-section extraction before further processing; short PDFs are used as-is |
| FR-4 | System shall extract structured query attributes (product type, grade, form, application) from raw input | Given a sample query, output is valid JSON containing these fields |
| FR-5 | System shall semantically match the query against the standards knowledge base | Given a query, top-k candidate standards are returned ranked by similarity score |
| FR-6 | System shall flag low-confidence matches instead of forcing a recommendation | Given a query below the confidence threshold, output includes `low_confidence: true` |
| FR-7 | System shall retrieve allied standards connected to a matched standard via the reference graph | Given a standard with known relations, all connected standards within 2 hops are returned with relation type |
| FR-8 | System shall never infer or invent a relationship not present in the relations data | Graph traversal is deterministic (BFS over stored edges only) — verified by code inspection, no LLM call in this path |
| FR-9 | System shall report the status (active/superseded/withdrawn) and amendment history of a matched standard | Given a standard with known status/amendments, output correctly reflects the stored metadata |
| FR-10 | System shall report mandatory certification requirements for a matched standard, where applicable | Given a standard flagged mandatory in certification data, output includes the certification scheme and mandatory flag |
| FR-11 | System shall generate a human-readable explanation grounded only in retrieved structured data | LLM prompt explicitly constrains output to supplied context; no standard number appears in the explanation that isn't in the input context |
| FR-12 | System shall support English and Hindi natural-language queries | Given a Hindi query from the gold test set, the system returns a valid recommendation |

## 2. User Roles and Permissions

| Role | Description | Permissions |
|---|---|---|
| Procurement Official (end user) | Submits queries/documents, receives recommendations | Query only — no write access to the standards knowledge base |
| Data Curator (internal, team-only for MVP) | Maintains/verifies the standards dataset | Read/write access to `standards.json`, `relations.json`, `certification_rules.json` |
| System | Automated pipeline execution | Full internal read access to all data stores |

Note: authentication/authorization is out of scope for MVP (single-user local
demo). A future portal-integrated version would require role-based access
control at the API layer — noted here for completeness, not built.

## 3. Business Rules

- BR-1: The system must never present an LLM-generated standard number as fact
  — every standard number in output must trace to the structured data layer.
- BR-2: A recommendation below the confidence threshold must be labeled
  low-confidence, never silently presented as a top match.
- BR-3: Certification and version/status information must come from direct
  data lookup, never from LLM inference.
- BR-4: Every relation edge must originate from a standard's own stated
  references (Normative References clause, Foreword cross-scope mentions) —
  never inferred by semantic similarity.
- BR-5: A field that could not be verified from source must be marked "not
  verified" rather than estimated or omitted.

## 4. Data Requirements

**Standards record:** standard_id, title, part_number, scope_description,
status, superseded_by, superseding_is, current_version_year, technical_committee,
product_keywords.

**Amendment record:** amendment_id, standard_id, amendment_number, date_issued,
summary_of_change (one record per standard minimum, `amendment_number: 0` if none).

**Cross-reference record:** ref_id, source_standard_id, target_standard_id,
reference_type (Normative Reference / Test Method / Terminology / Safety /
Installation / Related Product).

**Certification record:** certification_id, certification_name, standard_id,
mandatory (Yes/No), qco_reference, hs_code.

**Test query record:** query_id, input_text, expected_standard_id, language.

All fields follow a strict placeholder discipline: never blank — use "N/A"
(with reason) when a field genuinely doesn't apply, or "not verified" when it
could not be confirmed in reasonable time. No field may contain an estimated
or invented value.

## 5. Validations

- Text query input: reject/flag empty strings.
- PDF input: verify file is a valid, readable PDF; if text extraction yields
  no content (likely a scanned/image PDF), return an explicit error rather
  than proceeding with empty text.
- Standard ID references: normalize formatting inconsistencies (e.g. "IS
  1608 (Part 1):2022/ISO 6892-1:2019" vs a clean base ID) during ingestion,
  not at query time.
- Confidence score: must be a float in [0, 1]; threshold value configurable,
  not hardcoded inline.

## 6. Authentication / Authorization

Out of scope for MVP — single-user local/offline demo, no login system.
Documented here as a known gap for the scaled, portal-integrated version,
where role-based access (procurement official vs. data curator vs. admin)
would be required.

## 7. Error Handling

| Scenario | Handling |
|---|---|
| Empty or unreadable PDF | Return explicit error flag, do not proceed with empty query |
| LLM call fails (query understanding or synthesis) | Return a clear error state rather than a partial/guessed result |
| No candidate standard above confidence threshold | Return low-confidence result with the best available candidates for manual review, not a forced top pick |
| Standard referenced in graph but not present in full standards dataset | Return the reference by ID and relation type without full metadata, rather than erroring |
| Malformed or inconsistent standard ID in relations data | Normalized during ingestion; if unresolvable, logged and excluded rather than silently mismatched |

## 8. Edge Cases

- A tender document requesting multiple distinct products in one document
  (compound query) — MVP handles single primary product focus; multi-product
  decomposition is a scale-up item.
- A query matching a standard with no cross-references at all — return primary
  recommendation with an explicit "no allied standards found" rather than
  omitting the field.
- A query in a language other than English/Hindi — not validated in MVP;
  degrades to best-effort semantic matching via the multilingual embedding
  model, no guarantee.
- A standard appearing only as a cross-reference target, with no full record
  of its own (e.g., IS 228, IS 1387 in the current dataset) — returned as a
  known reference by ID/type, not treated as a data error.

## 9. Security

- No personally identifiable information is collected or stored by the MVP.
- Standards data is sourced only from official IS documents and the BIS "Know
  Your Standard" public portal — no unauthorized redistribution of licensed
  standard content.
- LLM API keys are handled via environment configuration, never hardcoded or
  logged.

## 10. Performance

- Target: sub-5-second end-to-end response time per query on the current
  11-standard in-memory dataset (two LLM calls + deterministic lookups).
- Retrieval and graph traversal steps must remain non-LLM and near-instant
  regardless of dataset size, by design (brute-force cosine similarity at
  current scale, swappable to indexed search at production scale without
  pipeline changes).

## 11. Acceptance Criteria

Each functional requirement (FR-1 through FR-12) above is independently
testable against the 26-query gold test set and is considered met when its
stated criterion passes for all applicable test queries.
