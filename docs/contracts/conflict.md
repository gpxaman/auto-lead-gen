# Contract: Conflict

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
First-class data representation of unresolved (or resolved) conflicts — both source-level (the 7
CONFLICT-00N records) and, in the future, potential runtime data conflicts (e.g., two Sentinels disagreeing).

## Source references
`docs/requirements/conflicts.md`, `docs/architecture/conflicts/CONFLICT-001.md` through `CONFLICT-007.md`.

## Requirement references
None directly (conflicts are a governance/traceability construct, not a functional requirement) — supports
REQ-000014 (schema conflict), REQ-000013 (archetype conflict) indirectly.

## Fields

### `conflict`
| Field | Required? | Tag | Notes |
|---|---|---|---|
| `conflict_id` | required | `SOURCE_SCHEMA` | e.g. `CONFLICT-001` through `CONFLICT-007`, preserved exactly for the seed set |
| `subject` | required | `SOURCE_SCHEMA` | e.g. "Raw Daily Lead Volume: 15,000/day vs. 1.5M-2.5M/day" |
| `status` | required | `DERIVED_CANONICAL_SCHEMA` | `OPEN` \| `UNDER_REVIEW` \| `RESOLVED` \| `SUPERSEDED` \| `UNRESOLVED` (exact Step 2 Section 15 list) |
| `resolution` | optional | `PROPOSED_SCHEMA` | null for all 7 seed conflicts currently (`NEEDS_USER_DECISION`, except CONFLICT-007's `PARTIALLY RESOLVED BY IMPLICATION`) |
| `resolver` | optional | `PROPOSED_SCHEMA` | |
| `resolved_at` | optional | `PROPOSED_SCHEMA` | |

### `conflict_participant`
| Field | Required? | Notes |
|---|---|---|
| `participant_id` | required | |
| `conflict_id` | required | |
| `side` | required | `A` \| `B` |
| `source_id` or `claim_id` | required (exactly one) | source-level conflicts point to `source_item`; runtime conflicts point to `claim` |
| `context` | required | `SOURCE_SCHEMA` for the 7 seed conflicts (their `context_a`/`context_b` fields, preserved verbatim) |

### `conflict_version`
Only populated if a conflict's UNDERSTANDING changes (new evidence found for either side) — none of the 7
seed conflicts have a version 2 yet.

## Validation rules
**Neither side of a conflict is ever overwritten** (Step 2 Section 15, explicit) — resolving a conflict
transitions `status` and populates `resolution`/`resolver`/`resolved_at`, but both `conflict_participant`
rows remain exactly as recorded.

## Provenance
`source_id` → `source_item`, preserving the exact page/SRC-ID citation trail already established in
`docs/architecture/conflicts/CONFLICT-00N.md`.

## Versioning & compatibility
`conflict_version` for understanding changes; the conflict's core two-sided structure never collapses to one
side.

## Security classification
`INTERNAL`.

## Examples
The 7 seed conflicts (CONFLICT-001 through 007) are the concrete, real (non-synthetic) example data for this
contract — already fully specified in `docs/architecture/conflicts/`, cited here rather than duplicated.
