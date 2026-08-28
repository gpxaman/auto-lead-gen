# Contract: Claim

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
The universal, reusable unit of "an assertion about something, not yet fully trusted." Every classification
act (client archetype, manufacturing domain, commercial estimate) in IECHM-LIOS produces a `claim`, never a
direct write to a "trusted" field. See `docs/database/logical-data-model.md`'s trust-level model and
`docs/architecture/data-lineage.md`.

## Source references
No single `SRC-XXXXXX` names "claim" as a concept explicitly — this is `PROPOSED_EXTENSION` as a formal,
reusable entity, though every individual USE of a claim (client classification SRC-000034, technical
classification SRC-000010/011, commercial estimation SCHEMA-002/005) is `SOURCE-DERIVED` behavior this
contract formalizes.

## Requirement references
REQ-000013, REQ-000016, REQ-000018, REQ-000019.

## Fields

| Field | Required? | Tag | Notes |
|---|---|---|---|
| `claim_id` | required | `PROPOSED_SCHEMA` | globally unique, non-semantic |
| `subject_type` / `subject_id` | required | `PROPOSED_SCHEMA` | polymorphic reference |
| `predicate` | required | `PROPOSED_SCHEMA` | e.g. `client_archetype`, `manufacturing_domain` |
| `value` | required | `PROPOSED_SCHEMA` | polymorphic asserted value |
| `claim_type` | required | `PROPOSED_SCHEMA` | `CLASSIFICATION` \| `SCORE` \| `STATUS` \| `FACT` |
| `source_record_ids[]` | required | `DERIVED_CANONICAL_SCHEMA` | at least the raw record(s) this was derived from |
| `confidence` | optional | `SOURCE_SCHEMA` | present in source as `budget_feasibility_score`, `drift_score_at_intake`, Strategy Ledger's Confidence Score — pattern generalized here |
| `trust_level` | required | `PROPOSED_SCHEMA` | one of the 12 values in `docs/database/logical-data-model.md` |
| `status` | required | `PROPOSED_SCHEMA` | `ACTIVE` \| `SUPERSEDED` \| `REJECTED` \| `EXPIRED` |
| `derivation_method`, `model_version_id`, `prompt_version_id`, `configuration_version_id`, `agent_instance_id`, `task_id` | optional (nullable for non-AI derivations) | `DERIVED_CANONICAL_SCHEMA` | universal provenance fields |
| `valid_from` / `valid_until` | optional | `PROPOSED_SCHEMA` | bounded-validity claims |
| `created_at` / `updated_at` | required | `PROPOSED_SCHEMA` | `updated_at` only changes on status transition |

## Validation rules
- `trust_level` transitions must follow the state machine in `docs/database/integrity-rules.md` (no direct
  `MODEL_INFERENCE` → `VERIFIED`).
- A claim's core content fields (`subject`, `predicate`, `value`) are immutable after creation.
- `trust_level = VERIFIED` requires at least one linked `verification` record with `result = VERIFIED`.

## Provenance
Full universal provenance field set, per `docs/database/provenance.md`.

## Versioning & compatibility
Content changes never mutate an existing claim — a new claim is created instead (see `docs/database/versioning.md`).
This contract itself may gain new `claim_type` values over time without breaking compatibility (open enum).

## Security classification
`CONFIDENTIAL` (per `docs/database/security.md`) — business intelligence.

## Examples
None — the source never provides a literal example of a standalone "claim" object (this is a
`PROPOSED_EXTENSION` entity synthesizing behavior scattered across multiple source schemas). No example is
fabricated here.
