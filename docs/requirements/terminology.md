# Terminology Register

For every important term, its exact source meaning, source pages, related terms, ambiguity, and a normalized
interpretation. Where the source itself never defines a term precisely, that is stated rather than papered
over.

## IECHM
**Source meaning:** Proper-noun label for "the firm" throughout the document — introduced when the user
(with typos) writes "ICN ICHN" (page 8) and the AI silently normalizes this to "IECHM" for the rest of the
conversation. **Ambiguity:** The source NEVER expands what IECHM stands for as an acronym. This is a
genuine SOURCE_INCOMPLETE gap, not an oversight in extraction. **Related terms:** IECHM-OS (page 26, the
working codename for the final master system prompt / architecture). **Normalized interpretation:** Treat
"IECHM" as an opaque proper-noun placeholder for the user's firm until the user provides the actual expansion
or confirms one.

## IECHM-OS
**Source meaning:** Appears once, in the title of the final Master Production System Prompt (page 26):
"MASTER PRODUCTION SYSTEM PROMPT: Autonomous B2B Manufacturing Acquisition, Slicing & Intelligence Engine
(IECHM-OS...)" — truncated in the source render immediately after. **Ambiguity:** Whether "IECHM-OS" names
the whole system, just the master prompt, or is a working title never formally adopted. **Normalized
interpretation:** Working codename for the final/most-complete architecture draft (Master Prompt v2).

## Lead / Raw Signal
**Source meaning:** Used somewhat interchangeably. "Raw signal" / "raw lead" = an unqualified scraped
listing/RFQ/post before any filtering (page 16, 19, 20, 27). "Lead" alone is used both for raw signals and
for qualified/scored leads depending on context — the source does not consistently disambiguate. **Normalized
interpretation:** This extraction treats "raw lead"/"raw signal" as pre-Layer-0/pre-qualification, and "lead"
(unqualified) as ambiguous — check surrounding context (funnel stage) whenever the term recurs in Step 1+.

## Client Archetype
**Source meaning:** A buyer-persona classification. Defined with 3 different lists across the document
(3-archetype narrative form, page 9; two separate 5-archetype list forms, pages 7 and 11-12) and 3 different
enum vocabularies across schema versions (SCHEMA-002/003/005). See client-archetypes.md and conflicts.md
CONFLICT-004. **Normalized interpretation:** No single canonical list exists in the source; Step 1+ requires
an explicit reconciliation decision (out of scope for Step 0).

## Macro Channel / Lead Source Type / Lead Channel Source Type
**Source meaning:** The mid-tier grouping between "client archetype" and "specific platform." Named
variously "Lead Source Archetypes (Macro Categories)" (page 7, 8 categories), "Macro Channel Types" (page 12,
6 categories: `FREELANCE_MARKETPLACES`, `B2B_TRADE_DIRECTORIES`, `COMMUNITY_FORUMS_SOCIAL`,
`AGENCY_BROKERAGES`, `ON_DEMAND_MFG_NETWORKS`, `OUTBOUND_SIGNALS`), and again as a 5-branch diagram on page 9
(`Marketplaces`, `B2B Directories`, `Communities`, `Brokerages`, `Outbound`). **Ambiguity:** the count of
macro categories shifts between 4 (page 5), 8 (page 7), 5 (page 9 diagram), and 6 (page 12, 27). **Normalized
interpretation:** The 6-value enum form from pages 12/27 (the most recent, schema-bound version) is the most
implementation-ready candidate, but this is not stated as canonical by the source itself.

## Platform
**Source meaning:** An individual named site/service (e.g., Upwork, Alibaba). Consistent usage throughout.

## Sub-Domain
**Source meaning:** A granular channel within a platform — e.g., a specific subreddit within Reddit, or an
RFQ sub-category within Alibaba. Central to the "5-Lead Rule" (THRESH-001/002). Consistent usage.

## Worker (Agent)
**Source meaning:** A persistent agent dedicated to one platform (Layer 3) or one sub-domain (Layer 4).
Consistent usage across pages 11-29.

## Sentinel
**Source meaning:** An "Auditor Sentinel" — one per architectural layer — whose sole job is hallucination/
anomaly detection (not proposal quality). Distinct from the Reviewer (which checks proposal-level compliance,
not model-integrity). Consistent usage, pages 13-15, 26, 28.

## Sanitizer
**Source meaning:** First-stage agent in the 4-node bidding pipeline; detects anti-bot traps and prompt
injections in a client brief. Consistent usage, pages 1-2, 26-28. **Not to be confused with** the Layer 0
deterministic pre-filter (pages 20, 27), which is a separate, non-AI, earlier-stage filtering mechanism that
operates on raw signals before the Sanitizer ever sees an individual qualified lead.

## Strategist
**Source meaning:** Second-stage agent; writes the bid *blueprint* (not the bid itself) using RAG-retrieved
historical win/loss data and the Explore/Exploit policy. Consistent usage.

## Writer
**Source meaning:** Third-stage agent; drafts the actual proposal text per the Strategist's blueprint and the
Sanitizer's mandatory constraints. In Master Prompt v2, additionally responsible for triggering the Slicer API
to generate a 3D preview render. Consistent usage.

## Reviewer
**Source meaning:** Fourth-stage agent; QA gate before submission. In Master Prompt v2, additionally audits
the pricing math itself. Consistent usage.

## Hot-Swap (Failover)
**Source meaning:** The act of replacing a hallucinating/faulty agent with a clean replacement while
transferring its serialized context/state. Consistent usage, pages 13-15, 26, 28-29.

## Drift (Drift Score, $D_t$)
**Source meaning:** A numeric anomaly/hallucination score computed per worker output via FORMULA-002
(incomplete in source). Threshold for failover: $D_t \ge 0.85$ (page 26, 28). **Ambiguity:** a SEPARATE,
non-reconciled trigger of "$\ge 3$ consecutive schema/validation errors" (also called $\tau_{drift} \ge 3$ on
page 14) is described as triggering the identical Hot-Swap action — the source never states whether these are
two independent OR-conditions, two equivalent expressions of the same thing, or a drafting inconsistency. This
extraction treats them as two independent OR-conditions (see THRESH-004/005) since both are stated as
sufficient triggers without qualification.

## Telemetry / Metric Evolution & Saturation Optimizer
**Source meaning:** The agent responsible for proposing new data fields to collect, and for self-limiting
into an idle state (`CHANNEL_DATA_SATURATED_IDLE_ACTIVE`) once further collection is not useful. Consistent
usage across pages 13-15, 28.

## Explore / Exploit
**Source meaning:** Reinforcement-learning-style terminology for the Strategist's 80%/20% strategy-selection
policy (page 2). Reused/restated identically in later drafts (pages 26-27). Consistent usage.

## RAG (Retrieval-Augmented Generation)
**Source meaning:** Used specifically to mean "query the agent's own historical proposal outcome database
before drafting a new bid." Consistent, narrow usage — not used in the source for any other retrieval purpose.

## "The 5-Lead Rule"
**Source meaning:** Shorthand (used by name only once, page 17, "You aren't running 500 agents all the
time... The 5-Lead Sub-Domain Rule") for THRESH-001/002 — spawn a sub-domain agent above 5 leads/day, retire
it below 2 leads/day over 7 days. Consistent usage, though the exact spawn/deprecate numbers are restated
(not renamed) across pages 11, 12, 14, 17, 26, 27.

## "The 10% Rule" / Pricing Rule
**Source meaning:** `P_bid = 0.90 × P_market`. **Ambiguity, IMPORTANT:** The rule's origin is the user's
literal statement (page 22) "i dont want to go less than 10 percentage of the actual market prize" — which
is genuinely ambiguous. Two readings are grammatically possible: (a) "I don't want to discount by less than
10%" (i.e., 10% is a MINIMUM discount, and could go deeper), or (b) the AI's chosen reading: "bid at a price
that is 10% below market, i.e. a fixed/exact 10% discount, no more no less." The AI's response text
immediately reframes it as "Pricing at 10% below market price (capturing 90% of prevailing market rates)"
and this exact-90%-of-market reading is what propagates through the rest of the document (formalized as
`P_bid = 0.90 × P_market` and later hardened into "never bid at deep discounts (>20% off)"). **Normalized
interpretation:** This extraction preserves the AI's operative interpretation as the one that governs all
downstream architecture, while flagging that the user's original phrasing could support a different reading
(a discount floor rather than an exact discount) that was never explicitly confirmed with the user in the
source conversation.

## Layer 0 / Layer 1 / Layer 2 / Layer 3 / Layer 4
**Source meaning, and a genuine numbering ambiguity:** Two DIFFERENT "Layer N" numbering schemes coexist in
the source, describing two different things:
1. **Agent-hierarchy layers** (pages 11-15, 26-27): Layer 1 = Central Command/Client Classification, Layer 2
   = Macro Channel Controllers, Layer 3 = Platform Workers, Layer 4 = Dynamic Sub-Domain Workers.
2. **Data-pipeline stages** (pages 20, 27): Layer 0 = deterministic pre-filter, Layer 1 = LLM Sanitizer/
   Classifier, "Layer 2-4" = collectively "Proposal Cluster, Slicing API & Hardware Dispatch" (page 27,
   not broken into individually-numbered sub-layers there).
**Ambiguity:** scheme 2's "Layer 1" (LLM Sanitizer/Classifier, a data-filtering stage) is NOT the same
concept as scheme 1's "Layer 1" (Central Command agent team) — despite sharing the name and both appearing in
the same overall architecture. The source does not flag this collision. **Normalized interpretation:** Step
1+ MUST treat these as two independent numbering schemes for two different axes (agent org-chart depth vs.
data-pipeline stage) and should not conflate "Layer 1" across the two schemes without renaming one of them.
