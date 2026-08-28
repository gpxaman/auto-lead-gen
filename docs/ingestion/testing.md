# Testing

Per Step 3 Sections 40-46, 55-56. All tests use `unittest` (Python stdlib) plus `jsonschema`
(already a dependency from Step 2). No production data anywhere — every fixture is marked
`"synthetic": true` and `"no_real_client_data": true`.

## Full suite composition

| Package | File(s) | Covers |
|---|---|---|
| Step 2 (backward compat) | `tests/validate_data_model.py` | 52 checks — re-run in Step 3 to prove nothing broke (Section 56) |
| `tests/ingestion/` | `test_engine_pipeline.py`, `test_idempotency_and_failures.py`, `test_envelope_schema.py` | 10 required scenarios (Section 41), retry/partial-failure (28-30), envelope schema validity |
| `tests/raw/` | `test_round_trip.py` | Mandatory raw round-trip test (Section 42) |
| `tests/security/` | `test_security.py` | Deterministic detection + trust-boundary proof (Section 45) |
| `tests/versioning/` | `test_versioning.py` | Raw-record and source versioning (Section 46) |
| `tests/replay/` | `test_replay.py` | Replay without mutating history (Section 32) |
| `tests/provenance/` | `test_provenance.py` | Full 8-hop provenance chain (Section 44) |
| `tests/sources/` | `test_registry.py` | Source Registry API + UNKNOWN semantics |
| `tests/connectors/` | `test_synthetic_connector.py` | Connector interface constraints |
| `tests/observations/` | `test_normalizer.py` | Non-lossy normalization |
| `tests/test_data_loss.py` | (top-level) | Comprehensive data-loss suite (Section 43, all 11 listed conditions) |

## Result (this session, executed)

```
STEP 2 TESTS: 52/52 passed
STEP 3 TESTS: 46/46 passed
TOTAL: 98/98 passed
```

## Backward compatibility (Step 3 Section 56)

`tests/validate_data_model.py` was run BEFORE any Step 3 code was written (to confirm the Step 2
baseline) and AGAIN after all Step 3 work was complete — identical 52/52 result both times. No
Step 2 contract, fixture, or schema was modified during Step 3 (only the NEW
`ingestion-envelope.v1.schema.json` was added).

## Bugs found and fixed during Step 3 development (transparency)

1. `docs/contracts/schemas/ingestion-envelope.v1.schema.json`'s `schema_detection` property did
   not initially accept `null`, causing `test_envelope_validates_against_json_schema` to fail for
   the common case where schema detection metadata isn't yet available. Fixed by widening the
   type to `["object", "null"]`.

No other bugs were found; all other tests passed on first implementation.
