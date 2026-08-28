# Ingestion — IECHM-LIOS Step 3

This directory documents the raw ingestion foundation built in Step 3. It links code
(`src/sources/`, `src/connectors/`, `src/raw/`, `src/security/`, `src/quarantine/`,
`src/observations/`, `src/schemas/`, `src/provenance/`, `src/ingestion/`), tests (`tests/...`),
and the governing architecture/requirements/source material.

## What Step 3 is

The first OPERATIONAL (not just documented) piece of IECHM-LIOS: a deterministic pipeline that
receives external data and preserves it without loss. Implements
`docs/architecture/canonical-architecture.md`'s Layer 0 (deterministic pre-filter) and the
RAW/OBSERVATION stages of `docs/database/logical-data-model.md`'s 9-stage lineage.

## What Step 3 is explicitly NOT

- Not lead qualification, client classification, scoring, or strategy (Step 3 Section 57).
- Not an autonomous agent swarm — the engine is deterministic, no LLM call exists anywhere in
  `src/` (Step 3 Section 58).
- Not live platform scraping — only `SyntheticFileConnector` (Step 3 Section 40) and the test-only
  `ScriptedConnector` (`tests/helpers.py`) exist; no real platform connector is implemented
  (Step 3 Section 38).
- Not physical manufacturing execution (Step 3 Section 59).
- Not a resolution of any open decision (`docs/architecture/open-decisions.md`) — see each
  document below for how the ambiguity is preserved.

## Document index

| Document | Covers |
|---|---|
| `architecture.md` | The conceptual flow (Step 3 Section 60) mapped onto actual modules |
| `source-registry.md` | `src/sources/` — Source/SourceVersion/SourceEndpoint/SourcePolicy/SourceHealth |
| `connector-interface.md` | `src/connectors/` — the Connector ABC and SyntheticFileConnector |
| `ingestion-lifecycle.md` | `src/ingestion/engine.py` — the run/item/raw-record pipeline |
| `raw-data.md` | `src/raw/` — RawRecord, hashing, version chaining |
| `deduplication.md` | Exact-duplicate vs. possible-duplicate vs. distinct-record logic |
| `versioning.md` | Source versioning, raw-record versioning, schema-version coexistence |
| `replay.md` | `IngestionEngine.replay()` — reprocessing without mutating history |
| `quarantine.md` | `src/quarantine/` and `src/security/` — the SAFE/SUSPICIOUS/MALICIOUS/UNKNOWN routing |
| `security.md` | The external-content-is-never-an-instruction trust boundary |
| `failure-handling.md` | Failure reasons, retries, dead-letter concept, partial-success semantics |
| `observability.md` | Metrics, structured logging, health checks |
| `testing.md` | The 98-test suite (52 Step 2 + 46 Step 3) and what each category proves |

## Source/requirement/ADR traceability

Every document below cites `SRC-XXXXXX`, `REQ-XXXXXX`, and ADR IDs where applicable, consistent
with `docs/requirements/source-traceability.csv`'s Step 3 columns.
