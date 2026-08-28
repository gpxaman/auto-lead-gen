"""
Deterministic security inspector. Per Step 3 Sections 18, 20, 58: the raw acquisition layer must
NOT depend on an LLM. This is a keyword/pattern-based, fully deterministic detector -- not an AI
classifier. It never modifies the raw payload; it produces a SEPARATE analysis record (Step 3
Section 18: "Store the security analysis separately").

CRITICAL TRUST-BOUNDARY RULE (Step 3 Section 20): this module's output is used to route content
to QUARANTINE or PROCESS. It NEVER interprets external content as an instruction to this system.
Detected phrases are treated purely as DATA to flag, never executed, never fed into any prompt
that would grant them authority. There is no code path anywhere in this module (or the rest of
Step 3) that takes matched text and uses it to alter this system's own behavior beyond routing to
SAFE/SUSPICIOUS/MALICIOUS/UNKNOWN.
"""
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from src.common.ids import new_id


class SecurityVerdict(str, Enum):
    SAFE = "SAFE"
    SUSPICIOUS = "SUSPICIOUS"
    MALICIOUS = "MALICIOUS"
    UNKNOWN = "UNKNOWN"


# Deterministic pattern set. Each entry: (pattern, severity_if_matched, detection_type).
# These are DATA PATTERNS being searched FOR, not instructions being followed.
_INJECTION_PATTERNS = [
    (re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions", re.IGNORECASE), "MALICIOUS", "PROMPT_INJECTION"),
    (re.compile(r"\bsystem\s*(message|prompt|instruction)\b", re.IGNORECASE), "SUSPICIOUS", "PROMPT_INJECTION"),
    (re.compile(r"\bexecute\s+(command|code|script)\b", re.IGNORECASE), "MALICIOUS", "COMMAND_INJECTION"),
    (re.compile(r"\bchange\s+(the\s+)?configuration\b", re.IGNORECASE), "SUSPICIOUS", "CONFIG_TAMPER_ATTEMPT"),
    (re.compile(r"\bdeveloper\s+(mode|instructions?)\b", re.IGNORECASE), "SUSPICIOUS", "PROMPT_INJECTION"),
    (re.compile(r"\byou\s+are\s+now\b", re.IGNORECASE), "SUSPICIOUS", "ROLE_OVERRIDE_ATTEMPT"),
    (re.compile(r"\bact\s+as\s+(if\s+you\s+are\s+)?an?\b", re.IGNORECASE), "SUSPICIOUS", "ROLE_OVERRIDE_ATTEMPT"),
]

_ANTI_BOT_TRAP_PATTERN = re.compile(
    r"(start\s+your\s+(proposal|response|bid)\s+with|solve\s+this\s+(math|puzzle)|type\s+the\s+word)",
    re.IGNORECASE,
)


@dataclass
class SecurityAnalysisResult:
    """Stored SEPARATELY from the raw payload -- see src/raw/models.py, this is never merged
    into RawRecord.raw_payload."""
    analysis_id: str
    verdict: SecurityVerdict
    detections: list[dict] = field(default_factory=list)  # [{pattern_type, matched_text, severity}]
    contains_anti_bot_trap: bool = False
    analyzed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    detector: str = "DeterministicKeywordInspector"
    detector_version: str = "1.0"


def _extract_text(raw_payload) -> str:
    """Flatten a payload (str, dict, list, bytes) into a searchable text blob. This is READ-ONLY
    extraction for inspection purposes -- the original raw_payload object is never touched."""
    if isinstance(raw_payload, bytes):
        return raw_payload.decode("utf-8", errors="replace")
    if isinstance(raw_payload, str):
        return raw_payload
    if isinstance(raw_payload, (dict, list)):
        import json
        return json.dumps(raw_payload, default=str)
    return str(raw_payload)


def inspect(raw_payload) -> SecurityAnalysisResult:
    """
    Deterministically inspect raw_payload for injection-style and anti-bot-trap patterns.
    Read-only: does not modify raw_payload. No LLM call anywhere in this function.
    """
    text = _extract_text(raw_payload)
    detections = []
    highest_severity = "SAFE"

    for pattern, severity, detection_type in _INJECTION_PATTERNS:
        match = pattern.search(text)
        if match:
            detections.append({
                "pattern_type": detection_type,
                "matched_text": match.group(0),
                "severity": severity,
            })
            if severity == "MALICIOUS":
                highest_severity = "MALICIOUS"
            elif severity == "SUSPICIOUS" and highest_severity != "MALICIOUS":
                highest_severity = "SUSPICIOUS"

    contains_anti_bot_trap = bool(_ANTI_BOT_TRAP_PATTERN.search(text))

    verdict = SecurityVerdict(highest_severity)
    return SecurityAnalysisResult(
        analysis_id=new_id("sec-"),
        verdict=verdict,
        detections=detections,
        contains_anti_bot_trap=contains_anti_bot_trap,
    )
