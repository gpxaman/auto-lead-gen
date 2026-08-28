# Sentinel Plane

Per Step 1 Section 21. The sentinel plane must be logically independent from the worker it observes — this is
a first-class architectural requirement, not a nicety.

## Conceptual flow

```
WORKER
    ↓
SENTINEL                  [independent process/agent — SRC-000037: "one agent which sole task is..."]
    ↓
VALIDATION                [schema compliance, URL/endpoint verification, numeric sanity — SRC-000039]
    ↓
DRIFT / ANOMALY           [drift score D_t, FORMULA-002 — SOURCE_INCOMPLETE]
    ↓
INCIDENT                  [logged: worker ID, model telemetry, error log — SCHEMA-004/006]
    ↓
QUARANTINE                [CEASE_OPERATIONS — SRC-000078]
    ↓
STATE PRESERVATION        [see context-migration.md]
    ↓
REPLACEMENT               [see hot-swap.md]
    ↓
VALIDATION                [the replacement itself must be checked before activation]
    ↓
RESUME                    [message bus resumes, <500ms / 384ms example latency]
```

Status: `SOURCE-DERIVED` throughout, synthesized from SRC-000037/039/078 and SCHEMA-004/006 into one linear
flow (the source describes these pieces separately across pages 13-15, 26, 28-29; this document is the first
place they are shown as one continuous pipeline — `INTERPRETATION` for the SEQUENCING/synthesis, though every
individual step is `SOURCE-DERIVED`).

## Independence requirement, explicit design consequence

"Independent" here means, at minimum:
1. A Sentinel's own compute/execution context is NOT shared with the worker(s) it observes (so a
   worker-level failure/hallucination cannot directly corrupt the Sentinel's judgment).
2. A Sentinel's drift-score history and incident log are stored OUTSIDE the worker's own state (consistent
   with Step 1 Section 31's explicit requirement that "an unhealthy agent cannot erase its own history" —
   applied here specifically to Sentinel independence, not just general telemetry).
3. Sentinel validation logic is explicitly `DETERMINISTIC` where possible (schema/URL/numeric checks, per
   SRC-000039 — "Pydantic / Zod contracts" are deterministic, not LLM judgment calls), reducing the chance
   that a Sentinel itself hallucinates about whether a worker hallucinated.

All 3 points are `INTERPRETATION` (necessary consequences of the source's stated independence requirement)
rather than `SOURCE-DERIVED` verbatim statements, since the source asserts independence as a design goal
without spelling out the specific isolation mechanisms.

## Thresholds — preserved exactly, treated as configurable policy

- `D_t ≥ 0.85` (THRESH-004) — continuous drift-score trigger.
- `≥ 3` consecutive schema/validation errors (THRESH-005, also called `τ_drift ≥ 3` on page 14) — discrete
  failure-count trigger.
- Per `terminology.md` "Drift" entry: these are treated as two INDEPENDENT OR-conditions (either one alone is
  sufficient to trigger quarantine) since the source states both as sufficient triggers without ever
  clarifying whether they're meant to be equivalent expressions of the same underlying signal or genuinely
  separate checks. **Not silently resolved into a single formula** — both thresholds are preserved and BOTH
  are checked in the canonical flow above.

## Genuine gap: who watches the Sentinel

The source never addresses Sentinel-level failure (a Sentinel itself being wrong, compromised, or down). This
is recorded as an open gap in `agent-topology.md`'s Sentinel entry and NOT filled in here with an invented
"meta-sentinel" layer, since the source gives no basis for designing one.

## Sizing

"1 Auditor per 5 workers" plus "1 per architectural layer" (TABLE-004: 20-55 agents in this role band).
`SOURCE-DERIVED`, illustrative sizing only (see `scaling-scenarios.md` for why this figure is scoped to the
`freelance-narrow` profile specifically and not re-derived for `full-firehose`, per CONFLICT-002).
