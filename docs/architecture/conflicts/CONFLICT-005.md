# CONFLICT-005 — Composition Breakdown Introduces Buyer-Intent Categories Absent From Every Client-Archetype List

## Source A
- **Source IDs:** SRC-000029, SRC-000025, SRC-000034 (the 3 archetype-enumeration passes; see CONFLICT-004)
- **Pages:** 7, 9, 11-12
- **Exact relevant statement:** All 3 archetype passes describe client TYPES (who the buyer is: an innovator,
  a middleman, an SME, etc.).
- **Interpretation:** A "buyer archetype" axis — classifying leads by WHO is asking.

## Source B
- **Source IDs:** SRC-000052
- **Pages:** 19
- **Exact relevant statement:** "Composition of the Firehose" breakdown: 60% E-Commerce/Middleman
  Customization, 20% Component & Part Sourcing (Build-to-Print), 12% Tooling & Injection Mold Fabrication, 5%
  PCB & Electronics Assembly, 3% True Turnkey NPD.
- **Interpretation:** A "request type" axis — classifying leads by WHAT is being asked for. "Component & Part
  Sourcing" and "Tooling & Injection Mold Fabrication" do not correspond to any named client archetype from
  Source A, and "Institutional/Government" is entirely absent from this breakdown despite being present in 2
  of the 3 archetype passes.

## Why they may differ
These may simply be two different, legitimately independent classification dimensions (buyer archetype vs.
request type) that the source conflates by presenting Source B immediately after and in apparent continuity
with archetype-related discussion, without ever explicitly stating "this is a second, separate axis."

## Technical implications
If Source B's percentages are naively mapped onto Source A's archetype enum, 32% of the described volume
(20% + 12%) has no valid archetype value to be recorded against.

## Data-model implications
Suggests the canonical data model needs (at minimum) two logically separate classification fields on a lead
record — `client_archetype` (who) and something like `request_type`/`manufacturing_domain` (what) — rather
than forcing one enum to carry both meanings. Note: `ManufacturingDomain` (SCHEMA-001, SRC-000011) already
exists in the source for the "what" axis and may already substantially cover this gap — Component & Part
Sourcing and Tooling & Injection Mold Fabrication map reasonably well onto existing `ManufacturingDomain`
values (`FULL_NPD_TURNKEY`-adjacent and `DFM_INJECTION_MOLDING` respectively) — but the source never
explicitly draws this connection either.

## Architecture implications
`docs/architecture/client-intelligence-model.md` and `docs/architecture/data-domains.md` should model
"buyer archetype" and "manufacturing/request domain" as related-but-distinct dimensions of a lead record.

## Operational implications
None directly — this is a data-modeling conflict, not an operational one.

## Economic implications
The 60/20/12/5/3% composition figures (SCENARIO-003) cannot be cleanly cross-tabulated against archetype-based
economic scenarios elsewhere (e.g., archetype-specific strategic angles from page 9) without this two-axis
reconciliation.

## Possible resolutions
1. Formally model 2 separate classification dimensions (buyer archetype × manufacturing/request domain) and
   treat the page-19 composition percentages as a distribution over the SECOND dimension, not the first.
2. Treat the page-19 composition as an approximate, informal restatement of buyer archetypes using different
   words, and attempt a lossy mapping (NOT RECOMMENDED — would require inventing a correspondence the source
   doesn't state).

## Recommended decision
Option 1. This is architecturally the cleaner and more defensible reading, and it reuses an already-existing
source concept (`ManufacturingDomain`) rather than inventing a new one from scratch — closer to
`INTERPRETATION` than `PROPOSED_EXTENSION` in the source-vs-canonical taxonomy.

## Decision status
**DECISION_STATUS = NEEDS_USER_DECISION** on whether this two-axis reading matches the user's actual mental
model, though it is architecturally recommended as the default working assumption for Step 2+.
