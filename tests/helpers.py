"""Shared test helpers. Nothing in this module touches real client data (Step 3 Section 40-41)."""
from pathlib import Path

from src.common.events import EventLog
from src.connectors.base import Connector, ConnectorType, RawFetchResult
from src.connectors.synthetic_file_connector import SyntheticFileConnector
from src.ingestion.engine import IngestionEngine
from src.observations.store import ObservationStore
from src.quarantine.store import QuarantineStore
from src.raw.store import IngestionItemStore, IngestionRunStore, RawRecordStore
from src.sources.registry import SourceRegistry
from src.sources.models import SourceType

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "ingestion"


class Stack:
    """Bundles a fresh, isolated set of stores + engine for one test."""

    def __init__(self):
        self.event_log = EventLog()
        self.source_registry = SourceRegistry(self.event_log)
        self.raw_store = RawRecordStore()
        self.run_store = IngestionRunStore()
        self.item_store = IngestionItemStore()
        self.observation_store = ObservationStore()
        self.quarantine_store = QuarantineStore()
        self.engine = IngestionEngine(
            source_registry=self.source_registry,
            raw_store=self.raw_store,
            run_store=self.run_store,
            item_store=self.item_store,
            observation_store=self.observation_store,
            quarantine_store=self.quarantine_store,
            event_log=self.event_log,
        )


def build_stack() -> Stack:
    return Stack()


def synthetic_connector() -> SyntheticFileConnector:
    return SyntheticFileConnector(FIXTURES_DIR)


class ScriptedConnector(Connector):
    """
    A second, minimal synthetic connector used ONLY for tests that need to control exactly what
    content is returned for a given source_identifier across successive calls (e.g. testing that
    a changed source item produces a new raw_record version). This does not compete with
    SyntheticFileConnector as a production connector -- it exists purely as a test double, and is
    itself fully deterministic (Step 3 Section 58).
    """
    connector_type = ConnectorType.OTHER

    def __init__(self, script: dict[str, list]):
        """script: {source_identifier: [payload_call_1, payload_call_2, ...]}"""
        self._script = {k: list(v) for k, v in script.items()}
        self._call_counts: dict[str, int] = {k: 0 for k in script}

    def discover(self) -> list[str]:
        return list(self._script.keys())

    def fetch(self, source_identifier: str) -> RawFetchResult:
        calls = self._script[source_identifier]
        idx = min(self._call_counts[source_identifier], len(calls) - 1)
        payload = calls[idx]
        self._call_counts[source_identifier] += 1
        if payload is None:
            raise ConnectionError(f"scripted failure for {source_identifier}")
        return RawFetchResult(
            source_identifier=source_identifier,
            raw_payload=payload,
            content_type="application/json" if isinstance(payload, (dict, list)) else "text/plain",
            source_url=f"scripted://{source_identifier}",
        )
