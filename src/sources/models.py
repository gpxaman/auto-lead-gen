"""
Source Registry data model. Per Step 3 Sections 5-7.

A SOURCE is a provider/location/channel/platform. It is explicitly NOT a lead -- do not confuse
the two (Step 3 Section 5). Where a value is not known, use the literal string "UNKNOWN", never
an invented default (Step 3 Section 6).
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from src.common.ids import new_id

UNKNOWN = "UNKNOWN"


class SourceType(str, Enum):
    """
    Broad category of where a source sits in docs/source-extraction/platforms.md's taxonomy.
    Open enum -- new values may be added; existing ones never removed (docs/database/
    integrity-rules.md).
    """
    FREELANCE_MARKETPLACE = "FREELANCE_MARKETPLACE"
    B2B_TRADE_DIRECTORY = "B2B_TRADE_DIRECTORY"
    ON_DEMAND_MFG_NETWORK = "ON_DEMAND_MFG_NETWORK"
    NPD_BROKER = "NPD_BROKER"
    AGENCY_DIRECTORY = "AGENCY_DIRECTORY"
    PUBLIC_TENDER = "PUBLIC_TENDER"
    CROWDFUNDING = "CROWDFUNDING"
    PATENT_REGISTRY = "PATENT_REGISTRY"
    COMMUNITY_FORUM = "COMMUNITY_FORUM"
    STARTUP_ECOSYSTEM = "STARTUP_ECOSYSTEM"
    SYNTHETIC_TEST = "SYNTHETIC_TEST"  # PROPOSED_EXTENSION -- for fixtures/testing only, never real production data


class SourceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DEPRECATED = "DEPRECATED"
    UNDER_EVALUATION = "UNDER_EVALUATION"


@dataclass
class SourceEndpoint:
    """WHERE, concretely, to reach a source (a URL, a file path for synthetic sources, etc.)."""
    endpoint_id: str
    source_id: str
    endpoint_type: str  # e.g. 'https_url', 'file_path', 'api_base_url'
    value: str


@dataclass
class SourcePolicy:
    """
    Per Step 3 Section 36. Versioned. All fields default to UNKNOWN/None rather than an invented
    value when the real-world policy is not yet documented.
    """
    policy_id: str
    source_id: str
    version: int
    access_method: str = UNKNOWN
    authentication_required: Optional[bool] = None
    rate_limit: Optional[dict] = None  # {requests, window_seconds, backoff, cooldown, concurrency}
    compliance_policy: str = UNKNOWN
    allowed_content: str = UNKNOWN
    security_policy: str = UNKNOWN
    normalizer_version: Optional[str] = None
    schema_version: Optional[str] = None
    connector_id: Optional[str] = None
    schedule: str = UNKNOWN
    retry_policy: Optional[dict] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class SourceHealthEvent:
    """One point-in-time health observation. Append-only -- see src/sources/registry.py."""
    event_id: str
    source_id: str
    recorded_at: str
    last_success: Optional[str] = None
    last_failure: Optional[str] = None
    success_count: int = 0
    failure_count: int = 0
    latency_ms: Optional[float] = None
    rate_limit_state: str = UNKNOWN
    availability: str = UNKNOWN
    authentication_state: str = UNKNOWN
    schema_state: str = UNKNOWN
    last_observed_content_hash: Optional[str] = None


@dataclass
class SourceVersion:
    """
    A versioned configuration snapshot of a Source. Updating a source's configuration creates a
    NEW SourceVersion row; the previous one is never destroyed (Step 3 Section 7).
    """
    source_version_id: str
    source_id: str
    version: int
    macro_channel: str = UNKNOWN
    platform: str = UNKNOWN
    subdomain: Optional[str] = None
    source_url: Optional[str] = None
    trust_level: str = "OBSERVED"  # per docs/database/logical-data-model.md's 12-value trust enum
    security_classification: str = "SENSITIVE"  # default per docs/database/security.md: raw external content
    configuration_version: Optional[str] = None
    connector_id: Optional[str] = None
    connector_version: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Source:
    """
    The stable identity of a source. Field-for-field per Step 3 Section 6's required list, plus
    a pointer to its latest SourceVersion (never a destructive overwrite of history).
    """
    source_id: str
    source_type: SourceType
    name: str
    display_name: str
    status: SourceStatus
    latest_source_version_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def new_source(source_type: SourceType, name: str, display_name: Optional[str] = None) -> Source:
    return Source(
        source_id=new_id("src-"),
        source_type=source_type,
        name=name,
        display_name=display_name or name,
        status=SourceStatus.UNDER_EVALUATION,
    )
