# Migration Strategy — Summary

Per Step 2 Section 48's documentation file list (`docs/database/migration-strategy.md`, distinct path from
Section 45's explicitly-required `docs/database/migrations.md`). This file is a short pointer/summary to
avoid duplicating content — **the full migration discipline lives in `migrations.md`**; this file exists to
satisfy Section 48's explicit path requirement and to give a one-page orientation.

## One-page summary

1. **No migration is ever destructive.** Old rows are never edited or deleted by a migration — see
   `migrations.md`'s non-destructive migration pattern.
2. **Every migration is an explicit, versioned transformation function**, not an ad-hoc script run once and
   forgotten — consistent with `versioning.md`'s rule that every entity family has a defined versioning
   strategy.
3. **Rollback = stop reading the new version**, not "undo a destructive change" — because nothing destructive
   ever happened.
4. **Validation is mandatory**: row-count checks, content-hash verification, provenance-chain spot-checks.
5. **No migration is executed in Step 2** — this project has no chosen database technology yet
   (`open-decisions.md` #7), so no concrete migration tooling exists. This document (and `migrations.md`)
   define the DISCIPLINE that whatever tooling is eventually chosen must implement.

## Known future migrations already anticipated by this project's own open decisions

| Anticipated migration | Triggered by resolving | Where it's detailed |
|---|---|---|
| Lead-entity schema consolidation (SCHEMA-002/003 → chosen canonical) | `open-decisions.md` #2 | `migrations.md`'s worked example |
| Client-archetype canonicalization (3 source sets → chosen union or single set) | `open-decisions.md` #4 | `entity-catalog.md`'s Client Domain section |
| Two-axis classification field addition (`manufacturing_domain` alongside `client_archetype`) | `open-decisions.md` #5, ADR-0003 | `entity-catalog.md`'s Lead Domain section |
| Drift-formula field completion (once FORMULA-002 is resolved) | `open-decisions.md` #15 | `entity-catalog.md`'s Formula Model section |

None of these are executed now. They are recorded here so that when the corresponding open decision is
resolved, the migration work is already scoped and doesn't require re-deriving what changed and why.

See `migrations.md` for full detail.
