# Logical Data Model — IECHM-LIOS

Per Step 2 Sections 3-4. This is the foundational document every other `docs/database/` and `docs/contracts/`
file builds on. **Technology-neutral** — no database vendor is assumed (per Step 2 Section 38 and open
decision #7). Scope: System A (IECHM-LIOS) only, per `docs/architecture/system-boundaries.md` / ADR-0001.

## The 9-stage lineage (Step 2 Section 3, extending Step 1's 7-category `data-lineage.md`)

```
SOURCE
    ↓
RAW DATA
    ↓
OBSERVATION
    ↓
CLAIM
    ↓
EVIDENCE
    ↓
VERIFICATION
    ↓
CANONICAL KNOWLEDGE
    ↓
DERIVED INTELLIGENCE
    ↓
DECISION
    ↓
ACTION
```

Each stage is a **distinct entity family**, never collapsed into one table merely because two stages "look
similar." Concretely:

| Stage | What it is | NOT the same as | Owning contract |
|---|---|---|---|
| SOURCE | The immutable Step 0 preserved document archive (design-time, not runtime data) | Runtime RAW DATA — the source PDF is not a scraped lead | N/A — filesystem-authoritative, see `source-document-model` below |
| RAW DATA | Exact, unmodified bytes/text as retrieved from an external system | OBSERVATION (which is raw data placed in operational context) | `raw-record` (this document) |
| OBSERVATION | A raw record recognized as pertaining to a specific external entity (a listing, an RFQ) at a point in time | CLAIM (which is an assertion ABOUT the observation, not the observation itself) | `raw-record`, `lead.md` |
| CLAIM | An assertion about a subject/predicate/value, produced by a person or model, not yet trusted | EVIDENCE (which supports a claim) or VERIFICATION (which checks it) | `claim.md` |
| EVIDENCE | A concrete artifact (URL, hash, snapshot) supporting a claim | VERIFICATION (an independent check that the evidence is valid) | `evidence.md` |
| VERIFICATION | The record of an independent check confirming (or contradicting) a claim, using its evidence | CANONICAL KNOWLEDGE (verification is an input to trust, not trust itself) | `verification.md` |
| CANONICAL KNOWLEDGE | A claim that has reached VERIFIED trust level and is safe for downstream use | DERIVED INTELLIGENCE (which is computed FROM canonical knowledge) | `lead.md`, `client.md`, `platform.md`, `subdomain.md` |
| DERIVED INTELLIGENCE | Computed/aggregated values built from one or more canonical records | DECISION (a derived metric is not itself a choice) | `metric.md`, `scenario.md` |
| DECISION | An explicit choice (human or system) made using derived intelligence | ACTION (a decision is not yet the act of doing something) | `audit.md` (via AUDIT_EVENT) |
| ACTION | The actual execution of a decision (e.g., spawning a worker, sending output to System B) | — | `event.md` (via domain events) |

## Data trust levels (Step 2 Section 4) — preserved exactly, not interchangeable

| Trust level | Meaning | Can it become VERIFIED automatically? |
|---|---|---|
| `RAW_SOURCE` | Bytes from the immutable Step 0 source document archive | N/A — not a runtime trust level, a design-time provenance tag |
| `RAW_EXTERNAL` | Bytes as retrieved from an external platform, unmodified | No |
| `OBSERVED` | A raw external record recognized as pertaining to a specific tracked entity | No |
| `MODEL_INFERENCE` | An LLM-produced judgment about an observation (e.g., "this is `client_archetype: NPD_Innovator`") | **No — never automatically.** Must pass through EVIDENCE_BACKED_CLAIM → VERIFIED |
| `UNVERIFIED_CLAIM` | Any claim (human or model) that has not yet been checked | No |
| `EVIDENCE_BACKED_CLAIM` | A claim with at least one attached EVIDENCE record | No — evidence existing is not the same as evidence being CHECKED |
| `VERIFIED` | A claim whose evidence has passed an independent VERIFICATION check | — (this IS the target state) |
| `DERIVED` | Computed from one or more VERIFIED (or explicitly-flagged lower-trust) inputs, with its own trust inherited from the weakest input unless explicitly re-verified | No, inherits |
| `HUMAN_DECISION` | An explicit choice made by a person | N/A — decisions aren't "verified," they're recorded |
| `SYSTEM_DECISION` | An automated action taken per policy (e.g., Hot-Swap quarantine) | N/A |
| `QUARANTINED` | Data associated with a Sentinel-flagged worker/incident, held pending review | No — explicitly blocked from promotion until reviewed |
| `RESOLVED` (n/a — not applicable to trust escalation) | — | — |
| `REJECTED` | A claim or verification attempt that failed | Terminal — a rejected claim does not silently retry into VERIFIED; a NEW claim must be created if re-asserted |

**The hard rule (repeated from Step 1, now enforced at the data-model level):** `MODEL_INFERENCE` → `VERIFIED`
is NEVER a direct transition. The only path is `MODEL_INFERENCE` → `UNVERIFIED_CLAIM` →
`EVIDENCE_BACKED_CLAIM` → `VERIFIED` (or → `REJECTED` / stays `UNVERIFIED_CLAIM` indefinitely). This is
enforced structurally: the `claim` entity's `trust_level` field transitions are constrained (see
`integrity-rules.md` state-transition table), not left to application-code discipline alone.

## Why a claim appearing "authoritative" does not grant VERIFIED status

Per Step 2 Section 4's explicit instruction ("A source claim must not automatically become VERIFIED merely
because it appears authoritative"): even a claim sourced from, e.g., a platform's own official RFQ metadata
(which might seem more trustworthy than a forum post) still enters the model as `RAW_EXTERNAL` →
`OBSERVED` → (classification produces a) `MODEL_INFERENCE`/`UNVERIFIED_CLAIM`, and must still acquire
EVIDENCE and pass VERIFICATION like any other claim. The SOURCE's apparent authority may inform how much
EVIDENCE is needed or how VERIFICATION is performed (e.g., a platform's own structured RFQ field might need
less independent checking than a free-text forum post), but it never skips the pipeline.

## Relationship to Step 1's 7-category taxonomy

Step 1's `data-lineage.md` defined 7 categories (RAW DATA / NORMALIZED DATA / MODEL INFERENCE / VERIFIED
DATA / DERIVED DATA / HUMAN DECISION / SYSTEM DECISION). Step 2's 9-stage lineage and 12 trust levels are a
**refinement, not a replacement** — every Step 1 category maps onto one or more Step 2 stages/trust-levels:

| Step 1 category | Step 2 stage(s) | Step 2 trust level(s) |
|---|---|---|
| RAW DATA | RAW DATA | `RAW_EXTERNAL` |
| NORMALIZED DATA | OBSERVATION | `OBSERVED` |
| MODEL INFERENCE | CLAIM | `MODEL_INFERENCE`, `UNVERIFIED_CLAIM` |
| VERIFIED DATA | CANONICAL KNOWLEDGE | `VERIFIED` |
| DERIVED DATA | DERIVED INTELLIGENCE | `DERIVED` |
| HUMAN DECISION | DECISION | `HUMAN_DECISION` |
| SYSTEM DECISION | DECISION, ACTION | `SYSTEM_DECISION` |

`EVIDENCE`, `VERIFICATION`, `EVIDENCE_BACKED_CLAIM`, `QUARANTINED`, and `REJECTED` are new refinements
introduced at Step 2 that Step 1 named conceptually (`evidence-model.md`) but did not formalize as data-model
trust levels.

## Source-document data model (Step 2 Section 6) — filesystem remains authoritative

**The database representation of the source archive NEVER replaces the filesystem archive under
`docs/source-extraction/`.** Any database-side `source_document` / `source_page` / `source_item` records are
a **queryable index/mirror**, not the canonical copy. If they ever diverge, the filesystem wins.

| Entity | Purpose | Key fields (conceptual) |
|---|---|---|
| `source_document` | One row per preserved source PDF (currently 1: the Gemini export) | `document_id`, `document_name`, `sha256` (nullable — see Step 0's manifest), `page_count`, `processed_at` |
| `source_document_version` | If the source document itself is ever re-supplied/re-extracted (e.g., the real binary is later provided) | `document_id`, `version`, `extraction_method`, `created_at` — supersedes, never overwrites, the prior extraction |
| `source_page` | One row per page (29 currently) | `page_id`, `document_id`, `page_number`, `content_ref` (pointer to the filesystem `.md` file, NOT a duplicate copy of its content) |
| `source_item` | One row per `SRC-XXXXXX` register entry | `source_id`, `page_id`, `category`, `exact_text`, `normalized_meaning`, `status` — mirrors `source-register.jsonl` exactly |
| `source_reference` | A pointer FROM any other entity (claim, requirement, ADR, contract field) TO one or more `source_item` rows | `reference_id`, `referencing_entity_type`, `referencing_entity_id`, `source_id` |
| `source_extraction_status` | Per-page extraction completeness/truncation flags | `page_id`, `status` (`COMPLETE`/`SOURCE_INCOMPLETE`), `truncation_notes` |
| `source_classification` | The category taxonomy applied to source items (`SOURCE_FACT`, `USER_REQUIREMENT`, `AI_PROPOSAL`, etc. — see Step 0's category list) | `category_id`, `category_name`, `description` |

This mirrors `docs/source-extraction/source-register.jsonl` field-for-field (`source_id`, `document`, `page`,
`section`, `category`, `exact_text`, `normalized_meaning`, `status`) — see `contracts/source-reference.md`
is NOT created as a separate contract (source referencing is a cross-cutting FIELD pattern used by nearly
every other contract, not a standalone domain), but every contract that needs to cite source material uses
this `source_reference` shape consistently.

## Scope note

This document, and everything under `docs/database/` and `docs/contracts/`, covers **System A (IECHM-LIOS)
data only**. System B/C entities (bid records, manufacturing orders) are out of scope per
`system-boundaries.md` — referenced only where IECHM-LIOS's own data touches the `INTERFACE_UNDEFINED`
boundary (see `contracts/README.md`).
