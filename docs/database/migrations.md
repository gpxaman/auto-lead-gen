# Migrations — IECHM-LIOS

Per Step 2 Section 45. Defines schema migration, data migration, backfill, version transformation, rollback,
validation, and checksum verification concepts. **No physical migration scripts are created in Step 2**
(no database vendor is chosen — `open-decisions.md` #7) — this is the conceptual migration DISCIPLINE that
any future vendor-specific migration tooling must follow.

## The governing rule

> "A migration must not silently destroy the previous representation."

This is the data-layer enforcement of Step 1's `schema-versioning.md` principle (`OLD DATA → VERSIONED
TRANSFORMATION → NEW DATA`, never an overwrite) and ADR-0004/ADR-0005.

## Migration types

| Type | Definition | Example in this project's context |
|---|---|---|
| Schema migration | Adding/changing the STRUCTURE of an entity (new field, new table) | Adding a `schema_version` field to lead records (itself a `PROPOSED_EXTENSION` per `schema-versioning.md` — no source schema version has this field today) |
| Data migration | Transforming EXISTING rows to match a new schema | If `open-decisions.md` #2 resolves to "canonicalize on SCHEMA-005," existing SCHEMA-002/003-shaped `lead_version` rows are NOT rewritten in place — see Backfill below |
| Backfill | Populating a new field for existing rows where the value can be derived/known | Computing `content_hash` for `raw_record` rows ingested before hash-computation was added, if ever needed |
| Version transformation | An explicit, testable function mapping v_n data to v_n+1 shape | The `schema-versioning.md`-mandated migration function for any future lead-schema consolidation |
| Rollback | Reverting a migration | See below — requires the pre-migration state to remain queryable, which the immutability rules in `integrity-rules.md` guarantee by construction |
| Validation | Confirming a migration produced correct output | Comparing record counts, spot-checking transformed field values against source before promoting |
| Checksum verification | Confirming no silent data corruption occurred during migration | `content_hash` comparison before/after for any raw-payload-touching migration |

## The non-destructive migration pattern (mandatory)

```
OLD SCHEMA VERSION (rows remain, untouched, forever queryable)
        │
        ▼
VERSIONED TRANSFORMATION FUNCTION (explicit, testable, versioned itself)
        │
        ▼
NEW SCHEMA VERSION (rows created fresh — NOT an UPDATE of the old rows)
        │
        ▼
Both versions coexist; application code reads whichever version(s) it's built against,
or a compatibility view/adapter bridges old readers to new data (see backward-compatibility.md — not yet
created; see `open-decisions.md` for whether this level of dual-read tooling is wanted)
```

**Concretely for THIS project's known future migration need (schema consolidation, CONFLICT-003/ADR-0004):**
when the user resolves `open-decisions.md` #2, the migration is: (1) write a transformation function
mapping SCHEMA-002/003-shaped records to whichever version is chosen; (2) run it to produce NEW rows in the
target shape; (3) leave the OLD rows exactly as they are, permanently; (4) update application read-paths to
prefer the new shape going forward. At no point are the SCHEMA-002/003-shaped original rows edited or deleted.

## Rollback

Because migrations are non-destructive (old rows persist), "rollback" in this system usually means: stop
reading/writing the NEW version and resume reading/writing the OLD version — not "undo a destructive change,"
since no destructive change was ever made. This is a materially safer rollback story than a typical
in-place-migration system, and is a direct consequence of the immutability rules in `integrity-rules.md`.

## Validation and checksum verification

Every migration that touches `raw_record` or `evidence` content must verify `content_hash` before and after
to detect corruption. Every migration producing new `claim`/`lead_version` rows must validate: (a) row counts
match expectations (no silent drops), (b) a sample of transformed records spot-checked against their source
inputs, (c) the new rows' `source_record_ids[]`/provenance fields correctly point back to the original data
(per `provenance.md`).

## What Step 2 does NOT do here

No actual migration script (SQL DDL, ORM migration file, etc.) is written, since that requires a chosen
database technology (`open-decisions.md` #7). This document is the CONTRACT any future migration tooling must
satisfy, referenced by `docs/database/migration-strategy.md` (the shorter cross-reference/summary version of
this document, created separately per Step 2 Section 48's file list) and `schema.sql`'s own header comment.
