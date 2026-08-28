# Agent Topology

Per Step 1 Section 12. Preserves every source-derived named agent role — no arbitrary new agents added.
Classifies each as AI AGENT / WORKER / ORCHESTRATOR / SENTINEL / DETERMINISTIC SERVICE / CONNECTOR /
SCHEDULED PROCESS, using `CLASSIFICATION_UNRESOLVED` where the source doesn't make this clear. **Scope note:**
per `system-boundaries.md`, only agents belonging to System A (IECHM-LIOS) are given full topology detail
here; System B/C agents (Sanitizer, Strategist, Writer, Reviewer, Estimator, Dispatch) are listed for
completeness/interface-awareness but marked out-of-scope.

**Naming note:** to avoid the source's own Layer-numbering collision (see `canonical-architecture.md`), this
document uses **Tier 1-4** for agent-hierarchy depth, reserving "Layer 0-4" for the data-pipeline-stage
model.

## Tier 0 — Central Director Agent

- **Role:** Top-level orchestrator of the entire agent hierarchy. **Source IDs:** SRC-000075 (page 27 org
  chart shows `[ CENTRAL DIRECTOR AGENT ]` at the apex). **Layer:** cross-cutting (controls all). **Parent:**
  none. **Responsibilities:** allocate/oversee Tier 1-4 teams; receive cascading-update triggers. **Inputs:**
  configuration changes, high-level strategy decisions. **Outputs:** directives to Tier 1-3 teams. **Tools:**
  not specified. **Knowledge:** not specified. **Memory:** not specified. **Events consumed:** `CONFIG_CHANGED`.
  **Events emitted:** cascading update triggers. **Health signals:** not specified by source (a genuine gap —
  who monitors the Director itself is unaddressed). **Failure modes:** single point of failure, unaddressed
  by source. **Replacement behavior:** not specified. **Configuration dependencies:** all. **Permissions:**
  implied full control. **Classification:** `ORCHESTRATOR`. **Status:** `SOURCE-DERIVED` (existence), most
  operational detail `UNRESOLVED`/gap in source.

## Tier 1 — Client Classification Swarm

- **Role:** classify buyer archetype, track concentration/proof. **Source IDs:** SRC-000033, SRC-000034.
  **Layer:** 1. **Parent:** Central Director. **Responsibilities:** REQ-000013, REQ-000016. **Inputs:**
  sanitized leads. **Outputs:** client archetype assignments. **Tools:** not specified (implied: LLM +
  classification schema). **Knowledge:** client archetype definitions (CONFLICT-004, multiple sets).
  **Memory:** not specified. **Events consumed:** none named. **Events emitted:** `CLIENT_CLASSIFIED`
  (`PROPOSED_EVENT`). **Health signals:** covered by Sentinel Plane generally. **Failure modes:**
  misclassification. **Replacement behavior:** standard Hot-Swap. **Configuration dependencies:** archetype
  taxonomy version. **Permissions:** read leads, write classification. **Classification:** `AI AGENT`.
  **Count:** 2-3 agents (source-stated, fixed regardless of scale — SRC-000033: "does not need more than
  few agents"). **Status:** `SOURCE-DERIVED`.

## Tier 2 — Macro Channel Controller Teams

- **Role:** govern one macro channel type (Freelance, B2B Trade, Community, Brokerage, On-Demand Mfg,
  Outbound). **Source IDs:** SRC-000038, TABLE-004. **Layer:** 2. **Parent:** Central Director.
  **Responsibilities:** REQ-000017 (channel-level fields), Source/Channel Intelligence subsystems.
  **Inputs:** platform-level aggregate data. **Outputs:** channel benchmarks. **Tools:** not specified.
  **Knowledge:** channel-type taxonomy (itself ambiguous across 4/8/5/6-category source variants — see
  `terminology.md` "Macro Channel"). **Memory:** not specified. **Events:** none named specifically.
  **Health signals:** Sentinel Plane. **Failure modes:** stale benchmarks. **Replacement behavior:** standard
  Hot-Swap. **Configuration dependencies:** channel-type taxonomy version. **Permissions:** read platform
  data, write channel benchmarks. **Classification:** `AI AGENT` team (`ORCHESTRATOR`-like at the team level).
  **Count:** 2 agents per team × 6 teams = 12 agents (TABLE-004; note the 6-team figure itself is only one of
  4 differing macro-category counts in the source — see `terminology.md`). **Status:** `SOURCE-DERIVED`.

## Tier 3 — Platform Worker Agents

- **Role:** dedicated per-platform recon/profile-maintenance agent. **Source IDs:** SRC-000038, TABLE-004,
  page 27 org chart ("Upwork Worker Agent," "Alibaba RFQ Worker Agent"). **Layer:** 3. **Parent:** relevant
  Tier 2 team. **Responsibilities:** REQ-000017 (platform-level fields), Platform Intelligence subsystem.
  **Inputs:** raw listings for its platform. **Outputs:** platform profile, lead records. **Tools:** the
  platform's scraper/API connector. **Knowledge:** platform-specific rules/culture (SRC-000035). **Memory:**
  not specified. **Events:** ingestion events. **Health signals:** Sentinel Plane. **Failure modes:**
  platform-side blocking, rule changes. **Replacement behavior:** standard Hot-Swap. **Configuration
  dependencies:** platform connector config. **Permissions:** read-only external access to its platform.
  **Classification:** `AI AGENT` + `CONNECTOR` (the scraping mechanism itself is a `CONNECTOR`/deterministic
  component; the parsing/classification is `AI AGENT`). **Count:** 1 per platform, ~75 at full scale.
  **Status:** `SOURCE-DERIVED`.

## Tier 4 — Sub-Domain Worker Agents (dynamic)

- **Role:** granular per-sub-domain recon agent, spawned/retired dynamically. **Source IDs:** SRC-000036,
  page 27 org chart ("DYNAMIC SPAWN ENGINE"). **Layer:** 4. **Parent:** relevant Tier 3 worker. **Responsibilities:**
  REQ-000015, Sub-domain Intelligence subsystem. **Inputs:** sub-domain-specific content. **Outputs:**
  sub-domain lead records. **Tools:** inherited from parent Tier 3 worker's connector, specialized for the
  sub-domain. **Knowledge:** sub-domain jargon/compliance parsers (SRC-000036: "inherits the specialized
  persona, sub-domain terminology, specific compliance constraints"). **Memory:** not specified. **Events
  consumed:** `SUBDOMAIN_SPAWN_TRIGGERED`. **Events emitted:** `SUBDOMAIN_RETIRE_TRIGGERED` when its own
  velocity drops. **Health signals:** Sentinel Plane. **Failure modes:** spawn thrashing (see
  `dynamic-worker-scaling.md`). **Replacement behavior:** standard Hot-Swap, OR retirement (a distinct,
  non-failure lifecycle exit) — see `context-migration.md` for why these two exits must be handled
  differently. **Configuration dependencies:** 5-Lead Rule thresholds (THRESH-001/002). **Permissions:**
  same as parent, scoped to sub-domain. **Classification:** `AI AGENT`. **Count:** dynamic, ~30-50 estimated
  at `freelance-narrow` scale (TABLE-004); unestimated at `full-firehose` scale (CONFLICT-002). **Status:**
  `SOURCE-DERIVED`.

## Cross-Cutting: Hallucination Sentinel (one per layer/tier)

- **Role:** independent anomaly/hallucination auditor. **Source IDs:** SRC-000037, SRC-000039. **Layer:**
  cross-cutting, logically independent of the tier it observes. **Parent:** none (independence is the point).
  **Responsibilities:** REQ-000018, REQ-000019. **Inputs:** worker outputs. **Outputs:** drift scores,
  incident reports. **Tools:** schema validators (Pydantic/Zod-style — deterministic). **Knowledge:** validity
  rules per data type. **Memory:** drift-score history. **Events consumed:** worker output events. **Events
  emitted:** `CEASE_OPERATIONS`, incident/admin-pin events. **Health signals:** unaddressed by source (gap —
  "who watches the Sentinel" is not answered). **Failure modes:** the gap above. **Replacement behavior:**
  unaddressed by source. **Configuration dependencies:** drift/failure thresholds (THRESH-004/005).
  **Permissions:** read worker output, issue kill signals. **Classification:** `SENTINEL` (explicitly its own
  category, distinct from `AI AGENT` — the source itself frames Sentinels as auditors, not task-performing
  agents). **Count:** "1 Auditor per 5 workers" + 1 per architectural layer (TABLE-004: 20-55 agents).
  **Status:** `SOURCE-DERIVED`.

## Cross-Cutting: Hot-Swap Failover Engine

- **Role:** execute quarantine→migrate→replace protocol. **Source IDs:** SRC-000078. **Layer:** cross-cutting.
  **Classification:** `DETERMINISTIC SERVICE` (the 4-step protocol is deterministic logic, not an LLM
  judgment call — the SENTINEL decides WHETHER to trigger it, but the engine itself executes mechanically).
  **Count:** 1 (implied singleton, or 1 per layer — source ambiguous). **Status:** `SOURCE-DERIVED`.

## Cross-Cutting: Telemetry / Metric Evolution & Saturation Optimizer

- **Role:** propose new metrics, self-idle at saturation. **Source IDs:** SRC-000037, SRC-000079. **Layer:**
  cross-cutting. **Classification:** `AI AGENT` (the metric-proposal function requires judgment, hence LLM-
  based) with a `DETERMINISTIC SERVICE` component (the 99.5%/72h threshold check itself). **Count:** 1
  (source implies a single "Telemetry Engine," TABLE-004 folds it into the 20-55 sentinel/optimizer count).
  **Status:** `SOURCE-DERIVED`.

## Out-of-scope agents (System B/C — referenced only, not built by IECHM-LIOS)

| Agent | Source | System | Classification |
|---|---|---|---|
| Sanitizer | SRC-000001 | B | `AI AGENT` |
| Strategist | SRC-000006 | B | `AI AGENT` |
| Writer | SRC-000005 | B | `AI AGENT` |
| Reviewer | SRC-000005 | B | `AI AGENT` |
| Estimator Agent | SRC-000066 | C | `AI AGENT` + `CONNECTOR` (cloud slicer integration) |
| Dispatch Agent | SRC-000066 | C | `SCHEDULED PROCESS`/`DETERMINISTIC SERVICE` (source describes it as reactive to `EVENT_CONTRACT_SIGNED`, not requiring ongoing LLM judgment — `CLASSIFICATION_UNRESOLVED` between these two) |
| Account Management Agent (re-order trigger) | SRC-000069 | B | `SCHEDULED PROCESS` (Day-25 trigger is time-based) + `AI AGENT` (drafting the outreach message) |

## Full-scale headcount cross-reference

TABLE-004 (Step 0) gives 140-195 total agents for the `freelance-narrow` scale profile. This document's
per-tier counts sum to: 1 (Director) + 2-3 (Tier 1) + 12 (Tier 2) + 75 (Tier 3) + 30-50 (Tier 4) + 20-55
(Sentinels/Optimizers) = **140-196**, consistent with the source's own total. No agent was added or removed
in producing this topology — it is a restatement/reorganization of TABLE-004 with full per-role detail added.
