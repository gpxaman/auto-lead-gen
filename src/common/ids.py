"""
Identifier generation. Per docs/architecture/open-decisions.md, non-semantic, globally unique
identifiers (uuid4) are used throughout -- no business meaning is ever encoded into an ID
(docs/database/versioning.md's identifier-strategy rule).
"""
import uuid


def new_id(prefix: str = "") -> str:
    """Generate a globally unique, non-semantic identifier. Optional human-readable prefix for
    debugging only (e.g. 'rr-' for raw_record) -- never relied upon for business logic."""
    raw = str(uuid.uuid4())
    return f"{prefix}{raw}" if prefix else raw
