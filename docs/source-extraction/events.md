# Extracted Events (named system events / signals)

| Event Name | Meaning | Source page(s) |
|---|---|---|
| `CEASE_OPERATIONS` | Non-maskable kill signal issued by a Sentinel to a hallucinating/faulty worker agent | 14, 26, 28 |
| `FAILOVER_HOTSWAP_TRIGGERED` | Telemetry event name in the v1 Node Health & Sentinel Telemetry Schema (SCHEMA-004) | 15 |
| `FAILOVER_HOTSWAP_DISPATCHED` | Telemetry event name in the v2 Node Failure & Hot-Swap Telemetry Contract (SCHEMA-006) — different name for a conceptually similar event; see CONFLICT-003 | 29 |
| `CHANNEL_DATA_SATURATED_IDLE_ACTIVE` | Administrative notice published when the Telemetry/Saturation Optimizer determines a channel's data schema has reached saturation and further exploratory metric discovery is not worthwhile | 14, 28 |
| `EVENT_CONTRACT_SIGNED` | Fires when a client accepts/pays for a bid; triggers Zero-Touch Machine Dispatch (Dispatch Agent pushes G-code to the machine's print queue) | 24 (implied, "Contract Signed Event"), 28 (named explicitly) |
| Upstream Mutation Trigger | Generic event class: "If an agent at any upstream layer mutates state ... " triggers deterministic downstream branching / cascading agent replication | 14 |
| Dynamic Sub-Domain Auto-Spawn ("The 5-Lead Rule") | Fires when a sub-domain sustains >5 leads/day; spawns a dedicated micro-worker agent for that sub-domain | 11, 12, 14, 17, 26, 27 |
| Sub-Domain Deprecation / Merge-Back | Fires when a spawned sub-domain agent's lead velocity drops below 2 leads/day over a 7-day trailing/rolling average; agent is serialized/drained and its function merged back into the parent worker | 12, 14, 26 |
| `CONTAINS_ANTI_BOT_TRAP` (data field, not a named event but a detection flag) | Set by the Sanitizer when a client brief contains a mandatory anti-automation phrase/keyword | 29 (field `contains_anti_bot_trap` in SCHEMA-005), conceptually throughout pages 1-2, 26-28 |
| `IS_PROMPT_INJECTION` (data field/detection flag) | Set by the Sanitizer when a client brief contains a detected prompt-injection attempt | 29 (field `is_prompt_injection`), conceptually pages 1-2, 26-28 |
| Day-25 Automated Re-Order Trigger | Fires at exactly 25 days post-delivery; account-management agent contacts the client proposing a repeat order at the locked-in discount | 25, 28 |
| Blue-Green (cascading) Replacement / Update | When top-level logic is updated, downstream agents provision a parallel ephemeral worker unit, validate it against current queue payloads, then execute a graceful cutover — described as "blue-green replication" | 14, 15, 26 |
