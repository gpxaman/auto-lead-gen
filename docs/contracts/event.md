# Contract: Event

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
The universal immutable event envelope used across IECHM-LIOS.

## Source references
SCHEMA-004 (v1 telemetry event), SCHEMA-006 (v2 telemetry event) — **both preserved, neither canonical**, per
CONFLICT-003. `docs/architecture/events.md`.

## Requirement references
REQ-000018, REQ-000020, REQ-000021.

## Fields (envelope — `DERIVED_CANONICAL_SCHEMA`, synthesizing SCHEMA-004/006's structure into a reusable envelope)

| Field | Required? | Notes |
|---|---|---|
| `event_id` | required | |
| `event_type` | required | e.g. `CEASE_OPERATIONS`, `FAILOVER_HOTSWAP_TRIGGERED` (v1 name) / `FAILOVER_HOTSWAP_DISPATCHED` (v2 name) — **both event type strings are valid, distinct types**, not aliases of one canonical name |
| `event_version` | required | payload schema version tag |
| `aggregate_type` / `aggregate_id` | required | polymorphic — which entity this event is about |
| `producer` | required | |
| `timestamp` | required | |
| `correlation_id` / `causation_id` | optional | |
| `payload` | required | shape depends on `event_type` + `event_version` |
| `payload_schema_version` | required | |
| `security_classification` | required | per `docs/database/security.md` |
| `idempotency_key` | optional but recommended | unique where present |

## Source-defined event types preserved exactly (see `docs/architecture/events.md` for full contract detail per event)
`CEASE_OPERATIONS`, `FAILOVER_HOTSWAP_TRIGGERED` (v1), `FAILOVER_HOTSWAP_DISPATCHED` (v2),
`CHANNEL_DATA_SATURATED_IDLE_ACTIVE`, `EVENT_CONTRACT_SIGNED` (System B/C boundary, referenced only).

## Newly proposed event types (all `PROPOSED_SCHEMA`, listed in full in `docs/architecture/events.md`)
`PLATFORM_DISCOVERED`, `PLATFORM_REGISTERED`, `PLATFORM_DEPRECATED`, `RAW_LEAD_INGESTED`,
`LEAD_REJECTED_LAYER0`, `INJECTION_DETECTED`, `CLIENT_CLASSIFIED`, `CHANNEL_BENCHMARK_UPDATED`,
`PLATFORM_PROFILE_UPDATED`, `EVIDENCE_ATTACHED`, `VERIFICATION_COMPLETED`, `VERIFICATION_FAILED`,
`AGENT_STATE_CHANGED`.

## Validation rules
Events are **fully immutable after creation — no field may ever be updated** (Step 2 Section 27, explicit).
Corrections emit a NEW event referencing the original via `causation_id`.

## Provenance
`producer` field identifies the agent/subsystem; `causation_id` chains events causally.

## Versioning & compatibility
`event_version`/`payload_schema_version` allow the SAME `event_type` to evolve its payload shape over time
without breaking old consumers — old-version events remain stored and readable.

## Security classification
Varies by `event_type` — set per-event via `security_classification`, default `INTERNAL`.

## Examples (from source, preserved verbatim — not fabricated)
```json
{
  "telemetry_event": "FAILOVER_HOTSWAP_TRIGGERED",
  "isolated_node_id": "worker-layer3-upwork-cad-04",
  "model_signature": "gpt-4o-2024-08-06",
  "consecutive_hallucinations": 3
}
```
(v1, SCHEMA-004, abbreviated — full version in `docs/source-extraction/json-schemas.md`)
```json
{
  "event_type": "FAILOVER_HOTSWAP_DISPATCHED",
  "anomaly_report": { "faulty_worker_id": "worker-layer3-alibaba-rfq-09", "drift_score": 0.92 }
}
```
(v2, SCHEMA-006, abbreviated)
