# CONFLICT-004 — Client Archetype Count and Naming Drift Across 3 Enumeration Passes

## Source A
- **Source IDs:** SRC-000029
- **Pages:** 9
- **Exact relevant statement:** Narrative form, 3 archetypes: "Archetype A: The NPD Innovator / Deep-Tech
  Startup," "Archetype B: The E-Commerce Brand / Middleman / Sourcing Arbitrageur," "Archetype C: The
  Overburdened SME / Mid-Market Engineering Team." No Crowdfunder or Institutional archetype present.
- **Interpretation:** Part of the "IECHM Global Lead Source & Strategic Acquisition Blueprint" — produced
  under the user's explicit "data alone... blueprint, not the agent" scope constraint (page 8).

## Source B
- **Source IDs:** SRC-000025 (page 7), SRC-000034 (pages 11-12)
- **Pages:** 7, 11, 12
- **Exact relevant statement:** Two SEPARATE list-form enumerations, each with 5 archetypes (adding "Funded
  Crowdfunders & Product Launchers" and "Government/Defense/Institutional Contractors" to the 3 from Source
  A), but the two 5-item lists use different wording per item and are themselves not verbatim-identical to
  each other, and both are truncated mid-sentence in the original PDF render.
- **Interpretation:** Both are AI-generated SYSTEM PROMPT drafts meant to be fed to another LLM instance,
  produced independently of the page-9 blueprint (one before it chronologically, page 7; one after, pages
  11-12).

## Why they may differ
The 3-archetype version may be a deliberately simplified subset chosen for a narrative blueprint document,
while the 5-archetype versions may represent "the complete" taxonomy meant for machine-consumable system
prompts — but the source never states this explicitly. It is equally possible the 3-archetype version is
simply an earlier, less complete pass that the AI didn't bother reconciling with the later, more complete
5-archetype lists once those existed.

## Technical implications
Any code that needs to enumerate "all client archetypes" needs an explicit decision about which list (or a
merged superset) is authoritative, since a naive implementation might miss Crowdfunder/Institutional entirely
if built from Source A alone.

## Data-model implications
Directly feeds `docs/architecture/client-intelligence-model.md`'s design of a hierarchy that can hold multiple
non-identical archetype SETS without pretending they are the same enumeration.

## Architecture implications
The Client Intelligence subsystem (`docs/architecture/subsystems.md` #7) must be built against a
canonical archetype list that is explicitly Step-1-authored (deriving from the union of all 3 source passes)
rather than blindly implementing whichever list was read first.

## Operational implications
Per-archetype strategic-angle guidance (Section 9's Archetype A/B/C strategic angles) exists ONLY for the
3-archetype version — the two 5-archetype list versions were truncated before their strategic-angle
guidance (if any) could be captured in the source. This means Crowdfunder and Institutional archetypes
currently have NO source-derived strategic-angle guidance at all, only a one-line profile description.

## Economic implications
None directly.

## Possible resolutions
1. Adopt the union of all 3 passes (5 archetypes total: NPD Innovator, Middleman/Reseller, SME, Crowdfunder,
   Institutional) as the canonical archetype set, explicitly noting that only the first 3 have source-derived
   strategic-angle guidance and the last 2 need that guidance authored fresh (as a `PROPOSED_EXTENSION`).
2. Treat the 3-archetype version as canonical (since it's the only one with full/untruncated per-archetype
   detail) and treat Crowdfunder/Institutional as lower-priority future additions.
3. Ask the user to confirm the final archetype list and provide strategic-angle guidance for the two
   under-specified archetypes.

## Recommended decision
Option 1 for the canonical LIST (don't drop real buyer types the user clearly cared about — they appear in 2
of 3 passes), combined with explicitly flagging the strategic-angle gap for Crowdfunder/Institutional rather
than inventing guidance to fill it.

## Decision status
**DECISION_STATUS = NEEDS_USER_DECISION** on whether to proceed with authoring new strategic-angle guidance
for Crowdfunder/Institutional archetypes (a `PROPOSED_EXTENSION`) or wait for the user to provide it.
