# Entity Catalog — IECHM-LIOS

Per Step 2 Sections 5-35. Full logical entity inventory. Every entity links to its owning domain, source
basis, and contract. Technology-neutral (Step 2 Section 38). None of these are physical tables yet — see
`docs/database/DATABASE_IMPLEMENTATION_OPTIONS` note at the bottom and `schema.sql` for the conditional
physical-schema attempt.

## Raw Data Layer (Section 5)

### `raw_record`
Immutable. Never overwritten — a changed external item produces a NEW `raw_record`, linked to prior versions
via `supersedes_raw_record_id`. Fields: `record_id`, `source_system`, `source_identifier`, `retrieved_at`,
`observed_at`, `raw_payload` (or a reference to blob storage), `content_type`, `content_hash`, `source_url`,
`request_metadata`, `response_metadata`, `retrieval_method`, `connector_version`, `schema_version`,
`ingestion_run_id`, `provenance`, `security_status`. Source: `SOURCE-DERIVED` (SRC-000009/013, the Recon
Engine pipeline's "Raw Listing Payload" stage) + `PROPOSED_EXTENSION` for the exact field list (the source
names the STAGE, not this field-level contract). Contract: `contracts/raw-record.md` — **note:** `raw-record`
is not in Step 2's explicit contract list (Section 20/49) but is created anyway since Section 5 explicitly
requires this field list; cross-referenced from `lead.md`.

## Source Document Data (Section 6)
See `logical-data-model.md`'s dedicated section — `source_document`, `source_document_version`, `source_page`,
`source_item`, `source_reference`, `source_extraction_status`, `source_classification`. Filesystem-authoritative,
not duplicated in a contract file (this is index/mirror data, not a domain the runtime system produces).

## Client Domain (Section 7)

| Entity | Purpose | Versioned? | Source |
|---|---|---|---|
| `client` | A real-world buyer entity (as best identified — may be pseudonymous, e.g. "the poster of listing X") | Yes | `PROPOSED_EXTENSION` — the source never names an identity-resolution concept distinct from the lead itself; needed to support "the same client posts multiple leads" |
| `client_archetype` | A canonical archetype DEFINITION (not an assignment) | Yes, via `client_archetype_version` | CONFLICT-004 — 3 non-identical source sets, ALL preserved as distinct `client_archetype_set` values (see below) |
| `client_archetype_version` | A specific version of the archetype taxonomy (Set A / Set B / Set C / a future canonical union) | N/A (each version is itself the unit) | `SOURCE-DERIVED` (the 3 sets) + `PROPOSED_EXTENSION` (the versioning wrapper) |
| `buyer_persona` | Free-text/structured persona detail (only populated for Set A archetypes, per CONFLICT-004's finding that Sets B/C are truncated) | Yes | `SOURCE-DERIVED`, partial |
| `buying_motivation` | e.g., "Speed," "Feasibility," "Cost-Down/VAVE," "Quality Compliance" | Yes | `SOURCE-DERIVED` (SRC-000016 concentration-matrix fields, page-9 "core driver") |
| `pain_point` | e.g., "Bridging POC → production-ready package" | Yes | `SOURCE-DERIVED` (Set A "Primary Bottleneck") |
| `buying_signal` | e.g., "Posts prototype photos asking for DFM advice" | Yes | `SOURCE-DERIVED` (TABLE-003 "Technical Indicators") |
| `client_classification` | The ASSIGNMENT of a client/lead to an archetype (a CLAIM, not a fact) | Yes, full claim lifecycle | `PROPOSED_EXTENSION` wrapper around `SOURCE-DERIVED` classification behavior |

**Explicit non-merge:** `client_archetype_set` is an enum (`SOURCE_SET_A`, `SOURCE_SET_B`, `SOURCE_SET_C`,
plus any future `CANONICAL_UNION` a human decision creates) — a `client_classification` record always states
WHICH set's vocabulary it used, never a flattened generic archetype name. This directly implements Step 2
Section 7's "Do not merge the multiple source archetype lists into one irreversible enumeration."

## Lead Domain (Section 8-9)

| Entity | Purpose | Versioned? | Source |
|---|---|---|---|
| `lead` | The stable identity of one tracked opportunity (survives re-observation) | Yes, via `lead_version` | `SOURCE-DERIVED` (concept), 3 non-identical schema shapes (SCHEMA-002/003/005) |
| `lead_version` | Each distinct state of a lead over time — **first observation is NEVER overwritten**, each new observation creates a new version | N/A (append-only) | `PROPOSED_EXTENSION` (versioning wrapper); field content per whichever schema version is in use |
| `lead_source` | A generic pointer entity: which macro channel / platform / sub-domain a lead came from | Yes | `SOURCE-DERIVED` |
| `lead_source_version` | If a lead's attributed source changes (rare, e.g. re-classification) | Yes | `PROPOSED_EXTENSION` |
| `macro_channel` | Channel-type definition (note: source gives 4/8/5/6 differing category counts — see `terminology.md`) | Yes, via `macro_channel_version` | `SOURCE-DERIVED`, multiple non-identical counts preserved |
| `platform` | Individual named platform (Upwork, Alibaba, etc.) | Yes, via `platform_version` | `SOURCE-DERIVED` (46 platforms, Step 0 `platforms.md`) |
| `platform_version` | Platform rule/tool/metric changes over time | N/A (append-only) | `SOURCE-DERIVED` fields (SRC-000035) |
| `subdomain` | Sub-domain within a platform (a subreddit, an RFQ category) | Yes, via `subdomain_version` | `SOURCE-DERIVED` |
| `subdomain_version` | Sub-domain worker lifecycle state changes | N/A (append-only) | `SOURCE-DERIVED` (THRESH-001/002) |
| `lead_classification` | Technical/commercial/client classification CLAIMS about a lead | Yes, full claim lifecycle | `SOURCE-DERIVED` |
| `lead_status` | Lifecycle status (new/qualified/rejected/etc.) — history preserved, never overwritten in place | Yes, append-only history | `PROPOSED_EXTENSION` |
| `lead_event` | Domain events specific to a lead (discovered, reclassified, scored) | N/A (immutable event log) | `PROPOSED_EXTENSION`, using the general `event` envelope |
| `lead_score` | A DERIVED value (e.g., `budget_feasibility_score`, SCHEMA-002) | Yes, history preserved | `SOURCE-DERIVED` (fields exist in schemas) |
| `lead_priority` | Derived from score + strategy | Yes | `PROPOSED_EXTENSION` |

**Hierarchy (Section 9):** `macro_channel` → `platform` → `subdomain` → `lead_source` → `lead`. A `lead` may
reference multiple `lead_source` records if the same opportunity is legitimately observed via more than one
channel (not assumed exclusive, per Section 9's explicit instruction — e.g., a lead cross-posted to both a
subreddit and a freelance board).

## Technical Intelligence (Section 10)

| Entity | Purpose | Source |
|---|---|---|
| `technical_classification` | `ManufacturingDomain` assignment + CAD/PCB/materials/process fields, as a CLAIM | SCHEMA-001, `SOURCE-DERIVED` |
| `manufacturing_domain_definition` | The enum definition itself (`CAD_MECHANICAL`, `PCB_ELECTRONICS`, etc. — 7 values from SCHEMA-001) | `SOURCE-DERIVED`, exact values preserved, none invented |
| `manufacturing_capability_reference` | IECHM's own capability profile (reference data, not per-lead) | `SOURCE-DERIVED` (`manufacturing-capabilities.md`) |

No manufacturing capability beyond what SCHEMA-001's `ManufacturingDomain` enum and
`manufacturing-capabilities.md` state is represented — per Section 10's explicit prohibition on inventing
capabilities.

## Commercial Intelligence (Section 11)

| Entity | Purpose | Source |
|---|---|---|
| `commercial_opportunity` | Budget/urgency/timeline/decision-maker/stage/value fields as CLAIMS, never actual commitments | SCHEMA-002 `commercial_parameters`, SCHEMA-005 `commercial_assessment` |
| `commercial_estimate` | A derived value with mandatory `source`, `calculation`, `assumptions`, `confidence`, `timestamp`, `model_version` fields | `PROPOSED_EXTENSION` wrapper, `SOURCE-DERIVED` fields (`budget_feasibility_score`, `estimated_market_price_usd`, etc.) |

**Explicit non-claim:** no `commercial_estimate` record represents "the client has committed to $X" — every
such record is explicitly an ESTIMATE with the above provenance fields attached, per Section 11's instruction.

## Evidence, Claim, Verification (Sections 12-14)
Full entity detail in `docs/database/evidence.md`. Summary: `claim`, `evidence`, `verification`,
`confidence_record`, `derivation`. A claim may have zero, one, or multiple evidence records (Section 12
explicit). Failed verification attempts are never deleted (Section 14 explicit) — `verification.status` can be
`FAILED` and the row persists.

## Conflict Model (Section 15)

| Entity | Purpose |
|---|---|
| `conflict` | First-class representation of an unresolved (or resolved) source/data conflict |
| `conflict_version` | If a conflict's understanding changes (new evidence found for either side) |
| `conflict_participant` | Links a conflict to the specific claims/sources on each side |

Status enum: `OPEN`, `UNDER_REVIEW`, `RESOLVED`, `SUPERSEDED`, `UNRESOLVED`. The 7 existing
`docs/architecture/conflicts/CONFLICT-00N.md` records are the SEED DATA for this table (see
`tests/fixtures/conflicts.synthetic.json` — actually these 7 are NOT synthetic, they are real project
conflicts; fixtures are for testing the MODEL, not for re-storing these 7, which live authoritatively in
`docs/architecture/conflicts/`).

## Assumption Model (Section 16)
`assumption` entity: `assumption_id`, `source_id`, `description`, `assumption_type` (`ECONOMIC`/`TECHNICAL`/
`MARKET`/`SCALING`/`HARDWARE`/`ARCHITECTURAL`/`OPERATIONAL`/`OTHER`), `confidence`, `status`,
`affected_scenarios`, `affected_components`, `validation_method`, `created_at`, `updated_at`. Seed data: the 8
assumptions in `docs/requirements/assumptions.md` (ASSUMPTION-001 through 008), each already fitting one of
these 8 types (e.g., ASSUMPTION-001 = `HARDWARE`, ASSUMPTION-003 = `ECONOMIC`, ASSUMPTION-006 = `ECONOMIC`).

## Scenario Model (Section 17)
`scenario` entity with the full economic field set (`raw_volume`, `filter_rate`, `qualified_volume`,
`bid_volume`, `win_rate`, `close_rate`, `AOV`, `revenue`, `margin`, `cost`, `profit`) plus
`scenario_id`/`scenario_name`/`scenario_type`/`source_ids`/`assumptions`/`inputs`/`formula`/`outputs`/
`context`/`status`/`version`. Seed data: SCENARIO-001 through 008 (`docs/source-extraction/economic-scenarios.md`)
and the two scale profiles (`freelance-narrow`, `full-firehose` — `docs/architecture/scaling-scenarios.md`),
kept as DISTINCT rows, never averaged/blended (Section 17 explicit).

## Formula Model (Section 18)
`formula` entity: `formula_id`, `source_id`, `formula_text`, `variables`, `inputs`, `outputs`, `status`,
`completeness`, `version`. Seed data: FORMULA-001 through 009. **FORMULA-002 (drift score) is stored with
`completeness = SOURCE_INCOMPLETE` and `formula_text` containing the exact truncated source text — the
missing terms are NOT reconstructed**, per Section 18's explicit instruction, consistent with Step 1's
`hallucination-detection.md`.

## Schema Registry (Section 19)
`schema_registry` entity: `schema_id`, `schema_name`, `schema_version`, `source_id`, `schema_type`,
`definition`, `status`, `created_at`, `supersedes`, `superseded_by`. Seed data: SCHEMA-001 through 006, none
deleted when a newer one appears — `SCHEMA-005.supersedes = SCHEMA-003` is recorded as a LINK, not a deletion
(and per `schema-versioning.md`, no version is yet marked canonical, so no `superseded_by` chain is finalized
— `open-decisions.md` #2).

## Agent Domain (Section 21)
`agent`, `agent_version`, `agent_instance`, `agent_state`, `agent_configuration`, `agent_health`,
`agent_capability`, `agent_permission`. Maps directly onto `docs/architecture/agent-topology.md`'s Tier 0-4
roles + Sentinels. `agent_state` is append-only history (never destructively overwritten, Section 21 explicit)
— current state is the latest row, but prior rows remain queryable, directly implementing
`context-migration.md`'s trust-taxonomy discipline at the data layer.

## Task Domain (Section 22)
`task`, `task_attempt`, `task_result`, `task_error`, `task_checkpoint`. **Failed attempts are preserved** — a
successful retry creates a NEW `task_attempt` row linked to the same `task`, the failed attempt row is
untouched (Section 22 explicit, directly implementing `context-migration.md`'s FAILED OUTPUT state class).

## Worker Domain (Section 23)
`worker`, `worker_version`, `worker_state`, `worker_checkpoint`, `worker_lifecycle_event`. Lifecycle enum:
`SPAWNED`, `ACTIVE`, `DEGRADED`, `QUARANTINED`, `DRAINING`, `RETIRED`, `FAILED`, `REPLACED` — matches
`docs/architecture/dynamic-worker-scaling.md` and `hot-swap.md` flows exactly. `worker_lifecycle_event` is the
immutable event log implementing the WORKER SPAWN FLOW / WORKER RETIREMENT FLOW from `data-flow.md`.

## Sentinel Domain (Section 24)
`sentinel`, `sentinel_check`, `sentinel_alert`, `sentinel_action`. Per Section 24's explicit rule, a Sentinel
NEVER modifies historical telemetry — `sentinel_check` rows are append-only and reference (not alter) the
`telemetry` rows they evaluated. Implements `docs/architecture/sentinel-plane.md`'s independence requirement
at the schema level: `sentinel_*` tables have no `UPDATE`/`DELETE` write path from worker-owned code paths in
the logical design (an access-control rule, formalized in `integrity-rules.md`).

## Configuration Domain (Section 25)
`configuration`, `configuration_version`, `configuration_change`, `configuration_scope`. Every
production-affecting change is auditable (Section 25 explicit) — `configuration_change` rows are immutable
and link to the `audit_event` they generated. Seed data: the 15 threshold/policy values catalogued in
`docs/architecture/configuration.md` (THRESH-001 through 015), each recorded as `configuration.version = 1`
(the source-derived starting value), open to versioned change via `open-decisions.md` items.

## Model/Prompt Versioning (Section 26)
`model_version`, `prompt_version`, `tool_version`, `connector_version`. Every AI-derived `claim` or `task_result`
carries foreign keys to all four of these, so provenance can always answer "which model/prompt/tool/connector
produced this" (Section 26's explicit requirement) — implements `docs/architecture/master-architecture.md`'s
provenance chain (`OUTPUT → TASK → AGENT → MODEL/PROMPT → INPUT → SOURCE → EVIDENCE`) concretely. **No
assumption that the latest model produced historical results** — every historical `claim`/`task_result` row's
`model_version_id` is fixed at creation time, never updated to point at a newer model.

## Event Domain (Section 27-28)
`event` envelope: `event_id`, `event_type`, `event_version`, `aggregate_type`, `aggregate_id`, `producer`,
`timestamp`, `correlation_id`, `causation_id`, `payload`, `payload_schema_version`, `security_classification`,
`idempotency_key`. **Immutable — corrections emit a NEW event, never rewrite history** (Section 27 explicit).
Seed data: the source-defined events (`CEASE_OPERATIONS`, `FAILOVER_HOTSWAP_TRIGGERED`/`DISPATCHED`,
`CHANNEL_DATA_SATURATED_IDLE_ACTIVE`, `EVENT_CONTRACT_SIGNED`) plus the 10 `PROPOSED_EVENT` additions from
`docs/architecture/events.md`.

**Event Sourcing vs. State (Section 28) — explicit decision per entity family:**

| Entity family | Treatment | Rationale |
|---|---|---|
| `lead`, `client`, `platform`, `subdomain`, `agent`, `worker`, `configuration`, `claim`, `verification` | EVENT HISTORY + CURRENT STATE (materialized view derived from, but not replacing, the event log) | High-value entities needing both fast current-state reads AND full audit trail |
| `raw_record`, `evidence`, `audit_event`, `task_attempt`, `worker_lifecycle_event`, `sentinel_check` | EVENT HISTORY ONLY (no separate "current state" concept — these ARE the history) | Inherently append-only/point-in-time facts, no meaningful "current value" to materialize |
| `telemetry` | RAW MEASUREMENTS preserved + separate AGGREGATE tables, aggregates never replace raw (Section 30 explicit) | High-volume, needs both granular audit and cheap dashboard queries |

Per Section 28's explicit instruction, **NOT every table is event-sourced** — this table makes that
determination explicit per entity family rather than defaulting to one pattern everywhere.

## Audit Domain (Section 29)
`audit_event`: `actor`, `actor_type`, `action`, `target`, `target_id`, `before`, `after`, `reason`,
`timestamp`, `correlation_id`, `source`, `network_metadata` (optional), `configuration_version`. **No secrets
stored** (Section 29 explicit) — `before`/`after` snapshots must be redacted of credential fields at the
application layer before persistence (an integrity rule, see `integrity-rules.md`).

## Telemetry Domain (Section 30)
`telemetry_measurement` (raw) + `telemetry_aggregate` (derived, never replaces raw). Covers: agent, worker,
task, lead, source, connector, model, prompt, event, system — count, rate, latency, error rate, throughput,
cost, token usage, drift, verification, queue depth, worker utilization (all metric types from Section 30).

## Strategy Domain (Section 31)
`strategy`, `strategy_version`, `strategy_experiment`, `strategy_result`, `strategy_ledger`. Seed data: the
Strategy Ledger structure from SRC-000007 (ST-01 through ST-04, TABLE-001) — preserved exactly, including the
80/20 Explore/Exploit split as a `configuration` value (not hardcoded), per `strategy-learning.md`'s explicit
non-optimality caveat. **Primarily a System B concept** (per `system-boundaries.md`) — modeled here for
completeness/interface-readiness and for the `PROPOSED_EXTENSION` System-A reuse case
(`strategy-learning.md`), not because IECHM-LIOS itself performs bidding-strategy decisions.

## Metric Evolution Domain (Section 32)
`metric_definition`, `metric_version`, `metric_proposal`, `metric_experiment`, `metric_evaluation`. Status
enum: `PROPOSED`, `EXPERIMENTAL`, `ACTIVE`, `REJECTED`, `DEPRECATED`, `SATURATED`, `RETIRED` — the `SATURATED`
status directly implements THRESH-006 (`CHANNEL_DATA_SATURATED_IDLE_ACTIVE`). **Never silently modifies
production schema** — a `metric_proposal` reaching `ACTIVE` status triggers a `schema_registry` migration
workflow (Section 32 explicit, consistent with ADR-0005).

## Memory Domain (Section 33)
`memory_item`, `memory_version`, `memory_reference`, `memory_embedding`, `memory_retrieval`, `memory_source`.
**RAG/vector storage is explicitly DERIVED** — every `memory_item` carries mandatory `memory_source`
references back to the canonical record(s) it was built from (Section 33 explicit, implementing
`docs/architecture/memory.md`'s "must not replace canonical structured data" rule at the schema level: there
is no path for a `memory_item` to exist without a `memory_source` foreign key).

## Security / Quarantine Domain (Section 34)
`security_event`, `quarantine_record`, `threat_indicator`, `content_sanitization_result`. **External content
never automatically becomes a trusted system instruction** (Section 34 explicit) — enforced by construction:
`raw_record.raw_payload` has no code path that feeds it directly into agent SYSTEM prompts; it only ever
enters as USER/DATA content subject to the Security/Sanitization subsystem (`docs/architecture/subsystems.md`
#6) before any classification agent sees it.

## Manufacturing Domain (Section 35) — Intelligence-side only
`manufacturing_requirement`, `manufacturing_classification`, `material`, `process`, `machine`,
`machine_capability`, `production_request`, `reorder_signal`. **These are intelligence-side records.** No
physical machine control, no unsafe control interface — per `docs/architecture/manufacturing-boundary.md`,
these entities record WHAT a lead is asking for, never DISPATCH anything to a machine. `machine`/
`machine_capability` are reference/classification data only (matching IECHM's stated capability profile,
`manufacturing-capabilities.md`), not live equipment-control records — and are explicitly flagged as
contingent on the unverified ASSUMPTION-001/002 where they reference the Universal 3D Printer specifically.

## Data Provenance (Section 36)
Every DERIVED record (claim, commercial_estimate, lead_score, task_result, metric value) carries:
`record_id`, `source_record_ids[]`, `parent_record_ids[]`, `evidence_ids[]`, `derivation_type`,
`derivation_timestamp`, `model_version_id`, `prompt_version_id`, `configuration_version_id`, `agent_id`,
`task_id`. This is a **cross-cutting field pattern**, not a standalone entity — every contract in
`docs/contracts/` that produces derived data includes this field set (see `contracts/README.md`'s provenance
section). Enables the trace: `OUTPUT → TASK → AGENT → MODEL/PROMPT → INPUT → SOURCE → EVIDENCE`.

## DATABASE_IMPLEMENTATION_OPTIONS (PROPOSED — not an approved decision, per Section 38)

No database vendor is approved anywhere in Step 0/1. The entities above are deliberately relational-agnostic
(they'd work as SQL tables, document-store collections, or a graph). Three PROPOSED technology shapes, none
adopted:

1. **PROPOSED: Relational (PostgreSQL-class)** — strong fit for the `claim`/`evidence`/`verification`
   provenance chain (foreign-key-heavy); JSONB columns could hold the variant lead-schema payloads
   (SCHEMA-002/003/005) without forcing premature schema unification.
2. **PROPOSED: Document store (MongoDB-class)** — natural fit for preserving 3 non-identical lead-schema
   shapes side-by-side without a rigid column set; weaker for the highly relational conflict/evidence graph.
3. **PROPOSED: Hybrid (relational core + document/JSONB for variant payloads + separate event log/append-only
   store for `event`/`audit_event`/`telemetry_measurement`)** — matches the EVENT HISTORY + CURRENT STATE
   split already decided per-entity-family above.

None of these is selected. See `open-decisions.md` #7. `docs/database/schema.sql` (if produced) targets
option 3 as the most defensible NEUTRAL starting point (a relational core is the safest default for a
provenance-heavy system regardless of final vendor, and can be revisited), explicitly labeled non-final.
