-- ============================================================================
-- IECHM-LIOS — PROPOSED Physical Schema (Step 2)
-- ============================================================================
-- STATUS: PROPOSED, ILLUSTRATIVE, NON-FINAL. NOT AN APPROVED ARCHITECTURE DECISION.
--
-- Per Step 2 Section 38/39: no database vendor has been approved anywhere in
-- Step 0 or Step 1 (see docs/architecture/open-decisions.md #7). This file
-- uses PostgreSQL-flavored SQL only because it is a widely-portable, commonly
-- understood lingua franca for illustrating a relational shape — it is NOT a
-- statement that PostgreSQL (or any relational database) has been selected.
-- See docs/database/entity-catalog.md's "DATABASE_IMPLEMENTATION_OPTIONS"
-- section for the 3 unselected candidate technology shapes.
--
-- SCOPE: This file covers only the CORE provenance/evidence/versioning/audit
-- entities central to the Absolute Data-Preservation Principle — it is NOT a
-- complete physical implementation of every entity in entity-catalog.md (that
-- would require committing to many unresolved decisions: canonical lead
-- schema version (#2), canonical client-archetype set (#4), two-axis
-- classification (#5), and more). Producing a "complete" schema today would
-- require silently resolving those open decisions, which Step 2 Section 2
-- explicitly forbids. Entities whose SHAPE depends on an open decision are
-- deliberately represented here as version-tolerant / JSONB-payload tables
-- rather than rigid typed columns, so no decision is silently baked in.
--
-- DO NOT RUN THIS AGAINST PRODUCTION. This is a design artifact, not a
-- migration to be applied. See docs/database/migrations.md for the discipline
-- any real migration must follow, and docs/architecture/open-decisions.md
-- for the decisions that must be made before this schema (or any schema)
-- becomes safe to implement for real.
-- ============================================================================

-- ---------------------------------------------------------------------------
-- SOURCE DOCUMENT DATA (Step 2 Section 6) — mirrors, does not replace, the
-- filesystem archive under docs/source-extraction/. Read-mostly, immutable.
-- ---------------------------------------------------------------------------

CREATE TABLE source_document (
    document_id     UUID PRIMARY KEY,
    document_name   TEXT NOT NULL,
    sha256          TEXT,                       -- nullable; see Step 0 manifest disclosure
    page_count      INTEGER NOT NULL,
    processed_at    TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE source_page (
    page_id         UUID PRIMARY KEY,
    document_id     UUID NOT NULL REFERENCES source_document(document_id),
    page_number     INTEGER NOT NULL,
    content_ref     TEXT NOT NULL,               -- pointer to docs/source-extraction/pages/page-NNN.md, NOT a copy
    UNIQUE (document_id, page_number)
);

CREATE TABLE source_item (
    source_id           TEXT PRIMARY KEY,        -- e.g. 'SRC-000001', matches source-register.jsonl exactly
    page_id              UUID NOT NULL REFERENCES source_page(page_id),
    section              TEXT,
    category              TEXT NOT NULL,          -- SOURCE_FACT | USER_REQUIREMENT | AI_PROPOSAL | ... (open enum, see Step 0 category list)
    exact_text            TEXT NOT NULL,
    normalized_meaning    TEXT NOT NULL,
    status                TEXT NOT NULL DEFAULT 'preserved'
);

-- ---------------------------------------------------------------------------
-- RAW DATA LAYER (Section 5) — immutable, append-only, never overwritten.
-- ---------------------------------------------------------------------------

CREATE TABLE raw_record (
    record_id            UUID PRIMARY KEY,
    source_system         TEXT NOT NULL,          -- e.g. 'upwork', 'alibaba_rfq'
    source_identifier     TEXT NOT NULL,           -- the external system's own ID for this item
    retrieved_at           TIMESTAMPTZ NOT NULL,
    observed_at             TIMESTAMPTZ NOT NULL,
    raw_payload              JSONB,                  -- or a blob-storage reference, vendor-dependent
    content_type              TEXT,
    content_hash               TEXT NOT NULL,
    source_url                  TEXT,
    request_metadata             JSONB,
    response_metadata            JSONB,
    retrieval_method             TEXT,
    connector_version_id         UUID,             -- FK to connector_version, defined below
    schema_version                TEXT,
    ingestion_run_id               UUID,
    security_status                 TEXT NOT NULL DEFAULT 'UNSCREENED',  -- UNSCREENED | SCREENED_CLEAN | FLAGGED
    supersedes_raw_record_id        UUID REFERENCES raw_record(record_id),  -- version chain, never an UPDATE
    created_at                       TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_system, source_identifier, content_hash)   -- idempotent-ingestion rule, integrity-rules.md
);
-- NOTE: no UPDATE trigger/permission should exist on raw_record's content columns in any real
-- implementation; this comment stands in for that constraint, which is technology-dependent.

-- ---------------------------------------------------------------------------
-- CLAIM / EVIDENCE / VERIFICATION TRIANGLE (Sections 12-14) — the heart of
-- the trust model. See docs/database/evidence.md for full field rationale.
-- ---------------------------------------------------------------------------

CREATE TYPE trust_level AS ENUM (
    'RAW_SOURCE', 'RAW_EXTERNAL', 'OBSERVED', 'MODEL_INFERENCE', 'UNVERIFIED_CLAIM',
    'EVIDENCE_BACKED_CLAIM', 'VERIFIED', 'DERIVED', 'HUMAN_DECISION', 'SYSTEM_DECISION',
    'QUARANTINED', 'REJECTED'
);

CREATE TABLE claim (
    claim_id             UUID PRIMARY KEY,
    subject_type          TEXT NOT NULL,          -- 'lead' | 'client' | 'platform' | 'worker' | ...
    subject_id             UUID NOT NULL,
    predicate                TEXT NOT NULL,
    value                      JSONB NOT NULL,       -- polymorphic asserted value
    claim_type                  TEXT NOT NULL,        -- CLASSIFICATION | SCORE | STATUS | FACT
    source_record_ids            UUID[] NOT NULL DEFAULT '{}',
    confidence                    NUMERIC(4,3),        -- 0.000 - 1.000, nullable
    trust_level                    trust_level NOT NULL DEFAULT 'MODEL_INFERENCE',
    status                          TEXT NOT NULL DEFAULT 'ACTIVE',  -- ACTIVE | SUPERSEDED | REJECTED | EXPIRED
    derivation_method                TEXT,
    model_version_id                  UUID,           -- nullable, see provenance.md
    prompt_version_id                  UUID,
    configuration_version_id            UUID,
    agent_instance_id                    UUID,
    task_id                                UUID,
    valid_from                              TIMESTAMPTZ,
    valid_until                              TIMESTAMPTZ,
    created_at                                TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                                 TIMESTAMPTZ NOT NULL DEFAULT now()
    -- CONTENT fields (subject/predicate/value) are never updated after creation;
    -- only status/updated_at may change (status-transition-only rule, integrity-rules.md)
);

CREATE TABLE evidence (
    evidence_id            UUID PRIMARY KEY,
    source_record_id         UUID REFERENCES raw_record(record_id),
    source_url                 TEXT,
    retrieved_at                 TIMESTAMPTZ,
    observed_at                   TIMESTAMPTZ,
    content_hash                    TEXT,
    evidence_type                    TEXT NOT NULL,   -- URL_PROOF | API_PAYLOAD | LISTING_HASH | SCREENSHOT | SNAPSHOT
    snapshot_reference                 TEXT,
    verification_status_cache            TEXT,          -- denormalized cache only; verification table is authoritative
    confidence                            NUMERIC(4,3),
    created_at                             TIMESTAMPTZ NOT NULL DEFAULT now()
    -- Immutable after creation except verification_status_cache.
);

CREATE TABLE claim_evidence (              -- many:many join, Section 12: a claim may have 0, 1, or many evidence rows
    claim_id      UUID NOT NULL REFERENCES claim(claim_id),
    evidence_id    UUID NOT NULL REFERENCES evidence(evidence_id),
    PRIMARY KEY (claim_id, evidence_id)
);

CREATE TYPE verification_result AS ENUM (
    'VERIFIED', 'PARTIALLY_VERIFIED', 'UNVERIFIED', 'CONTRADICTED', 'FAILED', 'EXPIRED'
);

CREATE TABLE verification (
    verification_id         UUID PRIMARY KEY,
    claim_id                  UUID NOT NULL REFERENCES claim(claim_id),
    method                      TEXT NOT NULL,
    verifier_agent_instance_id   UUID,
    verification_source            TEXT,
    verification_timestamp          TIMESTAMPTZ NOT NULL DEFAULT now(),
    result                            verification_result NOT NULL,
    confidence                         NUMERIC(4,3),
    notes                                TEXT,
    status                                TEXT NOT NULL DEFAULT 'ACTIVE'  -- ACTIVE | SUPERSEDED
    -- Immutable after creation. FAILED rows are never deleted (Section 14).
);

-- ---------------------------------------------------------------------------
-- CONFLICT MODEL (Section 15) — first-class, never overwritten.
-- ---------------------------------------------------------------------------

CREATE TABLE conflict (
    conflict_id       UUID PRIMARY KEY,
    subject             TEXT NOT NULL,
    status                TEXT NOT NULL DEFAULT 'OPEN',  -- OPEN | UNDER_REVIEW | RESOLVED | SUPERSEDED | UNRESOLVED
    resolution             TEXT,
    resolver                 TEXT,
    resolved_at                TIMESTAMPTZ,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE conflict_participant (
    participant_id      UUID PRIMARY KEY,
    conflict_id            UUID NOT NULL REFERENCES conflict(conflict_id),
    side                     TEXT NOT NULL,       -- 'A' | 'B'
    claim_id                   UUID REFERENCES claim(claim_id),        -- nullable
    source_id                    TEXT REFERENCES source_item(source_id), -- nullable; exactly one of claim_id/source_id populated
    context                        TEXT
);

-- ---------------------------------------------------------------------------
-- SCHEMA REGISTRY (Section 19) — never delete an old schema.
-- ---------------------------------------------------------------------------

CREATE TABLE schema_registry (
    schema_id          TEXT PRIMARY KEY,          -- e.g. 'SCHEMA-005'
    schema_name           TEXT NOT NULL,
    schema_version           TEXT NOT NULL,
    source_id                  TEXT REFERENCES source_item(source_id),
    schema_type                  TEXT NOT NULL,
    definition                     JSONB NOT NULL,   -- the actual schema shape, preserved verbatim
    status                          TEXT NOT NULL DEFAULT 'HISTORICAL',  -- HISTORICAL | CANDIDATE | CANONICAL
    supersedes                       TEXT REFERENCES schema_registry(schema_id),
    superseded_by                      TEXT REFERENCES schema_registry(schema_id),
    created_at                           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- CONFIGURATION (Section 25) — versioned, auditable.
-- ---------------------------------------------------------------------------

CREATE TABLE configuration (
    configuration_id     UUID PRIMARY KEY,
    scope                    TEXT NOT NULL,        -- e.g. 'sentinel.drift_threshold', 'worker.spawn_threshold'
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE configuration_version (
    configuration_version_id  UUID PRIMARY KEY,
    configuration_id             UUID NOT NULL REFERENCES configuration(configuration_id),
    version                         INTEGER NOT NULL,
    data                              JSONB NOT NULL,
    created_by                         TEXT NOT NULL,   -- actor id
    created_at                           TIMESTAMPTZ NOT NULL DEFAULT now(),
    activated_at                          TIMESTAMPTZ,
    retired_at                             TIMESTAMPTZ,
    UNIQUE (configuration_id, version)
);

-- ---------------------------------------------------------------------------
-- EVENT ENVELOPE (Sections 27-28) — fully immutable.
-- ---------------------------------------------------------------------------

CREATE TABLE event (
    event_id                 UUID PRIMARY KEY,
    event_type                  TEXT NOT NULL,
    event_version                 TEXT NOT NULL,     -- payload schema version tag, not a mutation marker
    aggregate_type                  TEXT NOT NULL,
    aggregate_id                      UUID NOT NULL,
    producer                            TEXT NOT NULL,
    "timestamp"                          TIMESTAMPTZ NOT NULL DEFAULT now(),
    correlation_id                        UUID,
    causation_id                           UUID,
    payload                                 JSONB NOT NULL,
    payload_schema_version                    TEXT,
    security_classification                     TEXT NOT NULL DEFAULT 'INTERNAL',
    idempotency_key                               TEXT UNIQUE
    -- No UPDATE/DELETE permitted in any real implementation.
);

-- ---------------------------------------------------------------------------
-- AUDIT (Section 29) — tamper-evident, no secrets.
-- ---------------------------------------------------------------------------

CREATE TABLE audit_event (
    audit_event_id      UUID PRIMARY KEY,
    actor                   TEXT NOT NULL,
    actor_type                TEXT NOT NULL,        -- 'HUMAN' | 'AGENT' | 'SYSTEM'
    action                      TEXT NOT NULL,
    target_type                   TEXT NOT NULL,
    target_id                       UUID NOT NULL,
    before                            JSONB,           -- MUST be redacted of SECRET-classified fields before insert
    after                              JSONB,           -- MUST be redacted of SECRET-classified fields before insert
    reason                               TEXT,
    "timestamp"                           TIMESTAMPTZ NOT NULL DEFAULT now(),
    correlation_id                          UUID,
    configuration_version_id                  UUID REFERENCES configuration_version(configuration_version_id)
    -- Fully immutable. This IS the tamper-evidence mechanism.
);

-- ---------------------------------------------------------------------------
-- AGENT / WORKER / TASK (Sections 21-24) — abbreviated core; full field list
-- in docs/database/entity-catalog.md. agent_state is append-only.
-- ---------------------------------------------------------------------------

CREATE TABLE agent (
    agent_id       UUID PRIMARY KEY,
    role_name        TEXT NOT NULL,      -- 'Client Classification Swarm', 'Platform Worker', 'Sentinel', ...
    tier               TEXT NOT NULL,     -- Tier 0-4, per docs/architecture/agent-topology.md's naming convention (ADR-0002)
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE agent_instance (
    agent_instance_id     UUID PRIMARY KEY,
    agent_id                UUID NOT NULL REFERENCES agent(agent_id),
    parent_agent_instance_id UUID REFERENCES agent_instance(agent_instance_id),
    spawned_at                 TIMESTAMPTZ NOT NULL DEFAULT now(),
    retired_at                   TIMESTAMPTZ
);

CREATE TABLE agent_state (                -- append-only; current state = latest row per agent_instance_id
    agent_state_id          UUID PRIMARY KEY,
    agent_instance_id          UUID NOT NULL REFERENCES agent_instance(agent_instance_id),
    status                        TEXT NOT NULL,     -- SPAWNED | ACTIVE | DEGRADED | QUARANTINED | DRAINING | RETIRED | FAILED | REPLACED
    drift_score                     NUMERIC(4,3),
    recorded_at                       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE task (
    task_id            UUID PRIMARY KEY,
    agent_instance_id     UUID NOT NULL REFERENCES agent_instance(agent_instance_id),
    task_type               TEXT NOT NULL,
    input_reference            TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE task_attempt (            -- append-only; failed attempts are never deleted
    task_attempt_id      UUID PRIMARY KEY,
    task_id                 UUID NOT NULL REFERENCES task(task_id),
    attempt_number             INTEGER NOT NULL,
    status                        TEXT NOT NULL,     -- SUCCESS | FAILED | IN_PROGRESS
    output_reference                TEXT,
    error                              TEXT,
    started_at                          TIMESTAMPTZ NOT NULL,
    completed_at                          TIMESTAMPTZ,
    configuration_version_id                UUID REFERENCES configuration_version(configuration_version_id),
    UNIQUE (task_id, attempt_number)
);

-- ---------------------------------------------------------------------------
-- MODEL / PROMPT / TOOL / CONNECTOR VERSIONING (Section 26)
-- ---------------------------------------------------------------------------

CREATE TABLE model_version (
    model_version_id   UUID PRIMARY KEY,
    provider               TEXT NOT NULL,
    model_name                TEXT NOT NULL,
    version_tag                  TEXT NOT NULL,
    created_at                     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE prompt_version (
    prompt_version_id   UUID PRIMARY KEY,
    prompt_name             TEXT NOT NULL,
    version                    INTEGER NOT NULL,
    prompt_text                   TEXT NOT NULL,
    created_at                      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (prompt_name, version)
);

CREATE TABLE connector_version (
    connector_version_id   UUID PRIMARY KEY,
    connector_name              TEXT NOT NULL,
    version                        TEXT NOT NULL,
    created_at                       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- END OF PROPOSED SCHEMA — remaining entity-catalog.md domains (Client, Lead,
-- Platform, Subdomain, Technical/Commercial Intelligence, Assumption,
-- Scenario, Formula, Sentinel, Telemetry, Strategy, Metric Evolution, Memory,
-- Security/Quarantine, Manufacturing) are intentionally NOT physically
-- schematized here. Each depends on at least one unresolved open decision
-- (canonical schema version, canonical archetype set, two-axis
-- classification, database technology itself) — see
-- docs/architecture/open-decisions.md. Schematizing them now would require
-- silently resolving those decisions, which Step 2 explicitly forbids.
-- Their logical shape is fully specified in docs/database/entity-catalog.md
-- and is ready to be physicalized once the relevant open decisions resolve.
-- ---------------------------------------------------------------------------
