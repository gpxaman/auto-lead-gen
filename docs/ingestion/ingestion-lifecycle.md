# Ingestion Lifecycle

Per Step 3 Sections 10-11, 26. Implementation: `src/ingestion/engine.py`, `src/raw/models.py`.

## `IngestionRun` (Step 3 Section 10)

One per `run_ingestion()` call. Status: `STARTED -> RUNNING -> COMPLETED | PARTIAL | FAILED |
CANCELLED`. Counters (`records_received/accepted/quarantined/failed/duplicated`) update
incrementally per item and are persisted after every item (`run_store.save(run)` inside the loop),
so partial progress is never lost even if the process were interrupted mid-run. **Failed runs are
never erased** — `IngestionRunStore.save()` always upserts, never deletes.

## `IngestionItem` (Step 3 Section 11)

One per received `source_identifier` per run, created BEFORE fetch is even attempted — so even a
network failure that never produces a raw record still gets a permanent `IngestionItem` row with
`processing_status = FAILED`. Unknown/malformed content proceeds through the SAME item lifecycle as
known content; there is no code path that skips creating an `IngestionItem`.

## Processing status flow

```
RECEIVED -> SECURITY_INSPECTED (implicit, not a stored intermediate state) -> QUARANTINED
                                                                             or NORMALIZED
                                                                             or FAILED
                                                                             or DEAD_LETTERED (not yet reached in Step 3, see failure-handling.md)
```

## Canonical Lead extraction boundary (Step 3 Section 23)

**`CANONICAL_LEAD_SCHEMA_DEFERRED`** — see `src/ingestion/lead_candidate.py` for the full
rationale. No `Lead`/`LeadVersion` class exists in `src/`. An `Observation` with
`observation_type = "lead_candidate"` is Step 3's intermediate representation, chosen because it
already exists in the Step 2 architecture for exactly this purpose and does not require resolving
`open-decisions.md` #2 (canonical lead schema version).

## Source IDs / Requirements

SRC-000009, SRC-000013, SRC-000053. REQ-000007, REQ-000009, REQ-000029.
