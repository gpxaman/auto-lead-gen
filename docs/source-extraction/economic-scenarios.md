# Extracted Economic Scenarios

Each scenario is numbered, with its trigger question, inputs, outputs, and source page(s). All are
SOURCE_ESTIMATE / illustrative AI-generated financial modeling in response to hypothetical user questions —
none are audited, verified, or presented in the source as guaranteed outcomes.

## SCENARIO-001 — Base-case agent/token/cost projection (source pages 15-17)
Trigger: "at the full scale how many agents ai will be there and how many tokens each consume and how much is
the cost"
Inputs: ~75 platforms, 15,000 raw leads/day, 140-195 agents, 2,500 input/300 output tokens per lead, 30%
sentinel overhead, 80/20 cheap/heavy model routing split.
Outputs: ~48.7M input tokens/day, ~5.8M output tokens/day; ~1.46B input / ~175M output tokens/month; LLM cost
~$2,243/mo; infrastructure ~$1,250/mo; **total ~$3,500/month**.

## SCENARIO-002 — $1,000-floor profitability (source pages 17-18)
Trigger: adds "assume each successful lead conversion earns 1000 dollar at the lowest is it profitable"
Inputs: SCENARIO-001 cost base ($3,500/mo); funnel: 450,000 raw leads/mo → 6,750 MQL (1.5%) → 337 bids (5%) →
50 responses (15%) → 10 closed deals (20%).
Outputs: break-even = 3.5 deals/mo; at 10 deals × $1,000 = $10,000 revenue, **$6,500/month net profit (stated
"185% ROI")**. Restated at $3,500 AOV: 10 deals × $3,500 = $35,000 revenue, **$31,500/month net profit
(stated "900% ROI")**.

## SCENARIO-003 — Scope-corrected firehose re-estimate (source pages 19-20)
Trigger: user challenges the 15,000/day figure as too narrow, demands middlemen/importers/all-manufacturing
scope.
Inputs: IndiaMART ~100M enquiries/month (~3.3M/day) cited as a scale reference; physical hardware/manufacturing
estimated at 15-20% of global trade volume.
Outputs: **Total Addressable Raw Firehose revised to 1.5M-2.5M raw signals/day** (supersedes-but-does-not-
delete SCENARIO-001's 15,000/day basis — see CONFLICT-001). Composition: 60% e-commerce/middleman
customization, 20% component/part sourcing, 12% tooling/injection mold fabrication, 5% PCB/electronics
assembly, 3% true turnkey NPD.
Layer 0 pre-filter funnel introduced: 2,000,000 → (95% dropped) → 100,000 → (top ~2%) → 2,000 qualified bids/day.

## SCENARIO-004 — "Category killer" cheapest-in-market daily P&L (source page 20)
Trigger: "assume the product is the most afforadble in the entire market while being top quality and then
free custom logo as well as changes"
Inputs: 2,000 bids/day, 30% response, 40% close, $2,000 AOV, 10-15% margin (12% used).
Outputs: 240 closed contracts/day; **$480,000/day gross sales; $57,600/day gross profit**. Physical
fulfillment bottleneck flagged (240 unique CNC/mold/PCB setups/day exceeds single-facility capacity within 48
hours) → recommends Aggregator Model pivot.

## SCENARIO-005 — Universal-printer hypothetical daily P&L (source pages 21-22)
Trigger: universal 3D printer hypothesis (ASSUMPTION-001) + "think about the actual profit and the metric."
Inputs: $3.15/kg aluminum, near-zero labor/tooling, 2,000 bids/day, 50% response, 80% close, $1,500 AOV,
~$250/contract cost.
Outputs: 800 closed contracts/day; **$1,200,000/day gross revenue; $1,000,000/day gross profit** ("$1 Million
in pure profit every single day"). Print-time physical throughput caveat stated (800 orders may require 800
hours of print time → needs a warehouse of printers running 24/7).

## SCENARIO-006 — 10%-below-market revised daily/monthly P&L (source page 22)
Trigger: "i dont want to go less than 10 percentage of the actual market prize" (pricing-rule constraint,
see FORMULA-001/THRESH-007).
Inputs: $5,000 traditional AOV → $4,500 IECHM AOV (10% discount); $300 estimated production cost/order; 2,000
bids/day, 30% response, 35% close.
Outputs: 210 closed contracts/day; **$945,000/day gross revenue; $63,000/day production cost; $882,000/day
gross profit**; **~$28.35M/month gross sales; ~$26.46M/month gross profit**. Per-order economics: $4,500 AOV,
~93.3% gross margin, ~$4,200 net profit/order (matches TABLE-009).

## SCENARIO-007 — Conversion-scaling growth-phase projection (source pages 24-25)
Trigger: "how much i an increase my lead conversation per day"
Inputs: three levers (bid-volume scale 2,000→5,000/day; conversion-rate lift via "Instant Proof" DFM/render
attachments, response 30%→45%, close 35%→50%; B2B re-order loop, +30-50% recurring orders after 90 days).
Outputs: TABLE-011 (Phase 1-4): from 75 deals/day ($337,500/day) at launch to 1,375 deals/day ($6,187,500/day)
at "Global Maximum" (5,000 bids/day, 45% reply, 50% close, 22.5% net conversion, 1,125 new + 250 repeat deals).

## SCENARIO-008 — Compounding/flywheel narrative claim (source page 23)
Trigger: "and this is compounding effect because of the brand value and the quality aswells as the system
getting better"
Claim (not independently quantified beyond the illustrative "700,000 successful bids" figure): "your AI has
already processed 700,000 successful bids" a year after launch, as the basis for an "Ultimate Barrier to
Entry" argument. Status: SOURCE_ESTIMATE / narrative claim, no derivation shown for the 700,000 figure.

## Cross-scenario reconciliation notes
- SCENARIO-001/002 rest on the 15,000 leads/day basis; SCENARIO-003 onward rest on the 1.5M-2.5M leads/day
  basis. These are NOT reconciled anywhere in the source. See `docs/requirements/conflicts.md` CONFLICT-001.
- SCENARIO-004 (no hardware assumption, $480K/day) vs. SCENARIO-005 (universal-printer hardware assumption,
  $1.2M/day) vs. SCENARIO-006 (universal-printer + 10%-discount rule, $945K/day) are three overlapping but
  mutually exclusive framings of "what price/volume should we run at" — the source moves through them
  sequentially as the user adds new constraints, without formally retiring the earlier framings.
