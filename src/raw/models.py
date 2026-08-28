"""
Raw data layer models. Reuses the Step 2 raw_record design (docs/database/schema.sql) exactly --
per Step 3 Section 12, this is NOT a second competing raw-record implementation, it is the Python
realization of that same logical shape, field-for-field.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class IngestionRunStatus(str, Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ProcessingStatus(str, Enum):
    RECEIVED = "RECEIVED"
    SECURITY_INSPECTED = "SECURITY_INSPECTED"
    QUARANTINED = "QUARANTINED"
    NORMALIZED = "NORMALIZED"
    FAILED = "FAILED"
    DEAD_LETTERED = "DEAD_LETTERED"


class SecurityStatus(str, Enum):
    UNSCREENED = "UNSCREENED"
    SAFE = "SAFE"
    SUSPICIOUS = "SUSPICIOUS"
    MALICIOUS = "MALICIOUS"
    UNKNOWN = "UNKNOWN"


class SchemaStatus(str, Enum):
    KNOWN = "KNOWN"
    KNOWN_LEGACY = "KNOWN_LEGACY"
    KNOWN_FUTURE = "KNOWN_FUTURE"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"
    PARTIAL = "PARTIAL"


class DuplicateStatus(str, Enum):
    DISTINCT_RECORD = "DISTINCT_RECORD"
    EXACT_DUPLICATE = "EXACT_DUPLICATE"
    POSSIBLE_DUPLICATE = "POSSIBLE_DUPLICATE"


class FailureReason(str, Enum):
    """Per Step 3 Section 29 -- exact list, no silent success reclassification."""
    NETWORK_FAILURE = "NETWORK_FAILURE"
    TIMEOUT = "TIMEOUT"
    AUTH_FAILURE = "AUTH_FAILURE"
    RATE_LIMITED = "RATE_LIMITED"
    MALFORMED_RESPONSE = "MALFORMED_RESPONSE"
    UNKNOWN_SCHEMA = "UNKNOWN_SCHEMA"
    SECURITY_QUARANTINE = "SECURITY_QUARANTINE"
    PARSER_FAILURE = "PARSER_FAILURE"
    STORAGE_FAILURE = "STORAGE_FAILURE"
    DUPLICATE = "DUPLICATE"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"


@dataclass
class RawRecord:
    """Field-for-field match to docs/database/schema.sql's raw_record table."""
    record_id: str
    source_id: str
    ingestion_item_id: str
    source_identifier: str
    raw_payload: Any
    content_type: str
    content_hash: str
    retrieved_at: str
    observed_at: str
    source_url: Optional[str] = None
    request_metadata: Optional[dict] = None
    response_metadata: Optional[dict] = None
    retrieval_method: Optional[str] = None
    connector_version: Optional[str] = None
    schema_version: Optional[str] = None
    security_status: SecurityStatus = SecurityStatus.UNSCREENED
    supersedes_raw_record_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class IngestionRun:
    """Per Step 3 Section 10 -- exact required field list."""
    ingestion_run_id: str
    source_id: str
    connector_id: str
    connector_version: str
    started_at: str
    status: IngestionRunStatus
    configuration_version: Optional[str] = None
    correlation_id: Optional[str] = None
    completed_at: Optional[str] = None
    records_received: int = 0
    records_accepted: int = 0
    records_quarantined: int = 0
    records_failed: int = 0
    records_duplicated: int = 0
    error_summary: Optional[str] = None


@dataclass
class IngestionItem:
    """
    Per Step 3 Section 11: every received item -- known, unknown, or malformed -- gets an
    immutable ingestion identity. This dataclass has no delete/discard path.
    """
    ingestion_item_id: str
    ingestion_run_id: str
    source_id: str
    received_at: str
    observed_at: str
    content_type: str
    content_hash: Optional[str] = None
    raw_record_id: Optional[str] = None
    processing_status: ProcessingStatus = ProcessingStatus.RECEIVED
    security_status: SecurityStatus = SecurityStatus.UNSCREENED
    schema_status: SchemaStatus = SchemaStatus.UNKNOWN
    duplicate_status: DuplicateStatus = DuplicateStatus.DISTINCT_RECORD
    error_reference: Optional[str] = None
    failure_reason: Optional[FailureReason] = None
