# Relationships — IECHM-LIOS Logical Data Model

Per Step 2 Section 48. Conceptual entity relationships (not a physical ER diagram with cardinality-enforced
foreign keys, since no database vendor is chosen — see `open-decisions.md` #7).

## Core lineage chain (every arrow is 1:many unless noted)

```
source_document ──1:many──> source_page ──1:many──> source_item
                                                         │
                                                    (referenced by, many:many)
                                                         ▼
raw_record ──1:many──> lead_version ──many:1──> lead ──many:many──> lead_source ──many:1──> subdomain
                                                                                    ──many:1──> platform
                                                                                    ──many:1──> macro_channel
     │
     └──1:many──> claim ──many:many──> evidence
                     │
                     └──1:many──> verification
                     │
                     └──(trust_level transitions, see integrity-rules.md)
```

## Client domain relationships

```
client_archetype_version (one per source set: A/B/C, or a future canonical union)
        │
        └──1:many──> client_archetype (individual archetype definitions within that set)
                            │
                            └──many:many──> buyer_persona, buying_motivation, pain_point, buying_signal

client ──1:many──> client_classification ──many:1──> client_archetype
                            │
                            └── IS-A claim (client_classification.claim_id references claim)
```

**Non-exclusivity note (Section 9):** a `lead` may link to MULTIPLE `lead_source` rows (cross-posted content);
a `client` may have MULTIPLE `client_classification` rows across DIFFERENT `client_archetype_version`s
simultaneously (e.g., classified under Set A AND Set B independently) — these are not mutually exclusive,
consistent with CONFLICT-004's preserved-not-merged treatment.

## Evidence/claim/verification triangle

```
claim ──many:many──> evidence
  │                      │
  │                 (evidence.verification_status is a DENORMALIZED cache;
  │                  the authoritative record is the verification table below)
  │
  └──1:many──> verification ──many:1──> claim (redundant path for query convenience)

verification.evidence_ids[] ──> evidence (which evidence items this verification attempt actually checked)
```

A `claim` can exist with ZERO evidence (Section 12: "A claim may have zero, one, or multiple evidence items")
— an evidence-less claim simply cannot progress past `UNVERIFIED_CLAIM` trust level (see `integrity-rules.md`
state-transition table — `EVIDENCE_BACKED_CLAIM` requires ≥1 evidence row to exist first).

## Conflict relationships

```
conflict ──1:many──> conflict_version (if understanding changes)
   │
   └──many:many──> conflict_participant ──many:1──> claim (or source_item, for source-level conflicts like CONFLICT-001 through 007)
```

A `conflict_participant` row can point EITHER to a `claim` (a runtime data conflict, e.g. two different
Sentinels producing contradictory drift assessments for the same worker) OR to a `source_item` (a source-level
conflict, e.g. CONFLICT-001's two lead-volume figures) — both use the same `conflict` entity shape, since the
STRUCTURE of "two sides, each with context, neither deleted" is identical regardless of whether the disputed
thing is source text or runtime data.

## Agent/Worker/Task/Sentinel relationships

```
agent ──1:many──> agent_version ──1:many──> agent_instance ──1:many──> agent_state (append-only)
                                                    │
                                                    ├──1:many──> task ──1:many──> task_attempt ──1:many──> task_result
                                                    │                                    │
                                                    │                                    └──0:1──> task_error
                                                    │
                                                    └──many:1──> worker (an agent_instance IS a worker, for Tier 3/4 roles)
                                                                     │
                                                                     └──1:many──> worker_lifecycle_event

sentinel ──1:many──> sentinel_check ──many:1──> agent_instance (observed_worker)
              │
              └──0:many──> sentinel_alert ──0:many──> sentinel_action ──> worker_lifecycle_event (a QUARANTINE action produces a lifecycle event)
```

**Independence enforcement (Section 24, ADR-0008):** `sentinel_check`/`sentinel_alert`/`sentinel_action` rows
have NO foreign key path that allows a `worker`/`agent_instance` to write or modify them — write access is
logically restricted to the Sentinel Plane's own code path, formalized in `integrity-rules.md`.

## Configuration/Event/Audit relationships

```
configuration ──1:many──> configuration_version ──1:many──> configuration_change
                                                                     │
                                                                     └──1:1──> audit_event

event (immutable envelope) ──many:1──> aggregate (polymorphic: lead, agent, worker, configuration, etc. via aggregate_type + aggregate_id)
audit_event ──many:1──> actor (polymorphic: a human user_id OR an agent_instance_id)
```

## Model/Prompt provenance fan-in

```
claim, task_result, commercial_estimate, lead_score, metric value (any DERIVED record)
        │
        ├──many:1──> model_version
        ├──many:1──> prompt_version
        ├──many:1──> tool_version
        ├──many:1──> connector_version
        ├──many:1──> configuration_version
        ├──many:1──> agent_instance
        └──many:1──> task
```

This fan-in is what makes the provenance trace (`OUTPUT → TASK → AGENT → MODEL/PROMPT → INPUT → SOURCE →
EVIDENCE`) queryable end-to-end — see `provenance.md`.

## Memory relationships

```
memory_item ──many:many──> memory_source (MANDATORY — Section 33: "Every memory item must preserve its source
                                            references"; no memory_item may exist with zero memory_source links)
        │
        └──1:1──> memory_embedding (the vector representation — DERIVED, not authoritative)
        │
        └──0:many──> memory_retrieval (a log of when this memory item was retrieved and by what)
```

## Cross-domain notes

- Every entity that produces a `claim` (client_classification, lead_classification, technical_classification,
  commercial_estimate) uses the SAME underlying `claim`/`evidence`/`verification` triangle — this is
  intentional normalization: there is exactly ONE way trust is established in this system, reused everywhere,
  not a different ad-hoc trust mechanism per domain.
- `source_reference` (from `logical-data-model.md`) attaches to almost every entity above (contracts,
  requirements, ADRs, even individual `configuration` values trace back to a `source_item` where applicable)
  — omitted from the diagrams above for readability, documented once here rather than repeated per diagram.
