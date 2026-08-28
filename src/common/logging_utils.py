"""
Structured logging with mandatory secret redaction.

Per Step 3 Section 49: every ingestion operation must produce structured logs carrying
ingestion_run_id/ingestion_item_id/source_id/connector_id/event_id/correlation_id/status/
duration/error_code. Must NEVER log passwords, API keys, tokens, secrets, private credentials,
or raw sensitive payloads unnecessarily.
"""
import json
import logging
import re

logger = logging.getLogger("iechm_lios.ingestion")
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

# Field-name patterns whose VALUES are always redacted, regardless of context.
_SECRET_KEY_PATTERN = re.compile(
    r"(password|api[_-]?key|secret|token|credential|authorization|auth[_-]?header)", re.IGNORECASE
)
_REDACTED = "***REDACTED***"


def redact(obj):
    """Recursively redact values whose key looks secret-like. Structure-preserving otherwise."""
    if isinstance(obj, dict):
        return {
            k: (_REDACTED if _SECRET_KEY_PATTERN.search(str(k)) else redact(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj


def log_structured(event: str, **fields) -> None:
    """
    Emit one structured JSON log line. `fields` is redacted before serialization -- this is the
    ONLY path ingestion code should use to log operational metadata, so redaction cannot be
    accidentally skipped by a call site.
    """
    safe_fields = redact(fields)
    record = {"event": event, **safe_fields}
    logger.info(json.dumps(record, default=str, sort_keys=True))
