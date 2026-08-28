# ADR-0002 — Resolve the Source's Layer-Numbering Collision via Layer 0-4 (pipeline) / Tier 1-4 (agent org-chart)

**Status:** ACCEPTED
**Source IDs:** SRC-000038 (data-pipeline scheme), SRC-000033/075 (agent-hierarchy scheme)
**Requirements:** N/A (documentation/naming convention, not a functional requirement)

## Context
The source uses "Layer N" for two genuinely different things: a data-pipeline-stage model (Layer 0 =
deterministic pre-filter ... Layer 1 = LLM qualification) and an agent-organization-depth model (Layer 1 =
Central Command/3 agents ... Layer 4 = dynamic sub-domain workers). These collide at "Layer 1" specifically,
which means two different things depending on which source passage is being read (`terminology.md`).

## Decision
This documentation set adopts **Layer 0-4** exclusively for the data-PIPELINE-STAGE model
(`canonical-architecture.md`), and **Tier 1-4** for the agent-organization-DEPTH model (`agent-topology.md`).
This is a naming-convention decision only — it does not resolve any substantive conflict about content, only
disambiguates which "layer" a given document is talking about.

## Alternatives considered
1. Keep the source's overloaded "Layer N" terminology and rely on context — rejected, too error-prone for a
   project built on traceability discipline.
2. Renumber the pipeline stages instead of the agent tiers — arbitrary either way; pipeline stages were kept
   as "Layer" since that numbering (0-4) is the more recently-stated, more complete version in the source
   (Master Prompt v2, pages 27-28).

## Consequences
Every Step 1 document consistently uses this convention. Future steps must preserve it or explicitly amend
this ADR (status → SUPERSEDED) rather than silently drifting back to ambiguous usage.

## Reversibility
Fully reversible (pure documentation convention).
