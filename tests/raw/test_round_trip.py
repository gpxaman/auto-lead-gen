"""
Mandatory raw payload round-trip test. Per Step 3 Section 42:
  RAW INPUT -> INGEST -> STORE -> RETRIEVE
must be byte-for-byte equivalent (or, for structured data, exactly content- and hash-equivalent)
to what was received.
"""
import json
import unittest

from src.common.hashing import compute_content_hash
from src.sources.models import SourceType
from tests.helpers import FIXTURES_DIR, build_stack, synthetic_connector


class TestRawRoundTrip(unittest.TestCase):
    def _run_single(self, stack, identifier):
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()
        stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=[identifier],
        )
        return [r for r in stack.raw_store.all() if r.source_identifier == identifier][0]

    def test_json_payload_round_trip_exact(self):
        stack = build_stack()
        rec = self._run_single(stack, "001_first_observation")

        original_bytes = (FIXTURES_DIR / "001_first_observation.json").read_bytes()
        original_parsed = json.loads(original_bytes)

        # Structured comparison: not just "some fields match" -- the ENTIRE parsed structure,
        # per Step 3 Section 42's explicit instruction not to compare only parsed fields.
        self.assertEqual(rec.raw_payload, original_parsed)

        # Hash verification: recompute the hash from the retrieved raw_payload and confirm it
        # matches the stored content_hash exactly.
        recomputed = compute_content_hash(rec.raw_payload, rec.content_type)
        self.assertEqual(recomputed.hash, rec.content_hash)

    def test_html_like_text_round_trip_byte_for_byte(self):
        stack = build_stack()
        rec = self._run_single(stack, "007_html_like")

        original_text = (FIXTURES_DIR / "007_html_like.html").read_text(encoding="utf-8")
        self.assertEqual(rec.raw_payload, original_text, "text content must round-trip byte-for-byte (as decoded text)")

    def test_malformed_content_round_trip_preserves_exact_text(self):
        stack = build_stack()
        rec = self._run_single(stack, "003_malformed")
        original_text = (FIXTURES_DIR / "003_malformed.json").read_text(encoding="utf-8")
        self.assertEqual(rec.raw_payload, original_text)


if __name__ == "__main__":
    unittest.main()
