# Replay

Per Step 3 Sections 32-33. Implementation: `src/ingestion/engine.py::IngestionEngine.replay()`.
Tests: `tests/replay/test_replay.py`.

## Separating INGESTION from PROCESSING (Step 3 Section 33)

```
RAW V1  ->  NORMALIZER V1  ->  OBSERVATION V1     (original ingestion)
RAW V1  ->  NORMALIZER V2  ->  OBSERVATION V2     (later replay, same raw record)
```

`replay(raw_record_id, normalizer_version="2.0")`:
1. Looks up the EXISTING raw record (does not re-fetch from the connector — the whole point is to
   reprocess something already safely stored).
2. Re-runs schema detection + normalization against that unchanged raw payload.
3. Creates a brand-new `Observation` row tagged with the given `normalizer_version`.
4. Emits a new `ObservationCreated` event with `payload.replay = true`.

The original raw record is never touched (no write path in `replay()` touches `RawRecordStore` at
all beyond a read via `.get()`), and the original `Observation` remains fully queryable via
`ObservationStore.by_raw_record()`, which returns ALL observations ever derived from that raw
record, across every normalizer version.

## Why this matters (Step 3 Section 32's stated rationale)

"This will be important for future model/schema changes" — e.g., once
`open-decisions.md` #2 (canonical lead schema) is resolved, every historical raw record can be
REPLAYED through a new normalizer targeting the newly-chosen schema, producing fresh Observations
without needing to re-scrape anything or destroy the original SCHEMA-002/003/005-tagged
observations.

## Source IDs / Requirements

Extends `docs/database/migrations.md`'s non-destructive migration pattern down to the
observation layer.
