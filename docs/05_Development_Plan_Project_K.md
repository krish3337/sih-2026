# Development Plan — Project K

---

## 1. Roadmap Overview

Two distinct phases, matching the competition structure:
- **Phase A (now → selection-round submission):** AI engine MVP, 11-standard
  curated dataset, CLI demo. Owned solely by the AI/backend workstream.
- **Phase B (36-hour offline hackathon, if selected):** scale-up — larger
  dataset, real infrastructure, frontend/backend/portal integration, full team.

## 2. Phase A — Setup

- Repository structure established (interfaces / impl / pipeline modules).
- Dependencies: sentence-transformers, pdfplumber, an LLM client library.
- `data/` populated from the verified Excel dataset (Standards, Amendments,
  Cross_References, Certifications, Test_Queries tabs) via a conversion
  adapter script into `standards.json`, `relations.json`,
  `certification_rules.json`.

**Definition of Done:** repository runs `run_demo.py` end to end with no
missing dependency errors.

## 3. Phase A — Data Layer

- Priority: adapter script converting the 5-tab Excel into the flat JSON
  schema the pipeline expects, including standard-ID normalization (handling
  inconsistent formats like "IS 1608 (Part 1):2022/ISO 6892-1:2019") and
  graceful handling of reference-only standards with no full record.
- Dependency: must complete before embedding/retrieval work, since retrieval
  is built against the normalized data.

**Definition of Done:** `data_loader.py` successfully loads all 11 standards,
131 relations, and certification records with no ID-mismatch errors.

## 4. Phase A — Backend/AI Core (ordered by dependency)

1. Interfaces + in-memory implementations (`VectorStore`, `GraphStore`,
   `StandardsRepository`, `LLMClient`)
2. Embedding + retrieval (`embedder.py`, `retriever.py`) — validate against
   the gold test-query set before moving on
3. Deterministic graph expansion and metadata/certification checks
4. Query understanding (LLM call 1)
5. Synthesis (LLM call 2), with the evidence-only constraint enforced in the
   prompt
6. PDF input handling (short spec vs. long tender segmentation)
7. Pipeline wiring (`recommend()`, `recommend_from_pdf()`) and CLI demo runner

**Definition of Done:** all 26 gold test queries run through the CLI and
produce either a correct match or a correctly-flagged low-confidence result,
with zero fabricated standard numbers in any output.

## 5. Phase A — Testing

- Run the full gold test-query set (English + Hindi) and record precision@1/@3.
- Manually verify at least one query per PS feature (semantic match, allied
  standards, version/amendment flag, certification flag, low-confidence
  handling, non-English input).
- Fix any data inconsistencies found during testing (e.g. the blank
  `certification_name` cell noted during data review) before demo recording.

**Definition of Done:** 3 demo queries selected and rehearsed, each cleanly
demonstrating a distinct PS feature combination.

## 6. Phase A — Demo Packaging & PPT

- Record or screenshot the 3 chosen demo queries.
- Assemble the PPT: problem framing, why plain RAG isn't sufficient, the
  architecture (deterministic-vs-LLM split), demo evidence, honest
  built-vs-planned scope statement, scalability reasoning (architecture +
  feasibility math + real ingestion bottleneck), team/roadmap.

**Definition of Done:** PPT + demo ready ahead of the submission deadline,
with the "built" and "planned" scope stated explicitly and separately.

## 7. Phase B (36-hour hackathon) — Priorities, if selected

1. Automated ingestion pipeline (regex-based clause parsing + LLM fallback)
   to scale dataset collection beyond manual curation.
2. Swap in production implementations behind existing interfaces: FAISS/
   ChromaDB for vector search, Postgres (or equivalent) for structured data
   and the reference graph — no pipeline rewrite required by design.
3. Category-anchored retrieval, once the corpus spans multiple industries
   beyond steel/metallurgical, to prevent cross-domain semantic confusion.
4. Hybrid (dense + sparse) retrieval and reranking, once dataset scale makes
   this worthwhile.
5. Backend API layer (FastAPI) exposing the pipeline for frontend/portal
   integration.
6. Frontend build per the UI/UX document.
7. OCR support for scanned tender documents, if needed.
8. Officer feedback endpoint for future retrieval tuning.

## 8. Milestones

| Milestone | Target |
|---|---|
| Data adapter + 11-standard dataset loaded | Before backend core work begins |
| Full pipeline running end to end on gold test set | Before demo recording |
| Demo + PPT finalized | Selection-round submission deadline |
| Automated ingestion + production infra | Within 36-hour hackathon (if selected) |
| Frontend + API integration | Within 36-hour hackathon (if selected) |

## 9. Definition of Done — Phase A (overall)

Project K's Phase A is complete when: the CLI demo runs reliably on the
11-standard dataset, all 6 PS-defined features are demonstrable, the gold
test set has been run and results recorded, zero fabricated standard data
appears in any output, and the PPT presents built vs. planned scope honestly
and specifically.
