# Failure Handling

Per Step 3 Sections 29-31. Implementation: `src/raw/models.py::FailureReason`,
`src/ingestion/engine.py`.

## Failure reasons (Step 3 Section 29, exact list)

`NETWORK_FAILURE`, `TIMEOUT`, `AUTH_FAILURE`, `RATE_LIMITED`, `MALFORMED_RESPONSE`,
`UNKNOWN_SCHEMA`, `SECURITY_QUARANTINE`, `PARSER_FAILURE`, `STORAGE_FAILURE`, `DUPLICATE`,
`PARTIAL_SUCCESS` — all 11 defined in `FailureReason`. Step 3's engine currently exercises
`NETWORK_FAILURE` (connector fetch exceptions) and `STORAGE_FAILURE` (unexpected exceptions during
processing); the rest exist in the enum for future connectors to use as they encounter those
conditions — not invented usage, just not yet triggered by the synthetic test scenarios.

## No silent success reclassification (Step 3 Section 29)

`IngestionRun.status` is computed strictly from whether ANY item failed
(`any_failure`) and whether ANY item succeeded (`any_success`):
`COMPLETED` only if zero failures; `PARTIAL` if a mix; `FAILED` if zero successes. There is no
code path that marks a run `COMPLETED` while a failure occurred.

## Retryable vs. non-retryable (Step 3 Section 30)

Not automated in Step 3 (no retry-scheduling logic exists yet — Step 3 builds the deterministic
foundation, not a production retry scheduler). Conceptually documented: `NETWORK_FAILURE`,
`TIMEOUT`, `RATE_LIMITED` are RETRYABLE; `MALFORMED_RESPONSE`, `UNKNOWN_SCHEMA`,
`SECURITY_QUARANTINE` are NON_RETRYABLE (retrying does not change a fundamentally quarantined or
malformed item's outcome — and per Section 30's explicit instruction, "security quarantine should
not be bypassed simply because retries are available," which this system respects by construction:
nothing in `IngestionEngine` ever re-attempts a quarantined item automatically).

## Dead-letter (Step 3 Section 31)

`ProcessingStatus.DEAD_LETTERED` exists in the enum as a conceptual target state but no automatic
dead-letter QUEUE/promotion logic is implemented in Step 3 (no fixture requires it — items either
succeed, get quarantined, or fail with a permanent `IngestionItem` record, which already satisfies
"must remain recoverable" without needing a separate dead-letter mechanism at this scale). Flagged
as a `PROPOSED_EXTENSION` for a future step once retry scheduling exists.

## Idempotency (Step 3 Section 28)

See `deduplication.md` (content-hash-based) and `src/common/events.py::EventLog`'s
`idempotency_key` deduplication (event-level). Both are tested in
`tests/ingestion/test_idempotency_and_failures.py`.

## Source IDs / Requirements

None directly (failure taxonomy is `PROPOSED_EXTENSION`, required by Step 3's own instructions
rather than the original source PDF).
