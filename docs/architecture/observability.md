# Observability

Per Step 1 Section 31. Preserves source telemetry concepts; defines the conceptual observability plane. The
plane must remain independent enough that an unhealthy agent cannot erase its own history.

## Source telemetry concepts preserved

| Signal | Source |
|---|---|
| Agent health | Drift score, consecutive-failure count (THRESH-004/005) |
| Task health | Implied by Agent State Management / Task State tracking (`context-migration.md`) |
| Lead throughput | Implied by all the volume figures throughout `economic-model.md`/`scaling-scenarios.md` |
| Source freshness | Implied by "Platform Concentration Matrix... verifiabl[e proof]" needing to be current (SRC-000034) |
| Errors | Schema/validation errors (THRESH-005) |
| Latency | Cutover latency examples (<500ms target, 384ms example — SCHEMA-006); sub-60-second bid-response latency (System B, THRESH-010, referenced only) |
| Token usage | Explicit throughout the cost projections (TABLE-005/006) |
| Cost | Explicit throughout (`economic-model.md`) |
| Drift | THRESH-004, FORMULA-002 (incomplete) |
| Hallucination | Root cause classifications (e.g., `STRUCTURAL_HALLUCINATION`, SCHEMA-004) |
| Verification | Verification pass/fail (`evidence-model.md`) |
| Worker utilization | Implied by the 5-Lead Rule needing per-worker lead-count tracking (THRESH-001/002) |
| Queue depth | Implied by "current queue payloads" validation during Blue-Green updates (SRC-000038) |
| Configuration version | Implied by the versioning discipline (`configuration.md`) — not explicitly named as an observable signal by source |
| Model version | Explicit in telemetry schema examples (`model_signature`, SCHEMA-004/006) |
| Prompt version | Not explicitly named by source as a tracked signal, though the 4 distinct system-prompt DRAFTS in the source (see `code-blocks.md`) demonstrate prompts DO version over time in practice |

## The independence requirement — why it matters

Step 1 Section 31: "The observability plane must remain independent enough that an unhealthy agent cannot
erase its own history." This is architecturally the SAME independence principle `sentinel-plane.md` requires
of Sentinels, applied to telemetry storage specifically: if a hallucinating or compromised agent could delete
or rewrite its own past telemetry records, the entire Hot-Swap/audit chain (`hot-swap.md`, `subsystems.md`
#28) becomes untrustworthy, since a bad actor (or a sufficiently broken agent) could cover its own tracks.
Concretely, this means: telemetry writes are append-only, and an agent's write permission scope does not
extend to its own historical record once written.

## Relationship to Audit (`subsystems.md` #28)

Observability is the real-time/near-real-time SIGNAL layer; Audit is the durable, tamper-evident RECORD layer.
Every observability signal that matters for incident review (drift, hallucination, hot-swap events) also
feeds Audit — but Observability additionally covers OPERATIONAL signals (throughput, latency, cost) that
don't necessarily need audit-grade permanence, just monitoring-grade recency.

## Status

`SOURCE-DERIVED` for every individual signal listed (all trace to a real source concept), `PROPOSED_EXTENSION`
for the unified "Observability" subsystem framing itself (the source never names it as such) and for the
append-only/independence ENFORCEMENT mechanism (the NEED is source-implied via the Sentinel-independence
requirement generalized here; the specific mechanism is not source-specified).
