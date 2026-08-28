"""
Ingestion envelope construction. Per Step 3 Section 25 and
docs/contracts/schemas/ingestion-envelope.v1.schema.json (DERIVED_CANONICAL_SCHEMA).
"""
from dataclasses import asdict, dataclass
from typing import Optional

from src.common.hashing import ContentHash


@dataclass
class IngestionEnvelope:
    ingestion_item_id: str
    ingestion_run_id: str
    source_id: str
    received_at: str
    observed_at: str
    content_type: str
    content_hash: dict  # {algorithm, hash, input_representation}
    security_status: str
    schema_status: str
    duplicate_status: str
    connector_id: Optional[str] = None
    connector_version: Optional[str] = None
    raw_record_id: Optional[str] = None
    schema_detection: Optional[dict] = None
    correlation_id: Optional[str] = None
    provenance: Optional[dict] = None

    def to_dict(self) -> dict:
        return asdict(self)


def build_envelope(
    ingestion_item_id: str,
    ingestion_run_id: str,
    source_id: str,
    received_at: str,
    observed_at: str,
    content_type: str,
    content_hash: ContentHash,
    security_status: str,
    schema_status: str,
    duplicate_status: str,
    connector_id: Optional[str] = None,
    connector_version: Optional[str] = None,
    raw_record_id: Optional[str] = None,
    schema_detection: Optional[dict] = None,
    correlation_id: Optional[str] = None,
    configuration_version: Optional[str] = None,
) -> IngestionEnvelope:
    return IngestionEnvelope(
        ingestion_item_id=ingestion_item_id,
        ingestion_run_id=ingestion_run_id,
        source_id=source_id,
        received_at=received_at,
        observed_at=observed_at,
        content_type=content_type,
        content_hash={
            "algorithm": content_hash.algorithm,
            "hash": content_hash.hash,
            "input_representation": content_hash.input_representation,
        },
        security_status=security_status,
        schema_status=schema_status,
        duplicate_status=duplicate_status,
        connector_id=connector_id,
        connector_version=connector_version,
        raw_record_id=raw_record_id,
        schema_detection=schema_detection,
        correlation_id=correlation_id,
        provenance={"configuration_version": configuration_version, "connector_version": connector_version},
    )
