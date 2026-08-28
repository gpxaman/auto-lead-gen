"""
Replay tests. Per Step 3 Sections 32-33: a historical raw record can be reprocessed with a new
normalizer version without modifying the original raw record; Observation V1 is not overwritten
by Observation V2.
"""
import unittest

from src.sources.models import SourceType
from tests.helpers import build_stack, synthetic_connector


class TestReplay(unittest.TestCase):
    def test_replay_creates_new_observation_without_touching_original(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = synthetic_connector()

        stack.engine.run_ingestion(
            source_id=source.source_id, connector=connector, connector_id="synthetic-file-connector",
            connector_version="1.0", identifiers=["001_first_observation"],
        )
        raw_record = [r for r in stack.raw_store.all() if r.source_identifier == "001_first_observation"][0]
        original_observations = stack.observation_store.by_raw_record(raw_record.record_id)
        self.assertEqual(len(original_observations), 1)
        v1 = original_observations[0]

        v2 = stack.engine.replay(raw_record.record_id, normalizer_version="2.0")

        self.assertNotEqual(v1.observation_id, v2.observation_id)
        self.assertEqual(v1.normalizer_version, "1.0")
        self.assertEqual(v2.normalizer_version, "2.0")

        all_observations = stack.observation_store.by_raw_record(raw_record.record_id)
        self.assertEqual(len(all_observations), 2, "V1 must remain queryable alongside the new V2")

        # The raw record itself is completely untouched by replay
        raw_after_replay = stack.raw_store.get(raw_record.record_id)
        self.assertEqual(raw_after_replay.raw_payload, raw_record.raw_payload)
        self.assertEqual(raw_after_replay.content_hash, raw_record.content_hash)

    def test_replay_of_unknown_raw_record_raises(self):
        stack = build_stack()
        with self.assertRaises(KeyError):
            stack.engine.replay("does-not-exist")


if __name__ == "__main__":
    unittest.main()
