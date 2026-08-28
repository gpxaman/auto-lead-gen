# Hardware / Manufacturing Boundary

Per Step 1 Section 28. Preserves every source concept involving physical manufacturing, and clearly
distinguishes INTELLIGENCE (System A / IECHM-LIOS) from EXECUTION (System C). No physical machine control is
implemented.

## Source manufacturing concepts, preserved

CAD, PCB, enclosures, 3D printing, DFM, injection molding, sheet metal, tooling, PCBA, build-to-print, OEM,
ODM, private label, turnkey NPD, materials, machines, slicing, machine APIs, production, re-orders — the full
catalogue is in `docs/source-extraction/manufacturing-capabilities.md` (Step 0) and is not repeated here
verbatim; this document adds the INTELLIGENCE/EXECUTION boundary analysis Step 1 requires.

## INTELLIGENCE vs. EXECUTION, explicitly separated

| Concern | INTELLIGENCE (System A / IECHM-LIOS — IN SCOPE) | EXECUTION (System C — OUT OF SCOPE) |
|---|---|---|
| CAD/PCB requirements | Classify which CAD tools/formats a LEAD is asking for (`ManufacturingDomain`, SCHEMA-001) | Actually producing CAD files or PCB layouts |
| DFM/tooling | Recognize that a lead needs DFM auditing / mold tooling as a service category | Performing the DFM audit or cutting the mold |
| 3D printing / the Universal Printer | Recognize a lead's stated manufacturing-process preference | Operating the (hypothetical) printer, slicing files, running the print job |
| Materials | Record a lead's stated material requirements as classification data | Sourcing/consuming actual raw material (aluminum, etc.) |
| Machine APIs / slicing | **NONE** — IECHM-LIOS has no interface to any machine API per `system-boundaries.md` (`INTERFACE_UNDEFINED` between System A and C) | Cloud Slicer Engine, G-code queue, machine firmware (SRC-000076) |
| Production / re-orders | Could, in principle, supply the ORIGINAL lead intelligence that informs a future re-order opportunity (a new lead-like signal) | Executing the re-order (System B's Day-25 trigger, SRC-000069) and manufacturing it (System C) |
| OEM/ODM/private-label/build-to-print | Classify a lead's request TYPE as one of these categories (ties into CONFLICT-005's "request type" axis) | Fulfilling the OEM/ODM/private-label order |

## Why this boundary matters specifically for THIS project

Section 28's instruction ("Do not implement physical machine control in Step 1... Define only the
architectural boundary") is not merely process hygiene here — the manufacturing side of the source rests
entirely on ASSUMPTION-001 (the unverified "Universal 3D Printer" hypothesis) and ASSUMPTION-002 (machine
built from scratch). IECHM-LIOS's architecture must NOT be built in a way that silently assumes this hardware
is real or available. By keeping Manufacturing Intelligence classification (a legitimate, hardware-agnostic
data-modeling task — "this lead wants injection molding" is true or false regardless of whether IECHM
actually owns a molding machine) strictly separate from Manufacturing Execution (which is entirely contingent
on the hardware assumption), IECHM-LIOS remains buildable and useful even if ASSUMPTION-001/002 turn out to be
false, aspirational, or simply not yet realized.

## Status

Every classification concept in the INTELLIGENCE column is `SOURCE-DERIVED`. Every execution concept in the
EXECUTION column is `HISTORICAL_ONLY` for IECHM-LIOS purposes (documented for interface-awareness, per
`source-concept-mapping.md`, not built here). No manufacturing execution, machine control, or slicing logic
is implemented in this repository at Step 1 (Section 42's explicit prohibition, doubly applicable here given
the additional hardware-assumption caveat).
