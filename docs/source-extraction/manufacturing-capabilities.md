# Extracted Manufacturing / Engineering Capabilities (IECHM Capability Scope)

## From "IECHM Enterprise Capability Profile" (source pages 8-9)

Pipeline diagram (page 8):
```
Ideation & Industrial Design
  → Parametric CAD & Simulation (Fusion 360 / SolidWorks)
  → Electronics Engineering (Schematic, Multi-Layer PCB, Firmware)
  → Rapid Prototyping (Large-Scale Top-Down Additive, SLA, CNC)
  → Tooling & DFM/DFA (Plastic Injection Molding, Sheet Metal, Casting)
  → Global Sourcing, Assembly, Consignment Inspection & Quality Certification
```

**Mechanical & Industrial Design** (page 8-9)
- Parametric 3D solid and surface modeling
- Ergonomic enclosures, complex mechanisms, customized human-interface hardware, mechanical load-bearing structures
- Thermal management, structural simulation (FEA), tolerance stack-up analysis

**Electronics & Embedded Systems** (page 8-9)
- Schematic capture, high-speed multi-layer PCB layout, component selection, BOM optimization
- Optoelectronics, sensor integration, high-polling rate controllers, motor/actuator drivers
- EMC/EMI design, test point layout for AOI/ICT

**Rapid Prototyping & Additive Manufacturing** (page 8-9)
- Large-format additive manufacturing (incl. custom high-volume / 1m³ envelope printing for full-scale mechanical rigs)
- Precision SLA/SLS resin prints for functional snap-fits and visual prototypes
- Soft tooling, urethane vacuum casting, fast-turn CNC machined prototypes

**DFM, Tooling & Volume Manufacturing** (page 9)
- Injection molding engineering (wall thickness analysis, draft angles, core-cavity design, parting lines, gate placement)
- Sheet metal fabrication, stamping, bending, extrusion profiling
- Enclosure finishing (CMF — Color, Material, Finish; SPI/VDI texture standards, anodizing, plating)

**Global Supply Chain & Quality Assurance** (page 9)
- Component verification, alternative parts sourcing, vendor qualification across global supplier networks
- Physical consignment inspection, incoming quality control (IQC), functional verification

## Master Prompt v2 restatement (source pages 25-26, "PHYSICAL INFRASTRUCTURE & HARDWARE CAPABILITIES")
- Parametric CAD (Autodesk Fusion 360, SolidWorks, STEP, IGES, DXF)
- Multi-layer PCB layout & schematic validation (KiCad, Altium Designer, Gerber RS-274X, IPC-2221 compliance)
- Automated DFM/DFA Auditing (wall thickness, draft angles, rib-to-wall ratios, tolerance stack-ups to ±0.0[truncated in source] mm)
- CMF specification, surface texturing (SPI/VDI standards), pre-shipment physical [inspection — truncated in source]

## Manufacturing Domain enum (SCHEMA-001, page 3)
```
CAD_MECHANICAL = "cad_mechanical"
PCB_ELECTRONICS = "pcb_electronics"
ENCLOSURE_DESIGN = "enclosure_design"
PROTOTYPING_3D_PRINT = "prototyping_3d_print"
DFM_INJECTION_MOLDING = "dfm_injection_molding"
SHEET_METAL = "sheet_metal"
FULL_NPD_TURNKEY = "full_npd_turnkey"
```

## `technical_specifications.domain` enum (SCHEMA-005, page 29, truncated)
```
MECHANICAL_CAD, ELECTRONICS_PCB, ENCLOSURE, DFM_TOOLING, TUR[truncated in source — presumably TURNKEY or similar]
```

## Scope-breadth statement (source page 19, user-driven)
User-defined manufacturing scope: "anything which IECHM can manufacture ... every manufacturing except
chemicals and fabrics and foods." AI response operationalizes this as: "plastics, sheet metal, CNC machining,
PCBs, tooling, machinery, consumer electronics, assemblies, and packaging."

## Deterministic blacklist / whitelist tokens (Layer 0, source page 20 and 27)
Blacklist keywords (page 20): "fabric," "wheat," "chemical," "software," "agricultural"
Blacklist categories (page 27, Master v2): "Textiles, Chemicals, Food, Software" (restated), plus blacklist
term list beginning `["apparel", "garment", "se[truncated in source]"` (incomplete array).
Hardware extraction "positive token" whitelist (page 27, truncated): `["CAD", "STEP", "STL", "IGES", "P[truncated in source]"]`.

NOTE (SOURCE_INCOMPLETE): The full blacklist/whitelist token arrays referenced in the Master Prompt v2 Layer 0
directives (page 27) are cut off in the original PDF render and cannot be recovered from the source as given.
Only the fragments quoted above are available.

## Hypothetical "Universal 3D Printer" hardware spec (user-introduced hypothesis — see assumptions.md ASSUMPTION-001)
From Master Prompt v2 Section 2 (source page 26), stated as IECHM's "Proprietary Universal 3D Printing Engine":
- Build Envelope: up to 2000mm × 1000mm × 1000mm monolithic build volume
- Material Compatibility: direct printing using raw, low-cost commodity industrial aluminum wire/feedstock [truncated in source] — also stated to be capable of printing ICs per the original user prompt (page 21)
- Energy Footprint: high-efficiency power envelope, under 5kW average running load
- Tooling & Setup Overhead: $0 tooling cost, $0 mold-cut setup, near-zero variable manual labor
- Self-Replication Capacity: machine firmware, kinematics, and structural components open to internal ma[nufacturing — truncated in source] (i.e., the machine can print its own replacement parts)
