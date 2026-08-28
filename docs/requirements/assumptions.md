# Assumption Register

Separates verified source information from assumptions, hypothetical technology, economic estimates, market
estimates, future capabilities, proposed architecture, and illustrative examples. See also
`docs/source-extraction/hardware-assumptions.md` and `docs/source-extraction/economic-scenarios.md` for the
full derivations underlying several of these.

## ASSUMPTION-001 — Universal 3D Printer exists
**Type:** SOURCE_HARDWARE_ASSUMPTION (hypothetical technology).
**Statement:** IECHM possesses a "universal 3D printer" capable of printing a 2m×1m×1m object including
integrated circuits, from raw cheap aluminum feedstock, using only a few kW of power.
**Origin:** User, page 21, explicitly framed as hypothetical: "assume the technology exists."
**Drift flag:** This hedge ("assume... exists") is present only on page 21. From page 23 onward, the
printer is treated as real, unqualified IECHM infrastructure and formally specified in the Master Prompt v2
"PHYSICAL INFRASTRUCTURE & HARDWARE CAPABILITIES" section (page 26) alongside genuinely conventional/real
capabilities (Fusion 360, SolidWorks, KiCad, Altium). **This extraction does NOT silently convert this
assumption into a verified fact** — every requirement or downstream document that depends on the printer
(REQ-000027, the pricing/COGS formulas, the hardware API integration requirements) is flagged as contingent
on ASSUMPTION-001 remaining true.
**Confidence:** LOW / UNVERIFIED. No manufacturing engineering evidence, patent, or technical specification is
provided anywhere in the source beyond the user's one-line description. IC printing via aluminum-feedstock
additive manufacturing is not an established production technology as of the source's stated date context
(August 2026) to the knowledge available to this extraction process — this is noted for the user's awareness,
not asserted as a correction to the source, which is preserved as-is.

## ASSUMPTION-002 — Machine is custom-built from scratch, IP owned by IECHM
**Type:** SOURCE_HARDWARE_ASSUMPTION.
**Statement:** The (hypothetical) universal printer's design, firmware, kinematics, and BOM are wholly owned/
authored by IECHM, not licensed or purchased from a vendor.
**Origin:** User, page 23: "the machine is custom built from scratch."
**Downstream dependents:** Self-replicating factory scaling strategy (page 24), Estimator/Dispatch agent deep
API integration (page 24), IP-moat argument (page 24).
**Confidence:** Explicitly user-asserted, not independently verifiable from the source.

## ASSUMPTION-003 — Raw aluminum price ~$3.15/kg (August 2026)
**Type:** SOURCE_ESTIMATE, externally cited.
**Statement:** "global raw industrial aluminum trades at roughly $3.15 per kg (or about ₹345 per kg on the
MCX)."
**Origin:** AI response, page 21, citing "Aluminium Price Today: MCX Rate, Trends & 2026 Outlook - Sahi" and
"Global price of Aluminum (PALUMUSDM) | FRED | St. Louis Fed" (page 22 sources list).
**Confidence:** MEDIUM — cited to named external sources, but those sources were not independently fetched or
verified as part of this Step 0 extraction. Should be re-verified against live pricing before being used in
any real pricing engine.

## ASSUMPTION-004 — Electricity cost $0.12/kWh
**Type:** SOURCE_ASSUMPTION, uncited.
**Statement:** Appears only inside FORMULA-001 (`C_mfg = (Mass_kg * $3.15) + (kWh * $0.12)`), with no
narrative justification or citation anywhere else in the source.
**Confidence:** LOW — unsourced, single occurrence.

## ASSUMPTION-005 — IECHM's physical facility is in Chennai
**Type:** SOURCE_FACT as asserted by the AI, but never independently confirmed by the user in this
document.
**Statement:** "IECHM is fulfilling from Chennai" (page 20); "keep the high-margin, complex work in-house in
Chennai" (page 21).
**Confidence:** LOW-MEDIUM — this is the ONLY place in the entire 29-page source where IECHM's location is
named, and it originates from the AI's own response rather than a direct user statement. It may be an AI
inference/invention rather than a fact the user provided. Flagged for explicit user confirmation before being
treated as a hard fact in Step 1+.

## ASSUMPTION-006 — All quantitative business projections (agent counts, token burn, cost, revenue, profit)
**Type:** SOURCE_ESTIMATE (illustrative financial/technical modeling), not verified targets, SLAs, or
guarantees.
**Statement:** Every number in `docs/source-extraction/economic-scenarios.md` (SCENARIO-001 through 008) —
including the headline claims of "$1 Million in pure profit every single day" (page 22) and "$26.46 Million"
monthly gross profit (page 22) — is AI-generated illustrative arithmetic produced in direct response to
hypothetical "what if" user questions, built on cascading unverified assumptions (lead volume, conversion
rates, AOV, margin) that are themselves marked SOURCE_ESTIMATE.
**Confidence:** LOW as literal business projections; MEDIUM as illustrations of the architecture's intended
economic logic (pricing rule, funnel structure, cost-control mechanisms). Step 1+ (architecture/requirements)
should treat these as illustrative of INTENDED MECHANISM (e.g., "there should be a Layer 0 pre-filter, a
pricing formula, a conversion funnel") rather than as literal performance targets to design toward.

## ASSUMPTION-007 — "10% Rule" interpretation
**Type:** Interpretive/normalization assumption made by the AI mid-conversation, not independently confirmed
by the user.
**Statement:** See terminology.md "The 10% Rule" entry — the user's literal phrasing ("i dont want to go less
than 10 percentage of the actual market prize") is ambiguous between "at least 10% off" and "exactly 10%
off," and the AI's chosen reading (exactly 10% off, `P_bid = 0.90 × P_market`) is what propagates through the
rest of the document without the user ever explicitly re-confirming that reading.
**Confidence:** MEDIUM — the user never objected to the AI's reformulation in subsequent turns, which is soft
evidence of tacit agreement, but this is not the same as an explicit confirmation.

## ASSUMPTION-008 — Benchmark citations (B2B conversion rates, quote-response-time benchmarks) are accurate and applicable
**Type:** SOURCE_ESTIMATE, externally cited, unverified.
**Statement:** Various 2026 B2B benchmark claims (e.g., "B2B conversion rates 2026: hit 8%," "buyers form
strong preferences within 4 hours of requesting a quote... close at a 35% higher rate") cited to named sources
(NUMRIQ, Vedain CRM, a B2B quote-time benchmark article) — see `docs/source-extraction/references.md`.
**Confidence:** LOW-MEDIUM — none of the cited sources were fetched or fact-checked in this extraction; the
benchmark figures are also being applied to a hypothetical hardware-manufacturing use case that may not match
the cited sources' original study population.
