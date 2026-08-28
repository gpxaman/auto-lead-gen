"""
Source Registry service. Per Step 3 Sections 5-9, 37.

DEVELOPMENT_ONLY in-memory implementation -- no production database vendor has been selected
(docs/architecture/open-decisions.md #7). This class is the internal API surface Step 3 Section 37
asks for: register/retrieve source, update version, register connector (see src/connectors/base.py),
retrieve connector, etc. Not exposed publicly; no auth boundary is implemented here since this is a
same-process library, not a network service (Step 3 Section 37's authorization requirement applies
once/if this is exposed over a real API boundary in a later step).
"""
from datetime import datetime, timezone
from typing import Optional

from src.common.events import Event, EventLog, make_event
from src.common.health import HealthResult, HealthStatus, simple_health
from src.common.ids import new_id
from src.sources.models import (
    Source,
    SourceEndpoint,
    SourceHealthEvent,
    SourcePolicy,
    SourceStatus,
    SourceType,
    SourceVersion,
    new_source,
)


class SourceRegistry:
    def __init__(self, event_log: EventLog):
        self._event_log = event_log
        self._sources: dict[str, Source] = {}
        self._versions: dict[str, list[SourceVersion]] = {}  # source_id -> append-only version list
        self._endpoints: dict[str, list[SourceEndpoint]] = {}
        self._policies: dict[str, list[SourcePolicy]] = {}  # source_id -> append-only policy version list
        self._health_events: dict[str, list[SourceHealthEvent]] = {}  # source_id -> append-only health log

    # -- Registration ------------------------------------------------------

    def register_source(
        self,
        source_type: SourceType,
        name: str,
        display_name: Optional[str] = None,
        macro_channel: str = "UNKNOWN",
        platform: str = "UNKNOWN",
        source_url: Optional[str] = None,
        connector_id: Optional[str] = None,
        connector_version: Optional[str] = None,
    ) -> Source:
        source = new_source(source_type, name, display_name)
        version = SourceVersion(
            source_version_id=new_id("srcv-"),
            source_id=source.source_id,
            version=1,
            macro_channel=macro_channel,
            platform=platform,
            source_url=source_url,
            connector_id=connector_id,
            connector_version=connector_version,
        )
        source.latest_source_version_id = version.source_version_id
        source.status = SourceStatus.ACTIVE

        self._sources[source.source_id] = source
        self._versions[source.source_id] = [version]
        self._endpoints[source.source_id] = []
        self._policies[source.source_id] = []
        self._health_events[source.source_id] = []

        evt = make_event(
            event_type="SourceRegistered",
            aggregate_type="source",
            aggregate_id=source.source_id,
            producer="SourceRegistry",
            payload={"source_id": source.source_id, "name": name, "source_type": source_type.value},
        )
        self._event_log.append(evt)
        return source

    def update_source_version(self, source_id: str, **version_fields) -> SourceVersion:
        """
        Create a NEW SourceVersion for this source. The previous version row is NEVER edited or
        deleted (Step 3 Section 7: "A source configuration update must not destroy the previous
        configuration").
        """
        if source_id not in self._sources:
            raise KeyError(f"unknown source_id: {source_id}")
        prior_versions = self._versions[source_id]
        next_version_number = max(v.version for v in prior_versions) + 1
        prior = prior_versions[-1]

        # Start from the prior version's values, apply only the fields the caller wants changed --
        # this is NOT an in-place mutation of `prior`; it produces an entirely new object.
        merged = {
            "macro_channel": prior.macro_channel,
            "platform": prior.platform,
            "subdomain": prior.subdomain,
            "source_url": prior.source_url,
            "trust_level": prior.trust_level,
            "security_classification": prior.security_classification,
            "configuration_version": prior.configuration_version,
            "connector_id": prior.connector_id,
            "connector_version": prior.connector_version,
        }
        merged.update(version_fields)

        new_version = SourceVersion(
            source_version_id=new_id("srcv-"),
            source_id=source_id,
            version=next_version_number,
            **merged,
        )
        self._versions[source_id].append(new_version)
        self._sources[source_id].latest_source_version_id = new_version.source_version_id
        self._sources[source_id].updated_at = datetime.now(timezone.utc).isoformat()

        evt = make_event(
            event_type="SourceUpdated",
            aggregate_type="source",
            aggregate_id=source_id,
            producer="SourceRegistry",
            payload={"source_id": source_id, "new_version": next_version_number, "superseded_version": prior.version},
        )
        self._event_log.append(evt)
        return new_version

    def add_policy_version(self, source_id: str, policy: SourcePolicy) -> None:
        self._policies.setdefault(source_id, []).append(policy)

    def add_endpoint(self, source_id: str, endpoint: SourceEndpoint) -> None:
        self._endpoints.setdefault(source_id, []).append(endpoint)

    # -- Retrieval -----------------------------------------------------------

    def get_source(self, source_id: str) -> Optional[Source]:
        return self._sources.get(source_id)

    def get_all_versions(self, source_id: str) -> list[SourceVersion]:
        """Full, un-truncated version history -- 'latest' is a pointer, not a deletion of history."""
        return list(self._versions.get(source_id, []))

    def get_latest_version(self, source_id: str) -> Optional[SourceVersion]:
        versions = self._versions.get(source_id, [])
        return versions[-1] if versions else None

    def get_policies(self, source_id: str) -> list[SourcePolicy]:
        return list(self._policies.get(source_id, []))

    def get_endpoints(self, source_id: str) -> list[SourceEndpoint]:
        return list(self._endpoints.get(source_id, []))

    def list_sources(self) -> list[Source]:
        return list(self._sources.values())

    # -- Health ----------------------------------------------------------------

    def record_health_event(self, source_id: str, health_event: SourceHealthEvent) -> None:
        """Append a health observation. Never overwrites prior health history (Step 3 Section 9)."""
        self._health_events.setdefault(source_id, []).append(health_event)

    def get_health_history(self, source_id: str) -> list[SourceHealthEvent]:
        return list(self._health_events.get(source_id, []))

    def get_latest_health(self, source_id: str) -> Optional[SourceHealthEvent]:
        events = self._health_events.get(source_id, [])
        return events[-1] if events else None

    def health_check(self) -> HealthResult:
        return simple_health("source_registry", HealthStatus.HEALTHY, detail=f"{len(self._sources)} sources registered")
