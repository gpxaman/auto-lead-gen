# Threshold Preservation Audit

Per Step 3 Section 3. Determines whether all 15 source thresholds (`docs/source-extraction/thresholds.md`)
still exist in the source-derived model, given that Step 2's `docs/contracts/configuration.md` explicitly
listed only 6 as configuration seed values.

## Finding: **Option A confirmed** — all 15 thresholds still exist; exactly 6 are IECHM-LIOS (System A)
## operational configuration values, and the other 9 are preserved elsewhere (as formulas, scenario data,
## or narrative record) because they govern System B/C behavior or describe observed statistics rather
## than System A configuration knobs. **Nothing was lost.**

## Full mapping — all 15 thresholds

| threshold_id | source_id | source_page(s) | exact_value | meaning | category | database representation | configuration representation | status |
|---|---|---|---|---|---|---|---|---|
| THRESH-001 | SRC-000036 | 11,12,14,17,26,27 | >5 leads/day | Sub-domain worker spawn trigger ("5-Lead Rule") | System A — Dynamic Worker Scaling | `subdomain` entity (`docs/contracts/subdomain.md`), `worker_lifecycle_event` | ✅ `configuration` seed value: `worker.spawn_threshold = 5` | PRESERVED, CONFIGURED |
| THRESH-002 | SRC-000036 | 12,14,26 | <2 leads/day, 7-day rolling avg | Sub-domain worker retirement trigger | System A — Dynamic Worker Scaling | same as above | ✅ `configuration` seed value: `worker.retire_threshold = {value:2, window_days:7}` | PRESERVED, CONFIGURED |
| THRESH-003 | SRC-000006 | 2,26,27 | 80% Exploit / 20% Explore | Strategist strategy-selection policy | System B (Strategy, referenced only) | `strategy_ledger` (`docs/contracts/strategy.md`) | ✅ `configuration` seed value: `strategist.explore_exploit_split = {exploit:80, explore:20}` (recorded for interface-completeness even though System B owns its execution) | PRESERVED, CONFIGURED |
| THRESH-004 | SRC-000078 | 26,28 | D_t ≥ 0.85 | Sentinel drift-score hot-swap trigger | System A — Sentinel Plane | `agent_state`, `sentinel_check` | ✅ `configuration` seed value: `sentinel.drift_threshold = 0.85` | PRESERVED, CONFIGURED |
| THRESH-005 | SRC-000037/078 | 14,15,26,28 | ≥3 consecutive schema/validation errors | Sentinel discrete failure-count hot-swap trigger | System A — Sentinel Plane | same as above | ✅ `configuration` seed value: `sentinel.consecutive_failure_threshold = 3` | PRESERVED, CONFIGURED |
| THRESH-006 | SRC-000079 | 14,28 | ≥99.5% consistency over 72h | Metric Evolution saturation-idle trigger | System A — Metric Evolution | `metric_definition` status=`SATURATED` (`docs/contracts/metric.md`) | ✅ `configuration` seed value: `saturation.threshold = {consistency:99.5, window_hours:72}` | PRESERVED, CONFIGURED |
| THRESH-007 | SRC-000059/074 | 22,25,27,29 | Bid = exactly 90% of market price | Pricing rule | System B — Pricing Engine (referenced, out of IECHM-LIOS scope per `system-boundaries.md`) | `formula` registry (FORMULA-001), `scenario`/`docs/architecture/economic-model.md` | Not a System A `configuration` row — System A does not execute pricing. Preserved as a `formula` record instead. | PRESERVED, NOT CONFIGURED (out-of-scope for A) |
| THRESH-008 | (economic-model.md, page 27) | 27 | >20% discount forbidden | Pricing rule ceiling | System B — Pricing Engine (referenced) | `formula` registry (FORMULA-001 context), `economic-model.md` | Not a System A config value; same reasoning as THRESH-007 | PRESERVED, NOT CONFIGURED (out-of-scope for A) |
| THRESH-009 | (source page 25) | 25 | ±0.05mm tolerance guarantee | System B proposal guarantee clause | System B — Bidding proposal terms (referenced) | `docs/source-extraction/thresholds.md` (Step 0 archive), cited in `economic-model.md` | Not a System A config value — a System B contractual term, not an IECHM-LIOS operational parameter | PRESERVED, NOT CONFIGURED (out-of-scope for A) |
| THRESH-010 | (source page 25) | 25 | Sub-60-second response latency | System B bid-submission latency target | System B — Bidding execution (referenced) | same | Not a System A config value | PRESERVED, NOT CONFIGURED (out-of-scope for A) |
| THRESH-011 | (source page 20) | 20 | 4-hour quote-response window | Cited external B2B benchmark (ASSUMPTION-008) | General/System B (referenced) | `assumption` entity (ASSUMPTION-008) | Not a System A config value — an external cited benchmark, not an enforced rule | PRESERVED, NOT CONFIGURED |
| THRESH-012 | SRC-000053 | 20,27 | ~95% of raw volume dropped by Layer 0 | Observed/expected outcome statistic of Deterministic Triage, not an input threshold itself | System A — Deterministic Triage (descriptive statistic) | `scenario` (SCENARIO-003, `full-firehose` profile, `docs/architecture/scaling-scenarios.md`) | Not itself a configurable knob — it is the RESULT of applying Layer 0's actual filter rules (blacklist/budget-sanity), which ARE configured (see THRESH-015 below) | PRESERVED, DESCRIPTIVE (not a direct config value) |
| THRESH-013 | SRC-000053/074 | 17,20,27 | ~1.5%–2% Layer-1 qualification rate | Observed/expected outcome statistic (also the subject of CONFLICT-006's dual-figure ambiguity) | System A — Client/Technical Classification (descriptive statistic) | `scenario` (multiple), `docs/architecture/conflicts/CONFLICT-006.md` | Not a configured knob — an observed/estimated classification yield, preserved distinctly per CONFLICT-006 (not merged into one number) | PRESERVED, DESCRIPTIVE (not a direct config value) |
| THRESH-014 | SRC-000069 | 25,28 | Day-25 post-delivery re-order trigger | Account-management re-order outreach timing | System B — Account Retention (referenced, out of IECHM-LIOS scope) | `event` type `REORDER_WINDOW_REACHED` (`PROPOSED_EVENT`, `docs/architecture/events.md`) | Not a System A config value — a System B lifecycle timer | PRESERVED, NOT CONFIGURED (out-of-scope for A) |
| THRESH-015 | SRC-000012/053 | 3,20,27 | "Budget Sanity Filter" — reject mathematically impossible RFQs (e.g., 100,000 units at $0.001/unit) | Deterministic Triage rejection rule | System A — Deterministic Triage (Layer 0) | `raw_record.security_status`/triage rejection log (`docs/database/entity-catalog.md` #5) | **Gap found and closed in Step 3** (see note below): promoted to a 7th `configuration` seed value: `triage.budget_sanity_filter = {enabled: true, rule_description: "reject listings whose stated unit price makes the stated volume mathematically uneconomical"}` — a qualitative rule rather than one number, which is why it was omitted from Step 2's contract's list of 6 NUMERIC seed values, but it IS a genuine System A configuration item and belongs in the registry | PRESERVED; **NEWLY CONFIGURED IN STEP 3** |

## Transparency note on THRESH-015

Step 2's `docs/contracts/configuration.md` listed exactly 6 "Seed values," all of them single numeric
thresholds. THRESH-015 (the Budget Sanity Filter) is a genuine System A Deterministic Triage rule — just as
operationally real as THRESH-001/002/004/005/006 — but it is a QUALITATIVE rule (a mathematical-plausibility
check) rather than one scalar number, which is plausibly why it wasn't grouped with the other 5 numeric seed
values in Step 2. This is not a data-loss finding — THRESH-015's text was fully preserved verbatim in Step 0
(`docs/source-extraction/thresholds.md`) and referenced in Step 1/2 architecture docs throughout — but Step 3
closes a real completeness gap by registering it as the ingestion system's 7th configuration value, since
Step 3 is precisely the layer (Deterministic Triage / raw ingestion) where this rule is operationally
enforced. See `src/ingestion/config_seed.py` for the implementation.

## Conclusion

**Option A is confirmed.** All 15 thresholds are traceable and preserved. 6 (soon 7, per the transparency note
above) are System A `configuration` values because they govern IECHM-LIOS's own operational behavior; the
remaining 8 are preserved as `formula`/`scenario`/`assumption`/`event` records because they describe System
B/C behavior or external benchmarks that IECHM-LIOS references but does not itself execute or enforce, per
`docs/architecture/system-boundaries.md` (ADR-0001). No repair of the Step 2 data model is required.

## Status
**THRESHOLD_PRESERVATION_STATUS: OPTION_A_CONFIRMED — NO REPAIR REQUIRED.**
