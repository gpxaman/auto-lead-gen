# Hot-Swap

Per Step 1 Section 24. The original worker's historical state must remain available for audit.

## The full sequence

```
FAILURE DETECTION       [Sentinel: D_t ≥ 0.85 OR ≥3 consecutive errors — THRESH-004/005]
        ↓
QUARANTINE               [CEASE_OPERATIONS issued — SRC-000078 step 1]
        ↓
STATE CHECKPOINT          [worker's active state frozen/serialized — SRC-000078 step 3]
        ↓
SAFE-STATE EXTRACTION     [filter per context-migration.md's state-class table: TRUSTED/VALIDATED/CONFIG/
                            CHECKPOINT states extracted for reuse]
        ↓
UNSAFE-STATE ISOLATION    [MODEL INFERENCE and FAILED OUTPUT routed to incident log only, NOT to replacement
                            — context-migration.md's core rule]
        ↓
REPLACEMENT CREATION      [clean fallback agent instantiated — SRC-000078 step 4; source explicitly allows
                            "an alternate model provider" per SCHEMA-006's example: openai → anthropic]
        ↓
CONTEXT MIGRATION         [safe-state handed to the new agent — see context-migration.md]
        ↓
VALIDATION                [the replacement is itself checked before going live — PROPOSED_EXTENSION, since the
                            source doesn't explicitly say the replacement is validated before activation, only
                            that the old worker was]
        ↓
ACTIVATION                [replacement resumes the message bus — source cites <500ms target / 384ms example
                            cutover_latency_ms in SCHEMA-006]
        ↓
OLD-WORKER RETIREMENT     [old worker fully stood down, but its incident record + historical state remains
                            queryable — Step 1 Section 24's explicit requirement]
```

Status: `SOURCE-DERIVED` for every step except the explicitly-flagged "VALIDATION" step, which is
`PROPOSED_EXTENSION` — added because activating an unvalidated replacement (which could itself be
misconfigured) without any check would undermine the entire point of the resilience plane.

## Why the old worker's state must remain queryable (audit requirement)

This is explicit in Step 1 Section 24 and is architecturally necessary for:
1. **Admin panel review** — SRC-000037/078's "pin that ai in the admin panel" requirement only has value if
   the pinned incident's full context remains inspectable after the fact, not just a summary.
2. **Pattern detection** — if the SAME model/provider repeatedly triggers Hot-Swap across many workers, this
   is only detectable if historical incident records persist and are queryable in aggregate (feeds
   `observability.md`).
3. **Post-hoc correction of downstream data** — if a quarantined worker's UNTRUSTED STATE later turns out to
   have already leaked into some CANONICAL KNOWLEDGE record before quarantine was triggered, having the full
   historical record is what makes it possible to trace and correct that leak.

## Data contract used

`SCHEMA-004` (v1, `FAILOVER_HOTSWAP_TRIGGERED`) and `SCHEMA-006` (v2, `FAILOVER_HOTSWAP_DISPATCHED`) are BOTH
preserved as valid historical/candidate telemetry contracts for this flow — see `schema-versioning.md` and
CONFLICT-003. Neither is chosen as canonical in Step 1.

## Explicit non-implementation

No actual failover infrastructure, message bus, or agent runtime is built in Step 1 (Section 42). This
document is the conceptual sequence a future implementation must realize.
