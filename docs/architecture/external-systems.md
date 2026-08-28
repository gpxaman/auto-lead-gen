# External Systems

Per Step 1 Section 33. Categorizes every external system referenced or implied by the source. No vendor is
invented where the source doesn't name one — those are marked `UNSPECIFIED`.

## LEAD SOURCES
Source IDs: `docs/source-extraction/platforms.md` (46 named platforms across 8 categories — Upwork, Alibaba,
Reddit, Clutch, Kickstarter, etc.). Purpose: raw lead/RFQ content. Dependency: read-only, external, not
controlled by IECHM-LIOS. Data exchanged: scraped HTML/text (inbound only). Security boundary: fully
untrusted (per `security.md`). Status: `SOURCE-DERIVED`, concrete vendor names given by source.

## AI/MODEL PROVIDERS
Source IDs: pages 3-4, 15-17, 26, 29. Named examples: OpenAI (`gpt-4o`, `gpt-4o-mini`, `GPT-4.1 Nano`),
Anthropic (`claude-3-5-sonnet-20241022`, "Claude 3 Haiku"). Purpose: LLM inference for classification/
generation agents. Dependency: hard dependency for every AI-classified subsystem. Data exchanged: prompts out,
completions in — includes potentially sensitive scraped lead content, a privacy/data-handling consideration
the source never addresses. Security boundary: outbound API calls, credential-protected. Status:
`SOURCE-DERIVED` as illustrative examples, `UNSPECIFIED` as a committed vendor choice (the source names
multiple providers interchangeably for cost-illustration purposes, never commits to one).

## STORAGE
Source IDs: page 16, "Vector Database (Pinecone / Weaviate)"; implied relational/document storage for the
lead/client/platform registries (never named). Purpose: persist all Data Domains (`data-domains.md`).
Dependency: hard dependency. Status: `SOURCE-DERIVED` for vector storage examples (Pinecone/Weaviate named
as illustrative options, not committed); `UNSPECIFIED` for primary structured-data storage — the source never
names a database technology for the lead/client/platform registries at all.

## SEARCH
Not concretely named by source beyond "Search Query Automation" as a generic Recon Engine extraction-tooling
category (page 7's Tier 5). Status: `UNSPECIFIED`.

## MARKET DATA
Source IDs: page 21-22, aluminum pricing cited to "Aluminium Price Today: MCX Rate, Trends & 2026 Outlook -
Sahi" and "Global price of Aluminum (PALUMUSDM) | FRED | St. Louis Fed" (`references.md`). Purpose: raw
material pricing for System C's COGS formula (FORMULA-001) — out of IECHM-LIOS scope, referenced only.
Status: `SOURCE-DERIVED` (named sources), not independently verified (ASSUMPTION-003).

## CAD/ENGINEERING TOOLS
Source IDs: throughout — Fusion 360, SolidWorks, KiCad, Altium Designer, STEP/IGES/DXF, Gerber RS-274X.
Purpose: named as REQUIREMENTS a lead may specify (classification data), not tools IECHM-LIOS itself
operates. Status: `SOURCE-DERIVED`, reference/classification data only.

## MANUFACTURING SYSTEMS
Source IDs: Xometry, Hubs, Protolabs Network, MacroFab, Fictiv (`platforms.md`, On-Demand Mfg Networks
category). Purpose: BOTH a lead-source category (platforms IECHM-LIOS could monitor for RFQs) AND a pricing-
comparison benchmark (page 21's Xometry/Fictiv cost comparison). Status: `SOURCE-DERIVED`.

## MACHINE SYSTEMS
Source IDs: the (hypothetical) Universal 3D Printer and its firmware/kinematics/Cloud Slicer Engine (pages
21-29). Purpose: System C execution — out of IECHM-LIOS scope entirely; `INTERFACE_UNDEFINED` per
`system-boundaries.md`. Status: `SOURCE_HARDWARE_ASSUMPTION`, contingent on ASSUMPTION-001/002.

## CRM
Not named by source at all. Status: `UNSPECIFIED` — no CRM system is referenced anywhere in the source, even
though the source's own "Account Retention & Automated Re-Order Engine" (System B, SRC-000069) is
functionally CRM-adjacent. This is a genuine gap: the source never says what system tracks client
relationships/delivery history over time.

## FUTURE BIDDING SYSTEM
= System B, per `system-boundaries.md`. Source IDs: SRC-000002 and throughout. Purpose: consumes IECHM-LIOS's
report/strategy output. Status: `SOURCE-DERIVED` (existence), `INTERFACE_UNDEFINED` (contract).

## FUTURE EXECUTION SYSTEM
= System C, per `system-boundaries.md`. Source IDs: pages 21-29. Purpose: manufacturing execution, reached
only via System B, not directly by IECHM-LIOS. Status: `SOURCE_HARDWARE_ASSUMPTION`, `INTERFACE_UNDEFINED`.

## Scraping/automation infrastructure (not in the Step 1 category list, but named heavily by source — recorded here for completeness)
Playwright, Firecrawl, BrightData, Browserbase (all named as illustrative examples, pages 2-4, 16). Status:
`SOURCE-DERIVED` as examples, `UNSPECIFIED` as a committed choice.

## Summary of `UNSPECIFIED` items (no vendor invented)
Primary structured-data storage technology; search infrastructure; CRM system; committed AI model provider;
committed scraping infrastructure provider; committed vector-database provider. All of these require a
real decision in a future step — see `open-decisions.md`.
