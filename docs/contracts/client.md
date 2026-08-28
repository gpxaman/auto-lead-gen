# Contract: Client

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved. **Does NOT canonicalize the
client-archetype set — see CONFLICT-004 / `open-decisions.md` #4.**

## Purpose
Represents a buyer entity and its archetype classification(s), across all 3 preserved source enumerations.

## Source references
SRC-000029 (Set A, 3 archetypes), SRC-000025 (Set B, 5 archetypes, page 7), SRC-000034 (Set C, 5 archetypes,
pages 11-12). See `docs/architecture/client-intelligence-model.md`.

## Requirement references
REQ-000013, REQ-000016.

## Fields

| Field | Required? | Tag | Notes |
|---|---|---|---|
| `client_id` | required | `PROPOSED_SCHEMA` | no source equivalent — the source never names client-identity resolution as distinct from the lead |
| `client_archetype_set` | required (per classification) | `DERIVED_CANONICAL_SCHEMA` | `SOURCE_SET_A` \| `SOURCE_SET_B` \| `SOURCE_SET_C` (open enum) |
| `client_archetype_value` | required (per classification) | `SOURCE_SCHEMA` | the specific value WITHIN the declared set — e.g. Set A's "NPD Innovator / Deep-Tech Startup," verbatim |
| `buyer_persona` | optional | `SOURCE_SCHEMA` (Set A only) | e.g. "Early-stage founders, patent holders..." — absent for Sets B/C (truncated in source) |
| `buying_motivation` | optional | `SOURCE_SCHEMA` (Set A only) | "core driver": Feasibility / Unit Margin (page 9 diagram) |
| `pain_point` | optional | `SOURCE_SCHEMA` (Set A only) | "Primary Bottleneck" |
| `buying_signal` | optional | `SOURCE_SCHEMA` | TABLE-003 "Technical Indicators," tied to platform not strictly to archetype |
| `classification_claim_id` | required | `DERIVED_CANONICAL_SCHEMA` | points to the `claim` record establishing trust for this archetype assignment |

## Validation rules
A `client` may simultaneously hold classification claims under MULTIPLE archetype sets (Set A AND Set B, e.g.)
— these are not mutually exclusive (per Step 2 Section 7's explicit non-merge instruction). `client_archetype_value`
must be a value that literally exists within the declared `client_archetype_set`'s source enumeration — no
invented archetype values.

## Provenance
`classification_claim_id` → `claim` → full provenance chain (model/prompt/evidence) per `docs/database/provenance.md`.

## Versioning & compatibility
New archetype sets (e.g., a future user-approved canonical union) may be ADDED to the open
`client_archetype_set` enum; existing sets A/B/C are never removed.

## Security classification
`CONFIDENTIAL`.

## Examples
None fabricated. The archetype VALUES themselves (Set A's 3, Sets B/C's 5 each) are preserved verbatim in
`docs/source-extraction/client-archetypes.md` and cited by reference, not duplicated as a "client record"
example (the source never shows one).
