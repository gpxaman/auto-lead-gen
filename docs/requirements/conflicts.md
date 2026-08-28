# Conflict Register

## CONFLICT-001 — Raw daily lead volume: 15,000/day vs. 1.5M-2.5M/day
- **source_A:** page 16 ("Let's assume the global hardware/NPD market generates 15,000 raw leads/signals per
  day"); restated/used through pages 17-18 (450,000/month = 15,000×30; TABLE-005/006/007/008; FORMULA-003/004/005).
- **source_B:** page 19-20 ("your true Total Addressable Raw Firehose across all 75+ platforms is realistically
  1.5 million to 2.5 million raw signals per day"); used from page 19 onward including the Master Prompt v1/v2
  ("ingests a raw global firehose of ~1.5 to 2.5 million signals per day," page 25, 27).
- **context_A:** Answering "at the full scale how many agents ai will be there and how many tokens each
  consume and how much is the cost" — scoped implicitly to Western-facing English-language NPD/CAD/PCB
  freelance job postings only (per the AI's own later admission on page 19: "heavily biased toward
  Western-facing, English-language freelance engineering and custom NPD design jobs").
- **context_B:** Directly triggered by the user explicitly rejecting the narrow scope ("it doesnt only include
  npd but also middel man and importers and all platforms and every manfacturing except chemicals and fabrics
  and foods... why 15k leads how you came to that point") and demanding the full addressable volume across
  B2B trade directories, importers, and middlemen.
- **possible_reason:** The two figures answer genuinely different questions (narrow NPD-freelance-only volume
  vs. the full physical-manufacturing B2B firehose) but are never explicitly reconciled as "these are two
  different metrics for two different scopes" — the source treats source_B as a correction/expansion of
  source_A without formally retiring source_A's associated calculations (agent census, cost table).
- **resolution_status:** UNRESOLVED. Step 1+ must decide whether the final architecture's agent-census/cost
  model (built on the 15,000/day basis, TABLE-004/005/006) needs to be re-derived against the 1.5M-2.5M/day
  basis, since Layer 0 (introduced specifically to handle the larger volume) did not exist at the time the
  original 140-195 agent count and ~$3,500/month cost figure were computed.

## CONFLICT-002 — Whether the Master Prompt v1 explicitly states its lead-volume basis matches the revised figure
- **source_A:** Master Prompt v1 / v2 (page 25, 27) explicitly states "~1.5 to 2.5 million signals per day" as
  the ingestion basis, consistent with source_B in CONFLICT-001.
- **source_B:** The AGENT COUNT and COST figures baked into the same overall document (pages 15-17) were never
  recomputed against this larger basis — no updated agent-census or cost table appears anywhere after page 20's
  Layer-0 introduction.
- **context_A / context_B:** Same as CONFLICT-001.
- **possible_reason:** The user never re-asked "at full scale how many agents/tokens/cost" after the volume
  revision, so the AI never recomputed those figures against the new basis.
- **resolution_status:** UNRESOLVED. This is a downstream consequence of CONFLICT-001 and is called out
  separately because it specifically affects `docs/architecture/` sizing work in later steps.

## CONFLICT-003 — Two non-identical versions of the Lead Entity schema and the Failover Telemetry schema
- **source_A:** SCHEMA-003 (page 14, `docs/source-extraction/json-schemas.md`) — Unified Lead Entity Data
  Schema v1: nested `layer_origin.client_archetype` with values `NPD_Innovator | Middleman_Reseller |
  Enterprise_SME | Crowdfunder | Institutional`; SCHEMA-004 (page 15) — telemetry event named
  `FAILOVER_HOTSWAP_TRIGGERED`.
- **source_B:** SCHEMA-005 (page 29) — Unified Lead Entity Schema v2 (formal JSON Schema draft-07): top-level
  `client_archetype` with values `NPD_INNOVATOR | MIDDLEMAN_OEM_RESIGN | SME_ENGINEERING_OVERFLOW |
  CROWDFUNDER_FUNDED | GOVERNMEN[truncated]`; SCHEMA-006 (page 29) — telemetry event renamed
  `FAILOVER_HOTSWAP_DISPATCHED`, restructured into `anomaly_report`/`failover_execution` sub-objects.
- **context_A:** Produced in System Prompt Draft 3 ("Autonomous Self-Healing Multi-Agent Lead & Intelligence
  Infrastructure"), in response to the user's cascading-updates/hallucination-sentinel requirement (page 13).
- **context_B:** Produced in Master Prompt v2 / IECHM-OS (final draft), in response to "make this prompt much
  more comprehensive and add more info" (page 26).
- **possible_reason:** v2 is a later, more polished draft; the user's request was to make the prompt "more
  comprehensive," not explicitly to redesign the schema, so the field/value renaming appears to be incidental
  drift across drafts rather than a deliberate correction.
- **resolution_status:** UNRESOLVED. Neither version is declared canonical by the source. Step 1+ (Database/
  Contracts design) must make an explicit decision and record it, rather than silently picking one.

## CONFLICT-004 — Client archetype count and naming drift across 3 enumeration passes
- **source_A:** Page 9, narrative form, 3 archetypes (NPD Innovator, Middleman/Reseller, Overburdened SME) —
  no Crowdfunder or Institutional archetype mentioned here.
- **source_B:** Pages 7 and 11-12, list form, 5 archetypes each (adds Funded Crowdfunders and Government/
  Institutional Contractors) — but the two 5-item lists themselves use different wording per item (truncated
  in source, so full reconciliation is not possible from the extraction alone).
- **context_A:** Page 9 is part of the "IECHM Global Lead Source & Strategic Acquisition Blueprint" — the
  user's explicitly-scoped "data alone... blueprint" deliverable (see REQ-000012 / conflicts around scope).
- **context_B:** Pages 7 and 11-12 are both AI-generated SYSTEM PROMPT drafts meant to be fed to another LLM
  instance, produced before and independent of page 9's blueprint.
- **possible_reason:** The 3-archetype version (page 9) may be a deliberately simplified subset for the
  blueprint narrative, while the 5-archetype versions are the "complete" taxonomy meant for the executable
  system prompts — but the source never states this explicitly; it could equally be an oversight/omission.
- **resolution_status:** UNRESOLVED.

## CONFLICT-005 — Composition breakdown (page 19) introduces buyer-intent categories not present in any client-archetype list
- **source_A:** The 3-archetype (page 9) and two 5-archetype (pages 7, 11-12) client archetype lists — see
  CONFLICT-004.
- **source_B:** Page 19 "Composition of the Firehose" — introduces "Component & Part Sourcing (Build-to-
  Print)" (20%) and "Tooling & Injection Mold Fabrication" (12%) as distinct buyer-intent categories with no
  corresponding named client archetype, and omits "Institutional/Government" entirely from the composition.
- **context_A / context_B:** source_B is a direct response to the scope-broadening user requirement (page 19)
  that explicitly asked to include middlemen/importers across all manufacturing types.
- **possible_reason:** The composition breakdown may describe REQUEST TYPES rather than BUYER ARCHETYPES (a
  different axis entirely — one buyer archetype could generate multiple request types), but the source doesn't
  explicitly draw this distinction.
- **resolution_status:** UNRESOLVED. Step 1+ should consider whether "buyer archetype" and "request type"
  need to be modeled as two separate, cross-referenced dimensions rather than one flat taxonomy.

## CONFLICT-006 — Layer 1 LLM-qualification rate: 1.5% vs. ~2%
- **source_A:** Page 17-18, TABLE-007/008: "Top 1.5% pass IECHM capability thresholds," applied to the
  450,000/month (15,000/day) basis, yielding 6,750 MQL/month.
- **source_B:** Page 20, 27: "Layer 1 ... passes the top 2% (2,000 leads)" out of the post-Layer-0 100,000
  leads (2,000,000/day basis), and restated on page 27 as "Identifies Top 2% - 5% Qualified -> 2,000 - 5,000
  Bids."
- **context_A / context_B:** Different lead-volume bases (see CONFLICT-001), and arguably different funnel
  stages being described (source_A's 1.5% is against the FULL raw pool; source_B's 2% is against the
  POST-LAYER-0 pool, which is itself only 5% of the full raw pool) — so these may not be directly comparable
  rates even though both are described similarly ("top X% qualified").
- **possible_reason:** Genuinely different filtering-stage definitions across the two architecture-scope eras
  of the document (pre- and post- Layer 0 introduction).
- **resolution_status:** UNRESOLVED — flagged specifically because a naive reader could conflate these two
  percentages as the same rate when they are not defined against the same denominator.

## CONFLICT-007 — Scope statement: "blueprint only, not the agent" (page 8) vs. "give me full prompt for building the ai system" (page 25)
- **source_A:** Page 8, user: "this is like the blueprints not the actual agent just the blueprint."
- **source_B:** Page 25, user: "give me full prompt for building the ai system with all the conversation we
  had for building the system."
- **context_A:** Early in the conversation, scoping the IECHM capability/lead-taxonomy blueprint specifically.
- **context_B:** Much later, after multiple rounds of adding agent architecture, sentinel/failover design, and
  hardware integration — the user's own request has evolved to explicitly ask for a buildable system prompt.
- **possible_reason:** Natural evolution of the user's ask over an 18-turn conversation; not necessarily a
  true logical conflict, but the source never states "the earlier data-only scope constraint no longer
  applies" — it is implicitly superseded by usage rather than explicitly retracted.
- **resolution_status:** PARTIALLY RESOLVED BY IMPLICATION (the later, more specific and more recent request
  functionally supersedes the earlier scope constraint), but NOT explicitly resolved in the source text
  itself. Recorded here per the no-silent-resolution rule; Step 0 does not resolve this on the user's behalf —
  the user (in the current, separate IECHM-LIOS Step 0 instructions) has again constrained the very first
  build step to "specification only, do not implement," which is consistent with treating CONFLICT-007's
  page-8 constraint as still relevant guidance rather than moot.
