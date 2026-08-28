"""
Deterministic schema-version detection. Per Step 3 Section 17: for every incoming structured
payload, attempt to determine schema_name/schema_version/schema_status. Never force an unknown
payload into a known schema.

Uses the SAME discriminator fields the Step 2 lead.v1.schema.json oneOf wrapper relies on
(lead_metadata / layer_origin / [lead_id + timestamp_utc + client_archetype + source_metadata +
technical_specifications + commercial_assessment + security_analysis]) -- see
docs/contracts/schemas/lead.v1.schema.json and docs/database/schema_registry seed data
(SCHEMA-002/003/005). This module does not invent new schema versions; it only recognizes the
ones already catalogued in docs/source-extraction/json-schemas.md.
"""
from dataclasses import dataclass
from typing import Optional

from src.raw.models import SchemaStatus

_SCHEMA_005_REQUIRED = {
    "lead_id", "timestamp_utc", "client_archetype", "source_metadata",
    "technical_specifications", "commercial_assessment", "security_analysis",
}


@dataclass(frozen=True)
class SchemaDetectionResult:
    schema_name: Optional[str]
    schema_version: Optional[str]
    schema_status: SchemaStatus
    detail: str


def detect_schema(raw_payload) -> SchemaDetectionResult:
    """
    Returns KNOWN + a schema_id (SCHEMA-002/003/005) if the payload matches one of the three
    preserved source lead-schema shapes (see docs/architecture/schema-versioning.md -- none of
    these is canonical, all three remain valid). Returns UNKNOWN if it is structured (a dict) but
    matches none of them. Returns INVALID if it is not even a dict/object. This function NEVER
    coerces an unrecognized shape into one of the known ones.
    """
    if not isinstance(raw_payload, dict):
        return SchemaDetectionResult(
            schema_name=None, schema_version=None, schema_status=SchemaStatus.INVALID,
            detail=f"payload is not a JSON object (type={type(raw_payload).__name__}); cannot be schema-matched",
        )

    keys = set(raw_payload.keys())

    if "lead_metadata" in keys:
        return SchemaDetectionResult(
            schema_name="UnifiedLeadEntity", schema_version="SCHEMA-002", schema_status=SchemaStatus.KNOWN_LEGACY,
            detail="matched SCHEMA-002 discriminator field 'lead_metadata'",
        )

    if "layer_origin" in keys:
        return SchemaDetectionResult(
            schema_name="UnifiedLeadEntity", schema_version="SCHEMA-003", schema_status=SchemaStatus.KNOWN_LEGACY,
            detail="matched SCHEMA-003 discriminator field 'layer_origin'",
        )

    if _SCHEMA_005_REQUIRED.issubset(keys):
        return SchemaDetectionResult(
            schema_name="UnifiedLeadEntity", schema_version="SCHEMA-005", schema_status=SchemaStatus.KNOWN,
            detail="matched all SCHEMA-005 required top-level fields",
        )

    if _SCHEMA_005_REQUIRED & keys:
        # Some but not all SCHEMA-005 fields present -- a partial/malformed instance of that schema
        missing = _SCHEMA_005_REQUIRED - keys
        return SchemaDetectionResult(
            schema_name="UnifiedLeadEntity", schema_version="SCHEMA-005", schema_status=SchemaStatus.PARTIAL,
            detail=f"partially matches SCHEMA-005; missing required fields: {sorted(missing)}",
        )

    return SchemaDetectionResult(
        schema_name=None, schema_version=None, schema_status=SchemaStatus.UNKNOWN,
        detail=f"structured payload did not match any known schema discriminator; top-level keys: {sorted(keys)}",
    )
