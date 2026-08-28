# API Boundaries — Conceptual Only

Per Step 1 Section 34. Defines conceptual API boundaries between internal subsystems and toward external
systems. No production API is implemented; no detailed payload is invented beyond what source schemas
already specify.

## Conceptual internal boundaries

| Boundary | Direction | Payload basis | Status |
|---|---|---|---|
| Ingestion → Intelligence | Raw payload → classification input | Implied by pipeline stages (`data-flow.md`) | `INTERFACE_UNDEFINED` for exact payload shape; stage existence `SOURCE-DERIVED` |
| Intelligence → Platform Research | Classified lead → platform-profile update trigger | Implied | `INTERFACE_UNDEFINED` |
| Platform Research → Agent Orchestration | Spawn/retire decisions | THRESH-001/002 | `SOURCE-DERIVED` for trigger LOGIC, `INTERFACE_UNDEFINED` for the actual API call shape |
| Agent Orchestration ↔ Evidence | Claims requiring evidence attachment | SRC-000034 | `INTERFACE_UNDEFINED` |
| Agent Orchestration ↔ Sentinels | Output submitted for validation | SRC-000039 | `INTERFACE_UNDEFINED` for exact call shape; validation CONTENT (schema/URL/numeric checks) is `SOURCE-DERIVED` |
| Sentinels → Strategy (via Telemetry) | Health/drift signals informing prioritization | Implied | `INTERFACE_UNDEFINED` |
| Intelligence → Future Bidding System (System B) | Report/strategy artifact | SRC-000002 | `INTERFACE_UNDEFINED` — **the single most consequential undefined boundary in the entire architecture**, since it is IECHM-LIOS's actual reason for existing (per `system-boundaries.md`) |
| Future Bidding System → Future Manufacturing System (System B → C) | Contract-signed event, G-code | SRC-000076 | Partially defined: `EVENT_CONTRACT_SIGNED` exists as a named trigger, but payload is `INTERFACE_UNDEFINED` |
| Admin/Control Plane → all subsystems | Pause/drain/quarantine/config commands | `agent-control-plane.md` | `INTERFACE_UNDEFINED`, operations LIST is `SOURCE-DERIVED`/`PROPOSED_EXTENSION` per that document |

## Why the Intelligence → System B boundary deserves special attention

Every other undefined interface in this document is an INTERNAL implementation detail that can be resolved
incrementally without external commitments. The Intelligence → System B boundary is different: it is
IECHM-LIOS's entire OUTPUT CONTRACT — what "done" looks like for this project. The source gives three
candidate shapes for what this could be (SCHEMA-002, SCHEMA-003, SCHEMA-005 — see `schema-versioning.md`),
but never states which one (if any) is what should actually be hand to System B, nor the delivery mechanism
(push API, shared database read access, scheduled file export, etc.), nor the update cadence (real-time
per-lead, batched daily digest, on-demand query). **This is flagged as the highest-priority item in
`open-decisions.md`.**

## What Step 1 explicitly does NOT do here

Per Section 34's explicit instruction: "Do NOT create production API implementations. Do NOT invent detailed
payloads unless directly supported by source schemas." Where a source schema DOES exist (e.g., for the
Intelligence → System B lead record itself), THAT schema's fields are the closest thing to a defined payload
— but even then, the TRANSPORT/PROTOCOL/CADENCE around it remains `INTERFACE_UNDEFINED`, and no REST/gRPC/
GraphQL endpoint design, authentication scheme, or versioning-header convention is proposed here.

## Full undefined-interface inventory

Consolidated from every document above: this list is authoritative for what future implementation work must
resolve before the system can actually connect its parts end-to-end:
1. Intelligence → System B output contract (schema version + transport + cadence)
2. System B → System C contract (payload for `EVENT_CONTRACT_SIGNED`, Estimator/Dispatch integration)
3. Every internal subsystem-to-subsystem call shape (all `PROPOSED_EVENT` payloads in `events.md` are named
   but not typed beyond a "payload concept" one-liner)
4. Admin/Control Plane command API
5. External LEAD SOURCE / AI PROVIDER / STORAGE integration contracts (`external-systems.md`'s `UNSPECIFIED`
   vendor list)
