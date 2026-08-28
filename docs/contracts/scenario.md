# Contract: Scenario

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
First-class representation of the source's economic/scaling scenarios, kept distinct — never confused with
actual production measurements (Step 2 Section 17, explicit).

## Source references
`docs/source-extraction/economic-scenarios.md` (SCENARIO-001 through 008), `docs/architecture/scaling-
scenarios.md` (`freelance-narrow`, `full-firehose` profiles).

## Requirement references
REQ-000033.

## Fields

| Field | Required? | Tag | Notes |
|---|---|---|---|
| `scenario_id` | required | `SOURCE_SCHEMA` | e.g. `SCENARIO-001` through `SCENARIO-008`, preserved exactly |
| `scenario_name` | required | `PROPOSED_SCHEMA` | |
| `scenario_type` | required | `DERIVED_CANONICAL_SCHEMA` | `COST_PROJECTION` \| `PROFITABILITY` \| `SCALE_PROFILE` \| `CONVERSION_FUNNEL` |
| `source_ids[]` | required | `DERIVED_CANONICAL_SCHEMA` | back to `source_item` |
| `assumptions[]` | required | `DERIVED_CANONICAL_SCHEMA` | links to `assumption` records |
| `inputs` / `formula` / `outputs` | required | `SOURCE_SCHEMA` | preserved exactly per scenario |
| `raw_volume`, `filter_rate`, `qualified_volume`, `bid_volume`, `win_rate`, `close_rate`, `AOV`, `revenue`, `margin`, `cost`, `profit` | optional (per applicability) | `SOURCE_SCHEMA` | economic scenarios only; exact Step 2 Section 17 field list |
| `context` | required | `SOURCE_SCHEMA` | the triggering user question / page reference |
| `status` | required | `PROPOSED_SCHEMA` | `ILLUSTRATIVE` (default — all 8 source scenarios are this) \| `VALIDATED` (none currently) |
| `version` | required | `PROPOSED_SCHEMA` | |

## Validation rules
**No scenario is ever collapsed/blended with another** (Step 2 Section 17, explicit) — each of the 8 source
scenarios is a permanently distinct row, even where they share overlapping assumptions (e.g., SCENARIO-004/
005/006 all build on similar 2,000-bids/day inputs but differ in margin/AOV assumptions and remain separate
rows).

## Provenance
`source_ids[]` → `source_item`; `assumptions[]` → `assumption`.

## Versioning & compatibility
Scenarios are historical facts about what was once modeled — immutable once recorded.

## Security classification
`CONFIDENTIAL` (business economic modeling).

## Examples
SCENARIO-001 through 008 themselves, preserved verbatim in `docs/source-extraction/economic-scenarios.md` —
cited, not re-fabricated here.
