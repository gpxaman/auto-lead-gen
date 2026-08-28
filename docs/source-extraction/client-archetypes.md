# Extracted Client Archetypes

The source defines client archetypes with meaningful DRIFT between three separate enumeration passes. All
three are preserved distinctly — later passes are not treated as corrections of earlier ones since the
document never explicitly says so.

## Pass 1 — Page 9 ("Client Archetypes & Tactical Positioning"), 3 archetypes, narrative form
| ID | Name | Profile | Primary Bottleneck | Strategic Angle |
|---|---|---|---|---|
| ARCH-A | NPD Innovator / Deep-Tech Startup | Early-stage founders, patent holders, funded hardware cos with unrefined concept/non-manufacturable prototype | Bridging POC → production-ready engineering package | Sell de-risking + turnkey delivery; DFM reviews, BOM cost reduction, functional prototyping milestones |
| ARCH-B | E-Commerce Brand / Middleman / Sourcing Arbitrageur | Amazon/Shopify brands, wholesale resellers, private-label distributors buying stock products from trade directories | Product differentiation, high defect rates, fragile enclosures, excessive landed costs | Sell customization, cost-down engineering (VAVE), quality assurance; enclosure redesign, mold optimization, pre-shipment inspection |
| ARCH-C | Overburdened SME / Mid-Market Engineering Team | Established industrial machinery/IoT/consumer appliance cos with internal engineering bandwidth constraints | Delayed roadmaps; needs specialized PCB routing, thermal analysis, quick-turn DFM | Sell immediate execution + plug-and-play bandwidth; native + standard exchange formats, zero onboarding friction |

## Pass 2 — Page 7 (System Prompt Draft 1, Tier 1), 5 archetypes, list form (each item truncated in source)
1. NPD Innovators / Inventors / Hardware Startups — "Creators building original products needing end-to-end CAD, P[truncated in source]"
2. E-Commerce / Reseller Middlemen (White-Label / OEM / ODM / Sourcing Arbitrage) — "Sellers looking to source, cu[truncated in source]"
3. Established Enterprise / SME Manufacturers — "Companies seeking fractional engineering bandwidth, specialized P[truncated in source]"
4. Funded Crowdfunders & Product Launchers — "Teams that raised capital on Kickstarter/Indiegogo with non-manufact[truncated in source]"
5. Government / Defense / Institutional Contractors — "Entities requiring strict-spec fabrication, rapid prototypi[truncated in source]"

## Pass 3 — Page 11-12 (System Prompt Draft 2, Layer 1), 5 archetypes, list form (each item truncated in source)
1. NPD Innovators & Hardware Startups — "Raw concepts, un-manufacturable prototypes, seed-funded ventures"
2. E-Commerce Brand Middlemen & Resellers — "White-label/OEM/ODM sourcing, catalog redesigns, tool modifications, [truncated in source]"
3. Overburdened SME / Mid-Market Industrial Teams — "Fractional engineering bandwidth, PCB layout overflow, DFM/DF[truncated in source]"
4. Funded Crowdfunders — "Kickstarter/Indiegogo campaigns facing manufacturing delays or tooling roadblocks"
5. Institutional & Public Contractors — "Formal technical tender seekers, rapid custom fixtures"

## Enum form — SCHEMA-002/003/005 (`client_archetype` field), 3 forms across schema versions
- SCHEMA-002 (page 10-11): `NPD_Innovator | Middleman_Reseller | Enterprise_SME | Crowdfunder`  (4 values, no institutional/government value)
- SCHEMA-003 (page 14): `NPD_Innovator | Middleman_Reseller | Enterprise_SME | Crowdfunder | Institutional`  (5 values)
- SCHEMA-005 (page 29): `NPD_INNOVATOR | MIDDLEMAN_OEM_RESIGN | SME_ENGINEERING_OVERFLOW | CROWDFUNDER_FUNDED | GOVERNMEN[truncated]`  (SCREAMING_SNAKE_CASE, different value names, list itself cut off in source — at least 4 values visible, likely a 5th)

NOTE (SOURCE_CONFLICT, CONFLICT-004): Three distinct enum vocabularies exist for what is conceptually the
same field across the document's lifetime (`NPD_Innovator` vs `NPD_INNOVATOR`; `Middleman_Reseller` vs
`MIDDLEMAN_OEM_RESIGN`; `Enterprise_SME` vs `SME_ENGINEERING_OVERFLOW`; `Crowdfunder` vs `CROWDFUNDER_FUNDED`;
`Institutional` vs `GOVERNMEN[...]`). None are declared canonical. All three preserved verbatim.

## Later composition-based archetype restatement — Page 19 ("Composition of the Firehose")
This is NOT phrased as a client-archetype list but as a % breakdown of what buyers in the expanded 1.5M-2.5M/day
firehose are requesting. Cross-referenced here because it re-derives archetype-like buyer intents:
- 60% — E-Commerce / Middleman Customization (OEM/ODM & White-Label) → maps to ARCH-B
- 20% — Component & Part Sourcing (Build-to-Print) → new intent not cleanly mapped to Pass 1-3 archetypes
- 12% — Tooling & Injection Mold Fabrication → new intent not cleanly mapped to Pass 1-3 archetypes
- 5% — PCB & Electronics Assembly (PCBA) → new intent not cleanly mapped to Pass 1-3 archetypes
- 3% — True Turnkey NPD (Napkin Sketch to Prototype) → maps to ARCH-A

NOTE (SOURCE_CONFLICT, CONFLICT-005): The page-19 composition breakdown introduces two new buyer-intent
categories ("Component & Part Sourcing / Build-to-Print" and "Tooling & Injection Mold Fabrication") that do
not correspond to any of the 5 named archetypes in Pass 2/3, and does not mention the Institutional/Government
archetype at all. This is preserved as a distinct, non-reconciled breakdown.
