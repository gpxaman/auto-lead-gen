# ADR-0003 — Model Client Archetype and Manufacturing/Request Domain as Two Separate Axes

**Status:** PROPOSED (not ACCEPTED — depends on CONFLICT-005, which remains `NEEDS_USER_DECISION`)
**Source IDs:** SRC-000029/025/034 (archetype sets), SRC-000052 (composition breakdown), SRC-000010/011
(ManufacturingDomain)
**Requirements:** REQ-000013

## Context
Per CONFLICT-005, the source's page-19 "Composition of the Firehose" breakdown introduces buyer-intent
categories ("Component & Part Sourcing," "Tooling & Injection Mold Fabrication") that don't map onto any
named client archetype, suggesting two distinct classification dimensions (WHO is asking vs. WHAT is being
asked for) were being conflated.

## Decision (PROPOSED, not yet accepted)
Model `client_archetype` (Client Intelligence domain) and `manufacturing_domain`/request-type (Technical
Classification domain, reusing the existing `ManufacturingDomain` enum from SCHEMA-001) as two separate,
cross-referenced fields on a lead record, rather than one enum trying to express both.

## Alternatives considered
1. Force the composition percentages into the existing archetype enum via a lossy best-guess mapping —
   rejected as inventing a correspondence the source doesn't state.
2. Treat the composition breakdown as a data-quality artifact to be ignored — rejected, discards real user-
   requested scope (SRC-000050's explicit broadening request).

## Consequences if accepted
`client-intelligence-model.md` and `data-domains.md` would formalize this as two linked fields;
`json-schemas.md`/`schema-versioning.md` migration work would need to add a `request_type`/`manufacturing_domain`
field to whichever lead schema becomes canonical (CONFLICT-003), if not already adequately covered by the
existing `ManufacturingDomain` reuse.

## Decision status
Kept as `PROPOSED`, not `ACCEPTED`, because it directly depends on the still-open CONFLICT-005. This ADR
exists to make the RECOMMENDATION concrete and reviewable, not to unilaterally resolve the conflict.

## Reversibility
Reversible pre-implementation; would require a schema migration if reversed post-implementation.
