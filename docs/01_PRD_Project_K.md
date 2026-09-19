# Product Requirements Document — Project K
### AI-Powered Indian Standards Recommendation Engine

---

## 1. Problem Statement

Procurement officials at government departments, PSEs, procurement agencies, and
private organizations must reference the correct Indian Standard(s) when preparing
tender specifications. With ~24,000 published IS standards, overlapping scopes,
frequent revisions, and standards that depend on other normative/allied standards,
officials routinely:
- Omit relevant standards
- Reference outdated/superseded editions
- Miss mandatory certification requirements
- Produce ambiguous specifications that lead to procurement disputes and reduced
  product quality

Project K is an AI-powered recommendation engine that analyzes a product description,
technical specification, or tender document and recommends the correct primary
standard, its allied/cross-referenced standards, current version status, and
applicable certification requirements.

## 2. Target Users

- **Primary:** Procurement officials preparing technical specifications for
  e-procurement tenders (government departments, PSEs, procurement agencies).
- **Secondary:** Private-sector procurement/quality teams doing the same task
  outside government process.
- **Internal:** A data curator role that maintains and verifies the standards
  knowledge base (currently filled by the team; a real operational role in the
  scaled product).

## 3. Goals & Objectives

- Reduce time and error in identifying the correct IS standard for a given
  procurement need.
- Surface allied/normative/test-method/terminology/safety/installation standards
  that officials would otherwise miss.
- Flag outdated or superseded standard versions before they're referenced in a tender.
- Surface mandatory certification requirements (BIS Product Certification, CRS,
  Hallmarking) where applicable.
- Support natural-language input in English and regional languages (Hindi
  validated in the current dataset).

## 4. Core Features (mapped to problem statement)

| # | Feature | MVP Status |
|---|---|---|
| 1 | Accept product description / spec / tender document as input (text or PDF) | Built |
| 2 | Semantic standard recommendation (not keyword matching) | Built |
| 3 | Allied/normative/test-method/terminology/related-product standards via reference graph | Built |
| 4 | Latest version + amendment flagging | Built |
| 5 | Mandatory certification requirement flagging (BIS/CRS/Hallmarking) | Built |
| 6 | Multilingual natural-language input | Built (English + Hindi validated) |

## 5. MVP Scope

Scoped deliberately to **steel/metallurgical department IS standards** rather than
the full ~24,000-standard corpus, to prove the recommendation mechanism correctly
before scaling.

**In scope for MVP:**
- 11 curated, verified steel/metallurgical standards (scope text, status, edition
  year, technical committee, amendment history, certification status)
- 131 verified cross-reference relationships across 4 relation types (Normative
  Reference, Test Method, Terminology, Related Product)
- Text and PDF input (short spec and long tender document, with automatic
  technical-section extraction from the latter)
- Deterministic retrieval, graph expansion, version check, and certification
  check — no LLM involvement in these steps, to eliminate hallucination risk on
  standard numbers and relationships
- LLM used only for (a) understanding the free-text query and (b) writing the
  final explanation from verified structured data
- A 26-query gold test set (English + Hindi pairs) for accuracy validation

**Explicitly deferred to post-selection scale-up (see Out of Scope):**
Full IS corpus coverage, automated large-scale ingestion, real vector/graph
database infrastructure, procurement portal integration, OCR for scanned
documents, Safety/Installation relation-type examples (not present in current
11-standard set).

## 6. User Stories

- As a procurement officer, I want to type a product description and get the
  correct IS standard, so I don't have to search manually across thousands of
  standards.
- As a procurement officer, I want to upload a draft tender document and have
  the relevant technical section automatically identified, so I don't have to
  extract it myself.
- As a procurement officer, I want to see allied/test-method/related standards
  for my primary match, so I don't omit a required cross-reference.
- As a procurement officer, I want to know if a standard is outdated or has
  amendments, so I don't reference a superseded edition.
- As a procurement officer, I want to know if certification is mandatory for a
  product, so I don't miss a compliance requirement.
- As a procurement officer, I want to query in Hindi as well as English, so the
  tool is usable regardless of my preferred working language.
- As a system, when confidence in a match is low, I want to say so explicitly
  rather than force a guess, so the officer isn't misled.

## 7. Success Metrics

- Precision@1 and Precision@3 on the 26-query gold test set (target: correct
  primary standard identified for the large majority of queries).
- 100% of low-confidence cases correctly flagged rather than force-guessed.
- 0 hallucinated standard numbers or relationships across all test queries
  (verified against the source data, not the LLM's memory).
- All 6 PS-defined features demonstrable live in the demo.
- Successful English and Hindi query handling on the gold set.

## 8. Assumptions

- The current 11-standard dataset, scope-verified from official IS PDF documents
  and the BIS "Know Your Standard" portal, is representative enough to validate
  the recommendation mechanism.
- Full-corpus scaling is a data-engineering and infrastructure problem, not an
  algorithm-redesign problem — the same pipeline logic extends to the full IS
  corpus with a bigger, automated data layer behind it.
- The team's frontend/backend members handle portal integration and UI
  separately; this PRD's MVP is the AI recommendation engine only.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Judges perceive the 11-standard dataset as too small | Present it as a validated, human-verified proof of mechanism, with an explicit, credible scale-up plan |
| LLM hallucinates a standard number in the explanation step | Structural constraint: LLM only explains data already retrieved deterministically, never generates standard numbers itself |
| Multilingual claim untested in practice | Gold test set includes real Hindi queries, validated before the claim is made publicly |
| Full-corpus data acquisition (24,000 standards) is a multi-month effort | Explicitly scoped out of this phase; roadmap names it as the primary post-selection workstream |

## 10. Out of Scope (this phase)

- Full ~24,000-standard IS corpus
- Automated web/portal scraping of BIS data
- OCR for scanned/image-only PDFs
- Procurement portal integration (API/UI embedding)
- User authentication and role-based access
- Production-grade vector/graph database infrastructure
- Officer feedback loop / continuous learning (planned, not built)

## 11. Acceptance Criteria for MVP

- Given a text query describing a steel product, the system returns the correct
  primary standard (per the gold test set) with a confidence score and a quoted
  scope-text snippet as evidence.
- Given a query matching a standard with real amendments, the system correctly
  surfaces the amendment/version status.
- Given a query matching a standard under mandatory certification, the system
  correctly flags the certification requirement.
- Given a query with no confident match, the system returns a low-confidence
  flag rather than a forced recommendation.
- Given a PDF (short spec or long tender), the system correctly extracts the
  relevant technical content and proceeds through the same pipeline as text input.
- Given a Hindi-language query, the system returns a correct or reasonably
  close match.
