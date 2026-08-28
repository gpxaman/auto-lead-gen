import unittest

from src.observations.normalizer import normalize
from src.schemas.detection import detect_schema


class TestNormalizer(unittest.TestCase):
    def test_dict_payload_wrapped_without_field_loss(self):
        payload = {"a": 1, "b": {"c": 2}, "unrecognized_field": "kept"}
        detection = detect_schema(payload)
        result = normalize(payload, detection)
        self.assertEqual(result.status, "NORMALIZED")
        self.assertEqual(result.normalized_payload["source_specific_payload"], payload)

    def test_non_dict_payload_is_pass_through_not_forced(self):
        detection = detect_schema("just some text")
        result = normalize("just some text", detection)
        self.assertEqual(result.status, "PASS_THROUGH_UNSTRUCTURED")
        self.assertIsNone(result.normalized_payload)


if __name__ == "__main__":
    unittest.main()
