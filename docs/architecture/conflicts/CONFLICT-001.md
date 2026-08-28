# CONFLICT-001 — Raw Daily Lead Volume: 15,000/day vs. 1.5M–2.5M/day

## Source A
- **Source IDs:** SRC-000043, SRC-000044, SRC-000045, SRC-000047
- **Pages:** 16, 17, 18
- **Exact relevant statement:** "Let's assume the global hardware/NPD market generates 15,000 raw leads/
  signals per day" (page 16); "450,000 leads/month" (= 15,000 × 30) used as the funnel basis through page 18.
- **Interpretation:** A volume estimate scoped, by the AI's own later admission (page 19), to "Western-facing,
  English-language freelance engineering and custom NPD design jobs" — i.e., narrow, freelance-board-only
  intake.

## Source B
- **Source IDs:** SRC-000051, SRC-000052, SRC-000053, SRC-000073, SRC-000074
- **Pages:** 19, 20, 25, 27
- **Exact relevant statement:** "your true Total Addressable Raw Firehose across all 75+ platforms is
  realistically 1.5 million to 2.5 million raw signals per day" (page 19); reused as the ingestion basis in
  Master Prompt v1/v2 ("ingests a raw global firehose of ~1.5 to 2.5 million signals per day," pages 25, 27).
- **Interpretation:** A volume estimate scoped to the FULL addressable market across B2B trade directories,
  importers/middlemen, and every physical-manufacturing category the user specified (all manufacturing except
  chemicals/fabrics/food) — i.e., broad, cross-channel intake.

## Why they may differ
Source A and Source B answer genuinely different questions, but the source document itself never explicitly
frames them that way. Source A was produced in direct response to "at the full scale how many agents ai will
be there and how many tokens each consume and how much is the cost" — a question the AI answered using an
implicit, narrow scope it had been operating under since page 4 (NPD/CAD/PCB freelance work specifically).
Source B was produced in direct response to the user explicitly REJECTING that narrow scope one turn later
("it doesnt only include npd but also middel man and importers and all platforms and every manfacturing
except chemicals and fabrics and foods"). The AI's response to Source B narrates this as a correction
("The 15,000 daily leads figure was drastically undercounted...") rather than as "here is a different metric
for a different scope" — which is itself ambiguous evidence: it could mean the AI now considers Source A
simply wrong, or it could mean Source A remains a valid metric for a narrower deployment profile that the
user may still want to run (e.g., an MVP/Phase-1 launch focused on freelance boards before expanding to full
B2B firehose scope).

## Technical implications
If Source B is the only architecturally relevant figure, IECHM-LIOS must be built assuming ~75+ platform
connectors and the Layer 0 deterministic pre-filter from day one (Layer 0 did not exist as a concept before
Source B). If Source A remains relevant as a Phase-1 scale, the system needs a scale-appropriate deployment
mode that does NOT require Layer 0 or the full 75-platform connector roster to deliver value.

## Data-model implications
The `UnifiedLeadEntity` schema and its qualification-scoring fields must be volume-agnostic (no hardcoded
assumptions about intake rate baked into the schema itself), since the actual production volume is unresolved.

## Architecture implications
Directly drives `docs/architecture/scaling-scenarios.md`: the canonical architecture must support multiple
declared scale profiles rather than being designed around a single hardcoded volume assumption.

## Operational implications
Cost, infrastructure sizing (proxies, compute, vector DB), and agent-fleet sizing (TABLE-004/005/006 in Step 0)
were computed against the Source-A basis and were NEVER recomputed against Source B anywhere in the source
document (this is CONFLICT-002, a direct downstream consequence). Operating IECHM-LIOS at Source-B scale using
Source-A-derived cost/agent-count figures would understate true operating cost.

## Economic implications
All of `docs/source-extraction/economic-scenarios.md` SCENARIO-001/002 rest on Source A; SCENARIO-003 onward
rest on Source B. Neither scenario set should be treated as validated against the other's assumptions.

## Possible resolutions
1. Treat Source A and Source B as two distinct, named deployment SCALE PROFILES ("Freelance-Only Profile" and
   "Full-Firehose Profile") that the architecture supports simultaneously via configuration, not as competing
   claims about the true production volume.
2. Treat Source B as the sole authoritative target scope and Source A as an obsolete early estimate,
   discarding it as a design input (but NOT discarding it as a historical source record — Level 1 stays
   immutable either way).
3. Treat neither as authoritative pending a real, current measurement of actual platform posting volume once
   IECHM-LIOS begins operating (both are speculative estimates with no empirical backing).

## Recommended decision
Resolution option 1 (multiple named scale profiles) is technically the safest path because it requires no
guess about user intent and keeps both source figures usable — see `docs/architecture/scaling-scenarios.md`
where this is worked out as the canonical architecture's approach. This recommendation is offered as
architecture guidance, not as a resolution of the underlying factual conflict, which remains open.

## Decision status
**DECISION_STATUS = NEEDS_USER_DECISION** — specifically: does the user intend an initial narrow-scope launch
(closer to Source A) with the option to expand later, or is full-firehose scope (Source B) the Day-1 target?
This determines Phase-1 platform-connector priority in `docs/architecture/implementation-roadmap.md`.
