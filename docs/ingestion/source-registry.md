# Source Registry

Per Step 3 Sections 5-9, 37. Implementation: `src/sources/models.py`, `src/sources/registry.py`.
Tests: `tests/sources/test_registry.py`.

## A source is not a lead (Step 3 Section 5)

`Source` describes WHERE data comes from (a provider/location/channel/platform). It is never
conflated with `Observation` (what was found through a source) or a future `Lead` (deferred, see
`docs/ingestion/ingestion-lifecycle.md`).

## Entities implemented

| Entity | Class | Notes |
|---|---|---|
| SOURCE | `Source` | stable identity, points to `latest_source_version_id` |
| SOURCE_VERSION | `SourceVersion` | versioned config snapshot; `SourceRegistry.update_source_version()` always appends, never edits |
| SOURCE_ENDPOINT | `SourceEndpoint` | where concretely to reach a source |
| SOURCE_POLICY | `SourcePolicy` | access method, rate limits, compliance, security policy — all default to `UNKNOWN`, never invented |
| SOURCE_HEALTH | `SourceHealthEvent` | append-only health log, `SourceRegistry.record_health_event()` |

## `UNKNOWN` semantics (Step 3 Section 6)

Every optional/unconfirmed field defaults to the literal `"UNKNOWN"` string (or `None` where the
type is inherently nullable) — never an invented value. See `tests/sources/test_registry.py::
test_unknown_values_use_explicit_unknown_not_invented_defaults`.

## Registry API (Step 3 Section 37)

`SourceRegistry` implements: `register_source`, `get_source`, `update_source_version`,
`get_all_versions`, `get_latest_version`, `add_policy_version`, `add_endpoint`,
`record_health_event`, `get_health_history`, `list_sources`, `health_check`. Not exposed over a
network API in Step 3 (in-process library only) — no authentication boundary is needed yet; this
is deferred to whichever future step exposes it as a real service (`open-decisions.md`).

## Events emitted

`SourceRegistered`, `SourceUpdated` (both defined in `src/sources/registry.py`, consistent with
`docs/architecture/events.md`'s `PROPOSED_EVENT` naming convention).

## Source IDs / Requirements

SRC-000014 through SRC-000023 (platform/channel taxonomy), SRC-000035 (platform/channel fields).
REQ-000010, REQ-000017.
