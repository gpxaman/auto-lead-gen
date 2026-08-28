# Schema Versioning

Per Step 1 Section 7. Catalogues every source schema document, preserves all versions distinctly (does not
merge them), and defines how the eventual system supports multiple schema versions without silent overwrite.

## Source schema inventory

| Schema ID | Source page | Source ID | Version | Purpose |
|---|---|---|---|---|
| SCHEMA-001 | 3 | SRC-000010, SRC-000011 | v0 (job-listing parse contract) | Pydantic model (`EngineeringJobSpec`, `ManufacturingDomain`, `ClientTrapDetection`) for normalizing ONE scraped job listing during recon |
| SCHEMA-002 | 10-11 | SRC-000032 | v0.5 (lead JSON, narrative example) | Example instance of a "Normalized Data Extraction Schema" — `lead_metadata`/`project_scope`/`commercial_parameters`/`strategic_qualification`; 4-value `client_archetype` enum, no Institutional value |
| SCHEMA-003 | 14 | SRC-000040 | v1 (Unified Lead Entity Data Schema) | `lead_id`/`layer_origin`/`technical_fingerprint`/`runtime_governance`; 5-value `client_archetype` enum (adds Institutional), nested under `layer_origin` |
| SCHEMA-004 | 15 | SRC-000041 | v1 (Node Health & Sentinel Telemetry Schema) | `FAILOVER_HOTSWAP_TRIGGERED` event contract, flat structure |
| SCHEMA-005 | 29 | SRC-000080 | v2 (Unified Lead Entity Schema, final) | Formal JSON Schema (draft-07); top-level `client_archetype` (5 SCREAMING_SNAKE_CASE values, different names than v1, list truncated); `source_metadata`/`technical_specifications`/`commercial_assessment`/`security_analysis` |
| SCHEMA-006 | 29 | SRC-000082 | v2 (Node Failure & Hot-Swap Telemetry Contract, final) | `FAILOVER_HOTSWAP_DISPATCHED` event contract, restructured into `anomaly_report`/`failover_execution` |

## Field-meaning differences, SCHEMA-003 (v1) vs. SCHEMA-005 (v2), Lead Entity

| Concept | v1 (SCHEMA-003) | v2 (SCHEMA-005) |
|---|---|---|
| Client archetype location | Nested: `layer_origin.client_archetype` | Top-level: `client_archetype` |
| Client archetype values | `NPD_Innovator \| Middleman_Reseller \| Enterprise_SME \| Crowdfunder \| Institutional` | `NPD_INNOVATOR \| MIDDLEMAN_OEM_RESIGN \| SME_ENGINEERING_OVERFLOW \| CROWDFUNDER_FUNDED \| GOVERNMEN[truncated]` |
| Macro channel field | `layer_origin.macro_channel_type` | `source_metadata.macro_channel` |
| Technical fields | `technical_fingerprint.*` (cad_tooling_required, manufacturing_domain, target_production_volume, stated_budget_usd, verification_artifacts) | `technical_specifications.*` (domain, cad_software, materials_requested, bounding_box_mm, file_attachments) — DIFFERENT field names, DIFFERENT structure (adds `bounding_box_mm` and `file_attachments`, drops `verification_artifacts` as a named field — evidence concept moved elsewhere, see `evidence-model.md`) |
| Governance/security fields | `runtime_governance.*` (worker id, model family, validation status, drift score) | `security_analysis.*` (anti-bot trap, injection flags, sanitized payload) — NOTE: these cover DIFFERENT concerns (v1's is about WORKER integrity, v2's is about LEAD CONTENT safety) — not a renaming of the same field, but a genuinely different concept occupying a similarly-named schema slot |
| Format | Example instance (illustrative values) | Formal JSON Schema (draft-07, type constraints) |

**This is a materially significant drift, not a cosmetic rename** — v1's `runtime_governance` and v2's
`security_analysis` are NOT the same concept despite superficially similar schema "slot" position; v1 tracks
WHICH WORKER produced this record and how much to trust it, while v2 tracks whether the LEAD'S SOURCE TEXT
contained a security threat. A future canonical schema likely needs BOTH concepts as separate fields, not one
replacing the other.

## Canonical versioning approach (architecture, not implementation)

```
OLD DATA (schema v_n)
    ↓
VERSIONED TRANSFORMATION (explicit migration function, v_n → v_n+1)
    ↓
NEW DATA (schema v_n+1)
```

Never:
```
OLD DATA → overwrite → NEW DATA
```

Concretely, the canonical architecture requires:
- Every lead/telemetry record carries an explicit `schema_version` field (not present in ANY source schema
  version — this is a `PROPOSED_EXTENSION` necessary for the versioning discipline this project requires).
- Historical schema versions (v0 through v2 as catalogued above) remain queryable/recoverable, not merged
  into a lossy "best guess" unified shape.
- A future migration (e.g., v1 → v2, or either → a new v3) is implemented as an explicit, testable
  transformation function, never a direct field-rename-in-place on production data.

## Status

No schema version is declared canonical in Step 1. Per CONFLICT-003, this is `NEEDS_USER_DECISION`. The
architecture is designed to be version-tolerant regardless of which version (or new v3) is eventually chosen
as the going-forward default.
