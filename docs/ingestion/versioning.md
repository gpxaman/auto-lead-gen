# Versioning (Ingestion-Specific)

Per Step 3 Sections 14, 46. See also `docs/database/versioning.md` for the general project-wide
versioning discipline; this document covers the ingestion-layer specifics.

## Raw record version chains

`RawRecordStore._version_chains: dict[(source_id, source_identifier), list[record_id]]` — an
append-only ordered list per `(source, source_identifier)` pair. `store_new_version()` always
appends; `supersedes_raw_record_id` links each new version to its immediate predecessor.
`get_version_chain()` returns the FULL, un-truncated history. Verified in
`tests/versioning/test_versioning.py::test_changed_content_creates_new_version_without_destroying_v1`.

## Source versioning

`SourceRegistry.update_source_version()` never edits an existing `SourceVersion` — it computes the
next monotonic version number, copies forward unset fields from the prior version, and appends a
new row. Verified in `test_source_configuration_update_preserves_prior_version`.

## Schema-version coexistence

`src/schemas/detection.py::detect_schema()` recognizes SCHEMA-002, SCHEMA-003, and SCHEMA-005
independently, using each schema's own discriminator fields — no payload is ever coerced into a
schema it doesn't structurally match. Verified in
`tests/ingestion/test_engine_pipeline.py::TestEngineMultipleSchemaVersions`.

## Observation versioning (via replay)

See `replay.md` — `Observation` rows are always freshly created (new `observation_id` per call to
`new_observation()`), so there is no update path that could overwrite `normalizer_version=1.0`
results with `normalizer_version=2.0` results.

## Source IDs / Requirements

SRC-000036 (worker versioning concept, generalized here to data versioning),
`docs/architecture/schema-versioning.md`, ADR-0004.
