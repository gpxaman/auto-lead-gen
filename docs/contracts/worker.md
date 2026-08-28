# Contract: Worker

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
Lifecycle tracking for Tier 3/4 platform and sub-domain workers, including the dynamic spawn/retire behavior
of the 5-Lead Rule and the Hot-Swap failure/replacement path.

## Source references
`docs/architecture/dynamic-worker-scaling.md`, `hot-swap.md`, THRESH-001/002/004/005.

## Requirement references
REQ-000015, REQ-000020.

## Fields

### `worker`
`worker_id`, `agent_instance_id` (a worker IS an agent_instance for Tier 3/4 roles, per `agent-topology.md`),
`platform_id` or `subdomain_id` (exactly one, depending on tier).

### `worker_version`
`worker_id`, `version`, `connector_version_id`.

### `worker_state`
`worker_id`, `status`, `recorded_at` — **status enum exactly matches Step 2 Section 23's 8 values, no more,
no fewer:** `SPAWNED`, `ACTIVE`, `DEGRADED`, `QUARANTINED`, `DRAINING`, `RETIRED`, `FAILED`, `REPLACED`.

### `worker_checkpoint`
`worker_id`, `checkpoint_data`, `trust_classification` (per `docs/architecture/context-migration.md`'s
10-class state taxonomy — e.g. `TRUSTED_STATE`, `TASK_STATE`, `CONFIGURATION_STATE` are eligible for migration
to a replacement; `MODEL_INFERENCE` and `FAILED_OUTPUT` are explicitly excluded per ADR-0006), `created_at`.

### `worker_lifecycle_event` (immutable event log)
`event_id`, `worker_id`, `from_status`, `to_status`, `trigger` (`SPAWN_THRESHOLD` \| `RETIRE_THRESHOLD` \|
`SENTINEL_QUARANTINE` \| `HOT_SWAP_REPLACEMENT` \| ...), `timestamp`.

## Validation rules
Status transitions must follow the flows in `docs/architecture/data-flow.md` (WORKER SPAWN FLOW / WORKER
RETIREMENT FLOW / HOT-SWAP FLOW). A `REPLACED` worker's history remains fully queryable (Step 2 Section 23:
"Worker history must remain queryable" — never purged).

## Provenance
`worker_checkpoint.trust_classification` is the concrete data-layer implementation of ADR-0006's rule that a
replacement worker must not inherit hallucinated information as trusted knowledge — only checkpoints tagged
with a "safe" trust classification are readable by the replacement's bootstrap process.

## Versioning & compatibility
`worker_lifecycle_event` is append-only/immutable.

## Security classification
`INTERNAL`.

## Examples
None fabricated — SCHEMA-004/006's telemetry examples (`worker-layer3-upwork-cad-04`, etc.) are cited from
`docs/source-extraction/json-schemas.md` as the closest source illustration of a worker identifier format,
not reproduced as a full worker record here.
