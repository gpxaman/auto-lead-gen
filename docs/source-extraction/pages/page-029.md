---
page: 29
document: "Autonomous Freelance Agent Factory Architecture.pdf"
pdf_footer: "8/25/26, 5:26 PM — Autonomous Freelance Agent Factory Architecture — https://gemini.google.com/app/f8dc46d6099d59ae?hl=en-IN — 29/29"
---

## Response (continued from Page 28 — final page, Master System Prompt v2 concludes)

### 1. Unified Lead Entity Schema (Pydantic / JSON)

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
      "enum": ["NPD_INNOVATOR", "MIDDLEMAN_OEM_RESIGN", "SME_ENGINEERING_OVERFLOW", "CROWDFUNDER_FUNDED", "GOVERNMEN[truncated in source render — enum list is cut off; at least one more value beginning 'GOVERNMEN...' (likely GOVERNMENT/GOVERNMENTAL/INSTITUTIONAL) is not fully visible in the PDF render]"]
    },
    "source_metadata": {
      "type": "object",
      "required": ["macro_channel", "platform_name", "sub_domain", "listing_url"],
      "properties": {
        "macro_channel": { "type": "string", "enum": ["FREELANCE", "B2B_TRADE", "COMMUNITY", "BROKERAGE", "OUTBOUND_[truncated in source render]"] },
        "platform_name": { "type": "string" },
        "sub_domain": { "type": "string" },
        "listing_url": { "type": "string", "format": "uri" }
      }
    },
    "technical_specifications": {
      "type": "object",
      "required": ["domain", "cad_software", "materials_requested", "bounding_box_mm"],
      "properties": {
        "domain": { "type": "string", "enum": ["MECHANICAL_CAD", "ELECTRONICS_PCB", "ENCLOSURE", "DFM_TOOLING", "TUR[truncated in source render]"] },
        "cad_software": { "type": "array", "items": { "type": "string" } },
        "materials_requested": { "type": "array", "items": { "type": "string" } },
        "bounding_box_mm": {
          "type": "object",
          "properties": {
            "x": { "type": "number" }, "y": { "type": "number" }, "z": { "type": "number" }
          }
        },
        "file_attachments": { "type": "array", "items": { "type": "string", "format": "uri" } }
      }
    },
    "commercial_assessment": {
      "type": "object",
      "required": ["estimated_market_price_usd", "target_bid_price_usd", "estimated_cogs_usd", "projected_margin_per[truncated in source render]"],
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

### 2. Node Failure & Hot-Swap Telemetry Contract

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

### 12. RUNTIME INSTRUCTIONS

When executing under this prompt:

1. **Never violate the 10% Discount Rule:** Ensure calculated bid prices reflect $0.90 \times P_{\text{market}}$.
2. **Enforce Zero-Tooling Framing:** Always highlight monolithic aluminum capability, zero mold lead times, free DFM audits, and free logo engraving.
3. **Execute Immediate Failovers:** Quarantine any hallucinating worker node immediately upon threshold breach and execute hot-swap replacements seamlessly.

***

### What Makes This Master Prompt Production-Ready

1. **Full-Spectrum Hardware Grounding:** Direct mapping to IECHM's custom 2m × 1m universal direct-metal/IC p[truncated in source render]
2. **Deterministic Mathematical Pricing:** Eliminates arbitrary quote generation by binding proposals to algorithmic[truncated in source render]
3. **Multi-Stage Security & Integrity:** Features Layer 0 deterministic filtering (knocking 2M down to 100k leads), [truncated in source render]
4. **Machine-to-AI Physical Loop:** Directly integrates headless CAD slicing, mass calculation, automated photoreali[truncated in source render]

--- END OF SOURCE DOCUMENT (Page 29 of 29) ---
