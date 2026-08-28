# ADR-0006 — Context Migration Filters Untrusted State From Replacement Agents

**Status:** ACCEPTED
**Source IDs:** SRC-000037
**Requirements:** REQ-000018, REQ-000020

## Context
The source's literal instruction is to "transfer its context and everything into replacement ai" upon agent
failure. Step 1 Section 23 explicitly warns: "A replacement worker must not inherit hallucinated information
as trusted knowledge" — a more specific and more recent instruction that qualifies the literal "everything."

## Decision
Context Migration (`context-migration.md`) filters transferred state through a 10-class trust taxonomy;
MODEL INFERENCE and FAILED OUTPUT are migrated to the incident log only, never presented to the replacement
agent as trusted context.

## Alternatives considered
1. Follow the literal "everything" instruction — rejected as unsafe and explicitly superseded by Step 1's own
   more specific governing instruction.

## Consequences
A replacement agent starts with strictly less "memory" than the failed agent had, trading continuity for
safety. This is a deliberate, flagged departure from a literal reading of the source text (see
`context-migration.md` for the explicit acknowledgment of this departure).

## Reversibility
Reversible as a policy (could be relaxed later), but relaxing it reintroduces the exact risk Step 1 Section
23 was written to prevent — any future change to this ADR should require equally explicit justification.
