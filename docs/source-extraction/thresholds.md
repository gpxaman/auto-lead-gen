# Extracted Thresholds

| ID | Threshold | Triggers | Source page(s) |
|---|---|---|---|
| THRESH-001 | Sub-domain lead volume > 5 leads/day | Spawns a dedicated micro-worker agent for that sub-domain ("The 5-Lead Rule") | 11, 12, 14, 17, 26, 27 |
| THRESH-002 | Sub-domain lead velocity < 2 leads/day, over a 7-day trailing/rolling average | Sub-agent is deprecated / drained / serialized and merged back into the parent worker | 12, 14, 26 |
| THRESH-003 | Explore/Exploit split: 80% Exploit / 20% Explore | The Strategist's default strategy-selection ratio when formulating a bid blueprint | 2, 26, 27 |
| THRESH-004 | Drift score $D_t \ge 0.85$ | Hot-Swap Failover triggered — CEASE_OPERATIONS issued, context migrated to replacement agent | 26, 28 |
| THRESH-005 | ≥3 consecutive schema/validation errors (also referenced as $\tau_{drift} \ge 3$ consecutive [failures]) | Hot-Swap Failover triggered (same action as THRESH-004) | 14, 15, 26, 28 |
| THRESH-006 | Data completeness/predictability ≥ 99.5% consistency over a 72-hour window | Telemetry Optimizer enters Formal Idle State, publishes `CHANNEL_DATA_SATURATED_IDLE_ACTIVE`, halts exploratory schema generation | 14, 28 |
| THRESH-007 | Pricing rule: bid must equal exactly 90% of estimated market price (10% discount) | Applied to every bid; "never deeper than X%" language present but the deeper-discount ceiling value itself is truncated in source render | 22, 25, 27, 29 |
| THRESH-008 | Discounts deeper than 20% off market (">20% off") | Explicitly forbidden — "must never bid at deep discounts (>20% off), which signal low quality" | 27 |
| THRESH-009 | Tolerance/quality guarantee: ±0.05 mm | Stated example clause: "If tolerances deviate by more than ±0.05 mm, we remanufacture at zero cost" | 25 |
| THRESH-010 | Response latency: sub-60-second bid submission | Stated to yield "~35% higher response rate than bidding after 10 minutes" | 25 |
| THRESH-011 | Response window: within 4 hours of a quote request | Cited B2B benchmark: buyers "form strong preferences within 4 hours"; responding in that window "close at a 35% higher rate" | 20 |
| THRESH-012 | Layer 0 deterministic pre-filter reduction: ~95% of raw volume dropped | 2,000,000 raw leads/day → ~100,000 pass Layer 0 | 20, 27 |
| THRESH-013 | Layer 1 LLM qualification rate: ~2% (also stated elsewhere as 1.5%) of the post-Layer-0 pool | 100,000 → ~2,000 qualified bids/day (page 20/27); alternately "Top 1.5% pass IECHM capability thresholds" applied directly to the 15,000/day-basis funnel on page 17 — see CONFLICT-001 for the differing base volumes | 17, 20, 27 |
| THRESH-014 | Sub-domain re-order consumption trigger: Day 25 post-delivery | Account agent initiates re-order outreach | 25, 28 |
| THRESH-015 | "Budget Sanity Filter" — mathematically impossible RFQs | Example given: "100,000 custom injection-molded ABS plastic cases but sets the target price at $0.001 per unit" → automatically dropped | 20 (also restated abstractly as "$100 complex machined al[uminum...]" on page 27, truncated) |
