# Memory / RAG

Per Step 1 Section 27. Separates memory/retrieval concepts cleanly; RAG must not replace canonical structured
data. No vector database is implemented.

## The distinct memory-adjacent concepts, separated

| Concept | Definition | Source basis | Canonical owner |
|---|---|---|---|
| Source archive | The immutable Step 0 preserved source (`docs/source-extraction/`) | N/A — this project's own Level-1 discipline, not from the source PDF | Outside System A's runtime entirely; a design-time artifact |
| Raw observations | Scraped, unprocessed lead content | SRC-000009 | Raw Payload Storage (`subsystems.md` #4) |
| Evidence | Proof artifacts attached to claims | SRC-000034 | Evidence Management (`subsystems.md` #12) |
| Verified knowledge | Claims that passed Verification | SRC-000039 | Canonical Knowledge (`data-lineage.md`) |
| Model inference | Unverified LLM judgments | Implied throughout | Distinct from Verified Knowledge — see `data-lineage.md` |
| Agent memory | An individual agent's own working/task context | SRC-000037 (context transfer) | Agent State Management (`subsystems.md` #16) |
| Strategy memory | Win/loss history for strategy decisions (Strategy Ledger) | SRC-000004, SRC-000007 | Strategy Learning (`strategy-learning.md`) — a System B concept, referenced only |
| Historical versions | Prior schema/config/agent versions | Configuration/schema versioning discipline | `configuration.md`, `schema-versioning.md` |
| Telemetry | Operational metrics over time | Implied throughout | Telemetry (`subsystems.md` #21) |

## RAG's specific, narrow role

The source uses "RAG" for exactly one purpose: "Fetch the last 5 successful proposals I submitted for
hardware design tasks on this site, and 5 proposals that were rejected" (SRC-000004) — a System B (bidding
Strategist) memory-retrieval pattern, drawing on Strategy Memory specifically, not on Verified Knowledge,
Evidence, or any other category above.

## The hard rule (Step 1 Section 27's explicit instruction)

> "RAG/vector storage is a retrieval mechanism. It must not replace canonical structured data."

Concretely: even if IECHM-LIOS (System A) adopts a RAG-style retrieval mechanism for its own agents (e.g., a
Client Classification agent retrieving similar past-classified leads as few-shot context), the RETRIEVED
content remains, per `data-lineage.md`, at best MODEL INFERENCE or evidence-for-consideration — it does NOT
become CANONICAL KNOWLEDGE simply by being retrieved and used as prompt context. The structured, versioned,
evidence-backed records (Client/Channel/Platform Intelligence) remain the actual source of truth; a vector
store is an ACCELERATOR for finding relevant context, never a replacement authority.

## Memory poisoning

Named explicitly as a security concern to preserve (Step 1 Section 30, "memory poisoning" / "evidence
poisoning") — see `security.md`. If RAG/vector memory is adopted for System A, it inherits the same
poisoning risk the source implicitly worries about for System B's Strategy Ledger (an attacker could try to
get bad "past outcomes" recorded to bias future retrieval) — flagged here as a cross-reference, detailed in
`security.md`.

## Explicit non-implementation

No vector database, embedding model, or retrieval infrastructure is implemented in Step 1 (Section 42). This
document defines the conceptual boundary memory/RAG must respect if and when it is implemented.
