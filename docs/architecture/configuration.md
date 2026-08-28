# Configuration Architecture

Per Step 1 Section 18. Every configuration concept must be versionable; every configuration change must
create an auditable event.

## Source-defined configurable concepts

| Configuration domain | Concrete source values | Source IDs |
|---|---|---|
| Platform configuration | Per-platform rules/ban-triggers, native tools, interaction mechanics (SRC-000035) | SRC-000035 |
| Channel configuration | MOV, velocity, setup-time benchmarks per macro channel type | SRC-000035 |
| Client configuration | Archetype taxonomy (which of the 3 sets is active — CONFLICT-004) | SRC-000029, 025, 034 |
| Sub-domain configuration | 5-Lead Rule thresholds: spawn >5/day, retire <2/day over 7-day avg | THRESH-001/002 |
| Agent configuration | Per-tier agent counts, model routing (80% cheap/20% heavy split, page 16) | TABLE-004, TABLE-005 |
| Prompt configuration | The system-prompt drafts themselves (4 versions catalogued in `code-blocks.md`) | pages 7-8, 11-12, 14-15, 25-29 |
| Model configuration | Named example models (gpt-4o-mini, Claude 3.5 Sonnet, etc.) and their cost tiers | `agents.md` (Step 0) model-provider table |
| Rate limits | Not concretely specified beyond "API/rate limits" being a thing the Recon Engine should extract per-platform (page 1) | SRC-000001 |
| Spawn policies | THRESH-001 (>5 leads/day) | SRC-000036 |
| Retirement policies | THRESH-002 (<2 leads/day, 7-day avg) | SRC-000036 |
| Sentinel policies | THRESH-004 (D_t ≥ 0.85), THRESH-005 (≥3 consecutive failures) | SRC-000078 |
| Cost limits | Narrative figures only (~$3,500/month) — never expressed as an ENFORCEABLE limit in source | SRC-000045 |
| Token limits | Not specified as an enforceable limit | — |
| Metric policies | THRESH-006 (≥99.5% consistency over 72h → saturation-idle) | SRC-000079 |
| Pricing policy | `P_bid = 0.90 × P_market`, max 20% discount (System B, referenced only) | FORMULA-001, THRESH-007/008 |

## Versioning requirement

```
CONFIG-V1 → CONFIG-V2 → CONFIG-V3 ...
```

Every configuration domain above must support this versioning discipline. **Concretely, this means:** when
the user eventually decides, e.g., which client-archetype set (CONFLICT-004) or which schema version
(CONFLICT-003) is canonical, that decision becomes `CONFIG-V1` for that domain — not a retroactive edit of
the Step 0/1 source record (which stays immutable per the core project rule).

## Configuration change → audit event

Every configuration change must produce a `CONFIG_CHANGED` event (`events.md`), which triggers the Blue-Green
Update Flow (`data-flow.md`) for any downstream agent/subsystem depending on that config, and is recorded in
the Audit subsystem (`subsystems.md` #28). This is `INTERPRETATION` — the source's cascading-update
requirement (SRC-000037/038) implies this pattern but never explicitly frames it as "every config change is
an auditable event."

## Explicit gaps (not filled in)

- **No source-defined configuration STORAGE mechanism** (file? database table? feature-flag service?) —
  `INTERFACE_UNDEFINED`, deferred to `open-decisions.md`.
- **No source-defined authorization model** for who may change which configuration domain — `PROPOSED_EXTENSION`
  need, not addressed by source at all.
- **No source-defined default values** for several thresholds referenced only as formulas without stated
  defaults (e.g., FORMULA-002's incomplete drift-score weights α/β/γ) — cannot be configured with real
  defaults until FORMULA-002's `SOURCE_INCOMPLETE` status is resolved (which Step 1 explicitly does NOT do).
