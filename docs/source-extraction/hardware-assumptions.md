# Extracted Hardware Assumptions

## ASSUMPTION-001 — The "Universal 3D Printer" (source pages 21-29)
Status: **SOURCE_HARDWARE_ASSUMPTION**, explicitly introduced by the user as hypothetical.

Verbatim user framing (page 21): "my production is essintaly a universal 3d printer which can even ic and it
only reqquries few kw for 2 meter into 1 meter and the absolute raw materials like raw cheapest form of
alluminium to print and **assume the technology exists** only think about the actual proift and the metric i
aske d" [sic, preserved verbatim].

The AI response explicitly frames this as a hypothesis throughout: "To calculate the exact sales and profit
under **your hypothetical scenario**..." (page 21) and "If **you truly have** a universal 3D printer..."
(page 22).

**This assumption is never walked back or re-qualified as hypothetical again after page 23** — from page 23
onward ("the machine is custom built from scratch") through the final Master Prompt v2 (pages 26-29), the
universal printer is treated as IECHM's actual proprietary production infrastructure and formally specified
as a firm capability under "PHYSICAL INFRASTRUCTURE & HARDWARE CAPABILITIES" (page 26). This is flagged as a
notable drift from hypothesis to unqualified architectural premise, without an explicit statement in the
source confirming the technology is real. See `docs/requirements/assumptions.md` for the requirements-level
treatment of this.

Specification as eventually formalized in Master Prompt v2 (page 26):
- Build Envelope: up to 2000mm × 1000mm × 1000mm monolithic build volume
- Material Compatibility: raw, low-cost commodity industrial aluminum wire/feedstock [+ IC printing capability per the original page-21 user prompt, not repeated verbatim in the page-26 spec text as extracted]
- Energy Footprint: under 5kW average running load
- Tooling & Setup Overhead: $0 tooling, $0 mold-cut setup, near-zero variable labor
- Self-Replication Capacity: firmware/kinematics/structural components open to internal manufacturing (i.e., can print its own spare/replacement parts)

## ASSUMPTION-002 — Machine built from scratch / IP ownership (source page 23)
Verbatim user statement: "the machine is custom built from scratch." AI response treats this as eliminating
CapEx as a scaling constraint and as the basis for: (a) self-replicating factory scaling (Printer A prints
parts for Printer B/C/D), (b) deep firmware-level API integration (Estimator/Dispatch agents), (c) an IP moat
argument (immune to proprietary metal-powder/license vendor lock-in).

## ASSUMPTION-003 — Raw material pricing (source page 21)
"In August 2026, global raw industrial aluminum trades at roughly $3.15 per kg (or about ₹345 per kg on the
MCX)." Cited to two sources (page 22): "Aluminium Price Today: MCX Rate, Trends & 2026 Outlook - Sahi" and
"Global price of Aluminum (PALUMUSDM) | FRED | St. Louis Fed." Status: SOURCE_ESTIMATE with cited external
sources (sources not independently re-verified by this extraction).

## ASSUMPTION-004 — Electricity cost (source page 27, formula only)
`$0.12` per kWh appears only inside FORMULA-001 (`C_mfg = (Mass_kg * $3.15) + (kWh * $0.12)`) with no
narrative statement or citation elsewhere in the source justifying this figure. Status: SOURCE_ASSUMPTION,
uncited, embedded in a formula only.

## ASSUMPTION-005 — IECHM's physical facility location (source page 20-21)
"IECHM is fulfilling from Chennai" (page 20, in the Layer 0 location-routing example) and "keep the high-
margin, complex work in-house in Chennai" (page 21). This is the only explicit statement of IECHM's physical
location anywhere in the source. Status: SOURCE_FACT (as asserted by the AI response, not independently
verifiable, and not stated by the user directly — the user never names Chennai in this document; it is the
AI's own inference/invention). Flagged for verification.

## ASSUMPTION-006 — "Assume the technology exists" instruction scope (source page 21)
The user's explicit instruction "assume the technology exists" is a scoping directive for a hypothetical
financial-modeling exercise, not a claim that IECHM currently possesses this technology. This distinction is
preserved rather than collapsed, since later architecture documents (Master Prompt v2) do NOT preserve this
hedge and present the printer as a real, existing capability without qualification.
