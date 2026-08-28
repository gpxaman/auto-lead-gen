"""
Normalization stage. Per Step 3 Section 21: normalization is DERIVED DATA. It must NEVER replace
raw data, and must NOT force canonical LEAD classification yet (Step 3 Section 23:
CANONICAL_LEAD_SCHEMA_DEFERRED -- see src/ingestion/lead_candidate.py).

This normalizer is intentionally a conservative, deterministic PASS-THROUGH: it reshapes a raw
payload into a common envelope (Step 3 Section 24: COMMON ENVELOPE + SOURCE-SPECIFIC PAYLOAD) but
does not drop, rename, or infer away any field. Unknown fields remain available through the raw
payload the observation still references via raw_record_id.
"""
from dataclasses import dataclass
from typing import Any, Optional

NORMALIZER_VERSION = "1.0"


@dataclass(frozen=True)
class NormalizationResult:
    status: str  # 'NORMALIZED' | 'PASS_THROUGH_UNSTRUCTURED' | 'FAILED'
    normalized_payload: Optional[dict]
    detail: str


def normalize(raw_payload: Any, schema_detection_result) -> NormalizationResult:
    """
    Deterministic, schema-aware but non-lossy normalization:
      - If raw_payload is a dict, wrap it AS-IS under a 'source_specific_payload' key inside a
        common envelope shape, plus the detected schema metadata. No field is dropped, renamed,
        or reinterpreted.
      - If raw_payload is not a dict (plain text, malformed content, etc.), it cannot be
        'normalized' into structured form without inventing structure that wasn't there --
        per the Absolute Rule ('do not rewrite incoming content'), we do NOT attempt this. The
        Observation for such content simply carries normalized_payload=None and status
        PASS_THROUGH_UNSTRUCTURED; the raw content remains the authoritative representation.
    """
    if isinstance(raw_payload, dict):
        envelope = {
            "common_envelope": {
                "schema_name": schema_detection_result.schema_name,
                "schema_version": schema_detection_result.schema_version,
                "schema_status": schema_detection_result.schema_status.value,
            },
            "source_specific_payload": raw_payload,  # verbatim, no fields dropped
        }
        return NormalizationResult(status="NORMALIZED", normalized_payload=envelope, detail="dict payload wrapped in common envelope, verbatim")

    return NormalizationResult(
        status="PASS_THROUGH_UNSTRUCTURED",
        normalized_payload=None,
        detail=f"payload type {type(raw_payload).__name__} is not structured; raw representation remains authoritative",
    )
