# Evidence Model

Per Step 1 Section 17. An LLM statement is NOT automatically evidence — this document formalizes that
distinction and preserves every source concept around proof/verification.

## The 5 conceptually distinct categories (per Step 1's explicit instruction)

| Category | Definition | Source basis |
|---|---|---|
| CLAIM | A statement an agent produces about a lead/client/platform ("this listing wants Fusion 360 files") | `SOURCE-DERIVED` — every classification act in the source produces claims (SRC-000010/011 schema fields) |
| EVIDENCE | The concrete artifact supporting a claim (a URL, a listing hash, a quoted excerpt) | `SOURCE-DERIVED` (partial) — SRC-000034 explicitly requires platform-concentration claims to carry "verifiabl[e proof]"; `verification_artifacts` field exists in SCHEMA-003 (`URL_PROOF`, `API_PAYLOAD`, `LISTING_HASH`) |
| VERIFICATION | An independent check that the evidence actually supports the claim (e.g., the URL resolves and the content matches) | `SOURCE-DERIVED` (partial) — SRC-000039 "URL/Endpoint verification" is a named Sentinel directive |
| CONFIDENCE | A numeric/qualitative measure of how much to trust a claim, distinct from binary verified/unverified | `SOURCE-DERIVED` — `drift_score_at_intake` (SCHEMA-003), `budget_feasibility_score` (SCHEMA-002), Strategy Ledger's "Confidence Score" column (TABLE-001) all instantiate this pattern, though inconsistently across different record types |
| DERIVED CONCLUSION | A downstream judgment built from one or more verified/confidence-scored claims (e.g., "this platform is high-value for Archetype B") | `INTERPRETATION` — implied by the existence of strategic-angle guidance (page 9) but never formalized as depending explicitly on verified inputs |

## Preserved source evidence concepts

| Concept | Source | Notes |
|---|---|---|
| URL evidence | SCHEMA-003 `verification_artifacts: URL_PROOF` | direct |
| API evidence | SCHEMA-003 `verification_artifacts: API_PAYLOAD` | direct |
| Listing evidence | SCHEMA-003 `verification_artifacts: LISTING_HASH` | direct — a hash, not the raw listing itself, is the artifact |
| Screenshots | Not explicitly named anywhere in the source | Absent — flagged as a gap, not invented |
| Snapshots | Implied by "raw listing payload" storage concept (page 2 pipeline diagram) but never called "snapshot" or given retention/versioning treatment | `INTERPRETATION` |
| Hashes | `LISTING_HASH` (SCHEMA-003) | direct |
| Retrieval timestamps | `extraction_timestamp` (SCHEMA-002), `timestamp_utc` (SCHEMA-005) | direct, present in 2 of 3 lead schema versions |
| Source references | `source_url`, `source_platform` (SCHEMA-002), `listing_url` (SCHEMA-005) | direct |
| Verification artifacts | `verification_artifacts` array (SCHEMA-003 only — absent from SCHEMA-002 and SCHEMA-005, a genuine cross-version inconsistency, see `schema-versioning.md`) | direct but version-inconsistent |

## Why the CLAIM → EVIDENCE → VERIFICATION → CONFIDENCE → DERIVED CONCLUSION chain matters here specifically

The source's own economic scenarios (`economic-scenarios.md`) are themselves an illustration of what happens
when this chain is skipped: SCENARIO-005's "$1 Million in pure profit every single day" is a DERIVED
CONCLUSION built directly on an unverified CLAIM (the universal-printer hardware assumption, ASSUMPTION-001)
with no EVIDENCE or VERIFICATION step in between. This is not a criticism of the source (it was explicitly a
hypothetical exercise, "assume the technology exists") — but it is exactly the pattern this Evidence Model
exists to prevent from happening SILENTLY inside IECHM-LIOS's actual lead-intelligence pipeline, where a
misclassified `client_archetype` or an unverified platform "rule" could silently propagate into strategic
output without ever being flagged as unverified.

## Conceptual data shape (NOT a database schema — Step 1 does not implement one, Section 42)

```
Claim
 ├── claim_id
 ├── subject (what this claim is about — a lead, a platform, a channel)
 ├── field (which attribute this claim asserts a value for)
 ├── asserted_value
 ├── produced_by (agent ID, model version)
 ├── produced_at
 └── evidence[] ──> Evidence
                      ├── evidence_id
                      ├── type (URL_PROOF | API_PAYLOAD | LISTING_HASH | ...)
                      ├── artifact_reference
                      └── verification ──> Verification
                                             ├── verified (bool)
                                             ├── verified_at
                                             ├── verified_by (Sentinel ID)
                                             └── method
```

This shape is `PROPOSED_EXTENSION` in its exact structure (never drawn this way in the source) but every
individual field it contains traces to a `SOURCE-DERIVED` concept per the table above.

## Explicit non-implementation

Per Step 1 Section 17's final instruction, no database is implemented here. This document defines the
conceptual model that `docs/database/` (a future step) would formalize into real schema.
