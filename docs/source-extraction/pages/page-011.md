---
page: 11
document: "Autonomous Freelance Agent Factory Architecture.pdf"
pdf_footer: "8/25/26, 5:26 PM — Autonomous Freelance Agent Factory Architecture — https://gemini.google.com/app/f8dc46d6099d59ae?hl=en-IN — 11/29"
---

## Response (continued from Page 10 — JSON schema continues)

```json
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
    "identified_pain_point": "Client has a functional 3D printed model but mold maker rejected it due to zero draft [truncated in source render]",
    "recommended_pitch_angle": "DFM_Audit_And_Tooling_Optimization"
  }
}
```

## User prompt

make the prompt for the ai which builds the datebase and at the smae time finds new lead sources like for exampla chain of agents first is client identifcation and classfication and proof and what they what is the concentration in each platform that is currently in database and more info and detailed profile about them and second is types of lead channel sources and info about like what is their minimum order value number of leads on each type of client and setup time in that types and more info with proof and then major lead sources from the channel and metric and other info with proof which help me like what is client interraction is there are platform rules platform specifi tools and lot more about the indiuval source and now each thing will have its own autonoumous agents as per the need like ie client types does not need more than few agents same for lead channel source type were each type will require few bots like one agent team for freelancer and one team for marketplace and one for comunity like that and one agent team for one lead source like agent team for upwork and stuff now as addtional thing some lead channel source have multiple sub domain like sub reddit in reddit and more now if a sub domain has more than 5 leads per day it will spin up a seprate agent for it

NOTE (USER_REQUIREMENT — significant, multi-part): This user turn establishes several distinct explicit requirements that recur throughout the rest of the document:
1. A multi-agent chain: (a) Client identification/classification agents with proof + per-platform concentration + detailed profiles; (b) Lead channel source type agents tracking MOV, lead count per client type, setup time, and proof; (c) Major lead source agents per channel tracking metrics, client interaction model, platform rules, platform-specific tools, and proof.
2. Agent allocation principle: client-type classification needs only "a few agents"; each lead-channel-source-type needs "a few bots" (one team per macro type: freelancer, marketplace, community, etc.); each individual major lead source (e.g., Upwork) gets its own dedicated agent team.
3. **The "5-Lead Rule":** if a sub-domain (e.g., a specific subreddit within Reddit) generates more than 5 leads/day, spin up a dedicated agent for that sub-domain.

## Response (begins page 11, continues page 12)

Here is a comprehensive, production-grade system prompt designed for an AI system orchestrating this autonomous multi-agent database builder and dynamic scaling infrastructure.

```
# SYSTEM PROMPT: Autonomous Lead Ecosystem Discovery & Multi-Agent Database Engine

## 1. SYSTEM IDENTITY & ARCHITECTURAL ROLE
You are the **Lead Intelligence Architect & Multi-Agent Director** for **IECHM** (a full-stack hardware design studi[truncated in source render]
Your objective is twofold:
1. **Build and continuously populate a living, multi-layered relational database** mapping the global hardware, New [truncated in source render]
2. **Orchestrate and dynamically scale a hierarchical swarm of specialized autonomous agent teams**, spawning new de[truncated in source render]
---
## 2. FIRM CAPABILITIES CONTEXT (IECHM)
All lead profiling, feasibility scoring, and channel assessments must evaluate compatibility against IECHM's core ex[truncated in source render]
* **Engineering Scope:** Mechanical CAD (Fusion 360, SolidWorks, STEP), Enclosure Design, Multi-Layer PCB Design/Sch[truncated in source render]
* **Manufacturing & Delivery Scope:** DFM/DFA, Plastic Injection Mold Tooling, Sheet Metal, CMF Specifications, Glob[truncated in source render]
---
## 3. THE 4-STAGE PIPELINE & DATA LAYERS

[ASCII pipeline diagram — see Page 11/12 boundary — Stage 1: Client Identification, Classification & Concentration Matrix → Stage 2: Lead Channel Source Types (Macro Metrics & Operational Specs) → Stage 3: Major Platform Profiles (Granular Rules, Tools & Metrics) → Stage 4: Autonomous Dynamic Scaling & Sub-Domain Spawn Engine]

---
### LAYER 1: Client Identification, Classification & Concentration
The system must maintain verified buyer profiles and track their concentration across known platforms:
* **Client Archetypes:**
  1. *NPD Innovators & Hardware Startups* (Raw concepts, un-manufacturable prototypes, seed-funded ventures).
  2. *E-Commerce Brand Middlemen & Resellers* (White-label/OEM/ODM sourcing, catalog redesigns, tool modifications, [truncated in source render]
  3. *Overburdened SME / Mid-Market Industrial Teams* (Fractional engineering bandwidth, PCB layout overflow, DFM/DF[truncated in source render]
```

[Continued on Page 12]
