# Contract: Lead

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved. **This contract does NOT pick a
canonical schema — see CONFLICT-003 / `open-decisions.md` #2.**

## Purpose
The central data product of IECHM-LIOS. Represents one tracked opportunity, across its full observation
history.

## Source references
SCHEMA-001 (job-listing parse contract), SCHEMA-002 (v0.5 narrative example), SCHEMA-003 (v1 Unified Lead
Entity), SCHEMA-005 (v2 final Unified Lead Entity). See `docs/architecture/schema-versioning.md`.

## Requirement references
REQ-000007, REQ-000009, REQ-000014, REQ-000015.

## Fields — three preserved, non-identical field sets (NOT merged)

### `lead` (stable identity wrapper — `PROPOSED_SCHEMA`, no source equivalent)
| Field | Required? | Notes |
|---|---|---|
| `lead_id` | required | stable across all observations |
| `first_observed_at` | required | never changes once set |
| `latest_lead_version_id` | required | denormalized pointer to the most recent `lead_version` |

### `lead_version` — payload shape depends on WHICH schema version this instance uses; `schema_id` field (required, `PROPOSED_SCHEMA`) declares which

**If `schema_id = 'SCHEMA-002'`** (`SOURCE_SCHEMA`, verbatim):
`lead_metadata` (`source_platform`, `source_url`, `extraction_timestamp`, `client_archetype`: 4-value enum),
`project_scope` (`title`, `domain_focus[]`, `required_cad_software[]`, `target_manufacturing_process`,
`project_maturity_stage`, `deliverables_demanded[]`), `commercial_parameters` (`client_stated_budget_usd`,
`target_production_volume`, `target_unit_target_cost_usd`, `geographic_destination`), `strategic_qualification`
(`budget_feasibility_score`, `iechm_capability_match`, `identified_pain_point`, `recommended_pitch_angle`).

**If `schema_id = 'SCHEMA-003'`** (`SOURCE_SCHEMA`, verbatim):
`lead_id`, `layer_origin` (`client_archetype`: 5-value enum, `macro_channel_type`, `platform_id`,
`sub_domain_id`), `technical_fingerprint` (`cad_tooling_required[]`, `manufacturing_domain`,
`target_production_volume`, `stated_budget_usd`, `verification_artifacts[]`), `runtime_governance`
(`responsible_worker_id`, `worker_model_family`, `auditor_validation_status`, `drift_score_at_intake`).

**If `schema_id = 'SCHEMA-005'`** (`SOURCE_SCHEMA`, verbatim, itself truncated in source):
`lead_id`, `timestamp_utc`, `client_archetype` (5-value SCREAMING_SNAKE_CASE enum, truncated), `source_metadata`
(`macro_channel`, `platform_name`, `sub_domain`, `listing_url`), `technical_specifications` (`domain`,
`cad_software[]`, `materials_requested[]`, `bounding_box_mm`, `file_attachments[]`), `commercial_assessment`
(`client_stated_budget_usd`, `estimated_market_price_usd`, `target_bid_price_usd`, `estimated_cogs_usd`,
`projected_margin_percent`), `security_analysis` (`contains_anti_bot_trap`, `required_verification_keyword`,
`is_prompt_injection`, `sanitized_text_payload`).

**Common wrapper fields added to ALL versions** (`DERIVED_CANONICAL_SCHEMA`, not in any source schema):
`schema_id`, `lead_version_id`, `observed_at`, `source_record_ids[]`, `claim_ids[]` (linking the classification
fields above to their underlying `claim` records rather than storing them as bare values — see Provenance
below), `trust_level`.

## Validation rules
- `schema_id` must reference a valid `schema_registry` row.
- A `lead_version`'s payload must validate against ITS OWN declared schema's shape — a `SCHEMA-002`-shaped
  payload is never required to also satisfy `SCHEMA-005`'s constraints, and vice versa.
- The FIRST `lead_version` for a given `lead_id` is never deleted or edited (Step 2 Section 8, explicit).

## Provenance
Each classification-bearing field within a `lead_version` (e.g., `client_archetype`, `manufacturing_domain`)
is, in the FULL canonical model, actually a pointer to a `claim` record (via `claim_ids[]`) rather than a bare
inline value — this is a `DERIVED_CANONICAL_SCHEMA` refinement beyond what any single source schema states,
necessary so that trust-level/evidence/verification tracking applies uniformly. Where a `lead_version` is
stored with inline values (matching the literal source schema shapes above) for compatibility/simplicity,
implementations MUST still maintain the underlying `claim` records as the source of truth for trust state.

## Versioning & compatibility
Per `docs/architecture/schema-versioning.md`: NO migration from SCHEMA-002/003 to SCHEMA-005 is performed by
this contract. All three remain independently valid `lead_version` shapes until `open-decisions.md` #2 is
resolved by the user, at which point a real migration (per `docs/database/migrations.md`) would be scoped.

## Security classification
`CONFIDENTIAL`. The `security_analysis.sanitized_text_payload` field (SCHEMA-005) may itself contain
`SENSITIVE` untrusted raw content and must be handled per `docs/architecture/security.md`'s "never treat
external content as a trusted instruction" principle even after sanitization.

## Examples
The literal instance examples from SCHEMA-002 (page 10-11) and the structural (non-instance) definitions from
SCHEMA-003/005 are preserved verbatim in `docs/source-extraction/json-schemas.md` — not re-fabricated here;
this contract cites them by schema ID rather than duplicating.
