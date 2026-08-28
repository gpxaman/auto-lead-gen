# Contract: Configuration

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
Versioned, auditable policy/threshold storage.

## Source references
`docs/architecture/configuration.md`, THRESH-001 through THRESH-015.

## Requirement references
REQ-000015, REQ-000018, REQ-000021, REQ-000022 (System B pricing rule, referenced only).

## Fields

### `configuration`
`configuration_id`, `scope` (e.g. `sentinel.drift_threshold`, `worker.spawn_threshold`).

### `configuration_version`
| Field | Required? | Tag | Notes |
|---|---|---|---|
| `configuration_version_id` | required | `PROPOSED_SCHEMA` | |
| `configuration_id` | required | `PROPOSED_SCHEMA` | |
| `version` | required | `PROPOSED_SCHEMA` | monotonic integer |
| `data` | required | mixed | the actual value(s) — for source-derived thresholds, `SOURCE_SCHEMA` (e.g. `{"spawn_threshold": 5, "unit": "leads/day"}` directly from THRESH-001) |
| `created_by` | required | `PROPOSED_SCHEMA` | actor id |
| `created_at` / `activated_at` / `retired_at` | required/optional | `PROPOSED_SCHEMA` | |

### `configuration_change` (immutable, auditable)
`configuration_id`, `old_version`, `new_version`, `changed_by`, `reason`, `audit_event_id`.

### `configuration_scope`
Defines the hierarchy a configuration value applies at: global / macro-channel / platform / sub-domain.

## Seed values (from Step 1's `configuration.md`, all preserved exactly)
`sentinel.drift_threshold = 0.85` (THRESH-004), `sentinel.consecutive_failure_threshold = 3` (THRESH-005),
`worker.spawn_threshold = 5/day` (THRESH-001), `worker.retire_threshold = 2/day over 7-day avg` (THRESH-002),
`strategist.explore_exploit_split = 80/20` (THRESH-003, System B, referenced), `saturation.threshold =
99.5%/72h` (THRESH-006).

## Validation rules
Every production-affecting change MUST produce a `configuration_change` + `audit_event` (Step 2 Section 25,
explicit — no silent config changes).

## Provenance
`configuration_change.audit_event_id` is mandatory, non-nullable.

## Versioning & compatibility
`CONFIG-V1 → CONFIG-V2 → ...` per entity, never an overwrite.

## Security classification
`CONFIDENTIAL`; blacklist/threshold values bordering `SENSITIVE` (adversary-relevant, per
`docs/database/security.md`).

## Examples
Seed values above are exact source-derived thresholds, cited not fabricated.
