# Extracted Formulas

## FORMULA-001 — Pricing engine (source page 27, "DYNAMIC PRICING & VALUE FORMULATION")
```
1. Prevailing Market Price Estimation:  P_market = Tooling + (N * Unit_Price) + Setup
2. Strict Contract Bidding Price:       P_bid = 0.90 * P_market   (Exact 10% Discount)
3. Hard COGS (Raw Aluminum + Power):    C_mfg = (Mass_kg * $3.15) + (kWh * $0.12)
4. Gross Margin Extraction:             Margin = (P_bid - C_mfg) / P_bid    (~85% - 94%)
5. Irresistible Value Multipliers:      Free CAD Modifications + Free Custom Logo Embedding
```
Also restated in LaTeX display form on page 22-27: `P_bid = 0.90 × P_market`.
Variables:
- `Tooling` — tooling/setup cost component of traditional market price (USD)
- `N` — unit count / production volume
- `Unit_Price` — per-unit traditional market price (USD)
- `Setup` — additional setup cost component (USD)
- `Mass_kg` — part mass in kilograms
- `$3.15` — stated raw aluminum price per kg (source page 21: "roughly $3.15 per kg" / "₹345 per kg on the MCX," August 2026)
- `kWh` — kilowatt-hours of electricity consumed
- `$0.12` — implied electricity price per kWh (not independently stated elsewhere in the source; appears only inside this formula)
Source pages: 22, 27.
Status: SOURCE_FORMULA.

## FORMULA-002 — Anomaly / hallucination drift score (source page 28)
```
D_t = α · Error_schema + β · Anomaly_numeric + γ · [truncated in source render]
```
Status: SOURCE_FORMULA, INCOMPLETE. Only the first two full terms and the start of a third (γ-weighted) term
are visible in the original PDF render; the full right-hand side is not recoverable from the source as given.
Trigger threshold associated with this score: `D_t ≥ 0.85` (page 28), and separately `τ_drift ≥ 3` consecutive
failures (page 14) — see `docs/source-extraction/thresholds.md` THRESH-004/THRESH-005 for the apparent
inconsistency between a 0-1 continuous drift score threshold (0.85) and a discrete failure-count threshold (≥3),
both described as triggering the same hot-swap action.

## FORMULA-003 — Daily/Monthly token burn arithmetic (source page 16)
```
Input Tokens/Day  = 15,000 leads × 2,500 tokens/lead × 1.3 (sentinel overhead) ≈ 48.7 Million
Output Tokens/Day = 15,000 leads ×   300 tokens/lead × 1.3 (sentinel overhead) ≈  5.8 Million
Input Tokens/Month  ≈ 1.46 Billion   (48.7M × 30)
Output Tokens/Month ≈  175 Million   (5.8M × 30)
```
Status: SOURCE_FORMULA (arithmetic derivation), SOURCE_ESTIMATE (inputs). Basis: 15,000 leads/day figure that
is later revised — see CONFLICT-001.

## FORMULA-004 — Break-even / profitability arithmetic, $1,000 floor scenario (source page 17)
```
Monthly Operating Cost ≈ $3,500
Break-even deals/month = $3,500 / $1,000 = 3.5 deals/month
Gross Revenue (10 deals) = 10 × $1,000 = $10,000
Net Profit = $10,000 − $3,500 = $6,500/month  (stated as "185% ROI")
```
Status: SOURCE_FORMULA / SOURCE_ESTIMATE. NOTE: the source's stated "185% ROI" for $6,500 profit on $3,500
cost is $6,500/$3,500 ≈ 185.7%, i.e. ROI defined here as (Net Profit / Cost) × 100 — preserved as given,
flagged as a definitional choice rather than verified/re-derived by this extraction.

## FORMULA-005 — $3,500 AOV scenario (source page 18)
```
10 closed deals × $3,500 = $35,000 Revenue
Net Profit = $35,000 − $3,500 = $31,500/month  (stated as "900% ROI")
```
Status: SOURCE_FORMULA / SOURCE_ESTIMATE. $31,500/$3,500 = 900% exactly, under the same ROI definition as FORMULA-004.

## FORMULA-006 — "Category killer" cheapest-in-market daily scenario (source page 20)
```
Bids Sent = 2,000/day
Response Rate = 30% → 600 active negotiations/day
Close Rate = 40% → 240 closed contracts/day
AOV = $2,000
Daily Gross Sales = 240 × $2,000 = $480,000/day
Gross Margin = 10%-15% (stated compressed range) → used as 12% for the point estimate
Daily Gross Profit = 12% × $480,000 = $57,600/day
```
Status: SOURCE_FORMULA / SOURCE_ESTIMATE.

## FORMULA-007 — Universal-printer hypothetical daily scenario (source pages 21-22)
```
Aluminum cost for 100× 1kg parts = 100 × $3.15 = $315
Bid price (example) = $2,500 vs traditional market $12,000 (~80% cheaper); markup on $315 material cost ≈ 800%

Bids = 2,000/day; Response Rate = 50% → 1,000 clients
Close Rate = 80% of respondents → 800 closed contracts/day
AOV = $1,500 (conservative)
Daily Gross Revenue = 800 × $1,500 = $1,200,000/day
Per-contract cost ≈ $250 (metal + shipping) → per-contract profit ≈ $1,250
Daily Gross Profit = 800 × $1,250 = $1,000,000/day
```
Status: SOURCE_FORMULA / SOURCE_ESTIMATE, resting on SOURCE_HARDWARE_ASSUMPTION ASSUMPTION-001 (hypothetical
universal 3D printer).

## FORMULA-008 — 10%-below-market revised daily/monthly scenario (source page 22)
```
AOV = $4,500 (= $5,000 traditional × 0.90)
Bids = 2,000/day; Response Rate = 30% → 600/day; Close Rate = 35% → 210 closed/day
Daily Gross Revenue = 210 × $4,500 = $945,000/day
Daily Production Cost = 210 × $300 = $63,000/day
Daily Gross Profit = $945,000 − $63,000 = $882,000/day
Monthly Gross Sales  ≈ $945,000 × 30 = $28,350,000  (stated "~$28.35 Million")
Monthly Gross Profit ≈ $882,000 × 30 = $26,460,000  (stated "~$26.46 Million")
```
Status: SOURCE_FORMULA / SOURCE_ESTIMATE. Also derives: Net Profit per Order = $4,500 − $300 = $4,200,
Gross Margin per Order = $4,200/$4,500 ≈ 93.3% (matches TABLE-009).

## FORMULA-009 — Layer 0 deterministic pre-filter funnel (source pages 20, 27)
```
Raw Daily Intake = 2,000,000 leads
Layer 0 filters ~95% → 100,000 leads remain
Layer 1 (LLM Sanitizer) passes top ~2% of the 100,000 → 2,000 leads
Layer 2+ (Bidding Agents) deploy to those 2,000/day
```
Status: SOURCE_FORMULA / SOURCE_ESTIMATE. Restated with a "2%-5% qualified → 2,000-5,000 bids" range on page 27.
