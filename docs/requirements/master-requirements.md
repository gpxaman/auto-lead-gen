# Master Requirements — IECHM-LIOS (Lead Intelligence Operating System)

Status: STEP 0 SPECIFICATION ONLY. No implementation has occurred. Every section below links back to
`docs/source-extraction/source-register.jsonl` (SRC-IDs), `docs/requirements/requirements-register.jsonl`
(REQ-IDs), and the topical extraction files under `docs/source-extraction/`. This document organizes, but
does not replace or delete, the underlying source material.

## 1. System Identity
IECHM-LIOS is System A in the 3-system split identified in `docs/architecture/system-boundaries.md`: a
Lead Intelligence Architect & Multi-Agent Director that builds and maintains a living database of client
archetypes, lead channels, platforms, and sub-domains for IECHM's hardware/NPD business, and produces
structured strategic output — but does NOT itself bid on jobs or dispatch manufacturing. See REQ-000001,
SRC-000002.

## 2. Business Context
IECHM operates as a full-stack hardware design studio, engineering consultancy, and manufacturing facility
(SRC-000028). The project originated from a request to automate freelance-platform lead generation and
evolved, over 18 conversational turns, into a global multi-channel B2B lead intelligence architecture. See
`docs/source-extraction/exact-source.md` for the full turn-by-turn narrative.

## 3. IECHM Capability Scope
See `docs/source-extraction/manufacturing-capabilities.md` in full. Summary: Mechanical & Industrial Design,
Electronics & Embedded Systems, Rapid Prototyping & Additive Manufacturing, DFM/Tooling/Volume Manufacturing,
Global Supply Chain & QA (SRC-000028), plus the contingent, unverified "Universal 3D Printer" hardware
premise (ASSUMPTION-001, ASSUMPTION-002 in `docs/requirements/assumptions.md`).

## 4. Client Archetypes
Three non-identical enumeration passes exist in the source (3-archetype narrative + two 5-archetype list
forms) plus 3 differing schema enum vocabularies. See `docs/source-extraction/client-archetypes.md` and
CONFLICT-004/CONFLICT-005 in `docs/requirements/conflicts.md`. REQ-000013.

## 5. Lead Sources
See `docs/source-extraction/platforms.md` for the full 46-platform catalogue across 8 macro categories, and
the escalating source-count estimates (10-15 → 30 → 50-75 → 100+) as the user progressively broadened scope.
REQ-000010, REQ-000011, REQ-000028.

## 6. Lead Channel Taxonomy
Macro channel category count itself shifts across the source (4 → 8 → 5-branch diagram → 6-value enum). See
`docs/requirements/terminology.md` "Macro Channel" entry. REQ-000011, REQ-000017.

## 7. Platform Intelligence
Per-platform required fields: identity/URL, interaction mechanics, platform rules/ban triggers, native tools,
quality metrics, sub-domain index (SRC-000035). REQ-000017.

## 8. Sub-domain Intelligence
The "5-Lead Rule": spawn a dedicated sub-domain agent above 5 leads/day (THRESH-001), deprecate below 2
leads/day over a 7-day trailing average (THRESH-002). See `docs/source-extraction/thresholds.md`. REQ-000015.

## 9. Lead Intelligence (data model)
Three non-identical versions of the unified lead entity schema exist (SCHEMA-002, SCHEMA-003, SCHEMA-005) —
see `docs/source-extraction/json-schemas.md` and CONFLICT-003. REQ-000014.

## 10. Technical Classification
`ManufacturingDomain` enum (SRC-000011), CAD/PCB software fields, deliverables, project maturity stage. See
`docs/source-extraction/json-schemas.md` SCHEMA-001.

## 11. Manufacturing Classification
See Section 3 above and `docs/source-extraction/manufacturing-capabilities.md`.

## 12. Evidence
Every client-archetype/platform-concentration claim is required to carry "verifiable proof" per the user's
explicit requirement (SRC-000033, SRC-000034) — this is a first-class requirement, not an optional nicety.
REQ-000016.

## 13. Security
Sanitizer (anti-bot trap + prompt-injection detection, two distinct categories per explicit user requirement)
and Reviewer (compliance QA gate). See `docs/source-extraction/security-rules.md`. REQ-000030, REQ-000031.
NOTE: this is System B (bidding pipeline) architecture, out of IECHM-LIOS's own build scope per
`system-boundaries.md`, but IECHM-LIOS's platform-rules/ban-trigger data (Section 7) is a direct INPUT to it.

## 14. Agent Architecture
Full agent roster: see `docs/source-extraction/agents.md`. 3-tier allocation model (client classification /
channel teams / platform teams) plus dynamic sub-domain spawning. REQ-000015. Full-scale census: 140-195
agents (SRC-000043) — treat as illustrative, not a target (ASSUMPTION-006).

## 15. Dynamic Scaling
Cascading upstream-mutation → downstream-respawn ("blue-green replication," SRC-000037/038); 5-Lead sub-domain
auto-spawn/deprecation (Section 8). REQ-000018.

## 16. Proposal/Bidding Architecture (OUT OF IECHM-LIOS SCOPE — reference only)
Sanitizer→Strategist→Writer→Reviewer pipeline (`docs/source-extraction/agents.md`). Belongs to System B per
`system-boundaries.md`. Referenced here because IECHM-LIOS's platform/channel data is its primary input.

## 17. Hardware Integration (OUT OF IECHM-LIOS SCOPE — reference only)
Estimator Agent, Dispatch Agent, Cloud Slicer, G-code queue (SRC-000066, SRC-000076). Belongs to System C, and
is entirely contingent on the unverified ASSUMPTION-001/002 (Universal 3D Printer). REQ-000027.

## 18. Pricing (OUT OF IECHM-LIOS SCOPE — reference only)
`P_bid = 0.90 × P_market`, hard COGS floor, ≤20% max discount (FORMULA-001, THRESH-007/008). See
`docs/requirements/terminology.md` "10% Rule" for the ambiguity in the user's original phrasing. REQ-000022,
REQ-000023. Belongs to System B.

## 19. Strategy
See `docs/source-extraction/strategies.md` for the full catalogue (platform sequencing, archetype-specific
angles, Explore/Exploit, Instant-Proof conversion lever, aggregator-model pivot, flywheel/compounding,
self-replicating hardware scaling).

## 20. Learning
RAG-based win/loss memory query before drafting a bid (SRC-000004); Explore/Exploit 80/20 (SRC-000006).
REQ-000003, REQ-000004. System B function, IECHM-LIOS may supply the historical outcome data feed.

## 21. Memory
Strategy Ledger (SRC-000007, TABLE-001). REQ-000005.

## 22. Telemetry
Metric Evolution & Saturation Optimizer — proposes new fields to collect, self-idles at ≥99.5% saturation over
72h (THRESH-006). REQ-000021.

## 23. Sentinels
One Hallucination Sentinel per architectural layer; validates schema compliance, URL existence, numeric
sanity (SRC-000039). REQ-000019.

## 24. Hot-Swap
4-step failover protocol, dual trigger (drift score ≥0.85 OR ≥3 consecutive failures) — see CONFLICT/
ambiguity note in `docs/requirements/terminology.md` "Drift" entry. THRESH-004/005. REQ-000020.

## 25. Context Migration
Ceased agent's state is serialized and transferred to a clean replacement agent (SRC-000037c, SCHEMA-004/006).
REQ-000018, REQ-000020.

## 26. Blue-Green Updates
Upstream state mutation → parallel ephemeral downstream worker provisioned, validated, then graceful cutover
(SRC-000038, page 14). REQ-000018.

## 27. Metric Evolution
See Section 22 (Telemetry) — same requirement, cross-referenced.

## 28. Saturation
`CHANNEL_DATA_SATURATED_IDLE_ACTIVE` event; halts exploratory schema generation once threshold met
(THRESH-006). REQ-000021.

## 29. Re-order System (OUT OF IECHM-LIOS SCOPE — reference only)
Day-25 post-delivery automated re-order trigger (SRC-000069). Belongs to System B (account management/sales
function), not lead intelligence.

## 30. Data Contracts
See `docs/source-extraction/json-schemas.md` in full — 6 distinct schemas across the document's lifetime, with
2 explicit version-drift conflicts (CONFLICT-003/004) requiring an explicit reconciliation decision in Step 1.

## 31. Events
See `docs/source-extraction/events.md` — 11 named/implied events catalogued with triggers and page refs.

## 32. APIs
Only System B/C APIs are specified in any detail (Cloud Slicer, machine G-code queue, platform-native APIs
referenced generically). IECHM-LIOS's own API surface (what it exposes to System B as its report/strategy
output) is NOT specified anywhere in the source — this is a genuine gap requiring Step 1+ design work, not
something to be filled in from the source.

## 33. Economic Scenarios
See `docs/source-extraction/economic-scenarios.md` — 8 numbered scenarios, all SOURCE_ESTIMATE, several
mutually exclusive/overlapping (SCENARIO-004 vs 005 vs 006), resting on two conflicting lead-volume bases
(CONFLICT-001). Treat as illustrative of intended mechanism, not literal targets (ASSUMPTION-006).

## 34. Operational Requirements
24/7 autonomous operation intent (SRC-000037, "24/7 complete autonomous system"); zero-downtime cascading
update requirement; anti-bloat/saturation guardrails to control cost at scale.

## 35. Open Questions
- What does "IECHM" stand for? (never expanded in source — terminology.md)
- Is IECHM's Chennai location a confirmed fact or an AI invention? (ASSUMPTION-005)
- Does the user intend IECHM-LIOS to include System B and/or System C, or strictly System A? (system-boundaries.md — currently scoped to System A only, pending user confirmation)
- Which of the 3 client-archetype enumerations, and which of the 3 lead-entity schema versions, should be canonical? (CONFLICT-003/004)
- Is the "10% Rule" a fixed exact discount or a discount floor? (terminology.md, ASSUMPTION-007)
- Should the agent-census/cost model be re-derived against the revised 1.5M-2.5M/day lead volume rather than the original 15,000/day basis? (CONFLICT-001/002)
- Is the Universal 3D Printer real, in-development, or purely illustrative for financial modeling purposes? (ASSUMPTION-001)

## 36. Conflicts
See `docs/requirements/conflicts.md` in full — 7 numbered conflicts, all UNRESOLVED (one PARTIALLY RESOLVED
BY IMPLICATION), none silently resolved by this extraction.

## 37. Assumptions
See `docs/requirements/assumptions.md` in full — 8 numbered assumptions, each typed and confidence-rated.

## 38. Source References
See `docs/source-extraction/references.md` for all AI-cited external sources (none independently verified),
and `docs/source-extraction/source-register.jsonl` for the full atomic source-fact register (82 entries,
SRC-000001 through SRC-000082) underpinning every statement above.
