# Deduplication

Per Step 3 Sections 14-15. Implementation: `src/raw/store.py::RawRecordStore.classify_incoming`.

## Three-way distinction (Step 3 Section 15, exact)

| Status | Meaning | Implementation |
|---|---|---|
| `EXACT_DUPLICATE` | Same `(source_id, source_identifier, content_hash)` seen before | Looked up in `_dedup_index`; the EXISTING `raw_record_id` is linked, no new raw record created |
| `POSSIBLE_DUPLICATE` | Not implemented in Step 3 -- would require fuzzy/semantic similarity detection across DIFFERENT `source_identifier`s, which needs classification logic explicitly out of scope for Step 3 (Section 57). The enum value exists (`src/raw/models.py::DuplicateStatus.POSSIBLE_DUPLICATE`) for future use; nothing in Step 3 currently produces it | -- |
| `DISTINCT_RECORD` | New `source_identifier`, OR same `source_identifier` with a DIFFERENT content hash (a legitimate content change) | Default outcome |

## The incoming observation is never deleted, even for exact duplicates (Step 3 Section 15)

An `IngestionItem` row is ALWAYS created and saved, and a `RawRecordReceived` event is ALWAYS
emitted, even when the underlying content is an exact duplicate — only the creation of a SECOND
`RawRecord` row is skipped. See `tests/ingestion/test_idempotency_and_failures.py::
test_retry_of_identical_delivery_deduplicates_events_but_stays_auditable`.

## Possible-duplicate resolution is manual, not automatic (Step 3 Section 15)

Since Step 3 does not implement `POSSIBLE_DUPLICATE` detection, no automatic-merge logic exists
at all for this status — the architecture's requirement ("do not automatically merge... create a
relationship requiring later resolution") is trivially satisfied by not yet having a path that
could auto-merge anything cross-identifier.

## Source IDs / Requirements

Implements `docs/database/integrity-rules.md`'s idempotent-ingestion rule
(`UNIQUE (source_system, source_identifier, content_hash)`).
