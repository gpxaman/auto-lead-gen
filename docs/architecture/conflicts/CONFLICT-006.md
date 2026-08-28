# CONFLICT-006 — Layer-1 LLM Qualification Rate: 1.5% vs. ~2%

## Source A
- **Source IDs:** SRC-000047 (TABLE-007/008 in Step 0)
- **Pages:** 17, 18
- **Exact relevant statement:** "Top 1.5% pass IECHM capability thresholds," applied directly to the full raw
  450,000/month pool (the CONFLICT-001 Source-A/15,000-per-day basis), yielding 6,750 MQL/month.
- **Interpretation:** A qualification rate measured against the FULL raw lead pool, with no intermediate
  deterministic filtering stage (Layer 0 did not exist yet in the document's timeline at this point).

## Source B
- **Source IDs:** SRC-000053, SRC-000074
- **Pages:** 20, 27
- **Exact relevant statement:** "Layer 1 ... passes the top 2% (2,000 leads)" out of the POST-Layer-0 pool of
  100,000 leads (itself only 5% of the 2,000,000/day raw pool); restated on page 27 as "Identifies Top 2% - 5%
  Qualified -> 2,000 - 5,000 Bids."
- **Interpretation:** A qualification rate measured against an ALREADY-FILTERED pool (post-Layer-0), not the
  full raw intake.

## Why they may differ
These may not actually be in numerical conflict at all — they could be measuring genuinely different things
(1.5% of ALL raw leads vs. 2% of an already-95%-reduced pool), in which case they are not contradictory
figures so much as differently-scoped figures that superficially look similar because both are phrased as
"top X% qualified." However, the source never explicitly clarifies this distinction, so a reader could easily
(and incorrectly) treat them as the same rate measured twice with slightly different results.

## Technical implications
If Layer 1's qualification logic is implemented using "1.5%" as a target selectivity against the FULL raw
pool (skipping Layer 0's 95% reduction), the resulting absolute lead counts differ by roughly an order of
magnitude from a Layer-1-after-Layer-0 implementation using "2%" against the reduced pool. This is not a
cosmetic difference — it directly determines downstream bid volume.

## Data-model implications
Suggests the qualification-rate CONFIGURATION needs to explicitly record which pool (raw vs. post-Layer-0) a
given percentage threshold is measured against, to avoid silently conflating the two in a future
implementation.

## Architecture implications
`docs/architecture/dynamic-worker-scaling.md` and `docs/architecture/data-flow.md` must clearly label each
filtering stage's input pool, and any qualification-rate configuration value must be paired with an explicit
statement of which stage/pool it applies to.

## Operational implications
Could materially affect projected downstream bid volume and thus (indirectly) cost and revenue projections if
conflated.

## Economic implications
Feeds into SCENARIO-002 (1.5%-basis) vs. SCENARIO-003/onward (2%-basis) in `economic-scenarios.md` — these are
not directly comparable without knowing which pool each percentage was measured against.

## Possible resolutions
1. Treat both figures as valid but scoped to different pipeline stages (1.5% of raw ≈ roughly consistent order
   of magnitude with 2% of post-Layer-0-reduced-pool, given Layer 0 itself removes ~95%) — i.e., they may be
   loosely mutually consistent once pool-scoping is made explicit, rather than truly conflicting.
2. Treat them as simply two independent, unreconciled estimates and pick one as a starting configuration
   default, to be tuned empirically once real data exists.

## Recommended decision
Resolution 1 — recording BOTH percentages with their correct pool-scope in the canonical qualification-rate
configuration schema (rather than picking one), since this is architecturally cheap to do and preserves both
without forcing a false single answer.

## Decision status
**DECISION_STATUS = NEEDS_USER_DECISION** is not strictly required here since resolution 1 does not force a
choice between the two — but the user should be aware that neither percentage has been empirically validated
against real platform data, and both remain `SOURCE_ESTIMATE`, not measured facts.
