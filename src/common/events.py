"""
Event envelope + immutable, append-only in-memory event log.

Per docs/contracts/event.md / docs/contracts/schemas/event-envelope.v1.schema.json (Step 2) and
Step 3 Section 27: events are immutable after creation. Corrections emit a NEW event referencing
the original via causation_id -- there is no update/delete path on this store by design (no method
exists to mutate a stored event; this is enforced structurally, not by convention).

DEVELOPMENT_ONLY: this is an in-memory store for Step 3's deterministic ingestion foundation.
No production event-bus vendor has been selected (docs/architecture/open-decisions.md #8).
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from src.common.ids import new_id


@dataclass(frozen=True)
class Event:
    event_id: str
    event_type: str
    event_version: str
    aggregate_type: str
    aggregate_id: str
    producer: str
    timestamp: str
    payload: dict
    payload_schema_version: Optional[str] = None
    security_classification: str = "INTERNAL"
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    idempotency_key: Optional[str] = None


def make_event(
    event_type: str,
    aggregate_type: str,
    aggregate_id: str,
    producer: str,
    payload: dict,
    event_version: str = "1.0",
    payload_schema_version: Optional[str] = None,
    security_classification: str = "INTERNAL",
    correlation_id: Optional[str] = None,
    causation_id: Optional[str] = None,
    idempotency_key: Optional[str] = None,
) -> Event:
    return Event(
        event_id=new_id("evt-"),
        event_type=event_type,
        event_version=event_version,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        producer=producer,
        timestamp=datetime.now(timezone.utc).isoformat(),
        payload=payload,
        payload_schema_version=payload_schema_version,
        security_classification=security_classification,
        correlation_id=correlation_id,
        causation_id=causation_id,
        idempotency_key=idempotency_key,
    )


class EventLog:
    """
    Append-only event store. No update() or delete() method exists -- immutability is enforced
    by the absence of a mutation API, not merely by convention (Step 3 Section 27).
    """

    def __init__(self):
        self._events: list[Event] = []
        self._by_idempotency_key: dict[str, Event] = {}

    def append(self, event: Event) -> tuple[Event, bool]:
        """
        Append an event. Returns (event, was_new).

        If event.idempotency_key matches an already-stored event, the ORIGINAL event is returned
        and was_new=False -- this is the idempotent-retry dedup path (Step 3 Section 28). The
        duplicate delivery attempt is NOT silently dropped from history entirely: callers are
        expected to log the retry (see src/common/logging_utils.py) even though no new Event row
        is created, keeping the retry auditable without creating two semantic events.
        """
        if event.idempotency_key and event.idempotency_key in self._by_idempotency_key:
            return self._by_idempotency_key[event.idempotency_key], False
        self._events.append(event)
        if event.idempotency_key:
            self._by_idempotency_key[event.idempotency_key] = event
        return event, True

    def all(self) -> list[Event]:
        return list(self._events)  # defensive copy -- callers cannot mutate internal history

    def by_aggregate(self, aggregate_type: str, aggregate_id: str) -> list[Event]:
        return [e for e in self._events if e.aggregate_type == aggregate_type and e.aggregate_id == aggregate_id]

    def by_type(self, event_type: str) -> list[Event]:
        return [e for e in self._events if e.event_type == event_type]

    def by_correlation(self, correlation_id: str) -> list[Event]:
        return [e for e in self._events if e.correlation_id == correlation_id]

    def causal_chain(self, event_id: str) -> list[Event]:
        """Follow causation_id backward from the given event to its root cause."""
        chain = []
        by_id = {e.event_id: e for e in self._events}
        current = by_id.get(event_id)
        while current is not None:
            chain.append(current)
            current = by_id.get(current.causation_id) if current.causation_id else None
        return chain
