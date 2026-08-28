# Database Security Classification — IECHM-LIOS

Per Step 2 Section 44. Conceptual classifications only — does not assume which business fields belong to
which category unless established by source/architecture; classification policy is configurable.

## The 5 classification levels

| Level | Meaning |
|---|---|
| `PUBLIC` | Safe to expose without restriction (e.g., the enum definition of `manufacturing_domain` values) |
| `INTERNAL` | Not secret, but not meant for external exposure (e.g., internal agent IDs, task queue depth) |
| `CONFIDENTIAL` | Business-sensitive (e.g., a specific lead's commercial estimate, strategy-ledger win rates) |
| `SENSITIVE` | Data requiring extra handling care (e.g., raw scraped content that might incidentally contain a third party's personal information, per the untrusted-content principle in `docs/architecture/security.md`) |
| `SECRET` | Credentials, API keys, tokens — **never stored in normal data records at all**, per Step 2 Section 44's explicit instruction; belongs exclusively in a dedicated secrets-management mechanism outside this data model's scope |

## Provisional classification by entity family (marked configurable, not final)

| Entity family | Provisional classification | Rationale |
|---|---|---|
| `source_document`, `source_item`, `schema_registry`, `formula`, `manufacturing_domain_definition` | `PUBLIC` (or `INTERNAL` if the user prefers not to expose architecture detail externally) | Reference/definitional data, not per-client sensitive |
| `raw_record` | `SENSITIVE` | Untrusted external content (`docs/architecture/security.md`'s "treat all external content as untrusted" principle) that may incidentally contain PII from a scraped listing's author |
| `claim`, `evidence`, `verification`, `lead`, `lead_version`, `client`, `commercial_estimate` | `CONFIDENTIAL` | Business intelligence — this is IECHM's competitive data |
| `agent_state`, `worker_lifecycle_event`, `task_attempt`, `sentinel_check` | `INTERNAL` | Operational detail, not business-sensitive but not for external eyes |
| `audit_event` | `CONFIDENTIAL` (may include `INTERNAL`-classified detail about who changed what) | Security/compliance sensitivity |
| `configuration`, `configuration_change` | `CONFIDENTIAL` — some configuration values (e.g., blacklist term lists, if adversaries could use them to evade Layer 0) are borderline `SENSITIVE` | Depends on the specific field |
| `security_event`, `quarantine_record`, `threat_indicator` | `SENSITIVE` | Exposing detection logic could help an adversary evade it |
| `strategy_ledger`, `strategy_result` | `CONFIDENTIAL` | Competitive/business-strategy sensitivity — this is exactly the kind of data the source's own "compounding flywheel" competitive-moat argument (page 23) treats as valuable |
| Any field holding an API key, credential, or token (e.g., `connector_version`'s associated auth config, if any) | `SECRET` | **Must never be stored inline in these entities at all** — referenced by pointer to a separate secrets store only |

## Explicit non-decision

This document does NOT finalize which specific FIELDS within each entity carry which classification (e.g.,
whether `client.buyer_persona_free_text` is `CONFIDENTIAL` or `SENSITIVE` specifically) — that level of
field-by-field policy is left `CONFIGURABLE`, consistent with Step 2 Section 44's instruction not to assume
categorization without establishment. The table above is a REASONABLE STARTING DEFAULT, explicitly labeled
provisional, not an approved policy.

## Relationship to `docs/architecture/security.md` (Step 1)

This document is the DATA-AT-REST classification layer; Step 1's `security.md` covers the broader
architectural security concerns (prompt injection, credential leakage, runaway cost, memory poisoning). They
are complementary — this document does not repeat Step 1's threat-model content.

## Never store secrets — enforcement note

Per the integrity rules (`integrity-rules.md`), `audit_event.before`/`after` snapshots must be
REDACTED of any `SECRET`-classified field values before persistence — an audit log that accidentally captures
a credential in a "before/after configuration change" snapshot would itself become a security liability. This
redaction requirement is recorded here and cross-referenced from `integrity-rules.md`, not treated as
optional.
