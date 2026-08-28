# Strategy Learning (Explore / Exploit)

Per Step 1 Section 26. Preserves the source's Explore/Exploit concept, the Strategy Ledger, and the 80/20
split as a source-defined STARTING policy — explicitly not claimed to be empirically optimal.

## Source basis

- Explore/Exploit split: 80% Exploit / 20% Explore (SRC-000006, THRESH-003, page 2).
- Strategy Ledger structure: Strategy ID, Approach, Win Rate, Confidence Score, Status (TABLE-001, SRC-000007).
- Loss-cause tracking / "Unseen Variables": scrape lost-bid outcomes and feed them back into the Strategist's
  memory (page 2 narrative, `docs/source-extraction/strategies.md`).
- Restated identically in later drafts (Master Prompt v1/v2, pages 26-27).

## Explicit non-claim about optimality

Per Step 1 Section 26's instruction: "If the source provides an 80/20 value: preserve it as a source-defined
starting policy. Do not claim it is empirically optimal." The 80/20 split is a common, generic
reinforcement-learning convention the AI reached for when asked to design a self-improving strategy loop — it
is NOT derived from any IECHM-specific data, backtest, or citation in the source. It is preserved exactly as
`80`/`20` and explicitly labeled a DEFAULT/STARTING configuration value (versionable per `configuration.md`),
not a validated optimum.

## Where this belongs architecturally

Per `system-boundaries.md`, the Explore/Exploit Strategist role as originally described (SRC-000006) is a
**System B (bidding executive) concept** — it decides which PROPOSAL STRATEGY to use when bidding, which is
out of IECHM-LIOS's build scope. However, per `source-concept-mapping.md`'s `COMPOSITE_MAPPING` entry, the
underlying Explore/Exploit PATTERN is architecturally reusable by System A (IECHM-LIOS) for its OWN internal
decisions — e.g., which under-explored platform/sub-domain to prioritize scraping next, or which classification
heuristic to trial — even though the source never explicitly proposes this reuse. This reuse is flagged
`INTERPRETATION`/`PROPOSED_EXTENSION`, not presented as something the source asked for.

## Strategy Ledger as a canonical data domain

The Strategy Ledger's structure (ID / Approach / Win Rate / Confidence Score / Status) is a reusable PATTERN
this document recommends adopting for ANY of IECHM-LIOS's own experimental decisions (e.g., "Approach: prioritize
scraping r/InjectionMolding over r/CAD this week" with a tracked outcome), consistent with the Metric
Evolution EXPERIMENT/EVALUATION pattern in `metric-evolution.md`. This is `PROPOSED_EXTENSION` — the source
never applies the Strategy Ledger concept outside of System B bidding strategy.

## What is explicitly out of scope here

The actual bid-pricing Explore/Exploit decision (which pricing/tone strategy to try on a given platform) stays
entirely within System B and is not built by IECHM-LIOS — this document exists to (a) preserve the source
concept faithfully and (b) note where the underlying PATTERN could architecturally extend to System A, not to
claim System A performs bidding strategy itself.
