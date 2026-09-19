# UI/UX Document — Project K

*Note: the AI/backend engine is being built independently of the frontend
workstream. This document specifies the intended user experience for the
team's frontend implementation and PPT visualization — it is not part of the
AI engine's own deliverable.*

---

## 1. User Journey

1. Procurement official opens the tool (standalone or embedded in an
   e-procurement portal).
2. Chooses input method: type a product description, or upload a tender/spec
   PDF.
3. Submits the query.
4. Reviews the recommendation: primary standard, allied standards, version
   status, certification requirement, and a plain-language explanation.
5. Optionally reviews the evidence (matched scope-text snippet) behind the
   recommendation.
6. Optionally provides feedback (accept/reject/correct) — future phase.
7. Copies or exports the recommended standard reference(s) into their tender
   specification.

## 2. Screens

**Screen 1 — Input**
- Text area for free-text product description / specification.
- File upload control for PDF (spec or tender document).
- Language is auto-detected; no manual language selector required.
- Single primary action: "Get Recommendation."

**Screen 2 — Results**
- Primary recommendation card: standard number, title, confidence indicator,
  matched scope-text snippet as evidence.
- If confidence is low: a visibly distinct "needs manual review" state instead
  of a normal result card — this must look different, not just say different,
  so an official doesn't mistake a low-confidence flag for a confident answer.
- Allied standards section: grouped by relation type (Normative Reference,
  Test Method, Terminology, Related Product, and Safety/Installation where
  present), each with its own standard number and title.
- Version status: current edition year; if amendments exist, a clearly
  visible badge/expandable summary of what changed and when.
- Certification section: mandatory/voluntary status, certification scheme
  name, and QCO reference (or "not verified" shown plainly if unconfirmed
  in the data — never hidden or guessed).
- Explanation panel: the plain-language synthesis, clearly presented as
  generated commentary on the data above it, not as an independent claim.

**Screen 3 — Low-confidence / no-match state**
- Explicit message that no confident match was found.
- Best-available candidates shown for manual review, clearly labeled as
  low-confidence, not as a recommendation.

## 3. Navigation

Linear flow for MVP: Input → Results → (optional) New Query. No multi-step
wizard needed at this scope. A "New Query" action always returns to Screen 1.

## 4. User Flows

- **Happy path:** input → confident match → results with all four data
  sections populated → done.
- **Low-confidence path:** input → no confident match → review state →
  official either refines the query or proceeds with manual research.
- **PDF (tender document) path:** upload → automatic technical-section
  extraction shown briefly (so the official can confirm the right section was
  used) → proceeds as the happy path.

## 5. Components

- Input text area + file upload control
- Primary action button
- Recommendation card (standard number, title, confidence badge, evidence
  snippet)
- Allied-standards list, grouped by relation type
- Version/amendment badge and expandable detail
- Certification status badge
- Low-confidence / review-needed state (visually distinct, not just a text
  difference)
- Loading state during processing

## 6. Interactions & Forms

- Submit is disabled until either text is entered or a file is uploaded.
- File upload validates file type (PDF only) before submission.
- Results appear progressively where possible (primary match first, allied
  standards and version/certification detail following) rather than a single
  blocking wait, if the frontend implementation supports it.

## 7. Loading / Error / Empty States

- **Loading:** clear processing indicator, since the pipeline involves two LLM
  calls and may take a few seconds.
- **Error (PDF unreadable / likely scanned):** explicit message that the
  document could not be read, not a silent empty result.
- **Empty (no allied standards found):** explicitly state "no allied standards
  found for this match" rather than omitting the section.
- **Error (system/LLM failure):** clear failure message with an option to retry.

## 8. Responsive Behavior

Single-column layout on mobile/narrow viewports; input and results stack
vertically. Allied-standards list and evidence snippets should remain fully
readable without horizontal scrolling.

## 9. Accessibility

- Sufficient color contrast for confidence/status badges — do not rely on
  color alone to distinguish confident vs. low-confidence results (pair color
  with a text label/icon).
- All interactive elements keyboard-navigable.
- Alt text or equivalent labeling for any status icons.

## 10. Typography, Colors, Spacing — Design Principles

- Clean, functional, government-tool-appropriate visual tone — not decorative;
  this is a compliance-adjacent professional tool, not a consumer app.
- Clear visual hierarchy: primary recommendation most prominent, supporting
  detail (allied standards, version, certification) secondary but easily
  scannable.
- Status colors used consistently and meaningfully (e.g., a distinct color for
  "mandatory certification" and for "low confidence") — never decorative.
- Generous spacing around the evidence snippet and explanation text, since
  these are the parts an official will actually read closely to verify trust
  in the recommendation.

## 11. Design Principle Summary

Every screen should make it obvious what the system is *confident* about
versus what needs *human verification* — this is the single most important
UX principle for a compliance tool, and it should be visually unmistakable,
not just stated in text.
