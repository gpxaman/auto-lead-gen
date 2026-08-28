"""
End-to-end pipeline tests covering the 10 synthetic scenarios required by Step 3 Section 41.
"""
import unittest

from src.raw.models import DuplicateStatus, IngestionRunStatus, ProcessingStatus, SchemaStatus, SecurityStatus
from src.sources.models import SourceType
from tests.helpers import build_stack, synthetic_connector


class TestEngineFirstObservation(unittest.TestCase):
    """Scenario 1: First observation."""

    def test_first_observation_accepted_and_observation_created(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        run = stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["001_first_observation"],
        )
        self.assertEqual(run.status, IngestionRunStatus.COMPLETED)
        self.assertEqual(run.records_accepted, 1)

        raw_records = [r for r in stack.raw_store.all() if r.source_identifier == "001_first_observation"]
        self.assertEqual(len(raw_records), 1)
        self.assertEqual(raw_records[0].security_status, SecurityStatus.SAFE)

        observations = stack.observation_store.by_raw_record(raw_records[0].record_id)
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0].observation_type, "lead_candidate")
        # Full source-specific payload preserved verbatim inside the normalized envelope
        self.assertIn("source_specific_payload", observations[0].normalized_payload)
        self.assertEqual(
            observations[0].normalized_payload["source_specific_payload"]["lead_id"],
            "synthetic-lead-0001",
        )


class TestEngineUnknownSchema(unittest.TestCase):
    """Scenario 4: Unknown schema -- must NOT be discarded."""

    def test_unknown_schema_preserved(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        run = stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["002_unknown_schema"],
        )
        self.assertEqual(run.records_accepted, 1)  # still ACCEPTED -- unknown schema is not a failure

        raw_records = [r for r in stack.raw_store.all() if r.source_identifier == "002_unknown_schema"]
        self.assertEqual(len(raw_records), 1)
        items = [i for i in stack.item_store.all() if i.raw_record_id == raw_records[0].record_id]
        self.assertEqual(items[0].schema_status, SchemaStatus.UNKNOWN)

        observations = stack.observation_store.by_raw_record(raw_records[0].record_id)
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0].observation_type, "unknown_content")
        # Full unrecognized payload still preserved verbatim
        self.assertIn("some_future_platform_format", observations[0].normalized_payload["source_specific_payload"])


class TestEngineMalformedPayload(unittest.TestCase):
    """Scenario 5: Malformed payload -- preserved as raw text, not discarded."""

    def test_malformed_json_preserved_as_text(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        run = stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["003_malformed"],
        )
        self.assertEqual(run.records_accepted, 1)

        raw_records = [r for r in stack.raw_store.all() if r.source_identifier == "003_malformed"]
        self.assertEqual(len(raw_records), 1)
        # Malformed JSON fell back to text/plain, but the exact original text is preserved
        self.assertIsInstance(raw_records[0].raw_payload, str)
        self.assertIn("this is not valid json", raw_records[0].raw_payload)


class TestEngineSecurityQuarantine(unittest.TestCase):
    """Scenario 6: Security quarantine."""

    def test_suspicious_content_is_quarantined_not_discarded(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        run = stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["004_security_suspicious"],
        )
        self.assertEqual(run.records_quarantined, 1)
        self.assertEqual(run.records_accepted, 0)

        raw_records = [r for r in stack.raw_store.all() if r.source_identifier == "004_security_suspicious"]
        self.assertEqual(len(raw_records), 1, "quarantined content must still be stored as a raw record, not dropped")
        self.assertEqual(raw_records[0].security_status, SecurityStatus.MALICIOUS)

        qrecords = stack.quarantine_store.by_raw_record(raw_records[0].record_id)
        self.assertEqual(len(qrecords), 1)
        # No Observation should be produced for quarantined content (never reaches normalization)
        self.assertEqual(stack.observation_store.by_raw_record(raw_records[0].record_id), [])


class TestEngineMultipleSchemaVersions(unittest.TestCase):
    """Scenario 10: Multiple schema versions coexisting."""

    def test_schema_002_and_003_both_detected_distinctly(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["005_multi_schema_002", "006_multi_schema_003"],
        )

        rec_002 = [r for r in stack.raw_store.all() if r.source_identifier == "005_multi_schema_002"][0]
        rec_003 = [r for r in stack.raw_store.all() if r.source_identifier == "006_multi_schema_003"][0]
        self.assertEqual(rec_002.schema_version, "SCHEMA-002")
        self.assertEqual(rec_003.schema_version, "SCHEMA-003")
        # Neither was forced into the other's shape or into SCHEMA-005
        self.assertNotEqual(rec_002.schema_version, rec_003.schema_version)


class TestEnginePartialSchema(unittest.TestCase):
    def test_partial_schema005_not_silently_upgraded_to_known(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["008_partial_schema005"],
        )
        rec = [r for r in stack.raw_store.all() if r.source_identifier == "008_partial_schema005"][0]
        items = [i for i in stack.item_store.all() if i.raw_record_id == rec.record_id]
        self.assertEqual(items[0].schema_status, SchemaStatus.PARTIAL)


class TestEngineHtmlLikeContent(unittest.TestCase):
    def test_html_like_content_preserved_unstructured(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["007_html_like"],
        )
        rec = [r for r in stack.raw_store.all() if r.source_identifier == "007_html_like"][0]
        self.assertIn("Synthetic Listing", rec.raw_payload)
        obs = stack.observation_store.by_raw_record(rec.record_id)
        self.assertEqual(obs[0].normalized_payload, None)  # PASS_THROUGH_UNSTRUCTURED, not force-normalized


if __name__ == "__main__":
    unittest.main()
