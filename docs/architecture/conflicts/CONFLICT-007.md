# CONFLICT-007 — "Blueprint Only" Scope Constraint vs. "Build the Full AI System" Request

## Source A
- **Source IDs:** SRC-000027
- **Pages:** 8
- **Exact relevant statement:** User: "right now this is just for the ... it's only be like just the data
  alone the data and strategy alone not building the agent okay this is like the blueprints not the actual
  agent just the blueprint."
- **Interpretation:** An explicit, direct scope constraint: the deliverable at that point in the conversation
  is data/strategy specification only — no executable/running agent.

## Source B
- **Source IDs:** SRC-000070
- **Pages:** 25
- **Exact relevant statement:** User: "give me full prompt for building the ai system with all the
  conversation we had for building the system."
- **Interpretation:** A request for a consolidated, executable system prompt covering the entire
  architecture — functionally a request to build (the specification for) the full agent system.

## Why they may differ
Seventeen conversational turns and roughly 17 pages separate these two statements. The user's own ask visibly
evolves over the conversation: early turns are exploratory/scoping ("just the blueprint"), later turns
explicitly request buildable artifacts (full system prompts, cost projections, "give me full prompt for
building the ai system"). The source never contains an explicit statement like "the earlier data-only
constraint no longer applies" — the scope simply appears to expand through the accumulation of the user's
subsequent, more specific requests, without a formal retraction of the earlier one.

## Technical implications
Whether IECHM-LIOS (this project, System A per `system-boundaries.md`) is scoped to intelligence/data
only, or is expected to ALSO contain a buildable agent-execution specification (System B's Sanitizer/
Strategist/Writer/Reviewer pipeline), materially changes what belongs inside this repository's architecture
vs. what belongs to a separate downstream project.

## Data-model implications
If System B's pipeline is in-scope, the data model needs to support live proposal-generation state (draft
bids, review status) in addition to intelligence/lead records. If out of scope, IECHM-LIOS's data model stays
focused on lead/client/platform intelligence only.

## Architecture implications
This conflict is why `docs/architecture/system-boundaries.md` explicitly scopes the CURRENT IECHM-LIOS project
to System A only, while documenting System B/C as external, referenced-but-not-built systems. That scoping
decision is itself the proposed resolution to this conflict for Step 1 purposes.

## Operational implications
Building System B/C functionality inside what the user separately (via the actual Step 0 and Step 1
instructions governing THIS build, outside the original source PDF) has repeatedly scoped as "architecture
only, no agent runtime, no bidding execution, no machine control" would violate those explicit, more recent
and more authoritative instructions regardless of how CONFLICT-007 is resolved with respect to the OLD source
PDF's internal scope drift.

## Economic implications
None directly.

## Possible resolutions
1. Treat the page-25 request as scope EXPANSION superseding the page-8 constraint, WITHIN THE ORIGINAL SOURCE
   CONVERSATION — meaning the source PDF's own later sections (System-B/C architecture) are legitimately
   part of "what the user asked for" historically, even though building them is separately out of scope for
   the CURRENT IECHM-LIOS repository per the governing Step 0/Step 1 instructions.
2. Treat the page-8 constraint as still the operative framing for what "the data/strategy blueprint system"
   (i.e., IECHM-LIOS) specifically is, with the page-25-onward material read as describing an ADJACENT,
   separately-scoped system (System B) that consumes IECHM-LIOS's output, consistent with the page-1 original
   two-system framing.

## Recommended decision
Resolution 2 is what `docs/architecture/system-boundaries.md` currently adopts, because it is also consistent
with the page-1 original two-system split (SRC-000002) and with the actual governing instructions for this
repository (Step 0/Step 1, which are more recent, more specific, and directly authored by the user for this
project, as opposed to the older source PDF transcript).

## Decision status
**DECISION_STATUS = PARTIALLY RESOLVED BY IMPLICATION** for the purposes of scoping the CURRENT IECHM-LIOS
repository (resolution 2, adopted). **NOT RESOLVED** as a question about what the ORIGINAL source conversation
intended internally — that remains genuinely ambiguous and is preserved as such in
`docs/source-extraction/exact-source.md` and Step 0's own conflict record.
