"""
Observation store. Append-only. Supports replay/reprocessing per Step 3 Sections 32-33: a raw
record may be processed multiple times (e.g. NormalizerV1 then later NormalizerV2), producing
Observation V1 and Observation V2 as SEPARATE rows -- V1 is never overwritten by V2.
"""
from typing import Optional

from src.common.health import HealthResult, HealthStatus, simple_health
from src.observations.models import Observation


class ObservationStore:
    def __init__(self):
        self._observations: dict[str, Observation] = {}

    def save(self, observation: Observation) -> Observation:
        """Always an INSERT -- observation_id is freshly generated per new_observation() call,
        so there is no update path here by construction."""
        self._observations[observation.observation_id] = observation
        return observation

    def get(self, observation_id: str) -> Optional[Observation]:
        return self._observations.get(observation_id)

    def by_raw_record(self, raw_record_id: str) -> list[Observation]:
        """All observations ever derived from one raw record -- across every normalizer version
        that has ever processed it. Demonstrates Step 3 Section 33's replay/reprocessing model."""
        return [o for o in self._observations.values() if o.raw_record_id == raw_record_id]

    def all(self) -> list[Observation]:
        return list(self._observations.values())

    def health_check(self) -> HealthResult:
        return simple_health("observation_store", HealthStatus.HEALTHY, detail=f"{len(self._observations)} observations stored")
