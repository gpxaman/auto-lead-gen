# Major Subsystems

Per Step 1 Section 11. All 30 required subsystems evaluated. Fields per subsystem: purpose, source IDs,
requirements, layer, inputs, outputs, owned state, dependencies, events, agents, deterministic components,
failure modes, security requirements, observability, scaling requirements, status. Status values follow
`source-vs-canonical.md`'s taxonomy (`SOURCE-DERIVED` / `INTERPRETATION` / `PROPOSED_EXTENSION`).

### 1. Source Discovery
Purpose: find new candidate platforms/sub-domains not yet in the registry. Source IDs: SRC-000014-000022.
Requirements: REQ-000010, REQ-000011. Layer: 2-3 (macro-channel and platform level). Inputs: web search,
user-supplied platform lists, macro-channel-team exploration. Outputs: candidate platform records for Source
Registry. Owned state: discovery candidate queue. Dependencies: none upstream. Events: `PLATFORM_DISCOVERED`
(`PROPOSED_EVENT`). Agents: Macro Channel Team agents (2-agent teams per channel type, SRC-000038).
Deterministic components: none named in source. Failure modes: false-positive discovery (non-viable platform).
Security requirements: standard web-fetch hygiene. Observability: discovery rate per channel type. Scaling:
bounded by channel-team count (fixed, ~6 teams per TABLE-004). Status: `SOURCE-DERIVED`.

### 2. Source Registry
Purpose: canonical, versioned list of all known platforms/sub-domains and their status (active/deprecated).
Source IDs: SRC-000021, SRC-000022, `platforms.md` (Step 0). Requirements: REQ-000010, REQ-000017. Layer:
2-3. Inputs: Source Discovery output, manual entries. Outputs: platform list consumed by Layer 3 workers.
Owned state: platform registry table. Dependencies: Source Discovery. Events: `PLATFORM_REGISTERED`,
`PLATFORM_DEPRECATED` (`PROPOSED_EVENT`). Agents: none (registry is data, not an agent). Deterministic
components: registry CRUD. Failure modes: stale/duplicate entries. Security requirements: write-access
control. Observability: registry size/growth over time. Scaling: linear with platform count (bounded, ~75-100
per source estimates). Status: `SOURCE-DERIVED` (as a concept) / `PROPOSED_EXTENSION` (as a formal subsystem
name — the source never names "Source Registry" explicitly, it is implied by the platform lists).

### 3. Lead Ingestion
Purpose: retrieve raw listing/RFQ content from a platform. Source IDs: SRC-000009, SRC-000013. Requirements:
REQ-000009. Layer: 0. Inputs: platform URLs from Source Registry. Outputs: raw HTML/text payload. Owned
state: none persistent (pass-through). Dependencies: Source Registry, stealth scraper infrastructure
(Playwright/Firecrawl, named as examples). Events: `RAW_LEAD_INGESTED` (`PROPOSED_EVENT`). Agents: Platform
Worker agents (Layer 3/Tier 3). Deterministic components: the scraper itself (not an LLM). Failure modes:
anti-bot blocking, rate limiting, Cloudflare/WAF challenges. Security requirements: credential handling for
any authenticated platforms (not detailed in source). Observability: ingestion success rate per platform.
Scaling: one worker per platform, dynamically expandable per sub-domain (5-Lead Rule). Status:
`SOURCE-DERIVED`.

### 4. Raw Payload Storage
Purpose: persist the raw scraped content prior to any AI processing, for auditability and reprocessing.
Source IDs: SRC-000009, SRC-000013 (implied — the source's pipeline diagram shows a distinct "Raw Listing
Payload" stage). Requirements: (implied by REQ-000009). Layer: 0. Inputs: Lead Ingestion output. Outputs: raw
payload records for Deterministic Triage. Owned state: raw payload store. Dependencies: Lead Ingestion.
Events: none named. Agents: none (deterministic). Deterministic components: storage write. Failure modes:
storage exhaustion at `full-firehose` scale (millions/day). Security requirements: raw untrusted content must
be stored as data, never executed. Observability: storage volume/retention. Scaling: must handle
`full-firehose` profile volume (1.5-2.5M/day) — a genuine capacity concern not addressed by the source at all.
Status: `SOURCE-DERIVED` (existence of the stage) / `PROPOSED_EXTENSION` (retention policy, not specified by
source).

### 5. Deterministic Triage (Layer 0)
Purpose: non-AI filtering of raw payloads — keyword blacklist/whitelist, budget sanity, location routing.
Source IDs: SRC-000012, SRC-000053. Requirements: REQ-000008, REQ-000029. Layer: 0. Inputs: Raw Payload
Storage. Outputs: triaged payloads (pass/reject) for Security/Sanitization or direct classification. Owned
state: blacklist/whitelist term lists (partially truncated in source, see `manufacturing-capabilities.md`).
Dependencies: Raw Payload Storage. Events: `LEAD_REJECTED_LAYER0` (`PROPOSED_EVENT`). Agents: none
(deterministic, explicitly "Traditional Code" per SRC-000053, not an LLM). Deterministic components: the
entire subsystem. Failure modes: over-aggressive filtering (false negatives — rejecting viable leads);
incomplete blacklist (source's own blacklist array is truncated, THRESH-015). Security requirements: must not
be bypassable by adversarial input designed to evade keyword matching. Observability: reject rate, reject
reason breakdown. Scaling: must handle full raw intake volume at low per-item cost (the source's entire
rationale for this subsystem, SRC-000053). Status: `SOURCE-DERIVED`. **Only required for `full-firehose`
scale profile** — see `scaling-scenarios.md`.

### 6. Security/Sanitization (recon-data variant)
Purpose: detect prompt-injection or adversarial content WITHIN scraped listing text before it reaches
LLM-based classifiers (Layers 1-4). Source IDs: SRC-000001, SRC-000030, SRC-000039 (the Hallucination
Sentinel's validation directives are the closest source analogue). Requirements: REQ-000019, REQ-000030.
Layer: 0-1 boundary. Inputs: triaged payloads. Outputs: sanitized payloads + flagged-injection records.
Owned state: injection-detection flags. Dependencies: Deterministic Triage. Events: `INJECTION_DETECTED`
(`PROPOSED_EVENT`). Agents: could be an LLM-based Sanitizer-equivalent, or folded into Layer 1 classification
— `CLASSIFICATION_UNRESOLVED`. Deterministic components: possibly a first-pass regex/keyword layer analogous
to Layer 0. Failure modes: missed injections corrupting downstream classification. Security requirements:
this IS the security requirement. Observability: injection-detection rate. Scaling: scales with Layer 0
output volume. Status: `INTERPRETATION` — the source's Sanitizer concept (SRC-000001) is explicitly a
System-B (bidding-brief) component; System A needs an analogous defense for its OWN scraped-content pipeline,
which the source never explicitly separates out as a distinct subsystem. This entire subsystem entry is
therefore `INTERPRETATION`, not `DIRECT_MAPPING`, per `source-concept-mapping.md`.

### 7. Client Intelligence
Purpose: classify buyer archetype, track pain point/motivation/MOV/platform-concentration with evidence.
Source IDs: SRC-000029, SRC-000025, SRC-000034 (3 archetype sets), SRC-000016. Requirements: REQ-000013,
REQ-000016. Layer: 1. Inputs: sanitized, classified leads. Outputs: client archetype assignment + profile
record. Owned state: client archetype registry, per-archetype profile detail. Dependencies: Security/
Sanitization, Evidence Management. Events: `CLIENT_CLASSIFIED` (`PROPOSED_EVENT`). Agents: Client
Classification Swarm (2-3 agents, SRC-000033). Deterministic components: none named. Failure modes:
misclassification; archetype-set ambiguity (CONFLICT-004). Security requirements: standard LLM output
validation (Sentinel plane). Observability: classification confidence, archetype distribution. Scaling: fixed
small team, does not scale with volume per source (SRC-000033: "does not need more than few agents"). Status:
`SOURCE-DERIVED`, canonical archetype set `NEEDS_USER_DECISION` (CONFLICT-004).

### 8. Channel Intelligence
Purpose: maintain macro-channel-type benchmarks (MOV, velocity, setup time, friction level). Source IDs:
SRC-000035. Requirements: REQ-000017. Layer: 2. Inputs: aggregated platform-level data. Outputs: channel
benchmark records. Owned state: channel benchmark table. Dependencies: Platform Intelligence (aggregates
upward from it). Events: `CHANNEL_BENCHMARK_UPDATED` (`PROPOSED_EVENT`). Agents: Macro Channel Team agents
(shared with Source Discovery, #1). Deterministic components: aggregation logic. Failure modes: stale
benchmarks. Security requirements: none specific. Observability: benchmark freshness. Scaling: one team per
macro channel type (~6 teams, fixed per TABLE-004). Status: `SOURCE-DERIVED`.

### 9. Platform Intelligence
Purpose: per-platform deep-dive profile (rules, tools, metrics, sub-domain index). Source IDs: SRC-000035.
Requirements: REQ-000017. Layer: 3. Inputs: Lead Ingestion + manual/researched platform rule data. Outputs:
platform profile records. Owned state: platform profile table. Dependencies: Source Registry. Events:
`PLATFORM_PROFILE_UPDATED` (`PROPOSED_EVENT`). Agents: one Platform Worker per platform (~75 at full scale,
TABLE-004). Deterministic components: none named. Failure modes: outdated platform-rule data (ban-trigger
phrases change). Security requirements: platform rules ARE security-relevant data (ban-trigger detection
feeds System B). Observability: per-platform data completeness. Scaling: 1:1 with platform count. Status:
`SOURCE-DERIVED`.

### 10. Sub-domain Intelligence
Purpose: granular per-sub-domain tracking with dynamic spawn/retirement. Source IDs: SRC-000036. Requirements:
REQ-000015. Layer: 4. Inputs: Platform Intelligence sub-domain index. Outputs: sub-domain-specific lead
records. Owned state: sub-domain agent registry, lead-velocity rolling averages. Dependencies: Platform
Intelligence. Events: `SUBDOMAIN_SPAWN_TRIGGERED`, `SUBDOMAIN_RETIRE_TRIGGERED` (`SOURCE-DERIVED` concepts,
event names `PROPOSED_EVENT`). Agents: dynamically spawned Sub-Domain Workers (Layer 4/Tier 4). Deterministic
components: the 5-Lead Rule threshold check itself is deterministic (a rolling-average calculation, not an
LLM judgment). Failure modes: spawn thrashing (rapid spawn/retire cycling near the threshold boundary — not
addressed by source; see `dynamic-worker-scaling.md` cooldown discussion). Security requirements: none
specific. Observability: active sub-domain worker count, spawn/retire event rate. Scaling: THIS is the
subsystem the 5-Lead Rule exists to bound (THRESH-001/002). Status: `SOURCE-DERIVED`.

### 11. Hardware/NPD Classification
Purpose: assign `ManufacturingDomain` and technical fields (CAD software, deliverables, project stage).
Source IDs: SRC-000010, SRC-000011. Requirements: REQ-000007. Layer: 1. Inputs: sanitized lead content.
Outputs: technical classification record. Owned state: none beyond the classification result itself
(persisted in the lead record). Dependencies: Security/Sanitization. Events: none named beyond classification
completion. Agents: could be the same Client Classification agents or a dedicated technical classifier —
`CLASSIFICATION_UNRESOLVED`. Deterministic components: enum validation (Pydantic-style). Failure modes:
domain misclassification, especially at the boundary flagged in CONFLICT-005 (buyer archetype vs. request
type conflation). Security requirements: standard output validation. Observability: classification confidence
per domain. Scaling: scales with lead volume. Status: `SOURCE-DERIVED`.

### 12. Evidence Management
Purpose: attach verifiable proof (URLs, listing hashes, screenshots, timestamps) to every claim. Source IDs:
SRC-000034 ("with verifiabl[e proof]"). Requirements: REQ-000016. Layer: cross-cutting. Inputs: raw
observations from any layer. Outputs: evidence-linked claims. Owned state: evidence artifact store.
Dependencies: none upstream (evidence can attach to any layer's output). Events: `EVIDENCE_ATTACHED`
(`PROPOSED_EVENT`). Agents: none dedicated (evidence-attachment is a cross-cutting responsibility of every
classifying agent). Deterministic components: hash computation, timestamp recording. Failure modes: evidence
gaps (unverifiable claims treated as verified — see `evidence-model.md` for why this must not happen
silently). Security requirements: evidence artifacts (e.g., stored HTML snapshots) are untrusted content and
must not be executed/rendered unsafely. Observability: evidence coverage rate (% of claims with attached
evidence). Scaling: scales with lead volume. Status: `SOURCE-DERIVED` (concept named) /
`PROPOSED_EXTENSION` (as a formal, unified subsystem — the source mentions "proof" repeatedly but never
designs an evidence subsystem).

### 13. Verification
Purpose: distinguish a raw claim from a verified fact (e.g., confirming a listed URL actually resolves and
matches the claimed content). Source IDs: SRC-000039 ("URL/Endpoint verification"). Requirements: REQ-000019.
Layer: cross-cutting. Inputs: Evidence Management artifacts. Outputs: verification status per claim.
Owned state: verification status flags. Dependencies: Evidence Management. Events: `VERIFICATION_COMPLETED`,
`VERIFICATION_FAILED` (`PROPOSED_EVENT`). Agents: Hallucination Sentinels perform this as part of their
validation directives. Deterministic components: URL-resolution checks, schema checks. Failure modes: false
verification (a URL resolves but content doesn't match the claim — not addressed by source). Security
requirements: verification fetches must be sandboxed (fetching untrusted URLs). Observability: verification
pass/fail rate. Scaling: scales with claim volume. Status: `SOURCE-DERIVED` (partial).

### 14. Agent Orchestration
Purpose: manage the full agent fleet's lifecycle (registration, provisioning, activation, task assignment).
Source IDs: SRC-000038, SRC-000075. Requirements: REQ-000015, REQ-000018. Layer: cross-cutting (controls all
layers). Inputs: agent-hierarchy configuration. Outputs: active agent instances, task assignments. Owned
state: agent registry, task queue. Dependencies: Configuration. Events: many (see `events.md`). Agents:
the Central Director Agent itself is part of this subsystem. Deterministic components: task-routing logic.
Failure modes: orchestration deadlock, runaway spawning. Security requirements: agent-permission boundaries
(agent-control-plane.md). Observability: agent count, task queue depth. Scaling: this subsystem itself must
scale to 140-195+ agents (TABLE-004) or more at `full-firehose` scale. Status: `SOURCE-DERIVED`. Full detail
in `agent-control-plane.md`.

### 15. Dynamic Worker Scaling
Purpose: implement the 5-Lead Rule spawn/retirement logic. Source IDs: SRC-000036. Requirements: REQ-000015.
Layer: 4, but mechanically a service used by Agent Orchestration. Inputs: lead-velocity metrics per
sub-domain. Outputs: spawn/retire decisions. Owned state: rolling-average velocity tracking. Dependencies:
Sub-domain Intelligence (#10), Agent Orchestration (#14). Events: `SUBDOMAIN_SPAWN_TRIGGERED`/
`SUBDOMAIN_RETIRE_TRIGGERED` (shared with #10). Agents: none itself (a deterministic policy engine acting on
agent orchestration). Deterministic components: the entire threshold-check logic. Failure modes: see #10.
Security requirements: none specific. Observability: spawn/retire event log. Scaling: is itself the
scaling mechanism. Status: `SOURCE-DERIVED`. Full detail in `dynamic-worker-scaling.md`.

### 16. Agent State Management
Purpose: track each agent's runtime state (healthy/degraded/quarantined/retired) and its task/memory context.
Source IDs: SRC-000037, SRC-000078. Requirements: REQ-000018, REQ-000020. Layer: cross-cutting. Inputs: agent
health signals. Outputs: state records consumed by Sentinel Plane and Hot-Swap. Owned state: per-agent state
records. Dependencies: Agent Orchestration. Events: `AGENT_STATE_CHANGED` (`PROPOSED_EVENT`). Agents: none
itself. Deterministic components: state-machine transitions. Failure modes: stale state (an agent reports
healthy but has actually failed). Security requirements: state records must not be attacker-writable.
Observability: agent state distribution over time. Scaling: linear with agent count. Status:
`PROPOSED_EXTENSION` (implied by hot-swap/sentinel needs; not named explicitly as a subsystem in source).

### 17. Context Migration
Purpose: transfer a failing agent's serialized state to its replacement. Source IDs: SRC-000037,
SCHEMA-004/006. Requirements: REQ-000018, REQ-000020. Layer: cross-cutting. Inputs: quarantined agent's state.
Outputs: bootstrapped replacement agent context. Owned state: migration checkpoint store. Dependencies: Agent
State Management (#16), Sentinel Plane (#19). Events: context-transfer events (part of hot-swap telemetry
contract, SCHEMA-006). Agents: none itself (a service invoked by Hot-Swap). Deterministic components:
serialization/deserialization logic. Failure modes: **hallucinated content being trusted as fact by the
replacement** (this is the exact failure mode Step 1 Section 23 warns about — "A replacement worker must not
inherit hallucinated information as trusted knowledge"). Security requirements: THIS is the core requirement
— state classes must be separated (see `context-migration.md`). Observability: migration success rate,
migration latency. Scaling: scales with failure rate, not lead volume. Status: `SOURCE-DERIVED`.

### 18. Hot-Swap
Purpose: execute the full failure→replacement cycle. Source IDs: SRC-000078. Requirements: REQ-000020. Layer:
cross-cutting. Inputs: Sentinel-issued `CEASE_OPERATIONS`. Outputs: replacement agent active. Owned state:
none beyond what #16/#17 own. Dependencies: Sentinel Plane, Agent State Management, Context Migration. Events:
`CEASE_OPERATIONS`, `FAILOVER_HOTSWAP_TRIGGERED`/`FAILOVER_HOTSWAP_DISPATCHED` (both versions preserved, see
`schema-versioning.md`). Agents: the "Hot-Swap Failover Engine" itself. Deterministic components: the 4-step
protocol logic. Failure modes: cascading failures if the replacement also fails immediately (not addressed by
source). Security requirements: admin-panel pinning must be tamper-evident. Observability: hot-swap frequency,
per-model failure rate. Scaling: scales with agent count and failure rate. Status: `SOURCE-DERIVED`.

### 19. Sentinel Plane
Purpose: independent, per-layer hallucination/anomaly auditing. Source IDs: SRC-000037, SRC-000039. Requirements:
REQ-000018, REQ-000019. Layer: cross-cutting, logically independent from the worker it observes (Step 1
Section 21's explicit requirement). Inputs: worker outputs. Outputs: drift scores, incident reports. Owned
state: drift-score history per worker. Dependencies: none (must be independently deployed from workers per
source design intent). Events: incident/quarantine events. Agents: one Sentinel per layer (SRC-000037: "for
each of the chain there is one agent"). Deterministic components: schema-validation checks (Pydantic/Zod-style
— deterministic, not LLM judgment, per SRC-000039). Failure modes: sentinel itself failing/being compromised
(not addressed by source — a genuine gap, "who watches the watcher"). Security requirements: sentinel
independence must be enforced architecturally, not just by convention. Observability: this subsystem IS
largely an observability subsystem. Scaling: 1 per layer (fixed) + "1 Auditor per 5 workers" at Layer 3/4
scale (TABLE-004). Status: `SOURCE-DERIVED`.

### 20. Hallucination Detection
Purpose: the specific analytical logic (drift score, consecutive-failure counting) used by Sentinels. Source
IDs: SRC-000077, SRC-000078. Requirements: REQ-000020. Layer: cross-cutting, part of #19. Inputs: worker
output + validation results. Outputs: drift score. Owned state: none beyond #19's. Dependencies: Sentinel
Plane. Events: none additional. Agents: none itself (a computation within Sentinel agents). Deterministic
components: FORMULA-002 (INCOMPLETE in source — `SOURCE_INCOMPLETE`, not reconstructed). Failure modes: the
formula's own incompleteness IS a failure mode for implementation — cannot be coded as-is without an
explicit, separately-justified completion (a `PROPOSED_EXTENSION` if ever completed). Security requirements:
none additional. Observability: drift score distribution. Scaling: scales with worker count. Status:
`SOURCE-DERIVED`, formula `SOURCE_INCOMPLETE`.

### 21. Telemetry
Purpose: collect operational metrics across all subsystems. Source IDs: SRC-000037 (metric-discovery agent),
implied throughout. Requirements: REQ-000018, REQ-000021. Layer: cross-cutting. Inputs: all subsystem events/
states. Outputs: metric time-series. Owned state: metric store. Dependencies: all subsystems (as data
sources). Events: metric-related events. Agents: the Telemetry/Metric Evolution Optimizer. Deterministic
components: aggregation pipelines. Failure modes: telemetry gaps (an unhealthy agent unable to report its own
history — flagged explicitly in Step 1 Section 31 as a design constraint: "an unhealthy agent cannot erase
its own history," meaning telemetry storage must be independent of the agent it's about). Security
requirements: telemetry store must be append-only/tamper-resistant. Observability: is this subsystem itself.
Scaling: high write volume at `full-firehose` scale. Status: `SOURCE-DERIVED`.

### 22. Metric Evolution
Purpose: propose new data fields/metrics to collect; self-idle at saturation. Source IDs: SRC-000037,
SRC-000079. Requirements: REQ-000018, REQ-000021. Layer: cross-cutting. Inputs: unstructured lead data,
current schema completeness stats. Outputs: proposed schema field additions; `CHANNEL_DATA_SATURATED_IDLE_ACTIVE`
notices. Owned state: saturation status per channel. Dependencies: Telemetry (#21). Events:
`CHANNEL_DATA_SATURATED_IDLE_ACTIVE` (`SOURCE-DERIVED` event name). Agents: the Metric Evolution/Saturation
Optimizer. Deterministic components: the 99.5%/72-hour threshold check (THRESH-006) is deterministic. Failure
modes: proposing metrics that directly mutate production schema without controlled migration — explicitly
forbidden by Step 1 Section 25 ("Metric evolution must not directly mutate production schemas without
controlled architecture/database migration"). Security requirements: schema-change proposals must go through
review, not auto-apply. Observability: proposal rate, acceptance rate. Scaling: one optimizer per channel
(implied). Status: `SOURCE-DERIVED`.

### 23. Strategy Intelligence
Purpose: platform-sequencing and channel-prioritization strategy for System A's OWN discovery/rollout (distinct
from System B's bidding strategy). Source IDs: SRC-000016 (platform sequencing), SRC-000006/SRC-000062
(Explore/Exploit, conceptually reusable). Requirements: (none directly registered — see below). Layer: 2-3.
Inputs: Channel/Platform Intelligence completeness data. Outputs: rollout priority recommendations. Owned
state: strategy recommendations. Dependencies: Channel Intelligence, Platform Intelligence. Events: none
named. Agents: could reuse the Macro Channel Team agents. Deterministic components: none. Failure modes:
stale recommendations. Security requirements: none specific. Observability: recommendation accuracy (not
measurable without real outcomes). Scaling: low (advisory function). Status: `INTERPRETATION` — the source's
Explore/Exploit and platform-sequencing concepts were designed for System B bidding strategy and
recon-platform-rollout strategy respectively; applying Explore/Exploit to System A's OWN platform-discovery
prioritization is a reasonable extension but not explicitly stated by the source.

### 24. Memory/RAG
Purpose: retrieval-augmented context for any agent needing historical precedent. Source IDs: SRC-000004
(System B's use case). Requirements: (System B primarily; System A's use is `PROPOSED_EXTENSION`). Layer:
cross-cutting. Inputs: historical records. Outputs: retrieved context for agent prompts. Owned state: vector
index. Dependencies: whatever historical data exists (Client/Channel/Platform Intelligence). Events: none.
Agents: none itself (a retrieval mechanism used by agents). Deterministic components: vector similarity
search. Failure modes: RAG replacing canonical structured data (explicitly forbidden — Step 1 Section 27:
"RAG/vector storage is a retrieval mechanism. It must not replace canonical structured data"). Security
requirements: memory-poisoning defense (Step 1 Section 30 names this explicitly as a security concept to
preserve). Observability: retrieval relevance. Scaling: scales with historical data volume. Status:
`HISTORICAL_ONLY` for the source's specific RAG use case (System B); `PROPOSED_EXTENSION` if System A adopts
an analogous pattern for its own agents.

### 25. Economic Analytics
Purpose: hold and present the source's economic scenarios without treating them as guarantees. Source IDs:
all of `economic-scenarios.md` (SCENARIO-001 through 008). Requirements: REQ-000033. Layer: cross-cutting
(reporting, not a pipeline stage). Inputs: none live (these are static, preserved scenario records at Step
1). Outputs: scenario reports. Owned state: scenario archive. Dependencies: none. Events: none. Agents: none.
Deterministic components: none. Failure modes: scenario figures being mistaken for live projections or
targets (explicitly guarded against — ASSUMPTION-006). Security requirements: none. Observability: n/a.
Scaling: n/a. Status: `SOURCE-DERIVED`, all figures explicitly `SOURCE_ESTIMATE`.

### 26. Cost Management
Purpose: track and bound actual operating cost (tokens, infrastructure) once implemented. Source IDs:
SRC-000043-000045 (illustrative figures only). Requirements: (implied, not directly registered). Layer:
cross-cutting. Inputs: token usage, infrastructure billing. Outputs: cost reports, limit-breach alerts. Owned
state: cost ledger. Dependencies: Agent Orchestration (token/spawn limits, Step 1 Section 13). Events: cost-
limit-breach events. Agents: none itself. Deterministic components: cost calculation. Failure modes: runaway
cost (explicitly named as a security concern, Step 1 Section 30 "runaway cost"). Security requirements: hard
spend caps. Observability: cost per lead, cost per agent. Scaling: must scale with (and bound) the
`full-firehose` profile's much larger token burn. Status: `PROPOSED_EXTENSION` — the source discusses cost
extensively as narrative analysis but never designs a Cost Management subsystem as such.

### 27. Configuration Management
Purpose: versioned storage of all configurable policy (thresholds, blacklists, spawn rules, model routing).
Source IDs: scattered — THRESH-001 through 015 are all, in effect, configuration values. Requirements: (none
directly registered as a subsystem; individual thresholds are `SOURCE-DERIVED`). Layer: cross-cutting. Inputs:
admin/user changes. Outputs: active configuration served to all subsystems. Owned state: config version
history. Dependencies: none. Events: `CONFIG_CHANGED` (triggers Blue-Green Updates, #14/cascading). Agents:
none itself. Deterministic components: the versioning/rollback logic. Failure modes: config drift between
what's documented and what's active. Security requirements: config-change authorization. Observability:
config version currently active per component. Scaling: n/a. Status: `PROPOSED_EXTENSION` as a unified
subsystem (see `configuration.md`), though every individual configurable value is `SOURCE-DERIVED`.

### 28. Audit
Purpose: tamper-evident record of admin actions, incidents, and configuration changes. Source IDs: SRC-000037
("pin that ai in the admin panel"). Requirements: REQ-000018. Layer: cross-cutting. Inputs: all
subsystem-generated events. Outputs: audit log. Owned state: append-only audit store. Dependencies: Telemetry
(#21), Configuration (#27). Events: consumes all events. Agents: none itself. Deterministic components: the
entire subsystem. Failure modes: audit-log tampering (must be prevented architecturally). Security
requirements: append-only, access-controlled. Observability: is itself an observability tool. Scaling: high
write volume. Status: `SOURCE-DERIVED` (partial — "admin panel" is named; a full audit subsystem is
`PROPOSED_EXTENSION`).

### 29. Administration
Purpose: human-facing control surface (the "admin panel" referenced repeatedly in source). Source IDs:
SRC-000037, SRC-000078. Requirements: REQ-000018, REQ-000020. Layer: cross-cutting. Inputs: Audit (#28),
Agent State Management (#16). Outputs: human-actionable views/controls. Owned state: none beyond what it
displays. Dependencies: nearly every subsystem (it's a UI/control layer). Events: admin-initiated commands
(pause, drain, quarantine — Step 1 Section 13's control-plane operations). Agents: none (human-operated).
Deterministic components: the entire UI layer. Failure modes: admin panel itself being a single point of
failure or an attack surface. Security requirements: strong auth, action logging. Observability: admin
action log (feeds Audit). Scaling: n/a (single control surface). Status: `SOURCE-DERIVED` (named, not
designed) — the source repeatedly references "the admin panel" as a destination for incident pins but never
specifies its own architecture.

### 30. External Integration
Purpose: the boundary layer connecting IECHM-LIOS to every external system (platforms, LLM providers,
System B, future System C). Source IDs: throughout. Requirements: (spans many). Layer: cross-cutting, sits at
every layer's edge. Inputs/Outputs: see `external-systems.md` and `api-boundaries.md`. Owned state: connector
credentials/config (not data itself). Dependencies: varies per integration. Events: varies. Agents: connector-
specific (Platform Workers, for platform integrations). Deterministic components: connector code itself.
Failure modes: upstream API changes breaking connectors. Security requirements: credential isolation per
connector, least-privilege access. Observability: per-connector health. Scaling: scales with connector count.
Status: `SOURCE-DERIVED` (existence of the boundary) / `INTERFACE_UNDEFINED` (most actual contracts, per
`system-boundaries.md` and `api-boundaries.md`).
