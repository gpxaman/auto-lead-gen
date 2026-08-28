# Query Patterns — IECHM-LIOS

Per Step 2 Section 48. Illustrative conceptual queries (pseudocode, not vendor-specific SQL/query-language,
since no database technology is chosen — `open-decisions.md` #7) demonstrating how the logical model answers
the questions posed in Step 2's Absolute Data-Preservation Principle.

## "What did we know?" (state at a point in time)

```
SELECT lead_version.*
FROM lead_version
WHERE lead_version.lead_id = :lead_id
  AND lead_version.observed_at <= :as_of_timestamp
ORDER BY lead_version.observed_at DESC
LIMIT 1
```
Because `lead_version` is append-only (never overwritten, per `integrity-rules.md`), this query is always
answerable for ANY historical timestamp, not just "now" — directly satisfying the requirement.

## "What did the source originally say?"

```
SELECT source_item.exact_text, source_item.page_id, source_page.page_number
FROM source_item
JOIN source_page ON source_item.page_id = source_page.page_id
WHERE source_item.source_id = :src_id
```
Resolves directly against the Step 0 filesystem-mirrored `source_item` table — this NEVER changes, since the
source archive is immutable (core project rule).

## "What did the system infer?"

```
SELECT claim.*
FROM claim
WHERE claim.subject_id = :lead_id
  AND claim.trust_level IN ('MODEL_INFERENCE', 'UNVERIFIED_CLAIM')
ORDER BY claim.created_at DESC
```
Distinguishes inference from verified fact by construction — trust_level is never silently promoted (per the
state-transition rules in `integrity-rules.md`), so this query can never accidentally return something that
was actually verified.

## "What evidence supported that inference?"

```
SELECT evidence.*
FROM evidence
JOIN claim_evidence ON evidence.evidence_id = claim_evidence.evidence_id
WHERE claim_evidence.claim_id = :claim_id
```
May legitimately return ZERO rows (a claim with no evidence yet) — this is expected and valid per Section 12.

## "What was verified?"

```
SELECT verification.*
FROM verification
WHERE verification.claim_id = :claim_id
ORDER BY verification.verification_timestamp DESC
```
Returns the FULL history including `FAILED` attempts (never deleted, per `integrity-rules.md`) — a query that
filters to `result = 'VERIFIED'` only would be a DIFFERENT, narrower query; this one intentionally shows
everything.

## "What configuration produced this result?"

```
SELECT configuration_version.*
FROM configuration_version
JOIN claim ON claim.configuration_version_id = configuration_version.configuration_version_id
WHERE claim.claim_id = :claim_id
```
Works because every derived record carries its `configuration_version_id` per `provenance.md`'s universal
field pattern.

## "What model/prompt/version produced this result?"

```
SELECT model_version.*, prompt_version.*
FROM claim
JOIN model_version ON claim.model_version_id = model_version.model_version_id
JOIN prompt_version ON claim.prompt_version_id = prompt_version.prompt_version_id
WHERE claim.claim_id = :claim_id
```
Per Section 26's explicit rule, this NEVER assumes the current/latest model — the foreign key was fixed at
claim-creation time and is never repointed.

## "What decision was made?"

```
SELECT audit_event.*
FROM audit_event
WHERE audit_event.target_id = :entity_id
  AND audit_event.action IN ('DECISION', 'CONFIGURATION_CHANGE', 'CONFLICT_RESOLUTION')
ORDER BY audit_event.timestamp DESC
```

## "What was changed later?" (full change history for any entity)

```
SELECT audit_event.*
FROM audit_event
WHERE audit_event.target_id = :entity_id
ORDER BY audit_event.timestamp ASC
```
Because `audit_event` is immutable and append-only, this reconstructs the FULL change timeline for anything
in the system, satisfying Step 2's closing principle in full: "every important output must remain traceable
backward through that chain."

## Compound query: full provenance trace (the master query this entire data model exists to support)

```
SELECT
  output.*, task.*, agent_instance.*, model_version.*, prompt_version.*,
  raw_record.*, source_item.*, evidence.*
FROM claim AS output
JOIN task ON output.task_id = task.task_id
JOIN agent_instance ON task.agent_instance_id = agent_instance.agent_instance_id
JOIN model_version ON output.model_version_id = model_version.model_version_id
JOIN prompt_version ON output.prompt_version_id = prompt_version.prompt_version_id
JOIN raw_record ON output.source_record_ids @> ARRAY[raw_record.record_id]  -- conceptual; exact syntax vendor-dependent
LEFT JOIN source_item ON raw_record.provenance_source_id = source_item.source_id  -- only populated where raw data traces to the Step 0 archive itself (rare — most raw_records are live external scrapes, not the preserved PDF)
JOIN evidence ON output.evidence_ids @> ARRAY[evidence.evidence_id]
WHERE output.claim_id = :claim_id
```

## Explicit scope note

These are illustrative, technology-neutral query SHAPES demonstrating the model answers the required
questions — not tuned, production-ready, vendor-specific queries. Actual query language, join syntax, and
performance optimization are deferred to `open-decisions.md` #7 (database technology).
