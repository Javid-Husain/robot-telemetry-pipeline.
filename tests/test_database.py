
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import closing

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import database


class TestTelemetryDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"

        self.path_patcher = patch.object(
            database,
            "get_database_path",
            return_value=self.db_path,
        )
        self.path_patcher.start()

        database.create_database()

        # Add a unique index for duplicate prevention.
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                connection.execute("""
                    CREATE UNIQUE INDEX idx_test_unique_reading
                    ON telemetry (
                        timestamp,
                        joint_position_deg,
                        temperature_c,
                        gripper_closed
                    )
                """)

    def tearDown(self):
        self.path_patcher.stop()

        # Ensure SQLite has no lingering connections before cleanup.
        self.temp_dir.cleanup()

    def test_identical_reading_is_not_inserted_twice(self):
        reading = {
            "timestamp": "2026-10-28T10:30:00+00:00",
            "joint_position_deg": 35.0,
            "temperature_c": 42.0,
            "gripper_closed": True,
        }

        first_insert = database.insert_readings([reading])
        second_insert = database.insert_readings([reading])

        self.assertEqual(first_insert, 1)
        self.assertEqual(second_insert, 0)

        # Explicitly open and close the connection.
        connection = sqlite3.connect(self.db_path)
        try:
            count = connection.execute(
                "SELECT COUNT(*) FROM telemetry"
            ).fetchone()[0]
        finally:
            connection.close()

        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
