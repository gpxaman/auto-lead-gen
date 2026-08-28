# ADR-0005 — Metric Evolution Proposals Require Versioned Migration, Never Direct Mutation

**Status:** ACCEPTED
**Source IDs:** SRC-000037, SRC-000079
**Requirements:** REQ-000021

## Context
The source's Metric Evolution/Saturation Optimizer proposes new data fields to collect. Step 1 Section 25
explicitly instructs: "Metric evolution must not directly mutate production schemas without controlled
architecture/database migration."

## Decision
An ACCEPT outcome from the Metric Evolution flow (`metric-evolution.md`) produces a schema-change PROPOSAL,
not an immediate mutation. It must go through the same `schema-versioning.md` discipline as any other schema
change before becoming active.

## Alternatives considered
1. Allow the optimizer to auto-apply accepted metrics directly (closer to a literal reading of the source's
   autonomous-discovery framing) — rejected per Step 1's explicit governing instruction, which takes
   precedence over an unqualified reading of the older source PDF.

## Consequences
Requires a review/approval step (human or architectural gate) before any optimizer-proposed field becomes
part of the live schema — a deliberate friction point trading some autonomy for safety.

## Reversibility
Fully reversible (a process/governance decision, not a data-structure commitment).
