# Hallucination and Drift

Per Step 1 Section 22. Documents source-defined detection concepts. The incomplete drift formula is preserved
exactly as incomplete — NOT reconstructed from general knowledge of how such formulas typically look.

## Source-defined detection concepts

| Concept | Source | Detail |
|---|---|---|
| Schema errors | SRC-000039 | "Strict schema compliance and type enforcement (Pydantic / Zod contracts)" |
| Unsupported claims | Implied by the Evidence Model's CLAIM-vs-VERIFIED distinction (`evidence-model.md`) | Not named directly as "hallucination detection" in source, but functionally the same concern |
| Numeric anomalies | SRC-000039 | "flagging impossible CAD file formats, invalid PCB layer counts, or unrealistic budg[ets]" (truncated) |
| Source failures | SRC-000039 | "URL/Endpoint verification (validating that scraped leads, URLs, and platforms exist)" |
| Contradictions | Not explicitly named by source as a detection category | Gap — not invented |
| Behavioral anomalies | Implied by the general "drift" concept but not itemized separately from numeric/schema anomalies | `INTERPRETATION` |
| Drift | SRC-000077, THRESH-004 | The formalized, scored version of all the above, feeding the quarantine trigger |
| Repeated validation failures | THRESH-005 | "≥3 consecutive schema/validation errors" |

## The incomplete drift formula — preserved exactly

```
D_t = α · Error_schema + β · Anomaly_numeric + γ · [truncated in source render]
```

**Status: `SOURCE_INCOMPLETE`.** This is the formula exactly as it appears in the source (page 28), with the
third term's coefficient (γ) and its full right-hand-side operand visible only as far as "γ ·" before the
original PDF's own rendering cuts it off. Per Step 1 Section 22's explicit instruction:

> "Preserve the source's incomplete drift formula exactly as incomplete. Do NOT reconstruct missing portions
> from general knowledge. If a formula is incomplete: status = SOURCE_INCOMPLETE"

**This document does not propose what the missing third term (or any subsequent terms) should be.** A
reasonable engineering guess (e.g., "γ · Anomaly_behavioral" or "γ · Contradiction_rate") is deliberately
withheld here, because inventing it — even plausibly — would misrepresent an AI-generated guess as if it were
part of the source specification. If a working drift-score formula is needed for implementation, that is a
NEW, explicitly-labeled `PROPOSED_EXTENSION` decision for a future step, made consciously, not smuggled into
this document.

## Consequence for implementation readiness

`D_t` as literally specified in the source CANNOT be computed — only α·Error_schema + β·Anomaly_numeric (2 of
at least 3 terms) are fully defined. This means:
- THRESH-004 (`D_t ≥ 0.85`) cannot be evaluated as written without either (a) a new, explicitly-proposed
  completion of the formula, or (b) falling back to THRESH-005 (the discrete ≥3-consecutive-failures
  condition) as the sole operative trigger until the formula gap is resolved.
- This is recorded as a blocking gap for Sentinel Plane implementation, to be raised in
  `docs/architecture/open-decisions.md`.

## Relationship to Evidence Model

Hallucination detection is the SENTINEL-SIDE mechanism that determines whether a MODEL INFERENCE (per
`data-lineage.md`) should be trusted enough to proceed toward VERIFICATION, or should instead trigger a
worker-level quarantine because the PATTERN of the worker's outputs (not just one output) indicates
unreliability. These are related but distinct: Evidence Model governs trust in individual CLAIMS; Hallucination
Detection governs trust in individual WORKERS over time.
