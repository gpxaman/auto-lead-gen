"""
Versioning tests. Per Step 3 Section 46: RAW V1 remains available after RAW V2; OBSERVATION V1
remains available after OBSERVATION V2 (via replay -- see tests/replay/test_replay.py); SCHEMA V1
remains available after SCHEMA V2 is introduced (schema detection recognizes multiple versions
side by side, already covered in tests/ingestion/test_engine_pipeline.py's multi-schema test).
"""
import unittest

from src.sources.models import SourceStatus, SourceType
from tests.helpers import ScriptedConnector, build_stack


class TestRawRecordVersioning(unittest.TestCase):
    def test_changed_content_creates_new_version_without_destroying_v1(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")

        connector = ScriptedConnector({
            "item-42": [
                {"lead_metadata": {"client_archetype": "NPD_Innovator"}, "project_scope": {"title": "v1 title"}},
                {"lead_metadata": {"client_archetype": "NPD_Innovator"}, "project_scope": {"title": "v2 title -- CHANGED"}},
            ]
        })

        run1 = stack.engine.run_ingestion(source.source_id, connector, "scripted", "1.0", identifiers=["item-42"])
        self.assertEqual(run1.records_accepted, 1)
        run2 = stack.engine.run_ingestion(source.source_id, connector, "scripted", "1.0", identifiers=["item-42"])
        self.assertEqual(run2.records_accepted, 1)  # content changed -> new version, NOT a duplicate

        chain = stack.raw_store.get_version_chain(source.source_id, "item-42")
        self.assertEqual(len(chain), 2, "both versions must remain in the chain")
        self.assertEqual(chain[0].raw_payload["project_scope"]["title"], "v1 title")
        self.assertEqual(chain[1].raw_payload["project_scope"]["title"], "v2 title -- CHANGED")
        self.assertEqual(chain[1].supersedes_raw_record_id, chain[0].record_id)

        # V1's content is byte-identical to what it always was -- proving no in-place mutation
        v1_again = stack.raw_store.get(chain[0].record_id)
        self.assertEqual(v1_again.raw_payload["project_scope"]["title"], "v1 title")

    def test_identical_content_refetched_is_exact_duplicate_not_a_new_version(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform")
        connector = ScriptedConnector({"item-99": [{"title": "same content"}, {"title": "same content"}]})

        stack.engine.run_ingestion(source.source_id, connector, "scripted", "1.0", identifiers=["item-99"])
        run2 = stack.engine.run_ingestion(source.source_id, connector, "scripted", "1.0", identifiers=["item-99"])

        self.assertEqual(run2.records_duplicated, 1)
        self.assertEqual(run2.records_accepted, 0)
        chain = stack.raw_store.get_version_chain(source.source_id, "item-99")
        self.assertEqual(len(chain), 1, "an exact duplicate must NOT create a second raw_record version")


class TestSourceVersioning(unittest.TestCase):
    def test_source_configuration_update_preserves_prior_version(self):
        stack = build_stack()
        source = stack.source_registry.register_source(SourceType.SYNTHETIC_TEST, "synthetic_platform", platform="synthetic_platform")
        v1 = stack.source_registry.get_latest_version(source.source_id)

        stack.source_registry.update_source_version(source.source_id, platform="synthetic_platform_v2")
        v2 = stack.source_registry.get_latest_version(source.source_id)

        self.assertNotEqual(v1.source_version_id, v2.source_version_id)
        self.assertEqual(v1.platform, "synthetic_platform")
        self.assertEqual(v2.platform, "synthetic_platform_v2")

        all_versions = stack.source_registry.get_all_versions(source.source_id)
        self.assertEqual(len(all_versions), 2, "prior configuration must remain queryable, not destroyed")


if __name__ == "__main__":
    unittest.main()
