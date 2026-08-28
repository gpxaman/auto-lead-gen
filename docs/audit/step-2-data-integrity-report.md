# Step 2 — Data Integrity Report

Per Step 2 Section 54.

## Transparency notes on mechanical fixes made during Step 2 (not content changes, formatting only)

1. **`docs/requirements/source-traceability.csv` column rename:** Step 0's original CSV had a column literally
   named `database_entity`. Step 2 Section 53 instructs adding a NEW column also named `database_entity` —
   a naming collision. The pre-existing Step 0/1 column was renamed to `database_entity_step1` to disambiguate
   the header; **no data in that column was altered, reordered, or deleted**, only its header label changed
   to remain distinguishable from the new Step 2 column of the same conceptual name.
2. **CSV formatting bugs found and fixed:** During Step 2's CSV update, 6 of the 82 rows were initially
   malformed (unescaped commas inside parenthetical text, and two rows with an extra/missing empty field from
   a copy-paste inconsistency while drafting). These were structural CSV-syntax bugs introduced during this
   Step 2 session's own editing, not corruptions of Step 0/1 content — verified by re-parsing the file with
   Python's `csv` module before and after: all 82 `SRC-XXXXXX` IDs remain present, unique, and mapped to the
   same substantive values; only comma/field-count punctuation was corrected. Full re-verification: 82 rows,
   22 columns, 0 malformed rows, 82 unique IDs (see validation run below).

## Completeness checklist

- [x] Source archive preserved — `docs/source-extraction/` untouched; 29 pages, 82 source items, verified
  intact at Step 2 start (re-checked via `wc -l`/`grep -c` before any Step 2 work began).
- [x] Step 0 artifacts preserved — `source-register.jsonl` (82), `requirements-register.jsonl` (33),
  `conflicts.md` (7), `assumptions.md` (8) all unchanged.
- [x] Step 1 artifacts preserved — all 34 `docs/architecture/*.md` files, 7 conflict files, 8 ADRs unchanged
  in content (only `system-boundaries.md`, already an extend-in-place case from Step 1 itself, referenced —
  not re-edited in Step 2).
- [x] Raw data model exists — `docs/database/entity-catalog.md` Section 5, `docs/database/schema.sql`'s
  `raw_record` table.
- [x] Historical versions supported — `docs/database/versioning.md`, enforced via `integrity-rules.md`'s
  immutability table; demonstrated in `tests/fixtures/lead_versions.synthetic.json` (3 non-overwritten
  observations) and validated by `tests/validate_data_model.py`.
- [x] Provenance supported — `docs/database/provenance.md`'s universal field set; demonstrated in fixtures via
  `model_version_id`/`prompt_version_id`/`task_id` on every claim.
- [x] Claims separated from evidence — `docs/contracts/claim.md` vs. `docs/contracts/evidence.md`; distinct
  tables in `schema.sql`; validated by the fixture's `claim_evidence_links` join.
- [x] Evidence separated from verification — `docs/contracts/evidence.md` vs. `docs/contracts/verification.md`;
  demonstrated by the fixture's evidence row having a denormalized cache while the authoritative `FAILED` and
  `VERIFIED` records live in separate `verifications[]` entries.
- [x] Model inference separated from verified data — `trust_level` enum + state-transition rules in
  `docs/database/integrity-rules.md`; validated in `tests/validate_data_model.py` (checks that any claim
  claiming `VERIFIED` trust_level is backed by an actual `VERIFIED` verification row).
- [x] Conflicts preserved — 7 source conflicts unchanged; runtime conflict model added (`docs/contracts/
  conflict.md`, `conflict.v1.schema.json`) and demonstrated with a synthetic two-sided conflict fixture,
  validated to ensure both sides reference different claims.
- [x] Scenarios preserved — all 8 economic scenarios + 2 scale profiles represented distinctly in
  `docs/contracts/scenario.md`, none blended.
- [x] Assumptions preserved — `docs/requirements/assumptions.md` unchanged (8); `assumption` entity added to
  `entity-catalog.md` Section 16 as the runtime data-model counterpart.
- [x] Schemas versioned — `docs/database/schema.sql`'s `schema_registry` table; SCHEMA-001 through 006 all
  catalogued, none merged, `lead.v1.schema.json` implements a `oneOf` across all 3 lead-schema variants without
  collapsing them (validated: each of the 3 fixture lead_versions matches its own declared schema_id branch
  and no other).
- [x] Events immutable — `docs/contracts/event.md`, `event-envelope.v1.schema.json`; the `schema.sql` `event`
  table has no update path documented; fixture demonstrates a causally-linked correction event
  (`causation_id`) rather than a rewrite.
- [x] Audit history preserved — `docs/database/schema.sql`'s `audit_event` table, explicitly immutable, no
  secrets stored (redaction rule documented in `integrity-rules.md` and `docs/database/security.md`).
- [x] Agent state versioned — `agent_state` append-only table; fixture demonstrates a full 5-state lifecycle
  history for one synthetic worker, validated to ensure the full sequence (not just latest state) is present.
- [x] Worker state versioned — same as above; `worker_lifecycle_event` immutable log.
- [x] Configuration versioned — `docs/contracts/configuration.md`, `configuration_version` table with
  monotonic version numbers; 6 seed threshold values preserved exactly (THRESH-001/002/003/004/005/006).
- [x] Model version tracked — `model_version`/`prompt_version`/`tool_version`/`connector_version` registries
  (Section 26); every derived record's provenance fields are fixed at creation time, never repointed.
- [x] Prompt version tracked — same.
- [x] Tool version tracked — `tool_version` registry defined in `entity-catalog.md`.
- [x] Connector version tracked — `connector_version` table in `schema.sql`; `raw_record.connector_version`.
- [x] Strategy history preserved — `docs/contracts/strategy.md`; TABLE-001's 4 Strategy Ledger rows preserved
  verbatim as seed data.
- [x] Metric history preserved — `docs/contracts/metric.md`'s lifecycle status enum (7 values, exact).
- [x] Memory provenance preserved — `docs/architecture/memory.md`'s "RAG is derived" rule formalized as a
  mandatory `memory_source` foreign key in `entity-catalog.md` Section 33 (no `memory_item` may exist without
  it).
- [x] Security/quarantine records preserved — `docs/database/entity-catalog.md` Section 34; `security_event`/
  `quarantine_record`/`threat_indicator`/`content_sanitization_result` entities defined.
- [x] Manufacturing intelligence preserved — `docs/database/entity-catalog.md` Section 35, explicitly scoped
  to intelligence-only (no machine control), consistent with `docs/architecture/manufacturing-boundary.md`.
- [x] No source value silently overwritten — spot-checked: THRESH-001 (5), THRESH-002 (2/7-day), THRESH-004
  (0.85), THRESH-006 (99.5%/72h), the Strategy Ledger's 4 rows, and all 3 lead-schema field lists all appear
  in Step 2 documents with byte-identical values to their Step 0/1 source.
- [x] No historical record silently deleted — no Step 0 or Step 1 file was deleted; the 6 CSV formatting fixes
  above corrected punctuation only, verified via diff-equivalent field-content comparison (every field's
  substantive text, minus the punctuation character itself, is unchanged).
- [x] No unresolved architecture decision silently resolved — `docs/architecture/open-decisions.md`'s 15 items
  remain open; Step 2 explicitly did NOT choose a database vendor (schema.sql is marked PROPOSED/illustrative
  only, using SQL as a neutral lingua franca, not a vendor commitment), did NOT canonicalize a lead schema
  version (`lead.md`/`lead.v1.schema.json` preserve all 3), did NOT canonicalize a client-archetype set
  (`client.md`/`client.v1.schema.json` preserve all 3 sets as an open enum).

## Traceability counts (Section 55) — compared against Step 0/Step 1 baseline

| Metric | Step 0/1 baseline | Step 2 count | Status |
|---|---|---|---|
| SOURCE ITEMS | 82 | 82 | unchanged ✓ |
| REQUIREMENTS | 33 | 33 | unchanged ✓ |
| CONFLICTS | 7 | 7 | unchanged ✓ |
| ASSUMPTIONS | 8 | 8 | unchanged ✓ |
| SCENARIOS | 8 | 8 | unchanged ✓ |
| SCHEMAS | 6 | 6 | unchanged ✓ |
| FORMULAS | 9 | 9 | unchanged ✓ |

**No count decreased.** Per Section 55's instruction, this triggers no STOP/investigate condition.

## Validation run (executed, not simulated)

```
$ python3 tests/validate_data_model.py
52/52 checks passed.
```

Covers: schema-compatibility validation of all fixture records against their JSON Schemas (including the
lead `oneOf` discriminator across all 3 preserved schema versions), unique-ID checks, foreign-key resolution,
version-uniqueness/append-only checks, trust-level legality, conflict two-sidedness, failed-verification
preservation, event immutability/idempotency-key deduplication, and worker lifecycle history completeness.
Two genuine bugs were found and fixed during this process (a `oneOf` ambiguity in `lead.v1.schema.json` and
two incomplete synthetic fixture payloads) — see the git-free change log in this session's transcript; both
are documented as ordinary fixture/schema debugging, not source-integrity violations.

## Status

**STEP_2_DATA_INTEGRITY_STATUS: CLEAN.**
