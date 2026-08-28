# Contract: Subdomain

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
Granular per-sub-domain tracking (e.g., a specific subreddit) with dynamic worker lifecycle state, per the
5-Lead Rule.

## Source references
SRC-000036, THRESH-001/002, `docs/architecture/dynamic-worker-scaling.md`.

## Requirement references
REQ-000015.

## Fields

| Field | Required? | Tag | Notes |
|---|---|---|---|
| `subdomain_id` | required | `PROPOSED_SCHEMA` | |
| `platform_id` | required | `SOURCE_SCHEMA` | parent platform |
| `subdomain_name` | required | `SOURCE_SCHEMA` | e.g. `r/HardwareStartups` |
| `current_lead_velocity` | required | `DERIVED_CANONICAL_SCHEMA` | count/day, computed |
| `rolling_7day_average` | required | `SOURCE_SCHEMA` | explicitly named window for the RETIREMENT condition (THRESH-002); the SPAWN condition's window is `SOURCE_INCOMPLETE` — see `dynamic-worker-scaling.md` |
| `worker_status` | required | `DERIVED_CANONICAL_SCHEMA` | `NOT_SPAWNED` \| `ACTIVE` \| `RETIRED` — mirrors `worker` lifecycle enum |
| `worker_instance_id` | optional | `PROPOSED_SCHEMA` | nullable if `NOT_SPAWNED` |
| `subdomain_version_id` | required | `PROPOSED_SCHEMA` | |

## Validation rules
`worker_status` transitions to `ACTIVE` only when `current_lead_velocity > 5/day` (THRESH-001, exact value
preserved). Transitions to `RETIRED` only when `rolling_7day_average < 2/day` (THRESH-002, exact value
preserved). **No other threshold values are invented** — spawn-condition window ambiguity (`SOURCE_INCOMPLETE`)
is preserved as an open gap, not silently assumed to match the 7-day retirement window.

## Provenance
`worker_instance_id` → `worker.md` contract → full agent provenance chain.

## Versioning & compatibility
Append-only lifecycle event history via `worker_lifecycle_event` (see `worker.md`).

## Security classification
`INTERNAL`.

## Examples
None fabricated. The source names example sub-domains (`r/HardwareStartups`, `r/PrintedCircuitBoard`,
`r/InjectionMolding`) as ILLUSTRATIVE category examples, not as data-record examples — cited from
`docs/source-extraction/platforms.md`, not reproduced as a fabricated "sample subdomain record."
