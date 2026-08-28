# Source vs. Canonical vs. Implementation — The Three Levels of Truth

This document establishes and maintains the separation required by Step 1 Section 3. It is the index that
every other Step 1 architecture document must be consistent with when it classifies a statement.

## The three levels

- **LEVEL 1 — SOURCE:** What `Autonomous Freelance Agent Factory Architecture.pdf` literally says, as
  preserved verbatim in `docs/source-extraction/` and indexed atomically in
  `docs/source-extraction/source-register.jsonl` (SRC-IDs). Immutable. Never edited by Step 1 or later.
- **LEVEL 2 — CANONICAL SPECIFICATION:** This project's current, implementation-oriented interpretation —
  everything under `docs/architecture/` produced in Step 1 (and revised in later steps). Versioned,
  supersedable, and explicitly NOT claimed to be identical to Level 1.
- **LEVEL 3 — IMPLEMENTATION:** Actual code, schemas, and running systems. Does not exist yet — Step 1
  produces no implementation (Step 1 Section 42).

## Classification taxonomy used throughout Step 1

Every architectural decision recorded in any Step 1 document must be tagged with exactly one of:

| Tag | Meaning |
|---|---|
| `SOURCE-DERIVED` | Directly stated in the source (an SRC-ID exists and the canonical statement is a restatement, not an extrapolation). |
| `INTERPRETATION` | The source implies this but does not state it explicitly; a judgment call was made to fill a structural gap (e.g., the source never says how System A should expose its output — Section 32/34 gap). |
| `PROPOSED_EXTENSION` | Not implied by the source at all; added because a working architecture requires it (e.g., new events, new subsystem boundaries not named in the source). Must never be presented as if the user asked for it. |
| `USER_DECISION_REQUIRED` | The source leaves multiple valid options (usually because of one of the 7 unresolved conflicts) and only the user can pick one. Tracked in `docs/architecture/open-decisions.md`. |

## Worked example: how one source statement moves through the three levels

- **LEVEL 1 (SOURCE):** SRC-000033, page 11 — user states the 3-tier agent allocation principle and the
  "5-Lead Rule" verbatim, with typos, in natural language.
- **LEVEL 2 (CANONICAL):** `docs/architecture/dynamic-worker-scaling.md` restates this as a formal policy:
  spawn threshold >5 leads/day, retirement threshold <2 leads/day over a 7-day rolling average — tagged
  `SOURCE-DERIVED` because the numbers and the trigger logic are explicit in the source (THRESH-001/002).
  The *mechanism* by which "spin up a separate agent" is technically realized (e.g., as a container, a
  serverless function, a long-lived process) is NOT specified by the source and is tagged `INTERPRETATION`
  or `PROPOSED_EXTENSION` where the canonical document has to pick something concrete enough to reason about.
- **LEVEL 3 (IMPLEMENTATION):** Does not exist. Would be a future worker-orchestration service.

## Why this separation matters for this project specifically

The source document is an AI-generated brainstorming transcript, not an engineering spec written by someone
with authority to make binding decisions — the AI proposed a great deal of concrete-sounding detail (schemas,
formulas, thresholds) in response to open-ended prompts, and the user never had a chance to review or approve
most of it line-by-line before the conversation moved on. Treating every AI-generated number and field name
in the source as automatically canonical would silently launder unreviewed AI speculation into "the spec."
This project instead requires that Level 2 documents explicitly own the decision to keep, adapt, or flag each
Level 1 statement — which is the entire purpose of the tagging system above.

## Where each Step 1 document's classifications live

Rather than duplicating every tag here, each Step 1 document (subsystems.md, agent-topology.md, events.md,
etc.) applies this taxonomy inline to its own content. This document is the DEFINITION of the taxonomy and
the RATIONALE for maintaining it — not a duplicate registry of every tag (that would drift out of sync with
the documents themselves). Cross-cutting summary tables of tag counts appear in
`docs/architecture/master-architecture.md` Section 3.
