# Blue-Green Configuration Updates

Per Step 1 Section 19. Preserves the source's cascading blue-green update concept exactly, and extends it
only where a real conceptual flow requires more detail than the source provides (each extension explicitly
flagged).

## Source basis

SRC-000037 (user requirement): "if one agent on top the chain updates one thing all the agents below will
spin up another unit." SRC-000038 (AI response, page 14): "Downstream agents do not simply edit their runtime
prompts; they provision a parallel ephemeral worker unit... The new unit runs validation checks against
current queue payloads. Upon passing, the controller executes a gra[ceful cutover]." Also restated more
briefly in Master Prompt v1/v2 as "blue-green replication" (page 15, 26).

## Canonical conceptual flow

```
CURRENT VERSION
    ↓
NEW VERSION
    ↓
DEPENDENCY ANALYSIS          [PROPOSED_EXTENSION — which downstream agents actually depend on the changed state]
    ↓
SHADOW / VALIDATION WORKERS  [SOURCE-DERIVED — "parallel ephemeral worker unit," SRC-000038]
    ↓
HISTORICAL REPLAY            [PROPOSED_EXTENSION — testing the shadow worker against past queue payloads, not just current ones]
    ↓
COMPARISON                   [PROPOSED_EXTENSION — old-worker output vs. shadow-worker output on the same input]
    ↓
SENTINEL VALIDATION          [SOURCE-DERIVED — the Sentinel Plane's existing validation directives apply equally to shadow workers, per general architecture]
    ↓
PROMOTE                      [SOURCE-DERIVED — "the controller executes a gra[ceful cutover]"]
        or
ROLLBACK                     [PROPOSED_EXTENSION — see below]
```

## Why "Dependency Analysis," "Historical Replay," and "Comparison" are flagged extensions, not source content

The source's own description is compact: "provision a parallel ephemeral worker unit," "runs validation
checks against current queue payloads," "graceful cutover." It does NOT specify:
- HOW the system determines which downstream agents are affected by an upstream change (Dependency Analysis).
- WHETHER validation uses only live/current traffic or also replays past traffic to check for regressions
  (Historical Replay).
- WHETHER the shadow worker's output is compared against the OLD worker's output on the same input, or simply
  checked in isolation for internal validity (Comparison).

These three steps are added because "runs validation checks against current queue payloads" is too vague to
implement safely on its own — a shadow worker could pass superficial schema validation while still being
behaviorally wrong (e.g., correctly-formatted but incorrect classifications). This is `PROPOSED_EXTENSION`,
clearly distinguished from the `SOURCE-DERIVED` shadow-worker-then-cutover skeleton.

## Rollback

The source describes NO rollback mechanism anywhere for either agent replacement (Hot-Swap) or configuration
updates — only forward promotion. `ROLLBACK` is `PROPOSED_EXTENSION`, included because a promote-only system
with no ability to revert a bad configuration change is not a credible production design, and because Step 1
Section 19's own instruction text explicitly asks this flow to represent a PROMOTE-or-ROLLBACK branch. This
extension is flagged, not silently presented as sourced.

## Old versions remain recoverable

Per Step 1's explicit instruction ("Old versions must remain recoverable"): every promoted configuration/agent
version supersedes the active version but does NOT delete the prior version's record — consistent with the
`configuration.md` versioning discipline (`CONFIG-V1 → CONFIG-V2 → ...`, never an overwrite) and the
`schema-versioning.md` principle (`OLD DATA → VERSIONED TRANSFORMATION → NEW DATA`, never an overwrite).

## Relationship to Sentinel Plane and Hot-Swap

Blue-Green updates and Hot-Swap failover are two DIFFERENT triggers for a similar "provision replacement,
validate, cutover" pattern: Blue-Green is triggered by an intentional UPSTREAM CHANGE (config/logic update);
Hot-Swap is triggered by a detected FAILURE (drift/hallucination). The source treats these as related but
distinct concepts (SRC-000037 lists them as separate requirements in the same breath, but with different
triggers) — this document preserves that distinction rather than merging them into one generic "replace an
agent" flow, since their trigger conditions, urgency, and rollback needs differ (a Blue-Green rollback is a
planned reversal; a Hot-Swap has no rollback concept at all in the source, only forward replacement).

## No deployment infrastructure implemented

Per Step 1 Section 19's explicit instruction and Section 42's prohibition, no actual deployment tooling,
orchestration platform, or CI/CD mechanism is specified or implemented here.
