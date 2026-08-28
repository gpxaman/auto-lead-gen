# Extracted Numbers / Numeric Scenarios Index

This file indexes every distinct numeric scenario or standalone quantitative claim in the source and points
to its full derivation. Formulas are in `formulas.md`; full economic scenarios are in `economic-scenarios.md`;
tables are in `tables.md`; thresholds are in `thresholds.md`. This file exists as a flat cross-reference so
no number is left un-indexed.

## Platform/source counts
- 10-15 viable NPD/hardware freelance platforms (page 4)
- ~30 total incl. dead/regional/general boards (page 4)
- 50-75 high-yield platforms across 4 lead-source types (page 5)
- 100+ active sources across 8 categories incl. brokers/tenders/crowdfunding (page 6)
- ~75 platforms used as the Layer 3 agent-count basis (pages 15, 16, 26, 27)
- 15-20 traditional freelance boards (TABLE-002, page 7)
- 20-25 B2B sourcing & trade sources (TABLE-002, page 7)
- 10-15 on-demand mfg network sources (TABLE-002, page 7)
- 15-20 NPD/agency broker sources (TABLE-002, page 7)
- 10-15 public sector/defense tender sources (TABLE-002, page 7)

## Agent counts — see agents.md / TABLE-004
- 140-195 total agents at full scale
- 3 / 12 / 75 / 30-50 / 20-55 per layer (see TABLE-004)
- 2-3 agents for Client Classification Swarm (page 12)

## Lead volume figures (CONFLICTING — see conflicts.md CONFLICT-001)
- 15,000 raw leads/signals per day (pages 16, 17, 18) — basis for SCENARIO-001/002
- 450,000 raw leads/month (= 15,000 × 30) (pages 17, 18, 19)
- 1.5 million to 2.5 million raw signals per day (pages 19, 20, 25, 27) — basis for SCENARIO-003 onward
- ~2,000,000/day used as the round-number working figure in Layer 0 math (pages 20, 27)
- IndiaMART: "10 crore (100 million) buyer enquiries every month" ≈ 3.3 million/day (page 19, cited as scale reference, not IECHM's own volume)
- 15%-20% of global trade volume estimated as "discrete physical manufacturing and hardware sectors" (page 19)

## Funnel/qualification percentages
- 1.5% qualification rate, Sanitizer discards 98.5% (page 17-18, TABLE-007/008)
- ~2% pass Layer 1 of the post-Layer-0 pool (page 20, 27) — note: differs numerically from the 1.5% above; both preserved
- 5% of qualified leads receive bids (page 18, TABLE-008)
- 15% client response rate, $1,000-floor scenario (page 17-18)
- 20% final conversion/close rate, $1,000-floor scenario (page 17-18)
- 95% of raw volume dropped by Layer 0 (page 20, 27)

## Token / cost figures — see formulas.md FORMULA-003, tables.md TABLE-005/006
- 2,500 input tokens / 300 output tokens per lead (page 16)
- 30% sentinel overhead multiplier (page 16)
- ~48.7M input / ~5.8M output tokens per day (page 16)
- ~1.46B input / ~175M output tokens per month (pages 16, 17)
- 80% volume → cheap models ($0.15/1M in, $0.60/1M out) (page 16)
- 20% volume → heavy models ($5.00/1M in, $15.00/1M out) (page 16)
- Total LLM cost ~$2,243/month (page 16)
- Infrastructure: proxies/stealth browsers $800-1,200/mo, vector DB ~$100/mo, serverless compute ~$150/mo → ~$1,250/mo total (page 16)
- Total operating cost ~$3,500/month (pages 16, 17)

## Revenue/profit figures — see economic-scenarios.md SCENARIO-001 through 008
- $6,500/month net profit at $1,000 AOV / 10 deals (page 17) — "185% ROI"
- $31,500/month net profit at $3,500 AOV / 10 deals (page 18) — "900% ROI"
- $480,000/day gross sales, $57,600/day gross profit, 12% margin, "category killer" scenario (page 20)
- $1,200,000/day gross revenue, $1,000,000/day gross profit, universal-printer scenario (pages 21-22)
- $945,000/day gross revenue, $63,000/day cost, $882,000/day gross profit, 10%-discount scenario (page 22)
- ~$28.35M/month gross sales, ~$26.46M/month gross profit, 10%-discount scenario monthly run-rate (page 22)
- Up to $6,187,500/day revenue at "Phase 4: Global Maximum" (1,375 deals/day @ $4,500 AOV) (page 25, TABLE-011)

## Physical/material figures
- Aluminum price: ~$3.15/kg (~₹345/kg on MCX), August 2026 (page 21)
- Electricity: $0.12/kWh (implied only, inside FORMULA-001, page 27; not independently stated elsewhere)
- Universal printer build envelope: 2000mm × 1000mm × 1000mm (2m × 1m × 1m) (pages 21, 26, 27)
- Universal printer power draw: under 5kW average (pages 21, 26)
- Example: 100 × 1kg parts = $315 aluminum cost (page 21)
- Traditional-market comparison: $8,000 CNC setup + $40/unit × 100 = $12,000 for 100 laptop enclosures, vs. IECHM bid of $2,500 (page 21)

## Pricing rule figures — see formulas.md FORMULA-001, thresholds.md THRESH-007/008
- P_bid = 0.90 × P_market (exact 10% discount) (pages 22, 25, 27, 29)
- Maximum allowable discount: >20% off is forbidden (page 27)
- Gross margin under 10% rule: ~85%-94% (page 27); point figure 93.3% (page 22, TABLE-009)

## Conversion-lever figures — see strategies.md, tables.md TABLE-011
- Bid volume: 2,000 → 5,000/day (2.5x) (page 24)
- Response rate: 30% → 45% via "Instant Proof" (page 24)
- Close rate: 35% → 50% via "Instant Proof" (page 24)
- Repeat orders: 30%-50% of daily closed orders after 90 days (page 24)
- Sub-60-second response latency → ~35% higher response rate vs. 10-minute bidding (page 25)
- Tolerance guarantee: ±0.05mm (page 25)
- Day-25 post-delivery re-order trigger (pages 25, 28)
- 4-hour quote-response window → 35% higher close rate if met (page 20, cited benchmark)

## Sentinel / reliability thresholds — see thresholds.md THRESH-004/005/006
- Drift score threshold: D_t ≥ 0.85 (pages 26, 28)
- Consecutive failure threshold: ≥3 (pages 14, 15, 26, 28)
- Saturation threshold: ≥99.5% consistency over 72 hours (pages 14, 28)
- Sub-agent spawn threshold: >5 leads/day (pages 11, 12, 14, 17, 26, 27)
- Sub-agent deprecation threshold: <2 leads/day over 7-day rolling average (pages 12, 14, 26)

## Compounding/flywheel narrative figure
- "700,000 successful bids" processed after one year, used as a competitive-moat argument (page 23) — not derived from any stated daily/monthly rate elsewhere in the document (2,000 bids/day × 365 days would be 730,000, which is close but not stated as the derivation).
