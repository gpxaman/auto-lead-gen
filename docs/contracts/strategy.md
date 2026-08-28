# Contract: Strategy

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
Explore/Exploit strategy tracking (primarily a System B concept, referenced here for interface-readiness and
the `PROPOSED_EXTENSION` System-A reuse case per `docs/architecture/strategy-learning.md`).

## Source references
SRC-000006 (Explore/Exploit 80/20), SRC-000007 (Strategy Ledger, TABLE-001).

## Requirement references
REQ-000004, REQ-000005 (System B).

## Fields

### `strategy` / `strategy_version`
`strategy_id`, `approach` (`SOURCE_SCHEMA` — e.g. "Highly technical, detailed breakdown," from TABLE-001),
`version`.

### `strategy_ledger` (seed: ST-01 through ST-04, exact source values)
| `strategy_id` | `approach` | `win_rate` | `confidence_score` | `status` |
|---|---|---|---|---|
| ST-01 | Highly technical, detailed breakdown | 65% | High | Active |
| ST-02 | Short, punchy, focus on past results | 30% | High | Deprecated |
| ST-03 | Video introduction offer | 15% | Low | Exploring |
| ST-04 | Challenge the client's premise | -- | None | Planned |
All 4 rows `SOURCE_SCHEMA`, verbatim from TABLE-001.

### `strategy_experiment` / `strategy_result`
`experiment_id`, `strategy_id`, `explore_or_exploit` (`EXPLORE`/`EXPLOIT`), `outcome`, `confidence_delta`.

## Validation rules
Strategy history is never overwritten (Step 2 Section 31, explicit) — each `strategy_result` is a new row;
`win_rate`/`confidence_score` on `strategy_ledger` are DERIVED/recomputed views over `strategy_result` history,
not directly mutable fields.

## Provenance
Full field set per `docs/database/provenance.md`.

## Versioning & compatibility
Append-only.

## Security classification
`CONFIDENTIAL` (competitive strategy data).

## Examples
TABLE-001 above, exact.
