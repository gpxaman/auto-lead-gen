# Integrity Rules — IECHM-LIOS

Per Step 2 Sections 40-42. Technology-neutral integrity constraints (not tied to a specific database
vendor's constraint syntax, per `open-decisions.md` #7).

## Foreign keys and referential integrity

Every reference field named across `entity-catalog.md` and `relationships.md` (e.g., `claim.evidence_ids[]`,
`verification.claim_id`, `task.agent_id`) must resolve to an existing row — with ONE deliberate exception
class: references to `model_version_id`/`prompt_version_id` on records with `derivation_type` values that
don't involve AI (e.g., `RULE_BASED_FILTER`) are legitimately nullable, not a referential-integrity gap.

## Unique identifiers

Every `*_id` field is globally unique across its entity type, generated at creation time, never reused (even
after logical/soft deletion — see below).

## Version uniqueness

Within a given parent entity, `(parent_id, version)` is unique — e.g., no two `configuration_version` rows
share the same `(configuration_id, version)` pair. Version numbers are monotonically increasing per parent,
never reused, never decremented.

## Immutability constraints (the most important rule set in this document)

| Entity | Immutability rule |
|---|---|
| `raw_record` | Content fields (`raw_payload`, `content_hash`, `source_url`, etc.) are write-once. Any "change" produces a new row + `supersedes_raw_record_id` link. |
| `event` | Fully immutable after creation — no field may ever be updated. Corrections are new events (Section 27). |
| `evidence` | Immutable after creation except the denormalized `verification_status` cache pointer. |
| `verification` | Immutable after creation — a `FAILED` row is never edited into a `VERIFIED` row; a new row is created instead. |
| `audit_event` | Fully immutable — this IS the tamper-evidence mechanism. |
| `source_item`, `source_page`, `source_document` | Immutable, mirroring the filesystem source archive's own immutability (the core project rule, inherited from Step 0). |
| `claim` | Content immutable; only `status` and `updated_at` (status-transition-only) may change. |
| `task_attempt` | Immutable once completed (success or failure) — a retry is a new `task_attempt` row. |

## Timestamps

Every entity carries at minimum `created_at`. Entities with a meaningful lifecycle additionally carry
`updated_at` (status-transition-only, per above), and versioned entities carry `activated_at`/`retired_at`
where relevant (e.g., `configuration_version`, `agent_version`).

## Enumerations — closed vs. open

| Enum | Closed (fixed, source-derived) or Open (extensible)? |
|---|---|
| `trust_level` (12 values) | Closed — defined in `logical-data-model.md`, not extensible without a formal architecture change |
| `verification.result` (6 values) | Closed — exact Section 14 list |
| `worker` lifecycle (8 values) | Closed — exact Section 23 list |
| `metric_definition.status` (7 values) | Closed — exact Section 32 list |
| `client_archetype_set` (`SOURCE_SET_A/B/C` + future canonical) | Open — new sets/unions may be added via `open-decisions.md` #4 resolution, but existing values are NEVER removed |
| `evidence_type` | Open — `PROPOSED_EXTENSION` types (`SCREENSHOT`, `SNAPSHOT`) may be added as needed |
| `manufacturing_domain` (7 values, SCHEMA-001) | Closed — exact source enum, no invented values (Section 10 explicit) |

## State transitions — `claim.trust_level` (the core enforcement point for the Absolute Data-Preservation Principle)

```
MODEL_INFERENCE ──┐
                   ├──> UNVERIFIED_CLAIM ──> EVIDENCE_BACKED_CLAIM ──> VERIFIED
RAW_SOURCE/        │           │                                          │
RAW_EXTERNAL ──────┘           │                                          │
                                ├──> REJECTED (terminal)                  │
                                └──> QUARANTINED ──> (review) ──> back to UNVERIFIED_CLAIM or REJECTED
                                                                            │
VERIFIED ──> DERIVED (only via an explicit derivation step, never a relabeling)
```

**Illegal transitions (must be structurally prevented, not just discouraged by convention):**
- `MODEL_INFERENCE` → `VERIFIED` directly (must pass through `UNVERIFIED_CLAIM` → `EVIDENCE_BACKED_CLAIM`).
- `UNVERIFIED_CLAIM` → `VERIFIED` without an `EVIDENCE_BACKED_CLAIM` intermediate (i.e., without at least one
  `evidence` row existing AND at least one `verification` row with `result: VERIFIED` existing).
- Any transition INTO `VERIFIED` without a corresponding `verification` row — `VERIFIED` status on a `claim`
  must be justified by a real `verification.result = VERIFIED` row, checkable by a foreign-key-style query.

## Referential integrity for conflicts

A `conflict` row's two `conflict_participant` entries must reference DIFFERENT claims/source_items (a
conflict needs two sides) and neither participant's referenced claim/source_item may be deleted while the
conflict references it (enforced via the general no-hard-delete rule below).

## Soft deletion — "deleted" ≠ "historically nonexistent" (Section 40 explicit)

**No entity in this system is ever hard-deleted.** Where a business process calls for "removing" something
(e.g., retiring a worker, deprecating a platform, rejecting a claim), the mechanism is always a STATUS
TRANSITION (`RETIRED`, `DEPRECATED`, `REJECTED`) on an otherwise-permanent row, never a `DELETE` statement.
This applies even to entities that might seem disposable (a failed `task_attempt`, a `REJECTED` claim, a
`QUARANTINED` worker's state) — all remain queryable forever, consistent with the project's core "nothing is
silently lost" rule extended from Step 0/1 into the runtime data layer.

**The one narrow exception, explicitly flagged, not yet resolved:** genuinely ephemeral operational data
(e.g., a `heartbeat` ping with no analytical value beyond "is this agent alive right now") MAY be a candidate
for real deletion/expiry — but this is deferred to `retention.md`'s `EPHEMERAL` classification and
`open-decisions.md` #11, not decided here.

## Idempotency (Section 42)

| Operation | Idempotency mechanism |
|---|---|
| Ingestion | `raw_record` uniqueness on `(source_system, source_identifier, content_hash)` — re-ingesting identical content produces no new row (deduplicated), but re-ingesting CHANGED content at the same `source_identifier` DOES produce a new version (this is not a contradiction: idempotency prevents ACCIDENTAL duplication of identical data, not legitimate new observations) |
| Events | `idempotency_key` field on the event envelope; a consumer processing the same `idempotency_key` twice must be a no-op the second time |
| Classification | A `claim` for the same `(subject, predicate, task_id)` triple is idempotent — retrying a classification task that already produced a claim does not produce a duplicate, but a genuinely NEW task (different task_id, e.g. a re-classification run) legitimately can produce a new, possibly-different claim (preserving both, per the conflicting-claims rule) |
| Worker creation | `worker` uniqueness on `(parent_platform_id, subdomain_id)` where applicable — prevents duplicate-worker spawning race conditions flagged as a gap in Step 1's `dynamic-worker-scaling.md` |
| Task execution | `task_attempt` is inherently append-only; idempotency here means "don't silently skip a legitimately-needed retry," which is why failed attempts are preserved rather than deleted-and-retried in place |
| Configuration changes | Each `configuration_change` is its own immutable row; applying the "same" change twice produces two `configuration_change` rows (both valid history) rather than being deduplicated — configuration changes are HUMAN/SYSTEM DECISIONS, not raw ingestion events, so exact-duplicate suppression is not appropriate here |

**Explicit balance (Section 42's closing instruction):** idempotent processing must never destroy legitimate
historical observations. The `raw_record` dedup rule above is scoped narrowly to BYTE-IDENTICAL content —
anything less than exact identity produces a new, preserved version.
