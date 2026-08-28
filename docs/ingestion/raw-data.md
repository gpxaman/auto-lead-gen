# Raw Data

Per Step 3 Sections 12-13, 24. Implementation: `src/raw/models.py::RawRecord`,
`src/raw/store.py::RawRecordStore`, `src/common/hashing.py`.

## Reuses the Step 2 design (Step 3 Section 12 explicit)

`RawRecord`'s fields match `docs/database/schema.sql`'s `raw_record` table exactly. This is not a
new/competing implementation.

## Content type handling (Step 3 Section 12)

- JSON payloads: stored as the complete parsed structure (a Python `dict`/`list`), never truncated.
- Text/HTML: stored as the complete decoded string.
- No binary handling is implemented in Step 3 (no fixture requires it); a future connector needing
  binary preservation would extend `RawFetchResult.raw_payload` to carry a blob reference, per the
  architecture's "preserve the binary reference where the storage architecture supports it" guidance
  — not implemented now because no requirement exercises it yet, consistent with not inventing
  unneeded scope.

## Content hashing (Step 3 Section 13)

`compute_content_hash()` — SHA-256, computed from the RAW representation:
- `bytes` -> hashed exactly as given.
- `str` -> UTF-8 encoded, then hashed.
- `dict`/`list` -> re-serialized with `sort_keys=True` for a DETERMINISTIC byte representation
  (so identical JSON content always hashes identically regardless of wire key ordering), then
  hashed. This canonicalizes SERIALIZATION only — the content itself is never altered.

Stores `algorithm`, `hash`, `input_representation` — exactly Step 3 Section 13's required fields.

## Common Envelope + Source-Specific Payload (Step 3 Section 24)

`src/observations/normalizer.py` wraps a dict payload as
`{"common_envelope": {...}, "source_specific_payload": <verbatim original>}` — the envelope
carries ONLY infrastructure metadata (schema detection results); the original payload is never
restructured.

## Source IDs / Requirements

SRC-000009, SRC-000013. REQ-000009.
