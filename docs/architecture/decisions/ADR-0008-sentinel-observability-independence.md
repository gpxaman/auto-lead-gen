# ADR-0008 — Sentinel and Observability Independence From the Agents They Observe

**Status:** ACCEPTED
**Source IDs:** SRC-000037, SRC-000039
**Requirements:** REQ-000018, REQ-000019

## Context
The source requires Sentinels to be independent auditors ("one agent which sole task is to prevent
hallunitations"), and Step 1 Section 31 explicitly requires that "an unhealthy agent cannot erase its own
history."

## Decision
Sentinel compute/state and Telemetry/Audit storage are architecturally isolated from the worker agents they
observe: no worker has write access to its own Sentinel-maintained drift-score history or its own telemetry/
audit trail (`sentinel-plane.md`, `observability.md`).

## Alternatives considered
1. Let each agent self-report its own health/telemetry without independent verification — rejected, defeats
   the entire purpose of the resilience plane and directly contradicts the source's explicit independence
   requirement.

## Consequences
Requires a genuinely separate execution/storage context for Sentinels vs. workers (not just a logical
separation within the same process), which is a real implementation cost accepted here because the source
and governing instructions both treat it as non-negotiable.

## Reversibility
Not recommended to reverse — this is a foundational safety property, not a convenience choice.
