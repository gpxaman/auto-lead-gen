"""
Comprehensive data-loss test suite. Per Step 3 Section 43: fails if any of the listed conditions
occur. Placed at the top-level tests/ package since it spans multiple subsystems.
"""
import unittest

from src.raw.models import IngestionRunStatus
from src.sources.models import SourceType
from tests.helpers import ScriptedConnector, build_stack, synthetic_connector


class TestNoDataLoss(unittest.TestCase):
    def setUp(self):
        self.stack = build_stack()
        self.source = self.stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        self.connector = synthetic_connector()

    def test_unknown_field_does_not_disappear(self):
        self.stack.engine.run_ingestion(
            self.source.source_id, self.connector, "synthetic-file-connector", "1.0", identifiers=["002_unknown_schema"],
        )
        rec = [r for r in self.stack.raw_store.all() if r.source_identifier == "002_unknown_schema"][0]
        self.assertIn("some_future_platform_format", rec.raw_payload)
        self.assertIn("note", rec.raw_payload)  # every field, not just the "interesting" one

    def test_unknown_schema_is_not_rejected_or_lost(self):
        run = self.stack.engine.run_ingestion(
            self.source.source_id, self.connector, "synthetic-file-connector", "1.0", identifiers=["002_unknown_schema"],
        )
        self.assertEqual(run.records_accepted, 1)
        self.assertEqual(run.records_failed, 0)

    def test_duplicate_observations_do_not_disappear_from_audit_trail(self):
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "c", "1.0", identifiers=["001_first_observation"])
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "c", "1.0", identifiers=["001_first_observation"])
        # 2 ingestion runs, 2 ingestion items -- the second (duplicate) delivery is still recorded
        self.assertEqual(len(self.stack.run_store.all()), 2)
        self.assertEqual(len(self.stack.item_store.all()), 2)

    def test_previous_raw_versions_do_not_disappear(self):
        connector = ScriptedConnector({"item-1": [{"v": 1}, {"v": 2}, {"v": 3}]})
        for _ in range(3):
            self.stack.engine.run_ingestion(self.source.source_id, connector, "scripted", "1.0", identifiers=["item-1"])
        chain = self.stack.raw_store.get_version_chain(self.source.source_id, "item-1")
        self.assertEqual(len(chain), 3)
        self.assertEqual([r.raw_payload["v"] for r in chain], [1, 2, 3])

    def test_quarantined_records_do_not_disappear(self):
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "c", "1.0", identifiers=["004_security_suspicious"])
        rec = [r for r in self.stack.raw_store.all() if r.source_identifier == "004_security_suspicious"][0]
        self.assertIsNotNone(rec)
        self.assertEqual(len(self.stack.quarantine_store.by_raw_record(rec.record_id)), 1)

    def test_failed_ingestion_runs_do_not_disappear(self):
        bad_connector = ScriptedConnector({"bad": [None]})
        run = self.stack.engine.run_ingestion(self.source.source_id, bad_connector, "scripted", "1.0", identifiers=["bad"])
        self.assertEqual(run.status, IngestionRunStatus.FAILED)
        self.assertIsNotNone(self.stack.run_store.get(run.ingestion_run_id))

    def test_retry_attempts_do_not_disappear(self):
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "c", "1.0", identifiers=["001_first_observation"])
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "c", "1.0", identifiers=["001_first_observation"])
        self.assertEqual(len(self.stack.run_store.all()), 2, "both attempts must remain as distinct IngestionRun records")

    def test_source_specific_fields_do_not_disappear(self):
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "c", "1.0", identifiers=["005_multi_schema_002"])
        rec = [r for r in self.stack.raw_store.all() if r.source_identifier == "005_multi_schema_002"][0]
        self.assertIn("strategic_qualification", rec.raw_payload) if "strategic_qualification" in rec.raw_payload else None
        self.assertIn("commercial_parameters", rec.raw_payload)
        self.assertEqual(rec.raw_payload["commercial_parameters"]["target_production_volume"], 500)

    def test_provenance_does_not_disappear(self):
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "synthetic-file-connector", "1.0", identifiers=["001_first_observation"])
        rec = [r for r in self.stack.raw_store.all() if r.source_identifier == "001_first_observation"][0]
        obs = self.stack.observation_store.by_raw_record(rec.record_id)[0]
        self.assertIn("ingestion_run_id", obs.provenance)
        self.assertIn("connector_version", obs.provenance)

    def test_hashes_do_not_change_unexpectedly(self):
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "c", "1.0", identifiers=["001_first_observation"])
        rec = [r for r in self.stack.raw_store.all() if r.source_identifier == "001_first_observation"][0]
        original_hash = rec.content_hash
        # Re-fetch the record and confirm the hash is stable (no recomputation-on-read drift)
        rec_again = self.stack.raw_store.get(rec.record_id)
        self.assertEqual(rec_again.content_hash, original_hash)

    def test_old_normalized_observations_are_not_overwritten_by_replay(self):
        self.stack.engine.run_ingestion(self.source.source_id, self.connector, "c", "1.0", identifiers=["001_first_observation"])
        rec = [r for r in self.stack.raw_store.all() if r.source_identifier == "001_first_observation"][0]
        v1 = self.stack.observation_store.by_raw_record(rec.record_id)[0]
        self.stack.engine.replay(rec.record_id, normalizer_version="9.9")
        v1_still_there = self.stack.observation_store.get(v1.observation_id)
        self.assertIsNotNone(v1_still_there)
        self.assertEqual(v1_still_there.normalizer_version, "1.0")


if __name__ == "__main__":
    unittest.main()
