# CONFLICT-002 — Master Prompt Ingestion Basis Not Reconciled With Its Own Agent/Cost Model

## Source A
- **Source IDs:** SRC-000073, SRC-000074 (and by extension SRC-000043/044/045)
- **Pages:** 25, 27
- **Exact relevant statement:** Master Prompt v1/v2 explicitly states "~1.5 to 2.5 million signals per day" as
  the system's stated ingestion basis (consistent with CONFLICT-001's Source B).
- **Interpretation:** The FINAL, most-polished architecture draft in the entire source document commits to
  the large-volume figure as the operative design basis.

## Source B
- **Source IDs:** SRC-000043, SRC-000044, SRC-000045 (TABLE-004, TABLE-005, TABLE-006 in Step 0)
- **Pages:** 15, 16, 17
- **Exact relevant statement:** The 140-195 total agent count, the ~$3,500/month cost figure, and the full
  token-burn model were all computed against the 15,000/day basis and are never recomputed anywhere in the
  source after the volume was revised upward by roughly 100-170x.
- **Interpretation:** The document's own headline "full-scale" sizing numbers (repeatedly cited by the user in
  follow-up questions, e.g. page 17-18's "$1,000 floor" profitability question) are stale relative to the
  document's own final stated ingestion basis.

## Why they may differ
This is not really a disagreement between two independent claims in the source — it is an internal
consistency gap. The user never asked "given the new 1.5-2.5M figure, how many agents/what cost now?" so the
AI never recomputed it. The 140-195 agent count and $3,500/month figure keep getting reused informally in
later economic scenarios (e.g., page 17's profitability scenario) without being flagged as potentially
outdated once the ingestion-volume premise changed on page 19-20.

## Technical implications
Layer 0 (the deterministic pre-filter) is specifically the source's own proposed answer to "how do you afford
to process millions of leads/day" (page 20) — meaning the ORIGINAL 140-195-agent/$3,500-month figure was
computed for a WORLD WITHOUT Layer 0. Any architecture that adopts both the large-volume figure AND Layer 0
needs a fresh agent-count/cost projection; reusing the old numbers would be internally inconsistent with the
source's own later design.

## Data-model implications
None directly — this is a sizing/economics conflict, not a schema conflict.

## Architecture implications
`docs/architecture/scaling-scenarios.md` must NOT present the 140-195 agent / $3,500/month figures as valid
for the large-volume + Layer 0 configuration. They are preserved as a distinct, smaller-scale scenario (tied
to CONFLICT-001's Source A) rather than silently carried forward as "the" cost model for the full system.

## Operational implications
Any real budget planning based on the source's headline "~$3,500/month" figure would be materially wrong if
the system is actually built to ingest 1.5-2.5M leads/day with 75+ platform connectors and a Layer 0 filter —
none of which existed in the world the $3,500/month figure was computed for.

## Economic implications
Every profitability scenario in `docs/source-extraction/economic-scenarios.md` that cites the $3,500/month
cost figure alongside revenue projections built on the larger lead-volume/composition figures (pages 19-25)
is internally inconsistent in the same way. This affects SCENARIO-004 through SCENARIO-008, all of which use
the $3,500/month-derived "operating cost" as a given without re-deriving it.

## Possible resolutions
1. Explicitly mark all pre-page-19 cost/agent-count figures as scoped to the Source-A (15,000/day) scenario
   only, and require any full-firehose-scale economic model to be treated as UNCOSTED pending a fresh
   projection (which is out of scope for architecture-only Step 1).
2. Produce a fresh, Step-1-native rough-order-of-magnitude estimate for the large-volume + Layer 0 case. This
   would be a `PROPOSED_EXTENSION`, not a source-derived figure, and would need to be clearly labeled as such
   if produced.

## Recommended decision
Resolution 1 for Step 1 (do not fabricate a new cost estimate under an architecture-only step); resolution 2
could be revisited in a later step focused on capacity planning, explicitly as new work product, not as a
source-derived number.

## Decision status
**DECISION_STATUS = NEEDS_USER_DECISION** on whether a fresh cost/sizing model is wanted at all before further
implementation planning, given that the source's own numbers cannot be trusted for the full-scale
configuration.
