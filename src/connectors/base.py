"""
Connector interface. Per Step 3 Sections 8, 38-39.

A connector's ONLY job is safe acquisition. Per Step 3 Section 39, a connector must NOT:
  - discard fields
  - classify the lead
  - make business decisions
  - rewrite evidence
  - decide whether a lead is qualified

This is enforced by the interface shape itself: fetch()/parse() return a RawFetchResult carrying
the payload exactly as acquired plus acquisition metadata only -- there is no method on this
interface through which a connector could express a classification or business judgment.

Per Step 3 Section 38: this is the ABSTRACTION only. No live platform scraper is implemented here
-- see src/connectors/synthetic_file_connector.py for the one synthetic connector Step 3 requires
for testing.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from src.common.ids import new_id


class ConnectorType(str, Enum):
    """
    Architectural categories of acquisition mechanism (Step 3 Section 8). These are
    PROPOSED_EXTENSION categories -- the source document never enumerates connector types this
    way; it describes scraping tools (Playwright, Firecrawl) narratively, not as a typed taxonomy.
    """
    API = "API"
    WEB = "WEB"
    RSS = "RSS"
    FILE = "FILE"
    WEBHOOK = "WEBHOOK"
    MANUAL = "MANUAL"
    OTHER = "OTHER"


@dataclass
class ConnectorVersion:
    connector_version_id: str
    connector_id: str
    version: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ConnectorHealth:
    connector_id: str
    status: str  # HEALTHY | DEGRADED | UNHEALTHY | UNKNOWN
    detail: str
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RawFetchResult:
    """
    Exactly what a connector is allowed to return: the acquired payload plus pure acquisition
    metadata. No classification field exists on this dataclass by design.
    """
    source_identifier: str
    raw_payload: Any  # bytes | str | dict | list -- whatever was actually received, unmodified
    content_type: str
    source_url: Optional[str] = None
    request_metadata: Optional[dict] = None
    response_metadata: Optional[dict] = None
    retrieved_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Connector(ABC):
    """Abstract connector interface: discover() -> fetch() -> parse(), per Step 3 Section 39."""

    connector_type: ConnectorType

    @abstractmethod
    def discover(self) -> list[str]:
        """Return a list of source_identifier strings available to fetch. Discovery only -- no
        content is retrieved or judged here."""
        raise NotImplementedError

    @abstractmethod
    def fetch(self, source_identifier: str) -> RawFetchResult:
        """Retrieve the raw content for one identifier. Must return the FULL payload, unmodified."""
        raise NotImplementedError

    def parse(self, fetch_result: RawFetchResult) -> RawFetchResult:
        """
        Default parse() is a no-op pass-through -- 'parsing' at the connector layer means, at
        most, extracting the payload from a transport envelope (e.g. unwrapping an HTTP response
        body), never restructuring/classifying/summarizing content. Connectors that need real
        unwrapping should override this while preserving the same non-judgment constraint.
        """
        return fetch_result
