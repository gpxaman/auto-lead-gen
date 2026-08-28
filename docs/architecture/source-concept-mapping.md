# Source Concept Mapping

Per Step 1 Section 10. For every major source concept: Source ID → Source Term → Canonical Component → Layer
→ Status → Notes. Status values: `DIRECT_MAPPING`, `COMPOSITE_MAPPING`, `HISTORICAL_ONLY`,
`PROPOSED_EXTENSION`, `UNRESOLVED`.

| Source ID(s) | Source Term | Canonical Component | Layer | Status | Notes |
|---|---|---|---|---|---|
| SRC-000001, SRC-000030 | Sanitizer (anti-bot/injection detection) | System B pipeline component (referenced only) | N/A (out of IECHM-LIOS scope) | `HISTORICAL_ONLY` for IECHM-LIOS; would be `DIRECT_MAPPING` within System B | See `system-boundaries.md` |
| SRC-000004 | RAG win/loss memory query | System B's Strategist memory | N/A (out of scope) | `HISTORICAL_ONLY` | `memory.md` documents the general RAG concept for completeness |
| SRC-000006, SRC-000062 | Explore/Exploit 80/20 | Strategy Learning (conceptually reusable by System A for platform-discovery experimentation, not just System B bidding) | Cross-cutting | `COMPOSITE_MAPPING` | See `strategy-learning.md` — the concept transfers even though the source only applied it to bidding |
| SRC-000007 | Strategy Ledger | System B memory structure | N/A (out of scope) | `HISTORICAL_ONLY` | — |
| SRC-000008, SRC-000006(reqs) | NPD/CAD/PCB scope constraint | Manufacturing Boundary / scope filter | Layer 0/1 | `DIRECT_MAPPING` | `manufacturing-boundary.md` |
| SRC-000010, SRC-000011 | `EngineeringJobSpec`, `ManufacturingDomain` | Technical Classification subsystem | Layer 1 | `DIRECT_MAPPING` | `data-domains.md` TECHNICAL domain |
| SRC-000012 | Budget Sanity Filter | Layer 0 deterministic triage rule | Layer 0 | `DIRECT_MAPPING` | `subsystems.md` #5 |
| SRC-000009, SRC-000013 | Stealth scraper → parser pipeline | Source Discovery + Lead Ingestion + Raw Payload Storage subsystems | Layer 0 | `COMPOSITE_MAPPING` | Splits into 3 subsystems in `subsystems.md` (#1, #3, #4) |
| SRC-000014 through SRC-000022 | Platform/channel lists | Platform Registry, Channel Registry | Layer 2, 3 | `DIRECT_MAPPING` | `platforms.md` (Step 0) is the source data; `subsystems.md` #2, #9 own it canonically |
| SRC-000024, SRC-000025, SRC-000026 | 6-tier taxonomy (client→channel→platform→sub-domain→recon strategy→bidding strategy) | Spans Layers 1-4 + System B interface | Layers 1-4 | `COMPOSITE_MAPPING` | Tier 6 (bidding strategy) is `HISTORICAL_ONLY` for IECHM-LIOS since it's a System B concern |
| SRC-000027 | "Blueprint not agent" scope constraint | System boundary definition | N/A | `DIRECT_MAPPING` | Directly shapes `system-boundaries.md` |
| SRC-000028 | IECHM capability pipeline | Manufacturing Boundary reference data | Cross-cutting (reference data, not a workflow stage) | `DIRECT_MAPPING` | `manufacturing-boundary.md` |
| SRC-000029, SRC-000025, SRC-000034 | 3 client archetype sets | Client Intelligence | Layer 1 | `COMPOSITE_MAPPING` (3 non-identical sets preserved) | `client-intelligence-model.md`, CONFLICT-004 |
| SRC-000030 | 5-branch lead source taxonomy diagram | Channel taxonomy | Layer 2 | `DIRECT_MAPPING` | — |
| SRC-000031, SRC-000032 | Master Lead Source Matrix, lead JSON v0.5 | Cross-layer strategy matrix + early schema draft | Layers 1-3 | `COMPOSITE_MAPPING` | Schema superseded by later versions — see `schema-versioning.md` |
| SRC-000033 | 3-tier agent allocation + 5-Lead Rule | Agent Topology + Dynamic Worker Scaling | Layers 1-4 (agent org-chart, Tier 1-4) | `DIRECT_MAPPING` | `agent-topology.md`, `dynamic-worker-scaling.md` |
| SRC-000034 | Layer 1 client profile fields (concentration matrix + proof) | Client Intelligence + Evidence | Layer 1, cross-cutting | `COMPOSITE_MAPPING` | `evidence-model.md` |
| SRC-000035 | Layer 2/3 channel/platform fields | Channel + Platform Intelligence | Layers 2, 3 | `DIRECT_MAPPING` | `subsystems.md` #8, #9 |
| SRC-000036 | 5-Lead Rule thresholds | Dynamic Worker Scaling | Layer 4 | `DIRECT_MAPPING` | THRESH-001/002 |
| SRC-000037 | Cascading updates + hallucination sentinel + context transfer + metric-discovery agent | Blue-Green Updates + Sentinel Plane + Context Migration + Metric Evolution | Cross-cutting | `COMPOSITE_MAPPING` | 4 distinct cross-cutting documents |
| SRC-000038 | 4-layer topology diagram | This document's Layer 0-4 model (data-pipeline scheme) | All | `DIRECT_MAPPING` | Note the Layer-numbering collision addressed in `canonical-architecture.md` |
| SRC-000039 | Sentinel validation directives | Sentinel Plane | Cross-cutting | `DIRECT_MAPPING` | `sentinel-plane.md` |
| SRC-000040, SRC-000041 | Schema v1 (Lead Entity + Telemetry) | Data Domains, Sentinel Plane | Layer 1, cross-cutting | `DIRECT_MAPPING` (as historical v1) | `schema-versioning.md` |
| SRC-000042 through SRC-000047 | Full-scale cost/agent/profitability projections | Economic Model + scaling-scenarios `freelance-narrow` profile | Cross-cutting (economics, not a pipeline stage) | `DIRECT_MAPPING`, flagged illustrative | `economic-model.md`, `scaling-scenarios.md` |
| SRC-000048 through SRC-000052 | Scope-broadening + firehose revision + composition breakdown | scaling-scenarios `full-firehose` profile; Client Intelligence (request-type axis) | Layer 0, 1 | `COMPOSITE_MAPPING` | CONFLICT-001, CONFLICT-005 |
| SRC-000053 | Layer 0 deterministic pre-filter | Layer 0 | Layer 0 | `DIRECT_MAPPING` | `subsystems.md` #5 |
| SRC-000054 | IECHM Chennai location | Reference/configuration data (firm profile) | Cross-cutting (config) | `DIRECT_MAPPING`, low confidence (ASSUMPTION-005) | `configuration.md` |
| SRC-000055 through SRC-000065 | Category-killer / universal-printer / 10%-discount economic scenarios | Economic Model (System B pricing, referenced) + Manufacturing Boundary (System C, referenced) | N/A (mostly System B/C) | `HISTORICAL_ONLY` for IECHM-LIOS core; `DIRECT_MAPPING` for reference/interface purposes | `economic-model.md`, `manufacturing-boundary.md` |
| SRC-000066 | Estimator/Dispatch Agents | System C interface (referenced) | N/A (out of scope) | `HISTORICAL_ONLY` | `manufacturing-boundary.md` |
| SRC-000067, SRC-000068, SRC-000069 | Conversion levers, growth phases, execution tactics | System B concerns (referenced) | N/A (out of scope) | `HISTORICAL_ONLY` | — |
| SRC-000070 through SRC-000075 | Master Prompt v1/v2 consolidation, pricing formula, agent org chart | Spans System A (agent org chart, Layer 0 triage) and System B (pricing) | Mixed | `COMPOSITE_MAPPING` | Org chart parts `DIRECT_MAPPING` to `agent-topology.md`; pricing parts `HISTORICAL_ONLY` |
| SRC-000076 | Machine-to-AI Hardware API | System C interface | N/A (out of scope) | `HISTORICAL_ONLY` | `manufacturing-boundary.md`, `api-boundaries.md` (INTERFACE_UNDEFINED) |
| SRC-000077, SRC-000078, SRC-000079 | Drift formula, hot-swap protocol, saturation guardrail | Sentinel Plane, Hot-Swap, Metric Evolution | Cross-cutting | `DIRECT_MAPPING` | Drift formula marked `SOURCE_INCOMPLETE` per `hallucination-detection.md` |
| SRC-000080, SRC-000082 | Schema v2 (Lead Entity + Telemetry) | Data Domains, Sentinel Plane | Layer 1, cross-cutting | `DIRECT_MAPPING` (as historical v2 / current-candidate) | `schema-versioning.md` |
| SRC-000081 | Runtime Instructions (3 rules) | Mixed: pricing rule (System B), zero-tooling framing (System C), immediate failovers (Sentinel Plane) | Mixed | `COMPOSITE_MAPPING` | Only the failover rule is `DIRECT_MAPPING` to IECHM-LIOS scope |

## Concepts with no clean single-layer home (explicitly cross-cutting, not forced into one layer)

- **Evidence/Verification** — touches every layer (a claim can originate from Layer 1 client classification,
  Layer 3 platform research, or Layer 4 sub-domain discovery, and all need the same evidence discipline).
- **Configuration** — every layer and every agent has configurable parameters (spawn thresholds, blacklists,
  rate limits) but the source never names a unified configuration subsystem; this is `PROPOSED_EXTENSION`
  as a formal subsystem, though every individual configurable value is `SOURCE-DERIVED`.
- **Cost tracking** — appears throughout as narrative dollar figures rather than as a named subsystem;
  formalized as `PROPOSED_EXTENSION` in `subsystems.md` #26.

## Traceability

This mapping is also reflected in the `canonical_component` / `architecture_document` columns added to
`docs/requirements/source-traceability.csv` in Step 1 (Section 38).
