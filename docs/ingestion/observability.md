# Observability

Per Step 3 Sections 49-51. Implementation: `src/common/logging_utils.py`, `src/common/health.py`.

## Structured logging (Step 3 Section 49)

`log_structured()` is the ONLY logging entry point ingestion code uses (`src/ingestion/engine.py`
calls it at every major transition: `ingestion_started`, `raw_record_stored`,
`raw_record_duplicate`, `raw_record_quarantined`, `observation_created`, `ingestion_completed`).
Every call is redacted (`redact()`) before serialization, so secret-like field names
(`password|api[_-]?key|secret|token|credential|authorization`) can never leak into logs even if a
future caller passes them in by mistake — the redaction is not opt-in per call site.

## Metrics (Step 3 Section 50)

Not implemented as a separate metrics-emission pipeline in Step 3 (no metrics backend is chosen —
`open-decisions.md` #10 territory) — but every metric Section 50 names is DERIVABLE from existing
stores without any additional instrumentation: `ingestion_runs_total` = `len(run_store.all())`,
`records_received/accepted/quarantined/failed/duplicated_total` = summed `IngestionRun` counters,
`records_versioned_total` = count of raw records with non-null `supersedes_raw_record_id`. This is
intentional: raw counters are preserved (never replaced by aggregates, per Section 50's explicit
instruction), and aggregation is a pure read-side computation over them.

## Health checks (Step 3 Section 51)

`HealthRegistry` + `simple_health()`. Implemented for: `source_registry`
(`SourceRegistry.health_check()`), `raw_record_store` (`RawRecordStore.health_check()`),
`observation_store` (`ObservationStore.health_check()`), `ingestion_engine`
(`IngestionEngine.health_check()`). Each distinguishes `HEALTHY | DEGRADED | UNHEALTHY | UNKNOWN`
per Section 51's exact requirement; a health check that itself raises an exception is reported
`UNHEALTHY`, never silently `HEALTHY` (see `HealthRegistry.check()`'s `except` clause).

Not yet implemented: `storage` (n/a — no external storage backend exists yet, in-memory only),
`connector_registry` (no separate registry exists; connectors are constructed directly),
`event_system` (the `EventLog` itself has no dedicated health check yet), `quarantine` (no
dedicated health check yet, though `QuarantineStore.all()`/`.active()` support building one
trivially). These are flagged gaps, not silently skipped without acknowledgment.

## Source IDs / Requirements

`docs/architecture/observability.md`'s 15 signal types (Step 1); this document operationalizes
the ingestion-relevant subset.
