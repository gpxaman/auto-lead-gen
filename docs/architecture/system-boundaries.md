# System Boundaries

**Version history:** Originally created in Step 0 (Sections 1-72 below, unchanged). Extended in Step 1 per
Step 1 Section 8, which requires a more rigorous responsibilities/inputs/outputs/dependencies/ownership/
interfaces analysis and explicit `INTERFACE_UNDEFINED` marking. Nothing from the Step 0 analysis was deleted
or altered — Step 1's additions appear in new sections below "What is explicitly OUT OF SCOPE." See
`docs/audit/step-1-source-integrity-findings.md` FINDING-001 for the rationale for extending this file in
place rather than creating a duplicate.

Per Step 0 instructions, this document determines and records whether the source distinguishes:

**A.** Lead intelligence / reconnaissance / database-building system
**B.** Proposal / bidding / site-execution system
**C.** Manufacturing / machine execution system

and what belongs inside IECHM-LIOS (this project) vs. later/external execution systems.

## A vs. B — Reasonably well-distinguished by the source

The user's very first prompt (page 1, SRC-000002) explicitly draws this boundary: "now what the second
automation does is automated freelancer were it bids for propasal... this is just freelacing site excutive
which bids and does all the work in the site and the second automation is the builder which gets the report
from the first automation to what type of agent it should build and what is stargery."

- **System 1 (= this project, IECHM-LIOS):** Finds/monitors lead sources, produces a structured report and
  strategy breakdown per platform. This is the "Lead Intelligence Architect" role named in every system-prompt
  draft (pages 7, 11, 14, 25-26). Its output is a report/data artifact, not a live bidding action.
- **System 2 (explicitly out of scope, referenced but not built here):** The "Freelancing Site Executive" —
  an autonomous agent, hyper-specialized per platform, that actually bids for proposals, learns the platform's
  communication style, and improves itself. The user states this "does not actualy do the work it bids for"
  (the work itself is handled by yet another, third, already-built automation not discussed further in this
  document).
- **Status:** BOUNDARY REASONABLY CLEAR at the outset, but **the source's own later requests blur it**: by
  page 11 ("now each thing will have its own autonoumous agents...") through the Master Prompt v1/v2 (pages
  25-29), the document is explicitly building out much of System 2's internal architecture (Sanitizer/
  Strategist/Writer/Reviewer, hallucination sentinels, pricing engine, hardware dispatch) as part of the "one
  unified system prompt." **This is preserved as BOUNDARY_BLURRED_BY_LATER_REQUESTS, not silently resolved.**
  Per CONFLICT-007, the user's page-8 scope constraint ("blueprint not the agent") and the page-25 request
  ("give me full prompt for building the ai system") sit in tension. This Step 0 IECHM-LIOS specification
  (per the current, separate instructions governing this build) explicitly re-establishes System 1's scope as
  "data/strategy blueprint and intelligence, not the actual bidding agent" — consistent with the earlier,
  narrower framing — but this is a DECISION being made now (in this Step 0 process), not something the
  original source document itself cleanly resolves.

## B vs. C — NOT clearly distinguished by the source; this is a genuine gap

The bidding/proposal-generation architecture (Sanitizer→Strategist→Writer→Reviewer, System B) and the
physical-manufacturing/machine-execution architecture (Universal 3D Printer, Estimator/Dispatch Agents,
Cloud Slicer, G-code dispatch, System C) are presented, from page 21 onward, as parts of the SAME master
system prompt, with no explicit statement that they are — or should be — separate services/systems.

- Page 24's "Deep API Integration" section explicitly wires the Dispatch Agent directly into "the machine's
  active print queue," and Master Prompt v2 Section 7 (pages 28) formalizes a "Machine-to-AI Hardware API &
  Cloud Slicing Integration" as one section of the same document that also contains the lead-intelligence
  database architecture (Sections 1-6, 9-12).
- **Status: BOUNDARY_UNRESOLVED.** The source never states whether: (a) IECHM-LIOS (lead intelligence) should
  merely PRODUCE data consumed by a separate bidding/manufacturing system (matching the page-1 framing), or
  (b) all three systems (intelligence, bidding, manufacturing) are meant to be one monolithic "IECHM-OS."
  Given the user's initial framing (page 1) explicitly separates "this automation" (recon/report) from "the
  second automation" (bidding executive) and a third, already-built, unnamed automation ("i have already
  build automation for it" — the work-execution system), and given that the CURRENT Step 0 instructions
  governing this build again scope the deliverable to "specification, not implementation" — **this project
  (IECHM-LIOS) is scoped, for now, to System A only: lead intelligence, database-building, and strategic
  reconnaissance.** System B (bidding execution) and System C (manufacturing/machine execution) are external
  systems that IECHM-LIOS is expected to produce structured OUTPUT for for, not to internally build.

## External systems and interfaces (as far as the source specifies)

| External system | Relationship to IECHM-LIOS | Source evidence |
|---|---|---|
| System 2 / "Freelancing Site Executive" (bidding agent) | Consumes IECHM-LIOS's report/strategy output; not built by IECHM-LIOS | Page 1 |
| The (unnamed) already-built work-execution automation | Performs the actual contracted work after a bid is won; entirely outside this document's scope; only referenced once | Page 1: "i have already build automation for it" |
| Freelance/B2B/broker/tender/crowdfunding platforms (Upwork, Alibaba, Reddit, etc.) | External data sources IECHM-LIOS scrapes/monitors | Throughout, see platforms.md |
| The (hypothetical) Universal 3D Printer / manufacturing hardware | External physical system IECHM-LIOS's data would eventually feed (via System B/C), NOT part of IECHM-LIOS itself | Pages 21-29; see hardware-assumptions.md ASSUMPTION-001 |
| LLM API providers (OpenAI, Anthropic) | External model providers referenced for cost/routing illustration | Pages 3-4, 15-17, 26, 29 |
| Vector database (Pinecone/Weaviate named as examples) | External memory store for RAG/Strategy Ledger | Page 16 |
| Scraping infrastructure (Playwright, Firecrawl, BrightData, Browserbase named as examples) | External tooling for recon | Pages 2-4, 16 |

## What belongs inside IECHM-LIOS (this project), per the above analysis

1. Client archetype identification, classification, and profiling (with proof/evidence tracking).
2. Lead channel source type taxonomy and per-channel benchmark metrics (MOV, velocity, setup time).
3. Individual platform deep-dive profiles (rules, tools, metrics, sub-domain index).
4. The database/data-model layer for all of the above (the "living, multi-layered relational database").
5. The discovery/scraping/recon agent swarm that populates and maintains that database (Layers 1-4 org chart
   from pages 11-12, 14, 27 — MINUS the proposal-generation pipeline itself).
6. The cross-cutting resilience plane (Hallucination Sentinels, Hot-Swap Failover, Telemetry/Saturation
   Optimizer) AS APPLIED TO THE RECON/DATABASE AGENTS.
7. Structured, versioned OUTPUT (a report / strategy artifact) meant to configure/inform System B (the bidding
   executive), per the page-1 framing.

## What is explicitly OUT OF SCOPE for IECHM-LIOS (belongs to System B / System C)

1. The Sanitizer→Strategist→Writer→Reviewer bid-generation pipeline (pages 1-2, 26-28) — this is System B's
   internal architecture, even though it is data-driven by IECHM-LIOS's output.
2. Actual bid/proposal submission to any platform.
3. The Estimator Agent / Dispatch Agent / Cloud Slicer / G-code queue integration (pages 24, 28) — this is
   System C (manufacturing execution).
4. The pricing engine's live execution (`P_bid = 0.90 × P_market`) — IECHM-LIOS may SUPPLY the market-price
   estimation data feeding this formula, but executing/quoting is a System B function.
5. The universal-printer hardware itself and its firmware/API (System C, and contingent on ASSUMPTION-001).

**BOUNDARY_UNRESOLVED note for the user:** This document makes an explicit, recorded judgment call (System
A-only scope for IECHM-LIOS) rather than inventing a boundary the source doesn't support. If the user intends
IECHM-LIOS to ALSO include System B and/or C, that should be stated explicitly before further architecture
work begins, since it changes the shape of the database schema, the agent roster, and the security-review
posture substantially (System B/C involve live financial transactions and physical manufacturing dispatch,
which carry materially different risk/authorization requirements than a read-only intelligence/reporting
system).

---

## STEP 1 EXTENSION — Detailed per-system responsibility/interface analysis

### System A (IECHM-LIOS, this project)

| Aspect | Detail | Status |
|---|---|---|
| Responsibilities | Discover platforms/sub-domains; scrape/monitor raw listings; classify client archetype and manufacturing domain; maintain platform/channel intelligence with evidence; run the recon-side agent swarm (Layers 1-4) and its resilience plane; produce structured, versioned strategic output | `SOURCE-DERIVED` |
| Inputs | Raw listings/RFQs/posts from external platforms (Section "External systems" above); user-configured platform priority; firm capability context (IECHM capability profile) | `SOURCE-DERIVED` |
| Outputs | A structured report/strategy artifact per platform, consumed by System B (SRC-000002); the `UnifiedLeadEntity` record (whichever schema version is eventually canonicalized, see `schema-versioning.md`) | `SOURCE-DERIVED` (existence of output) / `INTERFACE_UNDEFINED` (exact payload contract — see below) |
| Dependencies | External platforms (read-only); LLM API providers; vector DB; scraping infrastructure | `SOURCE-DERIVED` |
| Ownership | Owns: client/channel/platform/sub-domain intelligence data, evidence records, its own agent fleet and sentinel plane | `INTERPRETATION` (the source does not use the word "owns" but this follows from System A being the only system that writes this data) |
| Interface to System B | **`INTERFACE_UNDEFINED`.** The source states System A's output is "a report" and "what type of agent it should build and what is stargery" (SRC-000002) but never specifies a payload schema, delivery mechanism (API push? shared DB read? file export?), update cadence, or versioning contract for this specific interface. The `UnifiedLeadEntity` schemas (SCHEMA-002/003/005) are the closest thing to a candidate contract, but none of them were ever explicitly labeled "this is what gets handed to System B." |
| Interface to System C | **`INTERFACE_UNDEFINED`.** No source statement ties System A's output directly to System C at all — System C is only ever wired to System B (via the Estimator/Dispatch agents), not to System A. |

### System B (Bidding/Proposal Executive — referenced, NOT built by IECHM-LIOS)

| Aspect | Detail | Status |
|---|---|---|
| Responsibilities | Per-platform bidding, proposal generation (Sanitizer→Strategist→Writer→Reviewer), pricing decision, learning from win/loss outcomes | `SOURCE-DERIVED` |
| Inputs | System A's report/strategy output (`INTERFACE_UNDEFINED`, see above); live job/RFQ briefs from platforms; historical win/loss memory (RAG) | `SOURCE-DERIVED` |
| Outputs | Submitted bids/proposals to platforms; contract-signed events (feeding System C) | `SOURCE-DERIVED` |
| Dependencies | System A (report input); platform APIs/UIs for submission; LLM providers | `SOURCE-DERIVED` |
| Ownership | Owns: proposal drafts, pricing decisions, its own Strategy Ledger/RAG memory | `INTERPRETATION` |
| Interface to System C | Partially defined: `EVENT_CONTRACT_SIGNED` triggers Dispatch Agent → G-code queue (SRC-000076); the Estimator Agent calls a "Cloud Slicer Engine" (page 28) whose interface to System B's Writer agent (for 3D preview render generation, SRC-000066/page24) is named conceptually but not contractually specified — `INTERFACE_UNDEFINED` for exact payload. |

### System C (Manufacturing/Machine Execution — referenced, NOT built by IECHM-LIOS, contingent on ASSUMPTION-001)

| Aspect | Detail | Status |
|---|---|---|
| Responsibilities | Physical fabrication via the (hypothetical) Universal 3D Printer; slicing; G-code execution | `SOURCE_HARDWARE_ASSUMPTION` (contingent on ASSUMPTION-001/002 being true) |
| Inputs | Compiled G-code/toolpath data from System B's Dispatch Agent; client 3D files (STEP/STL) | `SOURCE-DERIVED`, contingent |
| Outputs | Manufactured physical parts; implicitly, delivery/shipment data (feeding the Day-25 re-order trigger, which is a System B function) | `INTERPRETATION` |
| Dependencies | Raw aluminum feedstock; electricity; the machine's own firmware/kinematics (owned per ASSUMPTION-002) | `SOURCE-DERIVED`, contingent |
| Ownership | Owns: machine state, print queue, physical inventory | `INTERPRETATION` |
| Interface to System A | **`INTERFACE_UNDEFINED`.** No direct connection specified anywhere in the source. |

## Conceptual (not contractual) interface diagram

```
[ External Platforms ] --(read-only scrape/monitor)--> [ SYSTEM A: IECHM-LIOS ]
                                                                |
                                                   (report/strategy output;
                                                    INTERFACE_UNDEFINED)
                                                                v
                                                      [ SYSTEM B: Bidding Executive ]
                                                                |
                                                (EVENT_CONTRACT_SIGNED; G-code/toolpath;
                                                 INTERFACE_UNDEFINED for exact payload)
                                                                v
                                                     [ SYSTEM C: Manufacturing Execution ]
```

This diagram is `PROPOSED_EXTENSION` in its explicit box-and-arrow form (the source never draws System A/B/C
as a single connected diagram — this is a synthesis of scattered statements across pages 1, 24, 28), though
every individual arrow/relationship it depicts is `SOURCE-DERIVED` or `INTERPRETATION` per the tables above.

No production API contract is defined for any of the `INTERFACE_UNDEFINED` items in this Step 1 pass — see
`docs/architecture/api-boundaries.md` for the conceptual (non-implementation) treatment of these gaps, and
`docs/architecture/open-decisions.md` for what requires explicit user input before these interfaces can be
designed for real.
