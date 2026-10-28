
import sys
import unittest
from pathlib import Path

# Make the src directory importable.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from validator import validate_reading


class TestTelemetryValidator(unittest.TestCase):

    def setUp(self):
        self.valid_reading = {
            "timestamp": "2026-10-28T10:30:00+00:00",
            "joint_position_deg": 35.0,
            "temperature_c": 42.0,
            "gripper_closed": True,
        }

    def test_valid_reading_passes(self):
        is_valid, errors = validate_reading(self.valid_reading)

        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_out_of_range_temperature_fails(self):
        reading = self.valid_reading.copy()
        reading["temperature_c"] = 250.0

        is_valid, errors = validate_reading(reading)

        self.assertFalse(is_valid)
        self.assertTrue(
            any("Temperature outside configured limits" in e for e in errors)
        )

    def test_out_of_range_joint_position_fails(self):
        reading = self.valid_reading.copy()
        reading["joint_position_deg"] = 150.0

        is_valid, errors = validate_reading(reading)

        self.assertFalse(is_valid)
        self.assertTrue(
            any("Joint position outside configured limits" in e for e in errors)
        )

    def test_missing_field_fails(self):
        reading = self.valid_reading.copy()
        del reading["timestamp"]

        is_valid, errors = validate_reading(reading)

        self.assertFalse(is_valid)
        self.assertTrue(
            any("Missing required field" in e for e in errors)
        )


if __name__ == "__main__":
    unittest.main()
