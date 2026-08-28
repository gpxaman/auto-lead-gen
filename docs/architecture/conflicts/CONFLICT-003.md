# CONFLICT-003 — Two Non-Identical Lead Entity / Telemetry Schema Versions

## Source A
- **Source IDs:** SRC-000040, SRC-000041 (SCHEMA-003, SCHEMA-004 in Step 0's `json-schemas.md`)
- **Pages:** 14, 15
- **Exact relevant statement:** Unified Lead Entity Data Schema v1 — nested `layer_origin.client_archetype`
  with values `NPD_Innovator | Middleman_Reseller | Enterprise_SME | Crowdfunder | Institutional`. Telemetry
  event named `FAILOVER_HOTSWAP_TRIGGERED`, flat structure.
- **Interpretation:** Produced in "System Prompt Draft 3" (Autonomous Self-Healing Multi-Agent Lead &
  Intelligence Infrastructure), in direct response to the user's cascading-updates/hallucination-sentinel
  requirement (page 13).

## Source B
- **Source IDs:** SRC-000080, SRC-000082 (SCHEMA-005, SCHEMA-006)
- **Pages:** 29
- **Exact relevant statement:** Unified Lead Entity Schema v2, a formal JSON Schema draft-07 document — flat
  top-level `client_archetype` with DIFFERENT values `NPD_INNOVATOR | MIDDLEMAN_OEM_RESIGN |
  SME_ENGINEERING_OVERFLOW | CROWDFUNDER_FUNDED | GOVERNMEN[truncated]`. Telemetry event RENAMED
  `FAILOVER_HOTSWAP_DISPATCHED`, restructured into `anomaly_report`/`failover_execution` sub-objects.
- **Interpretation:** Produced in Master Prompt v2 / IECHM-OS, the final and most polished draft, in response
  to "make this prompt much more comprehensive and add more info" (page 26).

## Why they may differ
v2 is later and more polished, and the user's request that produced it ("more comprehensive... add more
info") did not explicitly ask for a schema redesign — so the field renaming (`layer_origin.client_archetype`
→ top-level `client_archetype`; SCREAMING_SNAKE_CASE value changes; event name change) reads as incidental
drift across independently-generated drafts rather than a deliberate, announced migration. Also notably,
`MIDDLEMAN_OEM_RESIGN` appears to contain a typo (likely intended as something like `MIDDLEMAN_OEM_RESELL` or
similar) — preserved verbatim per the no-silent-correction rule.

## Technical implications
A system built directly against either schema in isolation would be incompatible with data produced against
the other. Any code or documentation elsewhere in a future implementation that assumes "the" lead schema
without specifying v1 or v2 is itself ambiguous.

## Data-model implications
This is the central conflict driving `docs/architecture/schema-versioning.md`: the canonical architecture
must treat v1 and v2 as genuinely different schema VERSIONS in a formal versioning sense (not variants of the
same thing to be merged), with any future migration modeled explicitly as `OLD DATA → VERSIONED
TRANSFORMATION → NEW DATA`, never a silent overwrite.

## Architecture implications
The canonical `UnifiedLeadEntity` concept in `docs/architecture/data-domains.md` and
`docs/architecture/canonical-architecture.md` must be versioned from the start, not merged into one
"true" shape.

## Operational implications
None yet (no implementation exists), but this conflict must be resolved (or explicitly deferred with a
versioning strategy) before any database schema work begins in a future step.

## Economic implications
None directly.

## Possible resolutions
1. Adopt v2 (the latest, most polished draft) as the CURRENT canonical schema going forward, while
   preserving v1 as a recorded historical schema version (not deleted, not silently merged).
2. Design a NEW v3 canonical schema in Step 1/2 that reconciles the two, explicitly derived as a
   `PROPOSED_EXTENSION` rather than presented as if the source settled on it.
3. Ask the user which enum vocabulary they actually prefer, since neither v1 nor v2's naming was ever
   reviewed/confirmed by the user in the source conversation (both were AI-generated in response to open
   requests, not dictated field-by-field by the user).

## Recommended decision
Option 1 is the lowest-risk default (most-recent-draft-as-current is a defensible convention for
AI-brainstormed material with no other signal), paired with explicit historical-version preservation per
`docs/architecture/schema-versioning.md`. This is a RECOMMENDATION only — Step 1 does not adopt it as final.

## Decision status
**DECISION_STATUS = NEEDS_USER_DECISION** — the user should confirm whether v2's specific field names/enum
values are actually what they want, since neither schema version was ever explicitly reviewed by the user
line-by-line in the original conversation.
