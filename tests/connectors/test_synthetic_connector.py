import unittest

from src.connectors.synthetic_file_connector import SyntheticFileConnector
from tests.helpers import FIXTURES_DIR


class TestSyntheticFileConnector(unittest.TestCase):
    def setUp(self):
        self.connector = SyntheticFileConnector(FIXTURES_DIR)

    def test_discover_lists_all_fixtures(self):
        identifiers = self.connector.discover()
        self.assertIn("001_first_observation", identifiers)
        self.assertIn("007_html_like", identifiers)
        self.assertEqual(len(identifiers), 8)

    def test_fetch_missing_identifier_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.connector.fetch("does_not_exist")

    def test_connector_does_not_classify_or_judge(self):
        """The connector interface has no field/method through which it could express a business
        judgment -- verified by inspecting the RawFetchResult shape it returns."""
        result = self.connector.fetch("001_first_observation")
        allowed_fields = {"source_identifier", "raw_payload", "content_type", "source_url", "request_metadata", "response_metadata", "retrieved_at"}
        actual_fields = set(result.__dataclass_fields__.keys())
        self.assertEqual(actual_fields, allowed_fields)


if __name__ == "__main__":
    unittest.main()
