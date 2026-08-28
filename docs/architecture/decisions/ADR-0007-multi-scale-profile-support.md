# ADR-0007 — Support Multiple Named Scale Profiles Instead of One Hardcoded Volume Assumption

**Status:** ACCEPTED
**Source IDs:** SRC-000044, SRC-000051 (CONFLICT-001)
**Requirements:** N/A (cross-cutting architectural property)

## Context
The source gives two incompatible daily-lead-volume figures (15,000/day vs. 1.5-2.5M/day, CONFLICT-001) with
no reconciliation, and never recomputes agent/cost sizing for the larger figure (CONFLICT-002).

## Decision
The canonical architecture (`scaling-scenarios.md`) treats both figures as named, independently valid SCALE
PROFILES (`freelance-narrow`, `full-firehose`) selectable via configuration, rather than picking one as "the"
true volume. Layer 0 (deterministic pre-filter) is architecturally present but only REQUIRED under the
`full-firehose` profile.

## Alternatives considered
1. Pick the larger, more recent figure as sole canonical target — rejected per the explicit "do not choose
   the largest number" / "do not choose the later version" prohibitions in Step 1 Section 4.
2. Pick the smaller figure as a conservative MVP target and discard the larger one entirely — rejected as
   discarding real user-stated scope-broadening intent (SRC-000050).

## Consequences
Every volume-dependent component (Layer 0, agent counts, cost models) must be profile-aware rather than
hardcoded, adding some design complexity in exchange for not guessing at unresolved user intent.

## Reversibility
Fully reversible/extensible — additional profiles could be added later without restructuring.
