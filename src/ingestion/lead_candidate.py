"""
Lead-extraction boundary. Per Step 3 Section 23:

  "Do NOT finalize the canonical LEAD schema in Step 3. The lead schema conflict remains
   unresolved (CONFLICT-003). ... If the architecture does not support a lead-candidate entity
   cleanly: do not invent one. Document the boundary as CANONICAL_LEAD_SCHEMA_DEFERRED."

Decision made here: Step 2's architecture DOES cleanly support an intermediate representation --
the Observation model (src/observations/models.py) already exists for exactly this purpose
("what was observed... not what is true"), and docs/contracts/lead.md already documents that a
canonical `lead`/`lead_version` entity requires choosing among SCHEMA-002/003/005 (open_decisions
#2), which Step 3 must not do.

Therefore Step 3 does NOT introduce a new LEAD_CANDIDATE class distinct from Observation --
doing so would be inventing a second intermediate representation the architecture does not ask
for, when Observation already fills that role. An Observation whose observation_type is
'lead_candidate' (see src/ingestion/engine.py) IS Step 3's lead-candidate representation: it
references raw_record + source + source_identifier (via subject_reference) exactly as Section 23
requires, and it discards no source-specific fields (the full source-specific payload is retained
verbatim inside normalized_payload.source_specific_payload, per src/observations/normalizer.py).

STATUS: CANONICAL_LEAD_SCHEMA_DEFERRED. No `Lead`/`LeadVersion` class exists in src/ as of Step 3.
Promoting an Observation into a canonical Lead record is explicitly OUT OF SCOPE for this step
(Step 3 Section 57: "Do NOT implement... client classification..."; this also applies to lead
finalization, which requires the still-open schema decision).
"""

LEAD_CANDIDATE_OBSERVATION_TYPE = "lead_candidate"

CANONICAL_LEAD_SCHEMA_STATUS = "CANONICAL_LEAD_SCHEMA_DEFERRED"
