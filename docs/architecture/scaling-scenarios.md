# Scaling Scenarios

Per Step 1 Section 5. Directly addresses CONFLICT-001/002. Preserves BOTH source lead-volume figures as named,
independent scale profiles rather than picking one as "correct." Numbers here are `SOURCE-DERIVED` /
`SOURCE_ESTIMATE`, never converted into production guarantees or SLAs (per ASSUMPTION-006 in Step 0).

## Why multiple profiles, not one number

The source itself never resolves whether 15,000/day (narrow, freelance-board scope) or 1.5M-2.5M/day (broad,
full-manufacturing-firehose scope) is the intended operating volume — see CONFLICT-001. Rather than guessing,
the canonical architecture is designed to be scale-profile-aware: which profile is active is a CONFIGURATION
decision (see `docs/architecture/configuration.md`), not a hardcoded architectural assumption.

## SCENARIO PROFILE: `freelance-narrow` (Source: SRC-000043/044/045, pages 16-18)

| Stage | Value | Source |
|---|---|---|
| INPUT VOLUME | 15,000 raw leads/day (freelance boards + limited B2B/community) | SRC-000044 |
| FILTERING | None described (no Layer 0 concept existed at this point in the source) | — |
| QUALIFICATION | ~1.5% of raw pool → 6,750 MQL/month | SRC-000047 |
| DOWNSTREAM WORK | 337 bids/month, 50 responses, 10 closed deals/month | TABLE-007/008 |
| AGENT REQUIREMENT | 140-195 total agents (Layers 1-4 + sentinels), ~75 platform workers | TABLE-004 |
| INFRASTRUCTURE IMPLICATION | No Layer 0 needed; proxies/vector-DB/compute sized for ~48.7M input tokens/day | TABLE-005, FORMULA-003 |
| ECONOMIC ASSUMPTIONS | ~$3,500/month total operating cost (SOURCE_ESTIMATE) | SRC-000045 |
| STATUS | `SOURCE-DERIVED`, internally self-consistent (agent count and cost were computed FOR this volume) |

## SCENARIO PROFILE: `full-firehose` (Source: SRC-000051/052/053/073/074, pages 19-27)

| Stage | Value | Source |
|---|---|---|
| INPUT VOLUME | 1.5M-2.5M raw signals/day (all B2B trade/importers/middlemen/freelance/community across ~75+ platforms, all manufacturing except chemicals/fabrics/food) | SRC-000051 |
| FILTERING | Layer 0 deterministic pre-filter (regex/keyword blacklist, budget-sanity check, location routing) removes ~95% | SRC-000053, THRESH-012 |
| QUALIFICATION | ~2%-5% of the post-Layer-0 pool (100,000) → 2,000-5,000 qualified bids/day | SRC-000074, THRESH-013 |
| DOWNSTREAM WORK | Growth-phase dependent — see TABLE-011 (75 to 1,375 closed deals/day across Phase 1-4) | SRC-000068 |
| AGENT REQUIREMENT | **NOT RE-DERIVED IN THE SOURCE** — see CONFLICT-002. The 140-195 figure from `freelance-narrow` predates Layer 0 and this volume and should NOT be reused here without recomputation. | CONFLICT-002 |
| INFRASTRUCTURE IMPLICATION | Requires Layer 0 (non-AI, high-throughput filtering) as a hard architectural prerequisite; residential-proxy/scraper-API needs scale with 75+ concurrent platform connectors | SRC-000053 |
| ECONOMIC ASSUMPTIONS | **NOT RE-DERIVED IN THE SOURCE** — the $3,500/month figure is stale for this profile (CONFLICT-002); downstream revenue scenarios (SCENARIO-004 through 008) assume this profile's lead volume without a matching recomputed cost basis | CONFLICT-002 |
| STATUS | `SOURCE-DERIVED` for volume/filtering/qualification; `UNRESOLVED` for agent count and cost (explicitly flagged, not filled in) |

## Cross-scenario notes

- Both profiles share the same downstream architecture (Layers 1-4, sentinel plane, pricing/strategy
  concepts) — the difference is purely in intake volume and the presence/absence of Layer 0. This means
  `full-firehose` is architecturally `freelance-narrow` PLUS a Layer 0 stage, not a fundamentally different
  system.
- A real deployment could plausibly start at `freelance-narrow` scale (lower infrastructure/agent
  investment, faster to stand up, matches the earliest platform-sequencing strategy from SRC-000016 — "start
  with Upwork and Freelancer.com") and grow into `full-firehose` scale as more channel connectors and Layer 0
  are built out — this progression is technically plausible and consistent with the source's own recommended
  platform-rollout SEQUENCING strategy, but the source never explicitly states this progression as the
  intended reading of the two volume figures. This is flagged as `INTERPRETATION`, not `SOURCE-DERIVED`.
- Neither profile's agent count or cost figures should be treated as calibrated to real-world platform
  posting rates — both are the AI's own estimates with no cited empirical basis (ASSUMPTION-006).

## Recommendation for `docs/architecture/implementation-roadmap.md`

Given the above, the roadmap treats `freelance-narrow` as the more implementation-tractable starting profile
(fewer connectors, no Layer 0 dependency, matches the source's own recommended platform sequencing), while
keeping the `full-firehose` profile as the documented target end-state the architecture must not preclude.
This is a `PROPOSED_EXTENSION` recommendation, not a decision — see `docs/architecture/open-decisions.md`.
