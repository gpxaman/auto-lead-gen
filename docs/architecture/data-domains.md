# Architectural Data Domains

Per Step 1 Section 32. Conceptual domain modeling only — no physical database schema. All 22 required domains
evaluated.

| Domain | Conceptual scope | Primary source | Owning subsystem |
|---|---|---|---|
| SOURCE | The immutable Step 0 preserved source material itself (a special, design-time-only domain) | Step 0 artifacts | N/A (outside runtime) |
| CLIENT | Buyer archetype, profile, pain point, motivation, MOV | 3 non-identical archetype sets, CONFLICT-004 | Client Intelligence (`subsystems.md` #7) |
| CHANNEL | Macro-channel-type benchmarks | SRC-000035 | Channel Intelligence (#8) |
| PLATFORM | Per-platform rules/tools/metrics | SRC-000035 | Platform Intelligence (#9) |
| SUBDOMAIN | Sub-domain-level data + dynamic worker state | THRESH-001/002 | Sub-domain Intelligence (#10) |
| LEAD | The unified lead record (3 non-identical schema versions, CONFLICT-003) | SCHEMA-002/003/005 | spans Layers 0-4 |
| TECHNICAL | `ManufacturingDomain`, CAD/PCB fields, deliverables | SCHEMA-001 | Hardware/NPD Classification (#11) |
| MANUFACTURING | IECHM capability profile, physical process taxonomy | `manufacturing-capabilities.md` | Manufacturing Boundary (reference data, not owned by a runtime subsystem) |
| COMMERCIAL | Budget, MOV, feasibility scoring | SCHEMA-002 `commercial_parameters`, SCHEMA-005 `commercial_assessment` | spans Client + Technical classification |
| EVIDENCE | Proof artifacts (URL/API/hash/timestamp) | SRC-000034, SCHEMA-003 `verification_artifacts` | Evidence Management (#12) |
| VERIFICATION | Verified/unverified status per claim | SRC-000039 | Verification (#13) |
| AGENT | Agent identity, role, tier, state | `agent-topology.md` | Agent Orchestration (#14), Agent State Management (#16) |
| TASK | What an agent is currently doing | Implied by Task State (`context-migration.md`) | Agent Orchestration (#14) |
| EVENT | All named/proposed events | `events.md` | spans all subsystems (event bus is cross-cutting) |
| CONFIGURATION | Versioned policy/threshold values | `configuration.md` | Configuration Management (#27) |
| TELEMETRY | Operational metrics | `observability.md` | Telemetry (#21) |
| SENTINEL | Drift scores, incident records | THRESH-004/005 | Sentinel Plane (#19) |
| STRATEGY | Explore/Exploit state, rollout prioritization | SRC-000006 (System B), `strategy-learning.md` (System A extension) | Strategy Intelligence (#23) — mostly System B, partial System A extension |
| METRIC | Derived/aggregated values | Implied throughout | Metric Evolution (#22) |
| MEMORY | RAG/vector-retrieved context | SRC-000004 (System B) | Memory/RAG (#24) — mostly System B, referenced for completeness |
| ECONOMICS | Preserved economic scenarios | `economic-scenarios.md` | Economic Analytics (#25) |
| AUDIT | Tamper-evident incident/admin-action log | SRC-000037 ("admin panel") | Audit (#28) |

## Cross-domain relationships (conceptual, not a physical ER diagram)

- LEAD is the central domain that CLIENT, TECHNICAL, COMMERCIAL, and EVIDENCE all attach to.
- PLATFORM and CHANNEL are hierarchical (many PLATFORMs roll up into one CHANNEL — see `terminology.md`
  "Macro Channel" for the source's own inconsistent category counts).
- SUBDOMAIN is hierarchical under PLATFORM.
- AGENT and TASK are related to every other domain as the PRODUCER of records in them.
- EVENT is the connective tissue between all domains (every domain's state changes are, in a well-designed
  system, mediated by events — per `events.md`).
- SENTINEL, TELEMETRY, and AUDIT all observe AGENT and, transitively, every domain AGENT touches.

## Explicit non-implementation

Per Step 1 Section 32's explicit instruction, this is conceptual domain modeling only. No physical database
schema, table design, or storage technology choice is made here — that is deferred to `docs/database/` in a
future step, informed by (not dictated by) this document.
