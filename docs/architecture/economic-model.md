# Economic Architecture

Per Step 1 Section 29. Preserves ALL source economic scenarios distinctly. No single scenario is selected as
"the" economic model.

## All scenarios represented separately (full detail in `docs/source-extraction/economic-scenarios.md`)

| Scenario | Raw volume basis | Filter rate | Qualified leads | Bid volume | Win/close rate | AOV | Revenue | Margin | Agent cost | Infra cost | Profit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SCENARIO-001 (base cost/agent projection) | 15,000/day | — | — | — | — | — | — | — | ~$2,243/mo LLM | ~$1,250/mo | (cost only, no revenue) |
| SCENARIO-002 ($1,000 floor) | 15,000/day (450,000/mo) | 1.5% | 6,750/mo | 337/mo | 15% resp / 20% close | $1,000 (or $3,500 restated) | $10,000/mo (or $35,000) | n/a | $3,500/mo total | (included above) | $6,500/mo (or $31,500/mo) |
| SCENARIO-003 (firehose revision) | 1.5M-2.5M/day | 95% Layer-0 drop, then ~2% | 2,000/day | 2,000/day | — | — | — | — | **not re-derived** (CONFLICT-002) | **not re-derived** | — |
| SCENARIO-004 (category killer) | 2M/day (implied) | (Layer 0 + Layer 1) | 2,000/day | 2,000/day | 30% resp / 40% close | $2,000 | $480,000/day | 12% | — | — | $57,600/day |
| SCENARIO-005 (universal printer) | 2M/day (implied) | (Layer 0 + Layer 1) | 2,000/day | 2,000/day | 50% resp / 80% close | $1,500 | $1,200,000/day | ~80-90% | ~$250/order | — | $1,000,000/day |
| SCENARIO-006 (10% discount rule) | 2M/day (implied) | (Layer 0 + Layer 1) | 2,000/day | 2,000/day | 30% resp / 35% close | $4,500 | $945,000/day | 93.3% | ~$300/order | — | $882,000/day (~$26.46M/mo) |
| SCENARIO-007 (conversion scaling) | scales 1,000→5,000 bids/day | — | — | 1,000-5,000/day | 25-45% resp / 30-50% close | $4,500 | $337,500-$6,187,500/day | — | — | — | — |
| SCENARIO-008 (flywheel/moat) | — | — | — | — | — | — | — | — | — | — | "700,000 bids processed," uncited derivation |

Every cell above retains its scenario and source-page context (see `economic-scenarios.md` for full citations)
— nothing here is presented as a blended or averaged "typical" figure.

## Explicit non-selection

Per Step 1 Section 29: "Do not select a single scenario. Represent each scenario separately." No scenario is
recommended as more likely, more realistic, or more useful than another in this document. Where earlier Step
0/1 documents (e.g., `scaling-scenarios.md`) make an ARCHITECTURAL recommendation about which SCALE PROFILE to
build toward first, that is a separate question from which ECONOMIC scenario is "true" — economic outcomes
depend on real-world conversion behavior that has never been measured.

## Why none of these are production guarantees

Every scenario in this table is `SOURCE_ESTIMATE` per Step 0's `ASSUMPTION-006`. None rests on a real
backtest, pilot, or measured conversion funnel — all are AI-generated illustrative arithmetic in response to
hypothetical "what if" questions, several explicitly contingent on the unverified Universal 3D Printer
hardware assumption (SCENARIO-005/006). Treating any of these numbers as a budget or revenue target would be
a misuse of this document.

## Relationship to `scaling-scenarios.md`

`scaling-scenarios.md` organizes the same underlying source material around TECHNICAL scale profiles
(`freelance-narrow` / `full-firehose`); this document organizes it around ECONOMIC scenario progression. Both
draw from the same source data and are cross-consistent (SCENARIO-001/002 correspond to `freelance-narrow`;
SCENARIO-003 onward correspond to `full-firehose`) but serve different analytical purposes.

## Out-of-scope note

Every dollar figure in this table originates from System B (bidding/pricing) or System C (manufacturing)
economics, per `system-boundaries.md` — IECHM-LIOS itself has no revenue model of its own; it is a cost
center (recon/intelligence infrastructure) whose OUTPUT feeds System B's revenue-generating activity. This
document preserves the full economic picture for context/traceability, not because IECHM-LIOS implements any
of this pricing/revenue logic itself.
