# Open Decisions

Per Step 1 Section 36. Every item below requires the user's explicit decision. None are made unilaterally by
this Step 1 process. Ordered roughly by how much they block subsequent work.

## 1. Lead-volume scale profile priority (CONFLICT-001, ADR-0007)
Does the user want an initial narrow-scope launch (`freelance-narrow`, ~15,000 leads/day, no Layer 0 needed)
with room to expand, or is full-firehose scope (`full-firehose`, 1.5-2.5M leads/day, Layer 0 required) the
Day-1 target? This determines Phase-1 platform-connector priority in `implementation-roadmap.md`.

## 2. Canonical lead-entity schema version (CONFLICT-003, ADR-0004)
Adopt SCHEMA-005 (v2, latest draft) as current-going-forward with SCHEMA-002/003 preserved as historical? Or
design a fresh v3 reconciling both? Or something else? Neither v1 nor v2's specific field names/enum values
were ever reviewed by the user line-by-line in the original source conversation.

## 3. IECHM-LIOS system boundary confirmation (system-boundaries.md, ADR-0001)
Confirm (or override) the working decision to scope this repository to System A (lead intelligence) only,
excluding System B (bidding) and System C (manufacturing) architecture/implementation.

## 4. Canonical client-archetype set (CONFLICT-004)
Adopt the union of all 3 source archetype passes (5 total: NPD Innovator, Middleman/Reseller, SME, Crowdfunder,
Institutional)? Note only the first 3 have full source-derived strategic-angle guidance — the last 2 would
need that guidance authored fresh as a `PROPOSED_EXTENSION`.

## 5. Two-axis classification (CONFLICT-005, ADR-0003)
Confirm or reject the recommendation to model `client_archetype` and `manufacturing_domain`/request-type as
two separate fields rather than one taxonomy.

## 6. Production scale target
Related to #1 but distinct: even within a chosen scale profile, what is the actual target lead throughput,
and over what timeframe? None of the source's figures were empirically validated.

## 7. Infrastructure choices (database technology)
No database technology is chosen anywhere in this project so far (`external-systems.md`: primary structured
storage is `UNSPECIFIED`). Relational? Document? Graph (given the multi-hierarchy client/channel/platform/
sub-domain structure)? This determines how `data-domains.md` translates into real schema in a future step.

## 8. Event technology
No message-bus/event-streaming technology is chosen (`events.md`, `api-boundaries.md`). Kafka-style log?
Simple pub/sub? Direct API calls without a formal event bus at all for an initial version?

## 9. AI/model provider commitment
The source names multiple providers illustratively (OpenAI, Anthropic) without committing to one
(`external-systems.md`). Given this session's own tooling context (Claude/Anthropic), does the user want a
single-provider commitment, or should the model-routing/fallback pattern from the source (cheap-model/heavy-
model split, cross-provider hot-swap fallback) be preserved as a real multi-provider design goal?

## 10. Deployment architecture
Not addressed by the source or by Step 1 (explicitly out of scope per Section 42). Cloud provider, containerization,
serverless vs. long-running processes — all undecided.

## 11. Data retention policy
Raw Payload Storage (`subsystems.md` #4) has no defined retention period. At `full-firehose` scale (millions
of leads/day), unlimited retention is likely infeasible; the source never addresses this at all.

## 12. Connector priority (which platforms to build first)
Even within a chosen scale profile, the source's own recommended sequencing ("start with Upwork and
Freelancer.com," SRC-000016) is a reasonable default, but the user should confirm whether this ordering still
matches current priorities before `implementation-roadmap.md`'s Phase ordering is treated as final.

## 13. External integration boundaries — credential/authorization model
Per `security.md`'s `PROPOSED_EXTENSION` items: who authorizes new platform-connector credentials, and what
is the process for adding a new external integration? Not addressed by source, not decided here.

## 14. Metric Evolution governance
`ADR-0005` establishes that proposed metrics require review before becoming active — but WHO reviews them
(a human? an automated policy?) is undecided.

## 15. Drift-formula completion (`hallucination-detection.md`)
FORMULA-002 is `SOURCE_INCOMPLETE`. Does the user want to (a) provide the missing terms if they exist
somewhere outside this document, (b) commission a fresh formula design as an explicit `PROPOSED_EXTENSION`,
or (c) operate on THRESH-005 (consecutive-failure count) alone until this is resolved?

## Explicit non-decisions
This document does not answer any of the above. Each is preserved as open pending the user's explicit input,
per Step 1 Section 36's instruction: "Do not make these decisions yourself."
