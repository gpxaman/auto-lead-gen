# Indexing Strategy — IECHM-LIOS

Per Step 2 Section 48. Conceptual indexing guidance — no physical index DDL, since no database vendor is
chosen (`open-decisions.md` #7). This document identifies WHICH access patterns need fast lookup, informing
(not dictating) whatever physical indexing a future vendor-specific implementation applies.

## High-value lookup patterns (candidates for indexing regardless of eventual technology)

| Pattern | Why it matters | Entities involved |
|---|---|---|
| "Give me the latest version of X" | Nearly every versioned entity is queried this way far more often than "give me version N" | All `*_version` tables — index on `(parent_id, version DESC)` |
| "Give me all claims about subject Y" | Core to the Client/Lead/Technical classification subsystems | `claim` — index on `(subject_type, subject_id)` |
| "Give me the verification history of claim Z" | Powers the "What was verified?" question from Step 2's closing principle | `verification` — index on `claim_id` |
| "Give me the full provenance chain for output O" | The `provenance.md` trace — must be efficient or the traceability guarantee becomes impractical to actually use | `claim`/`task_result` — index on `task_id`, `agent_id`, `model_version_id` |
| "Give me all active leads for platform P" | Core operational query for Platform Intelligence | `lead_source` — index on `(platform_id, lead_id)` where `lead_status = ACTIVE` (partial/filtered index candidate) |
| "Give me the 5-Lead Rule's rolling velocity for sub-domain S" | Powers `dynamic-worker-scaling.md`'s spawn/retire decision, needs to be FAST since it's checked frequently | `lead` events windowed by `(subdomain_id, observed_at)` — time-range index |
| "Give me all open conflicts" | Powers project governance/review workflows | `conflict` — index on `status` where `status IN (OPEN, UNDER_REVIEW)` |
| "Give me all rows this Sentinel flagged for worker W" | Powers Hot-Swap incident review | `sentinel_check`/`sentinel_alert` — index on `observed_worker_id` |
| "Give me the audit trail for actor A" | Compliance/security review | `audit_event` — index on `(actor_id, timestamp)` |
| "Give me evidence for claim C" | Core evidence-chain lookup | `evidence` — index via the `claim`↔`evidence` many:many join, or a denormalized `claim_id` array field with an appropriate index type depending on vendor |
| Content-hash deduplication check | Powers `integrity-rules.md`'s idempotent-ingestion rule | `raw_record` — unique index on `(source_system, source_identifier, content_hash)` |

## What is explicitly deferred

- Choice of B-tree vs. hash vs. GIN/inverted vs. vector-similarity index types — vendor-dependent.
- Partitioning/sharding strategy for high-volume tables (`raw_record`, `telemetry_measurement`, `event`) at
  `full-firehose` scale — deferred to `open-decisions.md` #7/#10 (database + deployment architecture).
- Full-text search indexing over raw lead content (relevant if a future "search past leads by keyword" feature
  is wanted) — not requested by the source, `PROPOSED_EXTENSION` if ever built, not designed here.

## Guiding principle

Every indexing decision must respect the immutability rules in `integrity-rules.md` — e.g., an index
supporting "latest version" queries must not be implemented in a way that requires mutating historical rows
(a common anti-pattern is maintaining an `is_latest` boolean flag that gets flipped on old rows when a new
version arrives — this document explicitly flags that such a flag, if used, must be treated as a DERIVED,
rebuildable cache field, never the authoritative record of history, consistent with `retention.md`'s
`DERIVED_REBUILDABLE` classification).
