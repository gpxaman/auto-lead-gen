# Extracted Strategies

## Bidding / Proposal Strategy Concepts

**Cultural-tone adaptation** (page 1): Recon Engine should extract whether a platform's proposal culture is
"highly corporate" or "casual and brief," and whether it uses a credit system (e.g., Upwork Connects) with
API/rate limits.

**RAG-based self-improvement loop** (page 1): Before writing a new bid, query the agent's own historical
database: "Fetch the last 5 successful proposals I submitted for hardware design tasks on this site, and 5
proposals that were rejected." Adapt language/pricing/tone to what converts on that specific platform.

**Explore vs. Exploit (Reinforcement Learning framing)** (page 2): 80% of the time, Exploit the highest
historical-win-rate strategy in vector memory; 20% of the time, Explore a completely new approach picked from
a "Planned" list in the Strategy Ledger (see TABLE-001). If a new strategy outperforms baseline, it becomes
the new default Exploit behavior.

**Loss-cause tracking / "Unseen Variables"** (page 2): Regularly scrape the site for the outcome of lost bids
(who won, for how much) and feed that back into the Strategist's memory — e.g., if a competitor consistently
underbids by 5%, adjust pricing algorithms accordingly.

**Platform sequencing strategy** (page 5): Start with Upwork and Freelancer.com (highest data volume to train
the Strategist's vector memory); once win rate stabilizes, scale horizontally to Guru, Cad Crowd, mid-tier
sites.

**Lead-source-type sequencing strategy** (page 5-6): Start with the Freelance category and the B2B Sourcing
category (Alibaba/Supplya RFQ monitoring), since together they "will provide more leads than a single
consultancy can handle."

**Archetype-specific strategic angles** (page 9):
- NPD Innovator → sell de-risking + turnkey delivery (DFM reviews, BOM cost reduction, functional prototyping milestones)
- Middleman/Reseller → sell customization + cost-down engineering (VAVE) + QA (enclosure redesign, mold optimization, pre-shipment inspection)
- Overburdened SME → sell immediate execution + plug-and-play bandwidth (native + standard exchange formats, zero onboarding friction)

**Pricing strategy — "10% below market" rule** (pages 22, 27, 29): `P_bid = 0.90 × P_market`. Rationale
given: massively undercutting the market (70-80% off) "triggers skepticism among enterprise B2B buyers who
assume low prices equal inferior quality," whereas a 10% discount "maintains high perceived value, avoids a
race to the bottom, and captures extraordinary profit margins." Never discount more than 20% ("signal low
quality") — see THRESH-008.

**Value-add hooks strategy** (pages 20, 22, 24-28): Free CAD modifications + free custom logo/branding +
instant turnaround, marketed as "irresistible value multipliers" layered on top of the 10%-discount price.

**"Instant Proof" conversion lever** (page 24): Attach an automated DFM report + a 3D preview render (with
the client's logo already embedded) directly to the bid submission, rather than sending a text-only proposal.
Stated impact: response rate 30%→45%, negotiation close rate 35%→50%.

**Sub-60-second response latency strategy** (page 25): Poll high-value RFQ feeds via WebSockets and bid within
the first 60 seconds of a posting going live.

**Automated risk-free guarantee strategy** (page 25): Contractual tolerance guarantee (±0.05mm) with free
remanufacture, framed as removing "100% of client purchase friction."

**Automated re-order / repeat-order strategy** (pages 25, 28): Track delivery dates, model consumption based
on client business type (e.g., Amazon FBA seller ~30-day inventory cycle), and trigger outreach at Day 25
post-delivery offering a one-click repeat batch at the locked-in discount.

**Aggregator / broker-model pivot strategy** (page 21): When physical fulfillment capacity is exceeded, IECHM
should transition to a Xometry/Hubs-style aggregator model — keep high-margin complex work in-house (Chennai),
route overflow to vetted partner factories across India and Asia, with automated visual inspection / physical
consignment certification enforced on partner-fulfilled orders to protect the quality guarantee.

**Self-replicating hardware scaling strategy** (page 24): Since IECHM owns the machine's IP/BOM from having
built it from scratch, use Printer A to print structural/mechanical components for Printers B, C, D — scaling
physical capacity at near-raw-material cost instead of $500,000/unit commercial-vendor CapEx.

**AI Compounding / Flywheel strategy** (page 23): Two linked flywheels — (1) AI Cognitive Flywheel: Execution
→ Evaluation → Reflection → Memory loop, compounding strategic experience per bid; (2) Economic & Brand
Flywheel: Initial Hook → Trust Building → Retention → Network Effects, compounding market lock-in. Framed as
an "Ultimate Barrier to Entry" against competitors who start their AI from zero.

**Bid-volume broadening lever** (page 24): Add more platform workers and micro sub-domain agents to expand
raw bidding capacity from 2,000 to 5,000 qualified bids/day (2.5x).
