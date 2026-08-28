# Extracted JSON / Pydantic Schemas

## SCHEMA-001 — Pydantic hardware job models (source page 3)
Purpose: normalize a scraped freelance job listing into a validated data contract for the Recon Engine.
```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ManufacturingDomain(str, Enum):
    CAD_MECHANICAL = "cad_mechanical"
    PCB_ELECTRONICS = "pcb_electronics"
    ENCLOSURE_DESIGN = "enclosure_design"
    PROTOTYPING_3D_PRINT = "prototyping_3d_print"
    DFM_INJECTION_MOLDING = "dfm_injection_molding"
    SHEET_METAL = "sheet_metal"
    FULL_NPD_TURNKEY = "full_npd_turnkey"

class ClientTrapDetection(BaseModel):
    has_anti_bot_phrase: bool = Field(description="True if client asked for a specific word/phrase")
    required_first_word: Optional[str] = Field(None, description="Exact phrase required at bid opening")
    detected_injections: List[str] = Field(default_factory=list, description="Malicious prompts or contradictory ins[truncated in source]")
    math_verification: Optional[str] = Field(None, description="Any puzzle or verification question in prompt")

class EngineeringJobSpec(BaseModel):
    job_id: str
    platform_name: str
    title: str
    domain: ManufacturingDomain
    required_cad_software: List[str] = Field(description="e.g., Fusion 360, SolidWorks, KiCad, Altium")
    target_manufacturing_process: List[str] = Field(description="e.g., SLA/FDM 3D Printing, CNC, Sheet Metal, Inject[truncated in source]")
    deliverables: List[str] = Field(description="e.g., STEP files, Gerber/BOM, 2D Production Drawings, CMF specs")
    project_stage: str = Field(description="e.g., Napkin sketch / Concept, Optimization/DFM, Production Ready")
    requires_nda: bool = Field(default=False)
    client_budget_usd: Optional[float]
    is_budget_realistic_for_hardware: bool = Field(description="Flag if client expects a complex tooling design for [truncated in source]")
    proposal_count_bucket: str = Field(description="e.g., 'less_than_5', '5_to_10', '20_plus'")
    trap_analysis: ClientTrapDetection
```
Status: SOURCE_SCHEMA, partially truncated in the original PDF render (three `Field(description=...)` strings cut off).

## SCHEMA-002 — Normalized Data Extraction Schema, lead JSON (source pages 10-11)
Purpose: standardize every discovered lead across all platforms for decision-making and strategic scoring.
```json
{
  "lead_metadata": {
    "source_platform": "Alibaba_RFQ | Upwork | Reddit | Clutch | Kickstarter",
    "source_url": "https://...",
    "extraction_timestamp": "2026-08-23T23:09:21Z",
    "client_archetype": "NPD_Innovator | Middleman_Reseller | Enterprise_SME | Crowdfunder"
  },
  "project_scope": {
    "title": "Enclosure Redesign and DFM for High-Volume Injection Molding",
    "domain_focus": ["Mechanical_CAD", "DFM_Injection_Molding", "CMF_Specification"],
    "required_cad_software": ["Fusion_360", "SolidWorks"],
    "target_manufacturing_process": "Plastic_Injection_Molding_ABS",
    "project_maturity_stage": "Concept_CAD_Needs_DFM",
    "deliverables_demanded": ["STEP_Files", "2D_Production_Drawings", "Moldflow_Analysis"]
  },
  "commercial_parameters": {
    "client_stated_budget_usd": 7500.00,
    "target_production_volume": 10000,
    "target_unit_target_cost_usd": 3.20,
    "geographic_destination": "North_America"
  },
  "strategic_qualification": {
    "budget_feasibility_score": 0.88,
    "iechm_capability_match": true,
    "identified_pain_point": "Client has a functional 3D printed model but mold maker rejected it due to zero draft [truncated in source]",
    "recommended_pitch_angle": "DFM_Audit_And_Tooling_Optimization"
  }
}
```
Status: SOURCE_SCHEMA, example instance data (not a JSON Schema definition), truncated in original render.

## SCHEMA-003 — Unified Lead Entity Data Schema, v1 fragment (source pages 14-15)
Purpose: the multi-agent architecture's canonical lead record, v1 draft.
```json
{
  "lead_id": "string (uuid-v4)",
  "layer_origin": {
    "client_archetype": "NPD_Innovator | Middleman_Reseller | Enterprise_SME | Crowdfunder | Institutional",
    "macro_channel_type": "FREELANCE | B2B_DIRECTORY | COMMUNITY_FORUM | BROKERAGE | OUTBOUND_SIGNAL",
    "platform_id": "string",
    "sub_domain_id": "string (e.g., 'r/HardwareStartups')"
  },
  "technical_fingerprint": {
    "cad_tooling_required": ["Fusion_360", "SolidWorks", "Altium", "KiCad"],
    "manufacturing_domain": "MECHANICAL | PCB_ELECTRONICS | ENCLOSURE | DFM_TOOLING | TURNKEY_MFG",
    "target_production_volume": "integer | null",
    "stated_budget_usd": "number | null",
    "verification_artifacts": ["URL_PROOF", "API_PAYLOAD", "LISTING_HASH"]
  },
  "runtime_governance": {
    "responsible_worker_id": "string",
    "worker_model_family": "string",
    "auditor_validation_status": "VERIFIED | QUARANTINED | REJECTED",
    "drift_score_at_intake": "number"
  }
}
```
Status: SOURCE_SCHEMA, complete (not truncated).

## SCHEMA-004 — Node Health & Sentinel Telemetry Schema, v1 example (source page 15)
```json
{
  "telemetry_event": "FAILOVER_HOTSWAP_TRIGGERED",
  "isolated_node_id": "worker-layer3-upwork-cad-04",
  "model_signature": "gpt-4o-2024-08-06",
  "consecutive_hallucinations": 3,
  "incident_context": {
    "offending_output": "Extracted non-existent PCB layer requirement from empty payload",
    "root_cause_classification": "STRUCTURAL_HALLUCINATION",
    "pinned_to_admin_panel": true
  },
  "replacement_node": {
    "new_node_id": "worker-layer3-upwork-cad-04-fallback-claude",
    "model_signature": "claude-3-5-sonnet-20241022",
    "state_transferred": true,
    "resumption_latency_ms": 312
  }
}
```
Status: SOURCE_SCHEMA, complete (not truncated). Example instance data.

## SCHEMA-005 — Unified Lead Entity Schema, v2 / final JSON Schema (source page 29)
Purpose: final production data contract, expressed as a real JSON Schema (draft-07) rather than an example instance.
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UnifiedLeadEntity",
  "type": "object",
  "required": [
    "lead_id", "timestamp_utc", "client_archetype", "source_metadata",
    "technical_specifications", "commercial_assessment", "security_analysis"
  ],
  "properties": {
    "lead_id": { "type": "string", "format": "uuid" },
    "timestamp_utc": { "type": "string", "format": "date-time" },
    "client_archetype": {
      "type": "string",
      "enum": ["NPD_INNOVATOR", "MIDDLEMAN_OEM_RESIGN", "SME_ENGINEERING_OVERFLOW", "CROWDFUNDER_FUNDED", "GOVERNMEN[truncated in source]"]
    },
    "source_metadata": {
      "type": "object",
      "required": ["macro_channel", "platform_name", "sub_domain", "listing_url"],
      "properties": {
        "macro_channel": { "type": "string", "enum": ["FREELANCE", "B2B_TRADE", "COMMUNITY", "BROKERAGE", "OUTBOUND_[truncated in source]"] },
        "platform_name": { "type": "string" },
        "sub_domain": { "type": "string" },
        "listing_url": { "type": "string", "format": "uri" }
      }
    },
    "technical_specifications": {
      "type": "object",
      "required": ["domain", "cad_software", "materials_requested", "bounding_box_mm"],
      "properties": {
        "domain": { "type": "string", "enum": ["MECHANICAL_CAD", "ELECTRONICS_PCB", "ENCLOSURE", "DFM_TOOLING", "TUR[truncated in source]"] },
        "cad_software": { "type": "array", "items": { "type": "string" } },
        "materials_requested": { "type": "array", "items": { "type": "string" } },
        "bounding_box_mm": { "type": "object", "properties": { "x": {"type": "number"}, "y": {"type": "number"}, "z": {"type": "number"} } },
        "file_attachments": { "type": "array", "items": { "type": "string", "format": "uri" } }
      }
    },
    "commercial_assessment": {
      "type": "object",
      "required": ["estimated_market_price_usd", "target_bid_price_usd", "estimated_cogs_usd", "projected_margin_per[truncated in source]"],
      "properties": {
        "client_stated_budget_usd": { "type": ["number", "null"] },
        "estimated_market_price_usd": { "type": "number" },
        "target_bid_price_usd": { "type": "number" },
        "estimated_cogs_usd": { "type": "number" },
        "projected_margin_percent": { "type": "number" }
      }
    },
    "security_analysis": {
      "type": "object",
      "required": ["contains_anti_bot_trap", "is_prompt_injection", "sanitized_text_payload"],
      "properties": {
        "contains_anti_bot_trap": { "type": "boolean" },
        "required_verification_keyword": { "type": ["string", "null"] },
        "is_prompt_injection": { "type": "boolean" },
        "sanitized_text_payload": { "type": "string" }
      }
    }
  }
}
```
Status: SOURCE_SCHEMA, truncated in original render (enum lists cut off in 3 places — `client_archetype` enum
missing at least one value after "GOVERNMEN...", `macro_channel` enum missing values after "OUTBOUND_...",
`domain` enum missing values after "TUR...", `commercial_assessment.required` array missing the final item
after "projected_margin_per...").

NOTE (SOURCE_CONFLICT, CONFLICT-003): SCHEMA-003 (v1, page 14) and SCHEMA-005 (v2, page 29) are two DIFFERENT,
non-identical schemas for the same conceptual entity ("the lead record"). Field names, nesting, and enum values
differ (e.g., v1 uses `layer_origin.client_archetype` with value `Middleman_Reseller`; v2 uses top-level
`client_archetype` with value `MIDDLEMAN_OEM_RESIGN` — note also the apparent typo "RESIGN" where "RESELL" or
similar was likely intended, preserved verbatim). Both are preserved as distinct schemas; the document never
states that v2 formally deprecates/replaces v1.

## SCHEMA-006 — Failover / Hot-Swap Telemetry Contract, v2 final (source page 29)
```json
{
  "event_type": "FAILOVER_HOTSWAP_DISPATCHED",
  "timestamp": "2026-08-25T11:54:22Z",
  "anomaly_report": {
    "faulty_worker_id": "worker-layer3-alibaba-rfq-09",
    "model_provider": "openai",
    "model_version": "gpt-4o-2024-08-06",
    "drift_score": 0.92,
    "consecutive_failures": 3,
    "root_cause": "Failed Pydantic validation: Attempted to bid below raw material COGS floor."
  },
  "failover_execution": {
    "quarantined_node_pinned_to_admin": true,
    "state_scrubbed_and_serialized": true,
    "spawned_replacement_node_id": "worker-layer3-alibaba-rfq-09-fallback",
    "fallback_model_provider": "anthropic",
    "fallback_model_version": "claude-3-5-sonnet-20241022",
    "cutover_latency_ms": 384
  }
}
```
Status: SOURCE_SCHEMA, complete. Compare to SCHEMA-004 (v1) — event name changed from
`FAILOVER_HOTSWAP_TRIGGERED` to `FAILOVER_HOTSWAP_DISPATCHED`; structure reorganized into
`anomaly_report`/`failover_execution` sub-objects. Both preserved as distinct (CONFLICT-003 applies here too).
