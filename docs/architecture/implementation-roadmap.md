# Implementation Roadmap

Per Step 1 Section 39. Conceptual, dependency-aware phase sequence. **No phase is implemented in Step 1**
(Section 42's explicit prohibition). Phase numbering matches the Step 1 instruction's own list, used
consistently in `source-traceability.csv`'s `implementation_phase` column.

| Phase | Name | Depends on | What it covers (conceptually) |
|---|---|---|---|
| 0 | Source Preservation | — | Step 0 (complete). |
| 1 | Canonical Architecture | Phase 0 | Step 1 (this document set). |
| 2 | Data Foundation | Phase 1 | Real database technology chosen (`open-decisions.md` #7); `data-domains.md` translated into physical schema; `evidence-model.md`'s conceptual shape implemented. |
| 3 | Contracts and Events | Phase 2 | Real event-bus technology chosen (`open-decisions.md` #8); `events.md`'s payloads fully typed; the Intelligence→System B interface (`api-boundaries.md`) gets its first real contract. |
| 4 | Ingestion | Phase 3 | Lead Ingestion + Raw Payload Storage (`subsystems.md` #3-4) for the FIRST platforms per the chosen scale profile (`open-decisions.md` #1, #12). |
| 5 | Deterministic Triage | Phase 4 | Layer 0 (`subsystems.md` #5) — only required if `full-firehose` profile is the target (`open-decisions.md` #1). |
| 6 | Classification | Phase 4/5 | Client Intelligence, Technical Classification (`subsystems.md` #7, #11) — requires canonical archetype set + schema version decided (`open-decisions.md` #2, #4, #5). |
| 7 | Evidence and Verification | Phase 6 | Evidence Management, Verification (`subsystems.md` #12-13). |
| 8 | Platform Intelligence | Phase 4 | Channel + Platform Intelligence (`subsystems.md` #8-9), Source Discovery/Registry (#1-2). |
| 9 | Agent Runtime | Phase 2, 3 | Agent Orchestration, Agent Control Plane (`subsystems.md` #14, `agent-control-plane.md`) — first real running agents. |
| 10 | Dynamic Workers | Phase 9 | 5-Lead Rule implementation (`dynamic-worker-scaling.md`) — requires `open-decisions.md` #6 (real throughput target) to size correctly. |
| 11 | Sentinels | Phase 9 | Sentinel Plane (`sentinel-plane.md`) — **blocked in part by `open-decisions.md` #15** (drift formula incomplete); can proceed using THRESH-005 alone in the interim. |
| 12 | Hot-Swap / Context Migration | Phase 11 | `hot-swap.md`, `context-migration.md`. |
| 13 | Metric Evolution | Phase 7, 9 | `metric-evolution.md` — requires `open-decisions.md` #14 (governance/review process). |
| 14 | Strategy Intelligence | Phase 6, 8 | System A's own prioritization use of Explore/Exploit (`strategy-learning.md`, `PROPOSED_EXTENSION`). |
| 15 | External Integrations | Phase 4, 9 | Real connector implementations for `external-systems.md`'s `UNSPECIFIED` items — AI provider, storage, scraping infra commitments (`open-decisions.md` #9). |
| 16 | Administration / Operations | Phase 11, 12 | Admin panel (`subsystems.md` #29), Audit (`subsystems.md` #28), Observability (`observability.md`). |
| 17 | Simulation | Phase 6-16 | Testing the full pipeline against historical/synthetic data before live scraping — **not described by the source at all**, `PROPOSED_EXTENSION`, but a prudent gate before Phase 18. |
| 18 | Testing / Load | Phase 17 | Validating the chosen scale profile actually performs as modeled (`scaling-scenarios.md`) — the first point at which the source's own illustrative figures get empirically checked. |
| 19 | Production | Phase 18 | Live operation. Delivers the Intelligence → System B output (`api-boundaries.md`'s highest-priority undefined interface, which MUST be resolved — `open-decisions.md` — before this phase can begin). |

## Explicit dependency notes

- **Phase 1 (this document set) does not commit to Phase 2's technology choices** — those remain
  `open-decisions.md` items, deliberately deferred rather than guessed at here.
- **Phases 5, 10, 15 branch based on `open-decisions.md` #1** (scale-profile choice) — a `freelance-narrow`
  launch could skip Phase 5 (Layer 0) entirely and use a much smaller Phase 15 connector roster than
  `full-firehose` would require.
- **Phase 11 has a known blocker** (`open-decisions.md` #15, the incomplete drift formula) that does not stop
  the phase entirely (THRESH-005's discrete failure-count condition remains usable on its own) but does limit
  it relative to what the source originally envisioned.
- **Phase 19 (Production) is gated on resolving the single most consequential open interface** — the
  Intelligence → System B contract — which has no source-derived answer at all and is pure
  `open-decisions.md` territory.

## What this roadmap deliberately does not do

Per Step 1 Section 39's explicit instruction, it does not implement any phase, does not commit to a specific
technology within any phase, and does not set calendar dates or resource estimates — it is a DEPENDENCY
ORDERING only.
