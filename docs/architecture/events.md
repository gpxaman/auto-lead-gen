# Event Architecture

Per Step 1 Section 14. Distinct from (and builds on) `docs/source-extraction/events.md`, which is the raw
Step 0 catalogue. This document adds the full event-contract fields Step 1 requires and explicitly separates
source-defined events from newly proposed ones.

## Source-defined events (full contract detail)

### `CEASE_OPERATIONS`
- **Source IDs:** SRC-000078. **Purpose:** non-maskable kill signal to a hallucinating/faulty worker.
- **Producer:** Hallucination Sentinel. **Consumer:** the targeted worker's runtime + Hot-Swap Engine.
- **Payload concept:** worker ID, reason. **Version:** not specified. **Idempotency:** `UNRESOLVED` (source
  doesn't say what happens if issued twice). **Ordering:** must precede admin-log/state-migration steps
  (source specifies this sequence explicitly: interrupt → log → serialize → replace). **Retry:** `UNRESOLVED`.
  **Dead-letter behavior:** `UNRESOLVED`. **Security:** must not be spoofable by a non-Sentinel source
  (`PROPOSED_EXTENSION` requirement, not stated by source but clearly necessary). **Retention:** implied
  permanent (feeds the admin panel/audit trail).

### `FAILOVER_HOTSWAP_TRIGGERED` (v1) / `FAILOVER_HOTSWAP_DISPATCHED` (v2)
- **Source IDs:** SRC-000041 (v1), SRC-000082 (v2). **Purpose:** records a hot-swap event for telemetry.
  **BOTH versions preserved** per CONFLICT-003 — not merged. **Producer:** Hot-Swap Failover Engine.
  **Consumer:** Telemetry/Audit. **Payload concept:** see SCHEMA-004 (v1) and SCHEMA-006 (v2) in
  `schema-versioning.md` — structurally different. **Version:** explicitly two source versions. **Idempotency,
  ordering, retry, dead-letter:** `UNRESOLVED` in source. **Security:** telemetry integrity (tamper-evidence).
  **Retention:** implied permanent (audit requirement).

### `CHANNEL_DATA_SATURATED_IDLE_ACTIVE`
- **Source IDs:** SRC-000079. **Purpose:** administrative notice that a channel's schema has reached
  saturation; halts exploratory metric proposals. **Producer:** Metric Evolution/Saturation Optimizer.
  **Consumer:** the optimizer itself (self-throttling) + admin panel. **Payload concept:** channel ID,
  saturation metric value. **Version:** not specified. **Idempotency:** likely idempotent by design (a
  standing status, not a one-time trigger) — `INTERPRETATION`. **Ordering:** n/a. **Retry:** n/a.
  **Dead-letter:** n/a. **Security:** none specific. **Retention:** implied standing/current-state, not just
  a log entry.

### `EVENT_CONTRACT_SIGNED`
- **Source IDs:** SRC-000076 (page 28 diagram), implied page 24. **Purpose:** triggers Zero-Touch Machine
  Dispatch (System C). **Producer:** System B (bidding executive, out of IECHM-LIOS scope). **Consumer:**
  System C's Dispatch Agent. **Payload concept:** contract/order details. **Version, idempotency, ordering,
  retry, dead-letter, security, retention:** all `UNRESOLVED`/`INTERFACE_UNDEFINED` in source — this event
  crosses the System B→C boundary which is itself `INTERFACE_UNDEFINED` per `system-boundaries.md`.
  **Note:** this event is OUT OF SCOPE for IECHM-LIOS to produce or consume; documented here for completeness
  of the source's full event catalogue only.

### Sub-domain spawn/retirement triggers (unnamed in source, behavior fully specified)
- **Source IDs:** SRC-000036. **Purpose:** the 5-Lead Rule spawn (>5 leads/day) and retirement (<2 leads/day,
  7-day rolling avg) triggers. **Producer:** Dynamic Worker Scaling subsystem (deterministic check). **Consumer:**
  Agent Orchestration. **Payload concept:** sub-domain ID, current velocity. **This document assigns canonical
  names** `SUBDOMAIN_SPAWN_TRIGGERED` / `SUBDOMAIN_RETIRE_TRIGGERED` since the source describes the BEHAVIOR
  precisely but never names the event itself — **event NAME is `PROPOSED_EVENT`, event TRIGGER LOGIC and
  thresholds are `SOURCE-DERIVED`.**

### Upstream Mutation / Cascading Update trigger (unnamed in source, behavior specified)
- **Source IDs:** SRC-000037, SRC-000038. **Purpose:** propagate an upstream config/state change into
  downstream ephemeral-worker provisioning (blue-green pattern). **This document assigns the canonical name**
  `CONFIG_CHANGED` (or `UPSTREAM_STATE_MUTATED` for non-config state changes) — **name is `PROPOSED_EVENT`,
  the cascading-provisioning BEHAVIOR it triggers is `SOURCE-DERIVED`.**

### Day-25 Re-order Trigger (unnamed in source, behavior specified)
- **Source IDs:** SRC-000069. **Purpose:** trigger automated re-order outreach 25 days post-delivery. Out of
  IECHM-LIOS scope (System B function) — documented for completeness. **Name assigned:** `REORDER_WINDOW_REACHED`
  (`PROPOSED_EVENT`), trigger timing `SOURCE-DERIVED`.

## Newly proposed events required by the canonical architecture (none presented as source requirements)

| Event | Purpose | Producer | Consumer |
|---|---|---|---|
| `PLATFORM_DISCOVERED` | New candidate platform found | Source Discovery | Source Registry |
| `PLATFORM_REGISTERED` / `PLATFORM_DEPRECATED` | Registry lifecycle | Source Registry | Platform Intelligence |
| `RAW_LEAD_INGESTED` | A raw payload was successfully scraped | Lead Ingestion | Raw Payload Storage |
| `LEAD_REJECTED_LAYER0` | Deterministic triage rejected a lead | Deterministic Triage | Telemetry |
| `INJECTION_DETECTED` | Adversarial content found in scraped lead text | Security/Sanitization | Sentinel Plane, Audit |
| `CLIENT_CLASSIFIED` | Archetype assignment completed | Client Intelligence | downstream classification stages |
| `CHANNEL_BENCHMARK_UPDATED` / `PLATFORM_PROFILE_UPDATED` | Registry data refreshed | Channel/Platform Intelligence | consumers of that data |
| `EVIDENCE_ATTACHED` | A claim received supporting evidence | any classifying agent | Evidence Management, Verification |
| `VERIFICATION_COMPLETED` / `VERIFICATION_FAILED` | Verification outcome | Verification subsystem | Client/Technical Intelligence |
| `AGENT_STATE_CHANGED` | An agent's health/lifecycle state changed | Agent State Management | Sentinel Plane, Admin |

Every event in this table is `PROPOSED_EVENT` — none is presented as if the source required it by that name;
all exist to make source-required BEHAVIORS (ingestion, classification, evidence-tracking) implementable as a
real event-driven system.

## What is explicitly NOT decided here

Message-bus technology, delivery guarantees (at-least-once vs. exactly-once), schema registry mechanics, and
retention policy defaults are NOT decided in Step 1 — see `docs/architecture/open-decisions.md`.
