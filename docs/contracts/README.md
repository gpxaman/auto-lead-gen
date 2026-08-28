# Data Contracts — IECHM-LIOS

Per Step 2 Sections 20 and 49. This directory defines versioned, conceptual data contracts for every major
domain the canonical architecture (Step 1) and data foundation (Step 2) require. **These are documentation
contracts, not running API implementations** — no production endpoint exists (Step 2 Section 56).

## Status of this contract set

All contracts in this directory are version `v0.1-DRAFT` — the FIRST formalization of these shapes, produced
directly from the logical data model in `docs/database/`. None has been implemented, none has been reviewed/
approved by the user, and none resolves the open decisions in `docs/architecture/open-decisions.md`.

## Universal contract structure

Every contract file below follows the same skeleton:

1. **Name, version, status** — always `v0.1-DRAFT` at this stage.
2. **Purpose** — one paragraph.
3. **Source references** — `SRC-XXXXXX` IDs this contract is built from.
4. **Requirement references** — `REQ-XXXXXX` IDs this contract satisfies.
5. **Fields** — required and optional, each tagged `SOURCE_SCHEMA` (verbatim from source), `DERIVED_CANONICAL_SCHEMA`
   (built from source + architecture reasoning), or `PROPOSED_SCHEMA`/`PROPOSED_EXTENSION` (architecturally
   necessary but not source-derived).
6. **Validation rules** — what makes an instance of this contract valid.
7. **Provenance** — how this contract's instances carry the universal provenance field set (`docs/database/provenance.md`).
8. **Versioning & compatibility** — how this contract itself evolves.
9. **Security classification** — per `docs/database/security.md`'s 5-level scheme.
10. **Examples** — **only included where the SOURCE itself provides an example.** No source examples are
    fabricated (Step 2 Section 49's explicit prohibition).

## Contract index

| Contract | File | Primary source schema(s) | Status |
|---|---|---|---|
| Lead | `lead.md` | SCHEMA-002, SCHEMA-003, SCHEMA-005 (all 3 preserved, none canonicalized — CONFLICT-003) | `v0.1-DRAFT` |
| Client | `client.md` | 3 non-identical archetype sets (CONFLICT-004) | `v0.1-DRAFT` |
| Platform | `platform.md` | SRC-000035, TABLE-003 | `v0.1-DRAFT` |
| Subdomain | `subdomain.md` | THRESH-001/002, SRC-000036 | `v0.1-DRAFT` |
| Claim | `claim.md` | `PROPOSED_EXTENSION` wrapper around source-derived classification behavior | `v0.1-DRAFT` |
| Evidence | `evidence.md` | SCHEMA-003 `verification_artifacts` | `v0.1-DRAFT` |
| Verification | `verification.md` | SRC-000039 | `v0.1-DRAFT` |
| Agent | `agent.md` | `docs/architecture/agent-topology.md` | `v0.1-DRAFT` |
| Task | `task.md` | Implied by Task State (`context-migration.md`) | `v0.1-DRAFT` |
| Worker | `worker.md` | `docs/architecture/dynamic-worker-scaling.md`, `hot-swap.md` | `v0.1-DRAFT` |
| Event | `event.md` | SCHEMA-004/006, `docs/architecture/events.md` | `v0.1-DRAFT` |
| Configuration | `configuration.md` | `docs/architecture/configuration.md`, THRESH-001-015 | `v0.1-DRAFT` |
| Telemetry | `telemetry.md` | `docs/architecture/observability.md` | `v0.1-DRAFT` |
| Strategy | `strategy.md` | SRC-000006/007 (System B, referenced) | `v0.1-DRAFT` |
| Metric | `metric.md` | `docs/architecture/metric-evolution.md`, THRESH-006 | `v0.1-DRAFT` |
| Scenario | `scenario.md` | `docs/source-extraction/economic-scenarios.md` | `v0.1-DRAFT` |
| Conflict | `conflict.md` | `docs/requirements/conflicts.md` (7 conflicts) | `v0.1-DRAFT` |

## System boundary note

Per `docs/architecture/system-boundaries.md`, contracts for `agent`/`task`/`worker`/`event`/`configuration`/
`telemetry` are System-A-INTERNAL (IECHM-LIOS's own operational data). `lead`/`client`/`platform`/`subdomain`
are System-A's PRODUCT (what it produces for System B, via the still-`INTERFACE_UNDEFINED` boundary — see
`docs/architecture/api-boundaries.md`). `strategy` is primarily a System-B concept, included here for
interface-readiness and the `PROPOSED_EXTENSION` System-A reuse case only.

## JSON Schemas

Machine-readable JSON Schema files for a subset of the above (where the underlying shape is stable enough to
be worth formalizing at Step 2) are under `contracts/schemas/` — see that directory's own files for the
`SOURCE_SCHEMA` / `DERIVED_CANONICAL_SCHEMA` / `PROPOSED_SCHEMA` marking convention.
