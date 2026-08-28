# Data Flow

Per Step 1 Section 15. Documents the complete conceptual flow plus the named sub-flows Step 1 requires.

## Primary intelligence flow

```
SOURCE DISCOVERY
    ↓
SOURCE REGISTRY
    ↓
RAW INGESTION
    ↓
RAW PAYLOAD (storage)
    ↓
DETERMINISTIC TRIAGE            [Layer 0 — only in `full-firehose` scale profile]
    ↓
SECURITY ANALYSIS               [prompt-injection / adversarial-content detection on scraped text]
    ↓
NORMALIZATION                   [into whichever UnifiedLeadEntity schema version is canonical — see schema-versioning.md]
    ↓
CLIENT CLASSIFICATION           [Layer 1 — buyer archetype, per client-intelligence-model.md]
    ↓
TECHNICAL CLASSIFICATION        [ManufacturingDomain, CAD/PCB fields — REQ-000007]
    ↓
COMMERCIAL CLASSIFICATION       [budget, MOV, feasibility scoring]
    ↓
EVIDENCE                        [attach proof — evidence-model.md]
    ↓
VERIFICATION                    [confirm claims resolve to real, matching sources]
    ↓
CANONICAL KNOWLEDGE             [the durable, trusted lead/client/platform/channel record]
    ↓
METRICS                         [telemetry aggregation]
    ↓
STRATEGY                        [System A's own platform-rollout prioritization — subsystems.md #23]
    ↓
INTELLIGENCE OUTPUT             [the report/strategy artifact handed to System B — INTERFACE_UNDEFINED]
```

Status: every stage above is `SOURCE-DERIVED` in existence (the source describes each concept somewhere), but
the STAGE ORDERING and the explicit separation of "Security Analysis" as its own stage (distinct from Layer 0
triage AND from System B's Sanitizer) is `INTERPRETATION` — the source never lays out all these stages in this
exact linear sequence in one place; this is a synthesis across pages 3, 14, 20, 27.

## DISCOVERY FLOW
`Source Discovery → Source Registry.` See `subsystems.md` #1-2. Triggered by Macro Channel Team exploration or
manual user input. `SOURCE-DERIVED` (existence) / `PROPOSED_EXTENSION` (as a named, isolated flow).

## PLATFORM RESEARCH FLOW
`Source Registry → Platform Worker assigned → Platform Intelligence populated (rules, tools, metrics,
sub-domain index).` Directly matches SRC-000035's required field list. `SOURCE-DERIVED`.

## WORKER SPAWN FLOW
`Sub-domain lead velocity monitored → exceeds 5/day (THRESH-001) → Dynamic Worker Scaling triggers
`SUBDOMAIN_SPAWN_TRIGGERED` → Agent Orchestration provisions new Tier 4 worker → worker inherits parent Tier 3
persona/compliance parsers (SRC-000036) → worker activated.` `SOURCE-DERIVED`.

## WORKER RETIREMENT FLOW
`Sub-domain velocity monitored on 7-day rolling average → falls below 2/day (THRESH-002) → Dynamic Worker
Scaling triggers `SUBDOMAIN_RETIRE_TRIGGERED` → worker state drained/serialized (NOT the same as a Hot-Swap
failure exit — see `context-migration.md` for why retirement and failure must be handled as distinct paths) →
worker deactivated, state archived for potential reactivation.` `SOURCE-DERIVED` (SRC-000036: "the sub-agent is
deprecated or merged back in[to the parent]").

## CONFIGURATION UPDATE FLOW
`Admin/user changes a config value → `CONFIG_CHANGED` event → Blue-Green Update Flow (below) initiated for
every downstream consumer of that config.` `SOURCE-DERIVED` (SRC-000037/038's cascading-update requirement).

## BLUE-GREEN UPDATE FLOW
`Upstream mutation detected → dependency analysis (which downstream agents depend on the changed state) →
parallel ephemeral "shadow" workers provisioned with new config/logic → shadow workers validated against
current queue payloads (SRC-000038) → on pass, graceful cutover (old worker retired, new worker promoted) →
on fail, shadow worker discarded, old worker remains active.` See `docs/architecture/blue-green-updates.md`
for full detail. `SOURCE-DERIVED` for the validate-then-cutover pattern; the explicit "historical replay" and
"comparison" steps are `PROPOSED_EXTENSION` (added because "validated against current queue payloads" alone
is underspecified for a real implementation — see `blue-green-updates.md`).

## SENTINEL FAILURE FLOW
`Worker produces output → Sentinel validates (schema, URL, numeric sanity) → drift score computed
(FORMULA-002, SOURCE_INCOMPLETE) → if D_t ≥ 0.85 OR ≥3 consecutive failures (dual OR-condition per
THRESH-004/005) → Quarantine Flow initiated.` `SOURCE-DERIVED`.

## QUARANTINE FLOW
`Sentinel issues `CEASE_OPERATIONS` → worker interrupted → incident (worker ID, model telemetry, error log)
pinned to admin panel → worker marked quarantined in Agent State Management.` `SOURCE-DERIVED` (SRC-000078).

## CONTEXT MIGRATION FLOW
`Quarantined worker's active state (task queue, message buffers, scratchpad) serialized and SANITIZED → state
classified per the trust taxonomy in `context-migration.md` (a hallucinated CLAIM must not be promoted to
TRUSTED KNOWLEDGE during this step) → sanitized state handed to replacement worker.` `SOURCE-DERIVED` for the
serialize-and-transfer mechanism; the explicit trust-classification step is `INTERPRETATION`/`PROPOSED_EXTENSION`
— required by Step 1 Section 23's explicit warning but not itself detailed by the source.

## HOT-SWAP FLOW
`Context Migration completes → clean replacement agent instantiated (potentially alternate model provider,
per SCHEMA-006's example) → replacement validated → replacement activated, resumes message bus (source cites
<500ms / 384ms example latency) → old worker fully retired (but its historical state remains queryable for
audit, per Step 1 Section 24's explicit requirement).` `SOURCE-DERIVED`.

## ROLLBACK FLOW
Not described by the source at all for the agent/hot-swap context (the source only ever describes forward
replacement, never reverting to a PRIOR agent version after a bad promotion). For Blue-Green config updates,
an implied rollback exists ("PROMOTE or ROLLBACK" — Step 1 Section 19's own instruction text, not sourced
from the original PDF). **Status: `PROPOSED_EXTENSION`** — genuinely absent from the source, included here
because Step 1 Section 19 explicitly requires representing it and because a promote-only system without
rollback is not a credible production design.

## METRIC EVOLUTION FLOW
`Telemetry observes lead data → Metric Evolution Optimizer detects information entropy (unexplained variance)
→ proposes new schema field → (implied) field proposed for human/architectural review, NOT auto-applied (per
Step 1 Section 25's explicit prohibition) → accepted fields become part of a new schema VERSION (see
schema-versioning.md), never an in-place mutation.` `SOURCE-DERIVED` for the observe→propose loop;
`INTERPRETATION` for the explicit "not auto-applied, goes through versioned migration" requirement (a
consequence of Step 1's own governing rules, not explicitly stated by the source PDF).

## SATURATION FLOW
`Metric Evolution Optimizer measures completeness/predictability for a channel → exceeds 99.5% over 72-hour
window (THRESH-006) → `CHANNEL_DATA_SATURATED_IDLE_ACTIVE` published → optimizer halts exploratory proposals
for that channel, drops to low-frequency sentinel-only polling.` `SOURCE-DERIVED` (SRC-000079).
