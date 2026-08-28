"""
Provenance test. Per Step 3 Section 44: verify
  OBSERVATION -> RAW RECORD -> INGESTION ITEM -> INGESTION RUN -> SOURCE -> CONNECTOR ->
  CONNECTOR VERSION -> CONFIGURATION
is fully traceable.
"""
import unittest

from src.provenance.trace import trace_observation
from src.sources.models import SourceType
from tests.helpers import build_stack, synthetic_connector


class TestProvenance(unittest.TestCase):
    def test_full_chain_is_traceable(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        run = stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["001_first_observation"],
        )
        raw_record = [r for r in stack.raw_store.all() if r.source_identifier == "001_first_observation"][0]
        observation = stack.observation_store.by_raw_record(raw_record.record_id)[0]

        trace = trace_observation(
            observation.observation_id,
            stack.observation_store, stack.raw_store, stack.item_store, stack.run_store, stack.source_registry,
        )

        self.assertTrue(trace.complete, f"provenance chain incomplete, missing: {trace.missing_links}")
        self.assertEqual(trace.raw_record_id, raw_record.record_id)
        self.assertEqual(trace.ingestion_run_id, run.ingestion_run_id)
        self.assertEqual(trace.source_id, source.source_id)
        self.assertEqual(trace.connector_id, "synthetic-file-connector")
        self.assertEqual(trace.connector_version, "1.0")
        self.assertEqual(trace.configuration_version, "CONFIG-V1")

    def test_trace_of_unknown_observation_reports_incomplete(self):
        stack = build_stack()
        trace = trace_observation(
            "does-not-exist", stack.observation_store, stack.raw_store, stack.item_store, stack.run_store, stack.source_registry,
        )
        self.assertFalse(trace.complete)
        self.assertIn("observation", trace.missing_links)


if __name__ == "__main__":
    unittest.main()
