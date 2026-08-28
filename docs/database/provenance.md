# Provenance — IECHM-LIOS

Per Step 2 Section 36 (and cross-referenced throughout Sections 5-35). Defines the universal provenance field
pattern and the traceability chain every derived record must support.

## The universal provenance field set

Applied to every DERIVED record (claims, commercial estimates, lead scores, task results, metric values,
memory items — anything NOT a raw/immutable fact):

| Field | Meaning |
|---|---|
| `record_id` | This record's own identifier |
| `source_record_ids[]` | Which `raw_record`(s) or upstream `claim`(s) this was built from |
| `parent_record_ids[]` | If this record is a revision/derivative of another record of the SAME type |
| `evidence_ids[]` | Supporting evidence, if any (may be empty for a pure MODEL_INFERENCE not yet backed) |
| `derivation_type` | e.g., `LLM_CLASSIFICATION`, `RULE_BASED_FILTER`, `AGGREGATION`, `HUMAN_ENTRY` |
| `derivation_timestamp` | When this record was produced |
| `model_version_id` | Which model produced it (nullable — not all records are AI-derived; e.g. Layer 0 deterministic triage results have `derivation_type: RULE_BASED_FILTER` and `model_version_id: null`) |
| `prompt_version_id` | Which prompt (nullable, same reasoning) |
| `configuration_version_id` | Which active configuration governed this derivation |
| `agent_id` | Which agent instance performed the derivation (nullable for pure deterministic/Layer-0 processing) |
| `task_id` | Which task this was produced under |

## The mandatory trace

```
OUTPUT
  ↓ (task_id)
TASK
  ↓ (agent_id)
AGENT
  ↓ (model_version_id, prompt_version_id)
MODEL/PROMPT
  ↓ (source_record_ids[])
INPUT
  ↓ (source_record_ids[] → raw_record → source_document/source_page, where applicable)
SOURCE
  ↓ (evidence_ids[])
EVIDENCE
```

Every arrow above must be a real, queryable foreign-key path in whatever physical database eventually
implements this model — this is the concrete, enforceable version of `docs/architecture/master-architecture.md`
Section 11's provenance requirement.

## Why this matters specifically for IECHM-LIOS's own credibility

The source PDF itself (`docs/source-extraction/economic-scenarios.md`) is a cautionary example of provenance
failure at scale: dollar figures like "$1,000,000/day profit" were produced with no visible chain back to
verified inputs — they rest on an unverified hardware assumption (ASSUMPTION-001), illustrative conversion
rates, and no cited empirical backing. IECHM-LIOS's OWN output (the Intelligence → System B report, per
`system-boundaries.md`) must never repeat this failure mode: every claim in that report must be traceable back
through this exact chain to either VERIFIED canonical knowledge or an explicitly-labeled estimate/assumption,
never presented as fact without that trace being available on request.

## Provenance for non-AI-derived data

Not every record has a `model_version_id`/`prompt_version_id` — Layer 0 deterministic triage
(`docs/architecture/subsystems.md` #5), schema validation checks, and human-entered configuration changes are
all legitimate `derivation_type` values that don't involve an LLM. The provenance chain still applies —
`configuration_version_id` and `agent_id` (or a human `actor_id` for manual entries) are always present even
when model/prompt fields are null.

## Provenance for the Source Document domain itself

`source_item` rows carry their own minimal provenance: `source_id` (their own identity), `page_id`,
`extraction_method` (implicitly: "supplied inline in conversation, platform-rendered text" per Step 0's
manifest disclosure) — this is the ROOT of the entire provenance chain; nothing traces further back than
this, by design, since the source document is Level 1 SOURCE (immutable, per the core project rule).

## Explicit scope limit

This document defines the LOGICAL provenance requirement. It does not specify indexing strategy for fast
provenance-chain queries (see `indexing-strategy.md`) or a physical storage mechanism (deferred per
`open-decisions.md` #7).
