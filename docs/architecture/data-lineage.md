# Data Lineage

Per Step 1 Section 16. Explicitly separates data categories so nothing overwrites another category silently.

## Conceptual lineage chain

```
RAW INPUT
    ↓
RAW OBSERVATION
    ↓
CLAIM
    ↓
EVIDENCE
    ↓
VERIFICATION
    ↓
CANONICAL KNOWLEDGE
    ↓
DERIVED METRIC
    ↓
STRATEGY
    ↓
SYSTEM DECISION
```

## The 7 explicitly separated data categories

| Category | Definition | Example (IECHM-LIOS context) | Mutable in place? |
|---|---|---|---|
| RAW DATA | Exact bytes/text as scraped, before any interpretation | The HTML/text body of a scraped Upwork job listing | Never — immutable once ingested (mirrors the Level-1-SOURCE immutability principle from Step 0/1, applied here to OPERATIONAL data too) |
| NORMALIZED DATA | Raw data reshaped into a structured field layout, no judgment applied yet | The same listing split into title/description/budget fields via straightforward parsing | Append new versions, don't overwrite |
| MODEL INFERENCE | An LLM's interpretation/judgment about normalized data | "This listing's `client_archetype` is probably NPD_Innovator" | Always tagged with confidence + producing model/version; never silently promoted to VERIFIED DATA |
| VERIFIED DATA | A claim that has passed the Verification subsystem's checks (e.g., URL resolves and matches) | "Confirmed: this listing's URL is live and matches the scraped content hash" | Append-only verification records, referencing the claim they verify |
| DERIVED DATA | Computed from other data, not observed directly | A channel's average MOV, computed from many individual lead records | Recomputed, not hand-edited; always traceable to its inputs |
| HUMAN DECISION | An explicit choice made by a person (the user, an admin) | The user resolving CONFLICT-003 by picking a canonical schema version | Immutable historical record once made; a later human decision supersedes but does not erase the prior one |
| SYSTEM DECISION | An automated action taken by the system based on the above | Hot-Swap Engine deciding to quarantine a worker because drift score ≥ 0.85 | Logged (Audit subsystem), never silently reversible without a corresponding new SYSTEM DECISION or HUMAN DECISION record |

## Why MODEL INFERENCE must never silently become VERIFIED DATA

This is the single most important discipline this document establishes, and it is a direct consequence of
Step 1 Section 17 (Evidence Model) and Section 22 (Hallucination): an LLM classifying a lead as
`client_archetype: NPD_Innovator` is, by itself, only ever a MODEL INFERENCE — a probabilistic judgment that
can be wrong (hallucinated, or simply mistaken). It becomes CANONICAL KNOWLEDGE only after passing through
EVIDENCE (what specifically supports this claim — e.g., a quote from the listing) and VERIFICATION (an
independent check, e.g., the Sentinel's schema/URL/numeric-sanity validation). Skipping straight from MODEL
INFERENCE to CANONICAL KNOWLEDGE is exactly the failure mode Step 1 Section 23 warns about for context
migration ("A replacement worker must not inherit hallucinated information as trusted knowledge") — the same
discipline applies to the primary intelligence pipeline, not just to agent-failure recovery.

## Mapping onto the primary Data Flow (`data-flow.md`)

| Data Flow stage | Lineage category produced |
|---|---|
| RAW INGESTION | RAW DATA |
| NORMALIZATION | NORMALIZED DATA |
| CLIENT/TECHNICAL/COMMERCIAL CLASSIFICATION | MODEL INFERENCE (a CLAIM) |
| EVIDENCE | EVIDENCE attached to the CLAIM |
| VERIFICATION | VERIFIED DATA (or verification-failed, which keeps the record at CLAIM status) |
| CANONICAL KNOWLEDGE | The verified, evidence-backed record — now trustworthy for downstream use |
| METRICS | DERIVED DATA |
| STRATEGY | Blend of DERIVED DATA + (eventually) HUMAN DECISION (strategic priorities the user sets) |
| INTELLIGENCE OUTPUT | Built exclusively from CANONICAL KNOWLEDGE + DERIVED DATA — MODEL INFERENCE that never reached VERIFIED status should not silently leak into the output handed to System B |

## Source basis and status

The 7-category separation itself is `PROPOSED_EXTENSION` — the source never names these categories explicitly.
It is required BECAUSE the source repeatedly emphasizes (in different words, across many pages) that
AI-generated claims are fallible and must be checked (Sanitizer/Reviewer/Sentinel concepts throughout) — this
document generalizes that source-wide theme into one explicit, reusable data-lineage discipline rather than
leaving it implicit and inconsistently applied stage-by-stage.
