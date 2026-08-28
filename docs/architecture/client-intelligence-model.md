# Client Intelligence Model

Per Step 1 Section 6. Preserves all 3 source client-archetype enumeration passes (see CONFLICT-004) without
pretending they are identical, and defines a conceptual hierarchy that can hold them.

## The 3 preserved source archetype sets

### SOURCE ARCHETYPE SET A — Narrative form, 3 archetypes (SRC-000029, page 9)
1. NPD Innovator / Deep-Tech Startup
2. E-Commerce Brand / Middleman / Sourcing Arbitrageur
3. Overburdened SME / Mid-Market Engineering Team

Each carries full source-derived detail: Profile, Primary Bottleneck, Strategic Angle (see
`docs/source-extraction/client-archetypes.md` Pass 1).

### SOURCE ARCHETYPE SET B — System Prompt Draft 1, 5 archetypes (SRC-000025, page 7)
1. NPD Innovators / Inventors / Hardware Startups
2. E-Commerce / Reseller Middlemen (White-Label / OEM / ODM / Sourcing Arbitrage)
3. Established Enterprise / SME Manufacturers
4. Funded Crowdfunders & Product Launchers
5. Government / Defense / Institutional Contractors

Each item's description is truncated mid-sentence in the source (`[truncated in source]`), so only partial
detail is recoverable (see `docs/source-extraction/client-archetypes.md` Pass 2).

### SOURCE ARCHETYPE SET C — System Prompt Draft 2, 5 archetypes (SRC-000034, pages 11-12)
1. NPD Innovators & Hardware Startups
2. E-Commerce Brand Middlemen & Resellers
3. Overburdened SME / Mid-Market Industrial Teams
4. Funded Crowdfunders
5. Institutional & Public Contractors

Also truncated mid-sentence per item (see `docs/source-extraction/client-archetypes.md` Pass 3). Note Set B
and Set C are NOT verbatim-identical to each other despite covering the same 5 conceptual buyer types —
different wording per item.

**None of the 3 sets is designated canonical by the source.** This document does not pick one; it defines a
STRUCTURE that can hold all 3, plus the enum-vocabulary variants from SCHEMA-002/003/005.

## Conceptual hierarchy (architectural structure — NOT a claim that every level is already source-defined)

```
CLIENT ARCHETYPE FAMILY
    ↓
CLIENT ARCHETYPE
    ↓
CLIENT SUBTYPE
    ↓
BUYER PERSONA
    ↓
BUYING MOTIVATION
    ↓
PAIN POINT
    ↓
BUYING SIGNAL
```

### Level-by-level source coverage

| Level | Source coverage | Status |
|---|---|---|
| CLIENT ARCHETYPE FAMILY | NOT explicitly named by the source as a grouping level above "archetype" — proposed here to hold the 5-conceptual-type union (NPD Innovator, Middleman/Reseller, SME, Crowdfunder, Institutional) as one family, distinct from the "request type" dimension identified in CONFLICT-005 | `PROPOSED_EXTENSION` |
| CLIENT ARCHETYPE | The 3 preserved sets above map to this level directly | `SOURCE-DERIVED` (3 non-identical variants) |
| CLIENT SUBTYPE | Not present in the source at all — e.g., no sub-splitting of "Middleman/Reseller" into "Amazon FBA seller" vs. "wholesale distributor" is ever done formally, though such distinctions appear informally in prose (e.g., page 20's "Amazon/Shopify sellers... importers") | `PROPOSED_EXTENSION` if formalized |
| BUYER PERSONA | Partially present as the "Profile" field in Set A (e.g., "Early-stage founders, patent holders, or funded hardware companies...") | `SOURCE-DERIVED` for Set A only |
| BUYING MOTIVATION | Present in Set A archetype table (Strategic Angle references "core driver": Feasibility / Unit Margin, per the page-9 ASCII diagram) | `SOURCE-DERIVED` for Set A only |
| PAIN POINT | Present in Set A as "Primary Bottleneck" | `SOURCE-DERIVED` for Set A only |
| BUYING SIGNAL | Present informally as "Technical Indicators" in TABLE-003 (Master Lead Source & Strategy Matrix, e.g. "Posts prototype photos asking for DFM advice") — tied to PLATFORM, not cleanly tied to archetype in a 1:1 way | `SOURCE-DERIVED`, but cross-cutting rather than strictly hierarchical |

## Explicit non-claims

- This hierarchy is a proposed ORGANIZING STRUCTURE for Step 2+ data modeling. It is NOT a claim that Sets B
  and C's archetypes have Buying Motivation / Pain Point / Buying Signal detail available — they don't (see
  CONFLICT-004's operational-implications note: only Set A has full per-archetype strategic detail).
- No new archetypes have been invented. Every archetype name above is a verbatim or near-verbatim restatement
  of source text.

## Relationship to CONFLICT-005 (buyer archetype vs. request type)

Per CONFLICT-005, "buyer archetype" (this document) and "manufacturing/request domain" (the `technical
classification`, `ManufacturingDomain` enum, see `docs/source-extraction/manufacturing-capabilities.md`) are
modeled as two SEPARATE, cross-referenced dimensions rather than one flat taxonomy. A given lead record is
expected to carry both a `client_archetype` value (from this document's hierarchy) and a
`manufacturing_domain`/request-type value (from the technical classification), rather than one enum trying to
express both.

## Open item

Which of Set A/B/C (or their union) is canonical for implementation is NOT decided here — see
`docs/architecture/open-decisions.md`.
