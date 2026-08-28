# Master Architecture — IECHM-LIOS

Per Step 1 Section 37. The primary architectural reference document. Every section links to its source IDs,
requirement IDs, and the detailed document(s) it summarizes. This document does not duplicate content
wholesale — it is the navigable index and synthesis point.

## 1. System Identity
IECHM-LIOS = System A (Lead Intelligence Architect & Multi-Agent Director) in a 3-system landscape. See
`system-boundaries.md`. Source: SRC-000002.

## 2. Source Baseline
`docs/source-extraction/` (29 pages, 82 source items, immutable, Step 0). Verified intact at Step 1 start —
see `docs/audit/step-1-source-integrity-findings.md`.

## 3. Canonical Interpretation
See `source-vs-canonical.md` for the 4-tag classification discipline (`SOURCE-DERIVED` / `INTERPRETATION` /
`PROPOSED_EXTENSION` / `USER_DECISION_REQUIRED`) applied throughout every document below.

## 4. System Boundaries
See `system-boundaries.md` (Step 0 + Step 1 extension). System A (this project) / System B (bidding,
referenced) / System C (manufacturing, referenced, contingent on ASSUMPTION-001). Interfaces largely
`INTERFACE_UNDEFINED` — see `api-boundaries.md`.

## 5. Architectural Layers
See `canonical-architecture.md`. Layer 0 (deterministic triage) through Layer 4 (sub-domain intelligence) +
cross-cutting observer/control plane. Resolves the source's own Layer-numbering collision via ADR-0002.

## 6. Major Subsystems
See `subsystems.md` — all 30 required subsystems documented (purpose, source IDs, requirements, layer,
inputs/outputs, owned state, dependencies, events, agents, deterministic components, failure modes, security,
observability, scaling, status).

## 7. Agent Architecture
See `agent-topology.md` — every source-derived agent role (Tier 0-4 + Sentinels + Hot-Swap Engine + Telemetry
Optimizer), classified as AI AGENT / WORKER / ORCHESTRATOR / SENTINEL / DETERMINISTIC SERVICE / CONNECTOR /
SCHEDULED PROCESS. Full-scale headcount cross-checked against TABLE-004 (140-196 agents, consistent).

## 8. Control Plane
See `agent-control-plane.md` — required operations (registration, provisioning, heartbeat, pause, drain,
quarantine, replacement, retirement, migration, cost/token/spawn limits). Mix of `SOURCE-DERIVED` and
`PROPOSED_EXTENSION`.

## 9. Data Flow
See `data-flow.md` — primary intelligence flow plus 12 named sub-flows (Discovery, Platform Research, Worker
Spawn/Retirement, Config Update, Blue-Green Update, Sentinel Failure, Quarantine, Context Migration, Hot-Swap,
Rollback, Metric Evolution, Saturation).

## 10. Data Lineage
See `data-lineage.md` — 7-category separation (RAW DATA / NORMALIZED DATA / MODEL INFERENCE / VERIFIED DATA /
DERIVED DATA / HUMAN DECISION / SYSTEM DECISION). MODEL INFERENCE must never silently become VERIFIED DATA.

## 11. Evidence
See `evidence-model.md` — CLAIM → EVIDENCE → VERIFICATION → CONFIDENCE → DERIVED CONCLUSION. Preserves
source's URL/API/hash/timestamp evidence-artifact concepts.

## 12. Configuration
See `configuration.md` — every threshold/policy value catalogued by domain, all versionable (`CONFIG-V1 →
CONFIG-V2 → ...`), every change auditable.

## 13. Event Architecture
See `events.md` — source-defined events (`CEASE_OPERATIONS`, `FAILOVER_HOTSWAP_TRIGGERED`/`DISPATCHED`,
`CHANNEL_DATA_SATURATED_IDLE_ACTIVE`, `EVENT_CONTRACT_SIGNED`) with full contract detail, plus explicitly
labeled `PROPOSED_EVENT` additions.

## 14. Dynamic Scaling
See `dynamic-worker-scaling.md` — the 5-Lead Rule (spawn >5/day, retire <2/day over 7-day avg) preserved
exactly, with explicit gaps flagged (cooldown, max-workers, reactivation semantics — none invented).

## 15. Sentinel Plane
See `sentinel-plane.md` — independence requirement, dual OR-condition thresholds (D_t≥0.85 OR ≥3 consecutive
failures), the unaddressed "who watches the Sentinel" gap.

## 16. Hallucination Detection
See `hallucination-detection.md` — drift formula FORMULA-002 preserved as `SOURCE_INCOMPLETE`, NOT
reconstructed. This is a blocking gap for real Sentinel implementation — see `open-decisions.md` #15.

## 17. Hot-Swap
See `hot-swap.md` — full failure→replacement sequence; old-worker state remains queryable for audit.

## 18. Context Migration
See `context-migration.md` — 10 state classes; MODEL INFERENCE/FAILED OUTPUT explicitly excluded from
"trusted" transfer (ADR-0006, a flagged departure from a literal reading of the source).

## 19. Metric Evolution
See `metric-evolution.md` — OBSERVATION→ANOMALY→PROPOSAL→EXPERIMENT→EVALUATION→ACCEPT/REJECT/NOTICE_ONLY/IDLE.
Saturation threshold (≥99.5%/72h) preserved exactly. Never mutates schema directly (ADR-0005).

## 20. Strategy Learning
See `strategy-learning.md` — Explore/Exploit 80/20 preserved as a starting policy, explicitly not claimed
optimal. Primarily a System B concept; reuse for System A's own prioritization is `PROPOSED_EXTENSION`.

## 21. Memory
See `memory.md` — memory-adjacent concepts separated (raw observation / evidence / verified knowledge / model
inference / agent memory / strategy memory / historical versions / telemetry). RAG never replaces canonical
structured data.

## 22. Manufacturing Boundary
See `manufacturing-boundary.md` — INTELLIGENCE (classify what a lead needs) vs. EXECUTION (actually
manufacture it) explicitly separated; EXECUTION is entirely System C, contingent on ASSUMPTION-001/002.

## 23. Economic Architecture
See `economic-model.md` — all 8 source economic scenarios preserved separately, none selected as canonical,
all explicitly `SOURCE_ESTIMATE`.

## 24. Security
See `security.md` — all external content treated as untrusted; source security concepts (injection,
sanitization) preserved; new concerns (credential leakage, runaway cost, memory poisoning) marked
`PROPOSED_EXTENSION`.

## 25. Observability
See `observability.md` — 15 signal types catalogued; independence requirement (an unhealthy agent cannot
erase its own history) generalized from the Sentinel-independence principle (ADR-0008).

## 26. External Systems
See `external-systems.md` — LEAD SOURCES, AI providers, storage, market data, CAD tools, manufacturing/machine
systems, CRM (absent from source — genuine gap), future bidding/execution systems. Several `UNSPECIFIED`.

## 27. API Boundaries
See `api-boundaries.md` — every internal and external boundary is `INTERFACE_UNDEFINED` at the payload/
transport/cadence level; the Intelligence → System B boundary is flagged as the highest-priority gap.

## 28. Open Decisions
See `open-decisions.md` — 15 items requiring explicit user input, none resolved unilaterally.

## 29. Source Conflicts
See `docs/architecture/conflicts/CONFLICT-001.md` through `CONFLICT-007.md` — all 7 preserved, all left
`NEEDS_USER_DECISION` or `PARTIALLY RESOLVED BY IMPLICATION` (CONFLICT-007 only), none silently resolved.

## 30. Proposed Extensions
Consolidated list of every `PROPOSED_EXTENSION` introduced across this Step 1 body of work (non-exhaustive
pointer — each is individually flagged in its home document): Layer 0/1 recon-side Security/Sanitization
subsystem; unified Configuration Management subsystem; Cost Management subsystem; formal Audit subsystem;
Agent State Management subsystem; control-plane operations (registration, pause, cost/token/spawn limits);
Blue-Green's Dependency Analysis/Historical Replay/Comparison/Rollback steps; 7-category data-lineage
taxonomy; 10-class context-migration trust taxonomy; 5 newly-named events (`PLATFORM_DISCOVERED`, etc.);
two-axis client/request classification (ADR-0003, pending); System-A reuse of Explore/Exploit and
Strategy-Ledger patterns.

## Summary status
`FOUNDATION_COMPLETE` — see `docs/audit/step-1-architecture-integrity-report.md` and the final Step 1 report
for the full justification of this status determination.
