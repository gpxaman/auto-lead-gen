# ADR-0004 — Preserve All Lead-Entity Schema Versions; Never Silently Merge

**Status:** ACCEPTED
**Source IDs:** SRC-000032, SRC-000040, SRC-000080 (SCHEMA-002/003/005)
**Requirements:** REQ-000014

## Context
Three non-identical versions of the "unified lead entity" concept exist in the source (CONFLICT-003), with
materially different field structures and enum vocabularies. No version is declared canonical by the source.

## Decision
All schema versions are preserved as distinct, queryable historical records (`schema-versioning.md`). Any
future migration is modeled explicitly as `OLD DATA → VERSIONED TRANSFORMATION → NEW DATA`, never an in-place
overwrite. This ADR accepts the PROCESS discipline (versioning, non-destructive migration) without accepting
WHICH version becomes canonical (that remains `NEEDS_USER_DECISION`, tracked separately in CONFLICT-003 and
`open-decisions.md`).

## Alternatives considered
1. Pick the latest draft (SCHEMA-005/v2) as canonical immediately and discard v1 — rejected per the explicit
   "do not silently resolve conflicts" rule; this would be choosing "the later version" exactly as Step 1
   Section 4 forbids doing without justification beyond recency.
2. Attempt to auto-merge v1 and v2 into a superset schema — rejected; the `runtime_governance` (v1) vs.
   `security_analysis` (v2) fields are NOT the same concept despite similar schema position (`schema-
   versioning.md`), so a naive merge would conflate two different meanings under one field name.

## Consequences
Every future document referencing "the lead schema" must specify which version, or explicitly state it is
schema-version-agnostic. Database implementation (a future step) must support versioned records from day one.

## Reversibility
Low-cost to maintain going forward; expensive to retrofit if skipped now and versions get silently merged
before this discipline is established.
