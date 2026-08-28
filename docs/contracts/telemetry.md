# Contract: Telemetry

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
Raw operational measurements + derived aggregates, kept distinct (aggregates never replace raw, per Step 2
Section 30, explicit).

## Source references
`docs/architecture/observability.md` (15 signal types), TABLE-005/006 (token/cost figures).

## Requirement references
REQ-000018, REQ-000021, REQ-000033.

## Fields

### `telemetry_measurement` (raw, high-volume)
| Field | Required? | Tag | Notes |
|---|---|---|---|
| `measurement_id` | required | `PROPOSED_SCHEMA` | |
| `subject_type` / `subject_id` | required | `PROPOSED_SCHEMA` | agent \| worker \| task \| lead \| source \| connector \| model \| prompt \| event \| system (Section 30's exact list) |
| `metric_name` | required | `DERIVED_CANONICAL_SCHEMA` | count \| rate \| latency \| error_rate \| throughput \| cost \| token_usage \| drift \| verification \| queue_depth \| worker_utilization (Section 30's exact list) |
| `value` | required | `PROPOSED_SCHEMA` | |
| `recorded_at` | required | `PROPOSED_SCHEMA` | |

### `telemetry_aggregate` (derived, never authoritative on its own)
`aggregate_id`, `subject_type`, `subject_id`, `metric_name`, `aggregation_type` (`SUM`/`AVG`/`P95`/...),
`window_start`, `window_end`, `value`, `computed_from_measurement_count`.

## Validation rules
`telemetry_aggregate` rows must be derivable/recomputable from `telemetry_measurement` — an aggregate that
cannot be traced to underlying raw measurements is invalid (Section 30: "Preserve raw measurements where
necessary. Aggregates must not replace raw telemetry.").

## Provenance
`telemetry_measurement.subject_id` provides the trace target; `telemetry_aggregate` additionally carries
`computed_from_measurement_count` as a sanity-check field.

## Versioning & compatibility
Append-only, no versioning needed beyond the metric-definition versioning covered in `metric.md`.

## Security classification
`INTERNAL`, cost/token-usage figures bordering `CONFIDENTIAL` (competitive-sensitivity, per the source's own
extensive cost-modeling emphasis).

## Examples
None fabricated — TABLE-005/006's illustrative token/cost figures are cited from Step 0, not treated as
telemetry RECORDS (they were AI-generated projections, not measured telemetry).
