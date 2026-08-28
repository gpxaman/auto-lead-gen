"""Validates IngestionEnvelope instances against docs/contracts/schemas/ingestion-envelope.v1.schema.json."""
import json
import unittest
from pathlib import Path

import jsonschema

from src.common.hashing import compute_content_hash
from src.ingestion.envelope import build_envelope

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "docs" / "contracts" / "schemas" / "ingestion-envelope.v1.schema.json"


class TestIngestionEnvelopeSchema(unittest.TestCase):
    def test_envelope_validates_against_json_schema(self):
        schema = json.loads(SCHEMA_PATH.read_text())
        content_hash = compute_content_hash({"a": 1}, "application/json")
        envelope = build_envelope(
            ingestion_item_id="item-1", ingestion_run_id="run-1", source_id="src-1",
            received_at="2026-08-10T00:00:00Z", observed_at="2026-08-10T00:00:00Z",
            content_type="application/json", content_hash=content_hash,
            security_status="SAFE", schema_status="KNOWN", duplicate_status="DISTINCT_RECORD",
            connector_id="synthetic-file-connector", connector_version="1.0",
            raw_record_id="rr-1", correlation_id="corr-1", configuration_version="CONFIG-V1",
        )
        jsonschema.validate(instance=envelope.to_dict(), schema=schema)  # raises on failure


if __name__ == "__main__":
    unittest.main()
