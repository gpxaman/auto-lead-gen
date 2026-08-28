# Metric Evolution

Per Step 1 Section 25. Preserves the autonomous metric-discovery concept and its saturation thresholds
exactly, without letting metric evolution mutate production schemas directly.

## Conceptual flow

```
OBSERVATION            [Telemetry Optimizer inspects unstructured lead data — SRC-000037]
        ↓
ANOMALY                 [unexplained variance / information not captured by current schema — INTERPRETATION,
                          the source says "regularly inspects... to propose... new" fields but doesn't name
                          the trigger "anomaly" explicitly]
        ↓
METRIC PROPOSAL          [a new field/metric is proposed]
        ↓
EXPERIMENT               [PROPOSED_EXTENSION — the source never describes testing a proposed metric before
                          adopting it; this step is added because silently adding fields without any trial
                          period risks schema churn]
        ↓
EVALUATION                [PROPOSED_EXTENSION — assessing whether the experiment justified the new field]
        ↓
   ACCEPT  or  REJECT  or  NOTICE_ONLY  or  IDLE
```

## The 4 outcomes

| Outcome | Source basis | Meaning |
|---|---|---|
| ACCEPT | `INTERPRETATION` (implied — a useful proposed metric must eventually become part of the schema somehow) | The new field is queued for a versioned schema migration (see `schema-versioning.md` — NEVER an in-place mutation) |
| REJECT | `INTERPRETATION` | The proposal is judged not useful and discarded |
| NOTICE_ONLY | `SOURCE-DERIVED` (SRC-000037: "if certain specs... is useless means it will put it as notice") | The optimizer publishes an administrative notice without adopting the metric — this is the user's OWN explicitly-requested behavior, distinct from a simple reject |
| IDLE | `SOURCE-DERIVED` (SRC-000037: "and remains ideal" [sic, "idle"]; formalized as `CHANNEL_DATA_SATURATED_IDLE_ACTIVE`, SRC-000079) | The optimizer stops proposing new metrics for a channel entirely once saturation is reached |

## Saturation threshold — preserved exactly

`≥ 99.5%` consistency/completeness, measured over a `72-hour window` (THRESH-006, SRC-000079). Not changed,
not rounded, not re-derived.

## Hard constraint: no direct schema mutation

Per Step 1 Section 25's explicit instruction: "Metric evolution must not directly mutate production schemas
without controlled architecture/database migration." This means an ACCEPT outcome above does NOT immediately
alter the live `UnifiedLeadEntity` schema — it produces a PROPOSAL that must go through the same versioned-
migration discipline as any other schema change (`schema-versioning.md`'s `OLD DATA → VERSIONED
TRANSFORMATION → NEW DATA` pattern), which in a real system implies human/architectural review before
becoming CONFIG-V(n+1) or SCHEMA-V(n+1). This is `INTERPRETATION` of Step 1's instruction, not something the
original source PDF itself states (the source is silent on WHETHER metric-optimizer proposals auto-apply or
require review — Step 1's governing instructions fill this gap explicitly, and this document follows them).

## Relationship to Telemetry (subsystem #21) and Configuration (#27)

Metric Evolution CONSUMES Telemetry data (to detect what's missing) and PRODUCES Configuration-domain change
proposals (new schema fields are, in effect, a configuration/schema-version change) — it does not own either
subsystem itself.
