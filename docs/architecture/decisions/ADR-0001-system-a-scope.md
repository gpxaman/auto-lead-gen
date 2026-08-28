# ADR-0001 — Scope IECHM-LIOS to System A (Lead Intelligence) Only

**Status:** ACCEPTED (as this project's current working scope; open to explicit user revision — see
`docs/architecture/open-decisions.md` item 3)
**Source IDs:** SRC-000002, SRC-000027, SRC-000070
**Requirements:** REQ-000001, REQ-000012

## Context
The source conversation describes 3 systems (recon/intelligence, bidding/proposal, manufacturing/execution)
with a scope boundary that is clear at the outset (page 1) but blurs by the end of the conversation
(CONFLICT-007). Separately, and more authoritatively for THIS repository, the actual Step 0 and Step 1
instructions governing this build both explicitly and repeatedly restrict deliverables to "specification,"
"architecture," and "blueprint" — never agent runtime, bidding execution, or machine control.

## Decision
IECHM-LIOS is scoped to System A only: lead discovery, classification, evidence-tracked intelligence, and
structured strategic output. System B (bidding) and System C (manufacturing) are documented as external,
referenced systems with `INTERFACE_UNDEFINED` boundaries, not built inside this repository.

## Alternatives considered
1. Scope IECHM-LIOS to include System B's architecture too (since the source's own later sections build it
   out extensively) — rejected because it contradicts the explicit, more recent, more specific governing
   instructions for this repository (Step 0/Step 1), which take precedence over an ambiguous internal
   scope-drift in the older source PDF transcript.
2. Scope IECHM-LIOS to all 3 systems as one monolithic "IECHM-OS" — rejected for the same reason, and because
   it would conflate risk profiles (a read-only intelligence system vs. one that transacts and dispatches
   physical manufacturing) inappropriately.

## Consequences
- The Intelligence → System B output contract (`api-boundaries.md`) becomes the single most important
  undefined interface this project must eventually specify.
- Every System B/C concept in the source (pricing engine, Sanitizer/Strategist/Writer/Reviewer, Estimator/
  Dispatch agents) is preserved for traceability/reference but not designed further within this repository.

## Reversibility
Fully reversible — this is a scope decision, not a data-destructive one. If the user wants System B/C
included, subsequent steps can extend the architecture without discarding anything built for System A.
