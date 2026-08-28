# Contract: Metric

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
Lifecycle tracking for the Metric Evolution / Saturation Optimizer's proposed data fields.

## Source references
SRC-000037, SRC-000079, THRESH-006, `docs/architecture/metric-evolution.md`.

## Requirement references
REQ-000018, REQ-000021.

## Fields

### `metric_definition` / `metric_version`
`metric_id`, `metric_name`, `description`, `computation_method`, `version`.

### `metric_proposal`
`proposal_id`, `proposed_metric_name`, `proposing_agent_instance_id`, `channel_id` (which channel's data
triggered this), `entropy_signal` (the "unexplained variance" that motivated the proposal), `proposed_at`.

### `metric_experiment` / `metric_evaluation`
`experiment_id`, `proposal_id`, `trial_data`, `evaluation_result`.

### Status enum (exact, Step 2 Section 32 list)
`PROPOSED`, `EXPERIMENTAL`, `ACTIVE`, `REJECTED`, `DEPRECATED`, `SATURATED`, `RETIRED`.

## Validation rules
A metric reaching `ACTIVE` status **must not directly mutate the production schema** — it must instead trigger
a `schema_registry` migration proposal (Step 2 Section 32, explicit, consistent with ADR-0005). `SATURATED`
status is set when THRESH-006 (≥99.5% consistency over 72h) is met for a channel, at which point further
`PROPOSED` metrics for that channel are auto-transitioned toward `NOTICE_ONLY` handling (see
`docs/architecture/metric-evolution.md`'s 4-outcome model — note this contract's status enum is the DATA
lifecycle; the `NOTICE_ONLY`/`IDLE` OUTCOMES from that architecture doc map onto `REJECTED`/`SATURATED`
respectively at the data layer).

## Provenance
`metric_proposal.proposing_agent_instance_id` traces to `agent.md`.

## Versioning & compatibility
`metric_version` increments per computation-method change; old versions retained for backward comparability.

## Security classification
`INTERNAL`.

## Examples
None fabricated — the source describes the PROCESS, never a literal proposed-metric example.
