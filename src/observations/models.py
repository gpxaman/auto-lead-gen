"""
Observation model. Per Step 3 Section 22: "What was observed from a source at a particular time"
-- explicitly NOT "what is true." An observation can later generate CLAIMS (Step 2's claim.md
contract) but is not itself a verified claim.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.common.ids import new_id


@dataclass
class Observation:
    observation_id: str
    source_id: str
    raw_record_id: str
    observed_at: str
    observation_type: str  # e.g. 'lead_candidate', 'platform_metadata', 'unknown_content'
    subject_reference: Optional[str] = None  # e.g. source_identifier this observation concerns
    normalized_payload: Optional[dict] = None
    confidence: Optional[float] = None
    normalizer_version: str = "1.0"
    provenance: Optional[dict] = None  # {ingestion_run_id, ingestion_item_id, connector_version, ...}
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def new_observation(
    source_id: str,
    raw_record_id: str,
    observed_at: str,
    observation_type: str,
    normalized_payload: Optional[dict],
    provenance: dict,
    subject_reference: Optional[str] = None,
    confidence: Optional[float] = None,
    normalizer_version: str = "1.0",
) -> Observation:
    return Observation(
        observation_id=new_id("obs-"),
        source_id=source_id,
        raw_record_id=raw_record_id,
        observed_at=observed_at,
        observation_type=observation_type,
        subject_reference=subject_reference,
        normalized_payload=normalized_payload,
        confidence=confidence,
        normalizer_version=normalizer_version,
        provenance=provenance,
    )
