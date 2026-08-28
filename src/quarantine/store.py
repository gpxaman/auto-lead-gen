"""
Quarantine store. Per Step 3 Section 19: quarantined content must retain full metadata and is
NEVER deleted simply because it was quarantined. Release is a status transition, not a deletion.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from src.common.ids import new_id


class QuarantineStatus(str, Enum):
    QUARANTINED = "QUARANTINED"
    UNDER_REVIEW = "UNDER_REVIEW"
    RELEASED = "RELEASED"
    CONFIRMED_MALICIOUS = "CONFIRMED_MALICIOUS"  # released FROM active quarantine queue, but record kept forever


@dataclass
class QuarantineRecord:
    quarantine_id: str
    raw_record_id: str
    reason: str
    detection_type: str
    detector: str
    detector_version: str
    severity: str
    status: QuarantineStatus = QuarantineStatus.QUARANTINED
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    released_at: Optional[str] = None
    release_actor: Optional[str] = None
    release_reason: Optional[str] = None


class QuarantineStore:
    def __init__(self):
        self._records: dict[str, QuarantineRecord] = {}

    def quarantine(
        self, raw_record_id: str, reason: str, detection_type: str, detector: str, detector_version: str, severity: str
    ) -> QuarantineRecord:
        record = QuarantineRecord(
            quarantine_id=new_id("qtn-"),
            raw_record_id=raw_record_id,
            reason=reason,
            detection_type=detection_type,
            detector=detector,
            detector_version=detector_version,
            severity=severity,
        )
        self._records[record.quarantine_id] = record
        return record

    def release(self, quarantine_id: str, release_actor: str, release_reason: str, confirmed_malicious: bool = False) -> QuarantineRecord:
        """
        Status-transition only. The record is NEVER removed from the store -- 'released' means
        the content is no longer actively blocking processing, not that its quarantine history
        is erased (Step 3 Section 19).
        """
        record = self._records[quarantine_id]
        record.status = QuarantineStatus.CONFIRMED_MALICIOUS if confirmed_malicious else QuarantineStatus.RELEASED
        record.released_at = datetime.now(timezone.utc).isoformat()
        record.release_actor = release_actor
        record.release_reason = release_reason
        return record

    def get(self, quarantine_id: str) -> QuarantineRecord:
        return self._records.get(quarantine_id)

    def by_raw_record(self, raw_record_id: str) -> list[QuarantineRecord]:
        return [r for r in self._records.values() if r.raw_record_id == raw_record_id]

    def all(self) -> list[QuarantineRecord]:
        return list(self._records.values())

    def active(self) -> list[QuarantineRecord]:
        return [r for r in self._records.values() if r.status in (QuarantineStatus.QUARANTINED, QuarantineStatus.UNDER_REVIEW)]
