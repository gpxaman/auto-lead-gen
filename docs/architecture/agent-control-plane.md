# Agent Control Plane

Per Step 1 Section 13. Conceptual definition only — no runtime is implemented in Step 1 (Section 42).

## Required control-plane operations

| Operation | Source basis | Status |
|---|---|---|
| Agent registration | Implied by Agent Orchestration needing to know which agents exist (`subsystems.md` #14) | `PROPOSED_EXTENSION` — never named explicitly in source |
| Agent provisioning | Implied by dynamic spawning (5-Lead Rule) and Blue-Green ephemeral worker provisioning | `SOURCE-DERIVED` (SRC-000038: "provision a parallel ephemeral worker unit") |
| Agent activation | Implied by the spawn→validate→cutover sequence in Blue-Green updates | `SOURCE-DERIVED` (implicit in SRC-000038) |
| Task assignment | Implied by Central Director → Tier 1-4 routing | `SOURCE-DERIVED` (implicit, org-chart structure) |
| Heartbeat | Not named by source at all | `PROPOSED_EXTENSION` — required for Sentinel/Hot-Swap to know an agent is unresponsive vs. quiet |
| Health | Drift score, consecutive-failure count | `SOURCE-DERIVED` (THRESH-004/005) |
| Configuration | Per-agent config dependencies noted throughout `agent-topology.md` | `SOURCE-DERIVED` (individual values) / `PROPOSED_EXTENSION` (unified delivery mechanism) |
| Pause | Not named by source | `PROPOSED_EXTENSION` — needed as a softer alternative to full `CEASE_OPERATIONS` |
| Drain | Closest source analogue: sub-domain retirement ("safely drained, serialized," SRC-000036/page 14) | `SOURCE-DERIVED` for sub-domain workers specifically; `PROPOSED_EXTENSION` if generalized to all agent types |
| Quarantine | `CEASE_OPERATIONS` + admin-panel pinning | `SOURCE-DERIVED` (SRC-000078) |
| Replacement | Hot-Swap protocol | `SOURCE-DERIVED` (SRC-000078) |
| Retirement | Sub-domain deprecation (<2 leads/day, 7-day average) | `SOURCE-DERIVED` for sub-domain workers (THRESH-002); `PROPOSED_EXTENSION` for other tiers (source never describes retiring a Tier 1-3 agent, only Tier 4) |
| State migration | Context Migration subsystem | `SOURCE-DERIVED` (SRC-000037) |
| Cost limits | Not named as a control-plane operation by source (cost is discussed narratively, not as an enforceable limit) | `PROPOSED_EXTENSION` |
| Token limits | Not named by source | `PROPOSED_EXTENSION` — necessary given the source's own emphasis on token-cost control via Layer 0/saturation-idling, even though it never frames this as a per-agent limit |
| Spawn limits | Not named explicitly, though "Maximum workers" is implied by any bounded-cost design | `PROPOSED_EXTENSION` |

## Why several of these are `PROPOSED_EXTENSION`, not gaps to silently fill from "common sense"

The source's agent-architecture discussion is a brainstorming transcript focused on WHAT the agents should DO
(classify, spawn, fail over) rather than HOW a control plane operationally manages them (heartbeats, pause/
resume, spend caps). This is a genuine, honest gap — not a case where the answer is "obviously" implied and
this document is just being pedantic about labeling it. A real control plane cannot be built from the source
alone; the `PROPOSED_EXTENSION` items above are the concrete list of what Step 2+ needs to design from
scratch, informed by (but not dictated by) the source.

## Conceptual control-plane responsibility boundary

The control plane is a `PROPOSED_EXTENSION` SUBSYSTEM as a whole (the source never names "the control plane"
as such), but it is not inventing new BEHAVIOR — it is the necessary operational substrate for behaviors the
source DOES specify (spawning, health-based failover, state migration, cascading updates). Its existence is
therefore `INTERPRETATION` (a structural necessity implied by explicit source requirements), while its
specific operation list mixes `SOURCE-DERIVED` (heartbeat/health/quarantine/replacement/migration — directly
named) and `PROPOSED_EXTENSION` (registration/pause/cost-and-token-limits/spawn-limits — not named, but
required to make the source-named behaviors safely operable).

## No runtime implementation

Per Step 1 Section 13's explicit instruction and Section 42's prohibition, this document defines WHAT the
control plane must eventually support, not HOW it is coded, deployed, or which technology implements it
(that is `INTERFACE_UNDEFINED` / deferred to `docs/architecture/open-decisions.md`).
