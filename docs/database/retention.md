# Retention — IECHM-LIOS

Per Step 2 Section 43. **No final retention periods are invented.** Every entity family is classified into
one of 5 buckets; exact durations are marked `UNDECIDED` where not established by source or approved
architecture (which is everywhere — the source never addresses retention at all, and Step 1's
`open-decisions.md` #11 explicitly left this open).

## The 5 classification buckets

| Bucket | Meaning |
|---|---|
| `MUST_PRESERVE` | Never deleted, ever — core to the project's audit/provenance guarantees |
| `LONG_TERM` | Retained for an extended period by default, but not necessarily forever |
| `CONFIGURABLE` | Retention period is a policy decision, not architecturally fixed |
| `DERIVED_REBUILDABLE` | Can be safely deleted/expired because it can be recomputed from `MUST_PRESERVE`/`LONG_TERM` data |
| `EPHEMERAL` | Genuinely short-lived operational data with no lasting analytical value |

## Classification by entity family

| Entity family | Bucket | Duration |
|---|---|---|
| `source_document`, `source_page`, `source_item` (Step 0 archive) | `MUST_PRESERVE` | Forever — core project rule |
| `raw_record` | `MUST_PRESERVE` (justification/audit value) — **but see the capacity caveat below** | `UNDECIDED` |
| `claim`, `evidence`, `verification` | `MUST_PRESERVE` | Forever — this IS the system's memory, per Step 2's closing principle |
| `conflict`, `assumption`, `scenario`, `formula`, `schema_registry` | `MUST_PRESERVE` | Forever |
| `audit_event` | `MUST_PRESERVE` | Forever — legally/operationally this is usually the LEAST negotiable retention class in any real system |
| `agent_state`, `worker_lifecycle_event`, `task_attempt` (incl. failures) | `LONG_TERM` | `UNDECIDED` — needed for incident review and pattern detection (`hot-swap.md`), but perhaps not literally forever at extreme scale |
| `configuration_change` | `MUST_PRESERVE` | Forever — audit requirement (Section 25 explicit) |
| `event` (domain events) | `LONG_TERM` | `UNDECIDED` — the EVENT HISTORY + CURRENT STATE split (`entity-catalog.md`) means current state can be cheaply rebuilt even if very old events are eventually archived/cold-stored |
| `telemetry_measurement` (raw) | `CONFIGURABLE`, likely with an aggregation-then-archive pattern | `UNDECIDED` |
| `telemetry_aggregate` (derived rollups) | `DERIVED_REBUILDABLE` in principle (could be recomputed from raw), but practically `LONG_TERM` since recomputation may be expensive at scale | `UNDECIDED` |
| `memory_embedding` | `DERIVED_REBUILDABLE` — can be regenerated from `memory_source` canonical records (per Section 33's "RAG is derived" rule) | `UNDECIDED`, but rebuildability means this is a LOW-RISK deletion candidate if storage pressure demands it |
| `sentinel_check` (routine, non-incident) | `CONFIGURABLE` | `UNDECIDED` |
| `sentinel_alert`, `sentinel_action` (actual incidents) | `LONG_TERM` (feeds Audit) | `UNDECIDED` |
| Heartbeat/liveness pings (if implemented per `agent-control-plane.md`'s `PROPOSED_EXTENSION` heartbeat op) | `EPHEMERAL` | `UNDECIDED`, but this is the clearest EPHEMERAL candidate in the whole model |
| `client_classification`, `lead_classification`, `technical_classification` (claims) | `MUST_PRESERVE` (they ARE claims, see above) | Forever |
| `security_event`, `quarantine_record`, `threat_indicator` | `MUST_PRESERVE` | Forever — security-relevant history |

## The capacity caveat for `raw_record`

Per `open-decisions.md` #11's own framing: at `full-firehose` scale (1.5-2.5M leads/day,
`docs/architecture/scaling-scenarios.md`), unlimited raw-payload retention is likely infeasible. This document
does NOT resolve that tension by inventing a retention period — it flags `raw_record` as `MUST_PRESERVE` in
principle (justification/audit value) while explicitly noting the duration is `UNDECIDED` and that a real
retention POLICY (possibly tiered: full payload short-term, hash+metadata-only long-term) is required before
`full-firehose` scale is operationally viable. This is exactly the kind of configurability Step 2 Section 2
requires ("If a data model needs to accommodate an unresolved decision: design for configurability/
versioning") rather than hard-coding an arbitrary retention number now.

## What this document does NOT do

Invent a single retention period for anything. Every `UNDECIDED` above is a genuine, flagged gap requiring
explicit user/architectural decision, added to `open-decisions.md` as item #11's fuller elaboration (not a
new numbered item, since #11 already covers this ground at the architecture level — this document operationalizes
it at the entity-by-entity level).
