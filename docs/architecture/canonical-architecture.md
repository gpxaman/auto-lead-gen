# Canonical IECHM-LIOS Architecture

Per Step 1 Section 9. This is the primary implementation-oriented layer model for System A (IECHM-LIOS only —
see `system-boundaries.md`). It preserves all source variants (multiple layer-numbering schemes, multiple
scale profiles) rather than collapsing them, per `docs/requirements/terminology.md` "Layer 0/1/2/3/4" entry
(which flags that the source itself uses TWO different, non-identical "Layer N" numbering schemes: an
agent-hierarchy scheme and a data-pipeline-stage scheme). **This document adopts the DATA-PIPELINE-STAGE
scheme as its Layer 0-4 numbering** (matching pages 20/27), and separately documents the agent-hierarchy
depth using different terminology (Tier 1-4, see `agent-topology.md`) to avoid perpetuating the source's own
naming collision.

## LAYER 0 — Deterministic Ingestion / Pre-Filtering

**Purpose:** Non-AI, high-throughput filtering of raw signals before any LLM token is spent. **Status:**
`SOURCE-DERIVED` (SRC-000053, pages 20, 27). **Only relevant/required under the `full-firehose` scale profile**
(see `scaling-scenarios.md`) — the `freelance-narrow` profile's source material never describes a Layer 0
stage. Components: keyword blacklist/whitelist matching, budget-sanity checking, location routing.
Reduces ~2,000,000 raw signals/day → ~100,000 (THRESH-012). See `docs/architecture/subsystems.md` #5
(Deterministic Triage).

## LAYER 1 — Client Intelligence

**Purpose:** Classify buyer archetype and evidence-track platform concentration. **Status:** `SOURCE-DERIVED`,
though drawing from 3 non-identical archetype enumerations (CONFLICT-004, see `client-intelligence-model.md`).
Also performs the LLM-based qualification pass described on page 20/27 ("Layer 1: LLM Sanitizer/Classifier") —
**NOTE the naming collision:** this data-pipeline "Layer 1" (an LLM qualification stage) is conceptually
distinct from the agent-hierarchy "Layer 1" (Central Command/Client Classification Swarm, 3 agents) described
on pages 11-12, 16 — both are called "Layer 1" in the source but describe different things (a pipeline stage
vs. an agent-org-chart depth). This canonical document keeps them separate: this section is the PIPELINE
STAGE; the ORG-CHART depth is documented in `agent-topology.md` as "Tier 1."

## LAYER 2 — Lead-Channel Intelligence

**Purpose:** Maintain macro-channel-type benchmark data (MOV, lead velocity, setup/approval time, dominant
client concentration, anti-scraping friction level — SRC-000035). **Status:** `SOURCE-DERIVED`.

## LAYER 3 — Platform Intelligence

**Purpose:** Per-platform deep-dive profiles: identity/URL, interaction mechanics, platform rules/ban
triggers, native tools, quality metrics, sub-domain index (SRC-000035). **Status:** `SOURCE-DERIVED`. One
dedicated agent/worker per platform (up to ~75 at `full-firehose` scale — see `agent-topology.md`).

## LAYER 4 — Sub-Domain Intelligence / Dynamic Workers

**Purpose:** Granular, per-sub-domain tracking (e.g., a specific subreddit), with dynamic agent
spawn/retirement governed by the 5-Lead Rule (THRESH-001/002). **Status:** `SOURCE-DERIVED`. See
`docs/architecture/dynamic-worker-scaling.md`.

## CROSS-CUTTING OBSERVER AND CONTROL PLANE

Applies uniformly across Layers 0-4. Not itself numbered as a "layer" in the source (it is explicitly
described as "cross-cutting," pages 14, 26, 28). Components, each with its own dedicated Step 1 document:

| Component | Status | Document |
|---|---|---|
| Evidence | `SOURCE-DERIVED` (partial — proof/verification concepts are named but not formalized) | `evidence-model.md` |
| Verification | `SOURCE-DERIVED` (partial) | `evidence-model.md` |
| Security (Sanitizer-equivalent for recon data) | `INTERPRETATION` — the source's Sanitizer is a System-B (bidding pipeline) component; System A needs an analogous but distinct data-integrity/prompt-injection defense for RAW SCRAPED CONTENT feeding its own classifiers, which the source does not explicitly separate out | `security.md` |
| Sentinels / Hallucination Detection | `SOURCE-DERIVED` | `sentinel-plane.md`, `hallucination-detection.md` |
| Telemetry / Metric Evolution | `SOURCE-DERIVED` | `metric-evolution.md`, `observability.md` |
| Drift | `SOURCE-DERIVED` (formula incomplete, SOURCE_INCOMPLETE) | `hallucination-detection.md` |
| Configuration | `INTERPRETATION` (source names many configurable concepts but never a unified configuration subsystem) | `configuration.md` |
| Blue-Green Updates | `SOURCE-DERIVED` | `blue-green-updates.md` |
| Context Migration | `SOURCE-DERIVED` | `context-migration.md` |
| Hot-Swap | `SOURCE-DERIVED` | `hot-swap.md` |
| Cost Control | `SOURCE-DERIVED` (partial — cost figures exist, but no explicit "cost control subsystem" is named) | `economic-model.md` |
| Audit | `PROPOSED_EXTENSION` (the "admin panel pinning" concept is source-derived, but a formal audit subsystem beyond that is not) | `subsystems.md` #28 |

## How source concepts NOT cleanly fitting this layer model are handled

Per Step 1 Section 9's explicit instruction ("Do not delete source concepts that do not fit neatly into these
layers. Instead create mappings"), every source concept is mapped in
`docs/architecture/source-concept-mapping.md`, including concepts that span multiple layers (e.g., "Evidence"
touches every layer) or that belong to System B/C and are only referenced here for interface purposes (e.g.,
the pricing engine).

## What this document is NOT

This is not a database schema, not an API spec, and not a deployment topology. It is the conceptual layer
model that `subsystems.md`, `agent-topology.md`, `data-flow.md`, and `data-domains.md` all build on
consistently.
