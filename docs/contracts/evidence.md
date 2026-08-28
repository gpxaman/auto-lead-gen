# Contract: Evidence

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
The concrete artifact(s) supporting a `claim`. Implements `docs/architecture/evidence-model.md` and
`docs/database/evidence.md`.

## Source references
SRC-000034 ("verifiabl[e] proof"), SCHEMA-003's `verification_artifacts` field (`URL_PROOF`, `API_PAYLOAD`,
`LISTING_HASH`).

## Requirement references
REQ-000016, REQ-000019.

## Fields

| Field | Required? | Tag | Notes |
|---|---|---|---|
| `evidence_id` | required | `PROPOSED_SCHEMA` | |
| `source_record_id` | optional | `DERIVED_CANONICAL_SCHEMA` | points to the `raw_record` this was extracted from |
| `source_url` | optional | `SOURCE_SCHEMA` | directly from `URL_PROOF` |
| `retrieved_at` / `observed_at` | optional | `SOURCE_SCHEMA` | matches `extraction_timestamp`/`timestamp_utc` pattern from SCHEMA-002/005 |
| `content_hash` | optional | `SOURCE_SCHEMA` | directly from `LISTING_HASH` |
| `evidence_type` | required | `DERIVED_CANONICAL_SCHEMA` | `URL_PROOF` \| `API_PAYLOAD` \| `LISTING_HASH` (all 3 `SOURCE_SCHEMA`) + `SCREENSHOT` \| `SNAPSHOT` (both `PROPOSED_SCHEMA`) |
| `snapshot_reference` | optional | `PROPOSED_SCHEMA` | absent from source entirely |
| `verification_status_cache` | required | `PROPOSED_SCHEMA` | denormalized; `verification` contract is authoritative |
| `confidence` | optional | `PROPOSED_SCHEMA` | |
| `created_at` | required | `PROPOSED_SCHEMA` | |

## Validation rules
Immutable after creation (except the denormalized cache field). A `claim` may reference 0, 1, or many
`evidence` rows (Step 2 Section 12, explicit).

## Provenance
`source_record_id` traces back to `raw_record`; no independent model/prompt provenance (evidence is a fact
about the world, not an AI-derived judgment — though the DECISION to attach a given evidence item to a given
claim may itself be AI-assisted, tracked on the `claim`, not on the `evidence` row itself).

## Versioning & compatibility
Evidence is never edited — new evidence types may be added to the open `evidence_type` enum over time.

## Security classification
`CONFIDENTIAL`, potentially `SENSITIVE` if the evidence artifact itself (e.g., a raw listing snapshot)
contains untrusted third-party content.

## Examples
None fabricated. `SCHEMA-003`'s `verification_artifacts: ["URL_PROOF", "API_PAYLOAD", "LISTING_HASH"]` is the
closest source example, and is a list of TYPE VALUES, not a full evidence-record example — preserved exactly
as such.
