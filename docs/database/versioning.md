# Versioning Strategy — IECHM-LIOS

Per Step 2 Section 37. Defines versioning rules for every entity family named in that section. Extends
`docs/architecture/schema-versioning.md` and `docs/architecture/configuration.md` (Step 1) with concrete
data-model rules.

## The universal rule

> "Use immutable historical versions wherever loss of history would be dangerous."

Applied per entity family below. **Default posture: append-only, supersession by pointer, never destructive
update**, unless a specific entity is explicitly justified as pure current-state (rare — see the EVENT
HISTORY + CURRENT STATE split in `entity-catalog.md`).

| Entity family | Versioning rule | Immutable historical versions required? |
|---|---|---|
| Source | `source_document_version` — only changes if the actual PDF binary is later supplied (currently version 1, text-extraction-only per Step 0's manifest) | Yes, though not expected to change often |
| Schema | `schema_registry` — SCHEMA-001 through 006 all coexist; a future canonical version is a NEW row with `supersedes` pointing backward, never an edit to an existing row | Yes — mandatory (ADR-0004) |
| Contract | Every `docs/contracts/*.md` file states an explicit version number (starts at `v0.1-DRAFT` for Step 2, see `contracts/README.md`); a breaking field change requires a new version file/section, not an edit of the old one | Yes |
| Configuration | `configuration_version` — `CONFIG-V1 → CONFIG-V2 → ...` per `docs/architecture/configuration.md`; every change produces a `configuration_change` + `audit_event` | Yes — mandatory |
| Agent | `agent_version` (the agent ROLE's definition/prompt/capability set changes over time) vs. `agent_instance` (a running instantiation) vs. `agent_state` (append-only runtime history) — three distinct versioning axes, not conflated | Yes |
| Worker | `worker_version` + `worker_lifecycle_event` (append-only) | Yes |
| Prompt | `prompt_version` — every distinct prompt text used gets its own row; the source's own 4 distinct system-prompt DRAFTS (`docs/source-extraction/code-blocks.md`) are themselves an example of this pattern happening informally, now formalized | Yes — mandatory (Section 26 explicit) |
| Model | `model_version` — e.g., `gpt-4o-2024-08-06` vs. `claude-3-5-sonnet-20241022` are different rows, never conflated; historical claims keep their ORIGINAL model_version_id forever | Yes — mandatory (Section 26: "Do not assume the latest model produced historical results") |
| Tool | `tool_version` | Yes |
| Connector | `connector_version` — a platform-scraper connector's version at time of ingestion is recorded on every `raw_record` | Yes |
| Event | Events are inherently immutable by construction (Section 27) — there is no "event_version" meaning "this event changed"; `event_version` instead means "which VERSION OF THE EVENT TYPE'S PAYLOAD SCHEMA" (i.e., it's a schema-version tag, not a mutation marker) | N/A — immutability is structural, not a separate versioning axis |
| Claim | Claims are not "versioned" in the edit sense — a changed assertion produces a NEW `claim` row; the OLD claim's `status` may transition to `SUPERSEDED` but its content is untouched | Yes |
| Evidence | Evidence is immutable once created (Section 12: "Do not allow a claim to lose its supporting evidence") — no versioning needed because evidence is never edited, only added | N/A — immutable by construction, not versioned |
| Strategy | `strategy_version` — the Strategy Ledger's win-rate/confidence-score fields update over time, but as NEW rows (append-only performance history), never overwriting the prior observation | Yes |
| Metric | `metric_definition` → `metric_version` — a metric's definition can evolve (e.g., a new calculation method), each a new version, old ones retained for backward comparability | Yes |

## Version identifier convention

Per `identifier-strategy` (see `integrity-rules.md`): every `*_version` entity uses a **monotonically
increasing integer per parent entity** (e.g., `configuration_version.version = 1, 2, 3...` scoped to one
`configuration_id`), NOT a semantic version string like "v2.1.3" — this avoids encoding business meaning into
an identifier (Step 2 Section 41's explicit rule) while still supporting simple "give me the latest" and
"give me version N" queries. Contract-level documents (`docs/contracts/*.md`) use human-readable semantic
versions (e.g., `v0.1-DRAFT`) since those are DOCUMENTATION artifacts, not database rows — this distinction
is deliberate, not an inconsistency.

## Supersession, not deletion

Every "new version replaces old version" relationship in this system is a **pointer** (`supersedes_id` /
`superseded_by_id`), never a `DELETE`. This applies uniformly to: schema versions, configuration versions,
agent versions, and — critically — to how a future resolution of CONFLICT-001 through 007 must be recorded:
resolving a conflict creates a NEW `conflict` row transition (`status: OPEN → RESOLVED`) with a
`resolution`/`resolver`/`resolved_at` fields populated, but the conflict's original `conflict_participant`
rows (both sides) remain exactly as they were — resolving a conflict never deletes the losing side's claim.

## Explicit non-goal

This document does not choose a physical versioning MECHANISM (e.g., temporal tables, SCD Type 2, event
sourcing with snapshots) — that is a database-technology-dependent implementation decision, deferred per
`open-decisions.md` #7. It defines WHAT must remain versioned/recoverable, not HOW.
