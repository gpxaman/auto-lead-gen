# Evidence — IECHM-LIOS Database Documentation

Per Step 2 Sections 12-14 and 48. Implements the conceptual structure from
`docs/architecture/evidence-model.md` as concrete entity definitions.

## `claim`

| Field | Type (conceptual) | Notes |
|---|---|---|
| `claim_id` | identifier | globally unique, non-semantic (Section 41) |
| `subject` | reference | what entity this claim is about (lead, client, platform, worker, etc.) |
| `predicate` | string | which attribute is being asserted (e.g., `client_archetype`) |
| `object`/`value` | polymorphic | the asserted value |
| `claim_type` | enum | e.g., `CLASSIFICATION`, `SCORE`, `STATUS`, `FACT` |
| `source_ids[]` | reference[] | which `raw_record`(s) this claim is based on |
| `evidence_ids[]` | reference[] | may be empty (Section 12) |
| `confidence` | number | 0-1, or null if not yet assessed |
| `trust_level` | enum | see `logical-data-model.md`'s 12-value trust-level list |
| `created_at` / `updated_at` | timestamp | `updated_at` only changes on STATUS transitions, never on content edits — a content change is a new claim |
| `valid_from` / `valid_until` | timestamp | supports claims that are only true for a bounded period (e.g., a platform rule that later changed) |
| `status` | enum | `ACTIVE`, `SUPERSEDED`, `REJECTED`, `EXPIRED` |
| `derivation_method` | string | how it was produced |
| `model_version` / `prompt_version` | reference | per `provenance.md` |

**Conflicting claims are never overwritten (Section 13 explicit).** If two observations produce different
values for the same subject/predicate, BOTH `claim` rows persist; at most, the OLDER one's `status` may
transition to `SUPERSEDED` if a clear temporal ordering justifies it — but a genuine disagreement (not simply
"the value changed over time" but "two sources disagree about the same point in time") is modeled as a
`conflict` linking both claims, not a silent overwrite.

## `evidence`

| Field | Type | Notes |
|---|---|---|
| `evidence_id` | identifier | |
| `source` | reference | |
| `source_url` | string | nullable |
| `retrieved_at` / `observed_at` | timestamp | |
| `content_hash` | string | |
| `evidence_type` | enum | `URL_PROOF`, `API_PAYLOAD`, `LISTING_HASH` (all 3 directly from SCHEMA-003's `verification_artifacts`) + `SCREENSHOT`, `SNAPSHOT` (`PROPOSED_EXTENSION` — absent from source, see Step 1's `evidence-model.md` gap note) |
| `raw_reference` | reference | points to the `raw_record` this evidence was extracted from |
| `snapshot_reference` | reference | nullable, if a point-in-time snapshot was taken |
| `verification_status` | enum | denormalized cache of the latest `verification` result — authoritative source is the `verification` table |
| `verification_method` | string | |
| `verifier` | reference | which Sentinel/agent/human performed verification |
| `confidence` | number | |
| `created_at` | timestamp | |

**Evidence is immutable once created (Section 12).** No `UPDATE` path exists for `evidence` rows except the
denormalized `verification_status` cache field, which is refreshed by INSERTING a new `verification` row and
updating only that cache pointer — never by editing the evidence's own factual content.

## `verification`

| Field | Type | Notes |
|---|---|---|
| `verification_id` | identifier | |
| `claim_id` | reference | |
| `method` | string | |
| `verifier` | reference | Sentinel/agent/human |
| `verification_source` | reference | |
| `verification_timestamp` | timestamp | |
| `result` | enum | `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `CONTRADICTED`, `FAILED`, `EXPIRED` (all 6 exactly as Section 14 specifies) |
| `confidence` | number | |
| `notes` | text | |
| `artifacts` | reference[] | |
| `status` | enum | `ACTIVE`, `SUPERSEDED` |

**Failed verification attempts are never deleted (Section 14 explicit).** A `FAILED` verification row persists
permanently; if a later re-verification attempt SUCCEEDS, that is a NEW `verification` row, not an edit of the
failed one. This means a claim's full verification HISTORY (including failures) is always queryable — directly
supporting the "What was verified?" question from Step 2's Absolute Data-Preservation Principle.

## `confidence_record` and `derivation` (supporting entities from `evidence-model.md`'s 5-category structure)

`confidence_record` is not a separate table in practice — `confidence` is a field on `claim` AND on
`verification` (they can differ: a claim might have LOW confidence from its originating model, while an
INDEPENDENT verification might assign a DIFFERENT confidence to its own check). `derivation` is realized as
the `derivation_type`/`derivation_timestamp` fields on `claim` (see `provenance.md`) rather than a standalone
table, since every claim has exactly one derivation record inherently (1:1, no need for a separate join
table).

## Explicit non-implementation

No physical storage engine, indexing, or query optimizer decisions are made here (see `indexing-strategy.md`,
`query-patterns.md`, and `open-decisions.md` #7).
