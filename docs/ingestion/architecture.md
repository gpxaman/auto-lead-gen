# Ingestion Architecture

Per Step 3 Section 60. Maps the intended conceptual flow onto the actual implementation.

```
SOURCE                    src/sources/models.py::Source
    |
SOURCE REGISTRY           src/sources/registry.py::SourceRegistry
    |
CONNECTOR                 src/connectors/base.py::Connector (SyntheticFileConnector implements it)
    |
INGESTION RUN              src/raw/models.py::IngestionRun  (created in IngestionEngine.run_ingestion)
    |
INGESTION ITEM              src/raw/models.py::IngestionItem (created per source_identifier)
    |
RAW RECORD                   src/raw/store.py::RawRecordStore.store_new_version
    |
HASH / VERSION CHECK          src/common/hashing.py::compute_content_hash + RawRecordStore.classify_incoming
    |
SECURITY INSPECTION            src/security/inspector.py::inspect (deterministic, no LLM)
    |
QUARANTINE OR PROCESS           src/quarantine/store.py::QuarantineStore  <-or-> continue
    |
NORMALIZATION                    src/observations/normalizer.py::normalize
    |
OBSERVATION                       src/observations/models.py::Observation
    |
(FUTURE CLASSIFICATION -- out of scope, per Step 3 Section 57)
```

Orchestrated by `src/ingestion/engine.py::IngestionEngine.run_ingestion()`, which is the single
entry point implementing this entire chain per external item, per Step 3's Absolute Rule
(nothing summarized, rewritten, or discarded at any stage).

## Preserved alongside the primary flow (per Step 3's closing "PERMANENT RULE")

- RAW RECORD + ALL VERSIONS — `RawRecordStore`'s `supersedes_raw_record_id` chain (`versioning.md`)
- ALL EVENTS — `src/common/events.py::EventLog`, immutable, append-only
- ALL FAILURES — `IngestionItem.processing_status = FAILED` rows, never deleted (`failure-handling.md`)
- ALL SECURITY RESULTS — `SecurityAnalysisResult`, stored separately from raw payload (`security.md`)
- ALL PROVENANCE — `src/provenance/trace.py::trace_observation` (`docs/database/provenance.md`)

## Source IDs

SRC-000009 (Recon Engine pipeline diagram), SRC-000013 (scraper skeleton), SRC-000053 (Layer 0
deterministic pre-filter). Requirements: REQ-000009, REQ-000029.

## Relationship to prior steps

- Layer 0 (`docs/architecture/canonical-architecture.md`) = this ingestion pipeline's Deterministic
  Triage stage (security inspection + schema detection are the concrete Layer-0-adjacent logic;
  the classic "keyword blacklist" concept from the source lives in `src/security/inspector.py`'s
  pattern set, generalized to injection/anti-bot-trap detection specifically — the BUDGET SANITY
  FILTER (THRESH-015) is registered in `src/ingestion/config_seed.py` but its numeric-plausibility
  CHECK LOGIC is not yet implemented in Step 3, since no real RFQ-with-price-and-volume fixture
  exists yet to exercise it; this is a known, flagged gap for the first real connector, not a
  silent omission).
- `docs/database/schema.sql`'s `raw_record` table = `src/raw/models.py::RawRecord`, field-for-field
  (Step 3 Section 12 explicit: not a second competing implementation).
