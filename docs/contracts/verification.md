# Contract: Verification

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
The record of an independent check confirming (or contradicting) a claim's evidence. Implements Step 2
Section 14 and `docs/database/evidence.md`.

## Source references
SRC-000039 ("URL/Endpoint verification (validating that scraped leads, URLs, and platforms exist)").

## Requirement references
REQ-000019, REQ-000020.

## Fields

| Field | Required? | Tag | Notes |
|---|---|---|---|
| `verification_id` | required | `PROPOSED_SCHEMA` | |
| `claim_id` | required | `PROPOSED_SCHEMA` | |
| `method` | required | `PROPOSED_SCHEMA` | e.g. `URL_RESOLUTION_CHECK`, `SCHEMA_VALIDATION`, `NUMERIC_SANITY_CHECK` — the latter two directly from SRC-000039 |
| `verifier_agent_instance_id` | optional | `PROPOSED_SCHEMA` | which Sentinel/agent/human |
| `verification_source` | optional | `PROPOSED_SCHEMA` | |
| `verification_timestamp` | required | `PROPOSED_SCHEMA` | |
| `result` | required | `DERIVED_CANONICAL_SCHEMA` | `VERIFIED` \| `PARTIALLY_VERIFIED` \| `UNVERIFIED` \| `CONTRADICTED` \| `FAILED` \| `EXPIRED` — exact list per Step 2 Section 14 |
| `confidence` | optional | `PROPOSED_SCHEMA` | |
| `notes` | optional | `PROPOSED_SCHEMA` | |
| `artifacts[]` | optional | `PROPOSED_SCHEMA` | |
| `status` | required | `PROPOSED_SCHEMA` | `ACTIVE` \| `SUPERSEDED` |

## Validation rules
Immutable after creation. **Failed verification attempts are never deleted** (Step 2 Section 14, explicit) —
a `FAILED` row persists permanently.

## Provenance
`verifier_agent_instance_id` traces to `agent.md`; `claim_id` traces to `claim.md`.

## Versioning & compatibility
`result` enum is closed (per `docs/database/integrity-rules.md`) — the 6 values are fixed by the governing
instructions and should not be silently extended.

## Security classification
`CONFIDENTIAL`.

## Examples
None fabricated — the source names the verification ACTION (URL/endpoint checks) but never shows an example
verification record.
