# Contract: Agent

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
Identity, role, tier, configuration, health, and permission model for every agent role in
`docs/architecture/agent-topology.md`.

## Source references
SRC-000033/037/038/039/075, TABLE-004.

## Requirement references
REQ-000015, REQ-000018, REQ-000019, REQ-000020.

## Fields

### `agent` (role definition)
| Field | Required? | Tag | Notes |
|---|---|---|---|
| `agent_id` | required | `PROPOSED_SCHEMA` | |
| `role_name` | required | `SOURCE_SCHEMA` | e.g. "Client Classification Swarm," "Hallucination Sentinel" — verbatim role names from source |
| `tier` | required | `DERIVED_CANONICAL_SCHEMA` | Tier 0-4 per ADR-0002's naming convention (disambiguates the source's own Layer-numbering collision) |
| `classification` | required | `DERIVED_CANONICAL_SCHEMA` | `AI_AGENT` \| `WORKER` \| `ORCHESTRATOR` \| `SENTINEL` \| `DETERMINISTIC_SERVICE` \| `CONNECTOR` \| `SCHEDULED_PROCESS` per `agent-topology.md` |

### `agent_version`
`agent_id`, `version`, `prompt_version_id`, `capability_set[]`, `created_at`.

### `agent_instance`
`agent_instance_id`, `agent_id`, `parent_agent_instance_id` (nullable — org-chart parent), `spawned_at`,
`retired_at`.

### `agent_state` (append-only, never destructively overwritten — Step 2 Section 21 explicit)
`agent_state_id`, `agent_instance_id`, `status`, `drift_score` (nullable, ties to FORMULA-002/THRESH-004,
`SOURCE_INCOMPLETE` formula), `recorded_at`.

### `agent_configuration`
`agent_instance_id`, `configuration_version_id`.

### `agent_health`
`agent_instance_id`, `heartbeat_at` (`PROPOSED_EXTENSION` — no heartbeat concept in source, per
`agent-control-plane.md`'s gap note), `consecutive_failures` (THRESH-005).

### `agent_capability`
`agent_id`, `capability_name`, `capability_description`.

### `agent_permission`
`agent_id`, `permission_scope` (e.g., "read-only external access to its own platform" per `agent-topology.md`).

## Validation rules
`agent_state` rows are INSERT-only; there is no code path to UPDATE a historical `agent_state` row (per
`docs/database/integrity-rules.md`). Sentinel-owned tables (`sentinel_check` etc., see `sentinel.md` domain
in `entity-catalog.md`) have no write path from `agent`/`worker`-scoped permissions, enforcing the
independence requirement (ADR-0008).

## Provenance
`agent_version.prompt_version_id` → `prompt_version` (per `docs/database/schema.sql`).

## Versioning & compatibility
`agent_version` increments on any role/prompt/capability change.

## Security classification
`INTERNAL`. `agent_permission` scope definitions are `CONFIDENTIAL` (operational security detail).

## Examples
None fabricated. The role names and counts (140-196 total, TABLE-004) are cited from Step 0/1, not
re-invented.
