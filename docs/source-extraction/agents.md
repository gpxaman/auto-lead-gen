# Extracted Agent / Role Definitions

## Site Executive pipeline (source pages 1-2) — "Supervisor-Worker Architecture"
| Agent | Role | Order |
|---|---|---|
| The Sanitizer | Defense: scans for anti-bot traps and prompt injections; neuters malicious instructions | 1st |
| The Strategist | Intelligence: queries vector memory of past wins/losses, writes a proposal blueprint (not the proposal itself); runs Explore/Exploit (80/20) | 2nd |
| The Writer | Executor: drafts the persuasive bid per the blueprint + mandatory constraints | 3rd |
| The Reviewer | QA: checks Writer's output against brief + constraints; rejects/sends back if a mandatory constraint (e.g. anti-bot trap phrase) was missed | 4th |

This same 4-role pipeline recurs, restated, in the Master Prompt v1 (page 26, Section 5, condensed) and
Master Prompt v2 (pages 27-28, Section 6 "THE 4-NODE SECURE CLUSTER") — with the Writer's role expanded to
include "Calls Slicer API: Generates 3D preview render with client's logo," and the Reviewer's role expanded
to include "Audits pricing math (P_bid = 0.90 × P_market)."

## Database/Discovery multi-agent hierarchy (source pages 11-12, System Prompt Draft 2)
| Layer | Team / Role | Agent count (as stated) |
|---|---|---|
| Central Director Agent | Top of hierarchy, oversees all branches | 1 (implicit) |
| Layer 1: Client Classification Swarm | Classifies buyer archetype, proof, per-platform concentration | 2-3 agents |
| Layer 2: Channel Type Swarms | One team per macro category (Freelance, B2B Trade, Community, Brokerage, etc.) | "a few bots" per macro type (not numerically fixed in this draft) |
| Layer 3: Platform & Sub-Domain Worker Agents | One dedicated team/agent per individual major lead source (e.g., "Upwork Worker Agent," "Alibaba RFQ Worker Agent") | 1 team per platform |
| Dynamic Spawn Engine | Spawns a dedicated sub-agent when a sub-domain exceeds 5 leads/day | Variable / on-demand |

## Cross-cutting resilience-plane agents (source pages 13-15, System Prompt Draft 3)
| Agent | Sole task | Trigger / behavior |
|---|---|---|
| Hallucination Sentinel (1 per layer) | Detect and report hallucinating agents; track drift score $D_t$ per worker | On threshold breach ($D_t \ge 0.85$ or ≥3 consecutive errors — see thresholds.md): issue `CEASE_OPERATIONS`, pin worker ID + model telemetry + error log to Admin Panel |
| Hot-Swap Failover / Context Migrator Engine | Serialize and transfer the ceased agent's context/state to a clean replacement agent | Triggered immediately after Sentinel's `CEASE_OPERATIONS`; resumes message bus in <500ms (page 26) / cutover_latency_ms 384 in the SCHEMA-006 example |
| Metric Evolution & Saturation Optimizer (Telemetry Engine) | Discover new metrics/data fields to collect from unstructured lead data | If data completeness/predictability ≥99.5% over a 72-hour window (page 14, 28), publishes `CHANNEL_DATA_SATURATED_IDLE_ACTIVE` notice and goes idle (drops exploratory schema calls, low-frequency polling) |

## Formal agent-count census (source pages 15-17, quantitative projection) — see tables.md TABLE-004/006
Total ecosystem: ~140 to 195 agents at "full global scale" (~75 platforms). Breakdown:
- Layer 1 (Central Command): 3 agents
- Layer 2 (Macro Channels): 12 agents (6 teams × 2 agents each)
- Layer 3 (Platform Workers): 75 agents (1 per platform)
- Layer 4 (Micro Sub-Domains): 30-50 agents (dynamic)
- Cross-Cutting Sentinels: 20-55 agents (1 auditor per 5 workers, + 1 Hot-Swap Engine, + 1 Telemetry Optimizer)

## Hardware-integration agents (source page 24, "Deep API Integration")
| Agent | Role |
|---|---|
| The Estimator Agent | Silently slices the client's CAD file in the cloud using the machine's exact acceleration profiles; calculates aluminum mass and kWh usage; sends a mathematically derived quote |
| The Dispatch Agent | On contract signature/payment, bypasses human operators and pushes compiled G-code/toolpath data directly into the machine's active print queue |

## Account-management agent (source page 25)
"Deploy an account management agent that tracks the delivery date of past client orders" and issues the
Day-25 automated re-order trigger message.

## Model providers/versions named as concrete examples (not requirements, illustrative only)
- `gpt-4o-mini` (page 3, 4 — scraper parsing model)
- `gpt-4o`, `gpt-4o-mini`, `Claude 3 Haiku`, `Claude 3.5 Sonnet` (page 16 — model-routing cost tiers)
- `gpt-4o-2024-08-06` (page 15, 29 — example hallucinating model in telemetry schema examples)
- `claude-3-5-sonnet-20241022` (page 15, 29 — example fallback/replacement model)
- `GPT-4.1 Nano` (page 17 — mentioned as a cheap-tier routing option)
- `GPT-5` (page 18 — mentioned only in a cited source title "OpenAI API Cost Calculator 2026 - GPT-4o, GPT-5")

NOTE: These model names/versions are AI-generated illustrative examples within a hypothetical architecture,
not verified technical commitments or a bill of materials. Preserved as SOURCE_EXAMPLE.
