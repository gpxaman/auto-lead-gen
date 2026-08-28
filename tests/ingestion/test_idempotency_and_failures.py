"""
Retry / idempotency / partial-failure tests. Per Step 3 Sections 28-30.
"""
import unittest

from src.raw.models import IngestionRunStatus
from src.sources.models import SourceType
from tests.helpers import ScriptedConnector, build_stack, synthetic_connector


class TestIdempotency(unittest.TestCase):
    def test_retry_of_identical_delivery_deduplicates_events_but_stays_auditable(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        run1 = stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["001_first_observation"],
        )
        run2 = stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["001_first_observation"],
        )
        # Second delivery of byte-identical content -> classified as EXACT_DUPLICATE, not a
        # second semantic raw_record -- this IS the idempotency guarantee.
        self.assertEqual(run2.records_duplicated, 1)

        raw_versions = stack.raw_store.get_version_chain(source.source_id, "001_first_observation")
        self.assertEqual(len(raw_versions), 1, "idempotent retry must not create a second raw_record")

        # But BOTH ingestion runs and BOTH ingestion items remain in history -- the retry is
        # auditable, not silently invisible (Step 3 Section 28).
        self.assertEqual(len(stack.run_store.all()), 2)
        items_for_identifier = [i for i in stack.item_store.all() if i.raw_record_id == raw_versions[0].record_id]
        self.assertEqual(len(items_for_identifier), 2)

    def test_event_log_deduplicates_by_idempotency_key(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()
        stack.engine.run_ingestion(source.source_id, connector, "synthetic-file-connector", "1.0", identifiers=["001_first_observation"])
        stack.engine.run_ingestion(source.source_id, connector, "synthetic-file-connector", "1.0", identifiers=["001_first_observation"])

        raw_events = stack.event_log.by_type("RawRecordReceived")
        keys = [e.idempotency_key for e in raw_events if e.idempotency_key]
        self.assertEqual(len(keys), len(set(keys)), "no two stored events should share an idempotency_key")


class TestPartialFailure(unittest.TestCase):
    def test_batch_with_one_bad_identifier_is_partial_not_total_failure(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        run = stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["001_first_observation", "999_does_not_exist"],
        )
        self.assertEqual(run.status, IngestionRunStatus.PARTIAL)
        self.assertEqual(run.records_accepted, 1)
        self.assertEqual(run.records_failed, 1)
        self.assertEqual(run.records_received, 2)

    def test_all_bad_identifiers_is_total_failure_not_silently_success(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = ScriptedConnector({"bad-1": [None], "bad-2": [None]})

        run = stack.engine.run_ingestion(source.source_id, connector, "scripted", "1.0", identifiers=["bad-1", "bad-2"])
        self.assertEqual(run.status, IngestionRunStatus.FAILED)
        self.assertEqual(run.records_accepted, 0)
        self.assertEqual(run.records_failed, 2)

    def test_failed_runs_are_never_erased(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = ScriptedConnector({"bad-1": [None]})
        run = stack.engine.run_ingestion(source.source_id, connector, "scripted", "1.0", identifiers=["bad-1"])

        self.assertIsNotNone(stack.run_store.get(run.ingestion_run_id))
        self.assertEqual(stack.run_store.get(run.ingestion_run_id).status, IngestionRunStatus.FAILED)


if __name__ == "__main__":
    unittest.main()
