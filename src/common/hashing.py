"""
Content hashing. Per Step 3 Section 13: every raw payload must receive a cryptographic content
hash, computed from the preserved RAW representation -- never from a normalized/summarized one.
"""
import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class ContentHash:
    algorithm: str
    hash: str
    input_representation: str  # exactly what bytes were hashed, for auditability


def compute_content_hash(raw_payload, content_type: str) -> ContentHash:
    """
    Compute a deterministic SHA-256 hash of the RAW payload as received.

    - If raw_payload is already bytes/str, it is hashed exactly as given.
    - If raw_payload is a dict/list (already-parsed JSON), it is re-serialized with sorted keys
      and no extraneous whitespace to get a DETERMINISTIC byte representation -- this is hashing
      the raw JSON structure itself, not a normalized/summarized derivative of it. This is the
      one legitimate exception the architecture allows (docs/database/schema.sql documents
      raw_payload as JSONB): the *content* is unchanged, only its serialization is canonicalized
      so identical content always hashes identically regardless of key ordering on the wire.
    """
    if isinstance(raw_payload, bytes):
        data = raw_payload
        input_representation = f"raw_bytes(len={len(data)})"
    elif isinstance(raw_payload, str):
        data = raw_payload.encode("utf-8")
        input_representation = "raw_text_utf8"
    else:
        # dict/list -- canonical JSON serialization of the exact same content
        data = json.dumps(raw_payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        input_representation = "canonical_json(sort_keys=true)"

    digest = hashlib.sha256(data).hexdigest()
    return ContentHash(algorithm="sha256", hash=digest, input_representation=input_representation)
