import unittest

from src.common.events import EventLog
from src.sources.models import SourceHealthEvent, SourceStatus, SourceType
from src.sources.registry import SourceRegistry
from src.common.ids import new_id


class TestSourceRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = SourceRegistry(EventLog())

    def test_register_source_emits_event_and_sets_active(self):
        source = self.registry.register_source(SourceType.FREELANCE_MARKETPLACE, "synthetic_upwork_like")
        self.assertEqual(source.status, SourceStatus.ACTIVE)
        events = self.registry._event_log.by_type("SourceRegistered")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].aggregate_id, source.source_id)

    def test_unknown_values_use_explicit_unknown_not_invented_defaults(self):
        source = self.registry.register_source(SourceType.FREELANCE_MARKETPLACE, "no_url_yet")
        v1 = self.registry.get_latest_version(source.source_id)
        self.assertEqual(v1.macro_channel, "UNKNOWN")
        self.assertEqual(v1.platform, "UNKNOWN")
        self.assertIsNone(v1.source_url)

    def test_health_history_is_append_only(self):
        source = self.registry.register_source(SourceType.FREELANCE_MARKETPLACE, "health_test")
        for i in range(3):
            self.registry.record_health_event(source.source_id, SourceHealthEvent(
                event_id=new_id("sh-"), source_id=source.source_id, recorded_at=f"2026-08-0{i+1}T00:00:00Z",
                success_count=i,
            ))
        history = self.registry.get_health_history(source.source_id)
        self.assertEqual(len(history), 3, "health history must accumulate, not just keep the latest")


if __name__ == "__main__":
    unittest.main()
