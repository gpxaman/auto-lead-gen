# Contract: Platform

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
Per-platform deep-dive profile: identity, interaction mechanics, rules, tools, metrics, sub-domain index.

## Source references
SRC-000035 (page 12, full field list), TABLE-003 (Master Lead Source & Strategy Matrix), `docs/source-extraction/platforms.md`
(46 named platforms).

## Requirement references
REQ-000017.

## Fields

| Field | Required? | Tag | Notes |
|---|---|---|---|
| `platform_id` | required | `PROPOSED_SCHEMA` | |
| `platform_name` | required | `SOURCE_SCHEMA` | e.g. "Upwork" |
| `macro_channel_id` | required | `SOURCE_SCHEMA` | link to `macro_channel` — note: source itself gives 4/8/5/6 differing category-count schemes (see `terminology.md`); `open-decisions.md` does not force a choice here, this field simply points to whichever `macro_channel` taxonomy version is active |
| `url` | optional | `PROPOSED_SCHEMA` | not explicit in source as a structured field, though platform URLs are referenced throughout |
| `interaction_mechanics` | required | `SOURCE_SCHEMA` | Open bidding \| Direct RFQ \| Buyer Request \| Direct Message \| Broker Introduction (SRC-000035) |
| `platform_rules[]` | optional | `SOURCE_SCHEMA` | ban triggers, off-platform-comm rules — content varies per platform, not itemized generically in source |
| `native_tools[]` | optional | `SOURCE_SCHEMA` | Connects, Escrow, Native Chat APIs, Verified Supplier Badges |
| `quality_metrics` | optional | `SOURCE_SCHEMA` | conversion rate, win-rate benchmarks, avg proposal lifespan |
| `subdomain_index[]` | optional | `SOURCE_SCHEMA` | pointer to `subdomain` rows |
| `anti_scraping_friction_level` | optional | `SOURCE_SCHEMA` | Low \| Medium \| High Cloudflare/WAF (page 12) |
| `platform_version_id` | required | `PROPOSED_SCHEMA` | versioning wrapper |

## Validation rules
`platform_name` uniqueness within a given `macro_channel_id`. Rule/tool changes create a NEW `platform_version`
row, never an in-place edit (per `docs/database/versioning.md`).

## Provenance
`platform_version` changes should carry `configuration_version_id`/`agent_instance_id` if AI-assisted
research updated the profile, or a human actor ID if manually curated.

## Versioning & compatibility
Append-only version history per platform.

## Security classification
`INTERNAL` for most fields; `platform_rules[]` (ban triggers) borderline `SENSITIVE` (per
`docs/database/security.md`'s reasoning about detection-logic exposure, applied analogously here since ban
triggers are adversary-relevant knowledge too).

## Examples
TABLE-003's rows (e.g., "Upwork / Cad Crowd | Freelance Platform | NPD Innovator/SME | Requests .STEP, Fusion
360...") are the closest source example and are preserved verbatim in `docs/source-extraction/tables.md`
(TABLE-003) — cited, not re-fabricated.
