
import sqlite3
from contextlib import closing
from pathlib import Path


def get_database_path():
    project_root = Path(__file__).resolve().parent.parent
    return project_root / "data" / "robot_telemetry.db"


def create_database():
    """Create the database and telemetry table."""

    database_path = get_database_path()

    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    joint_position_deg REAL NOT NULL,
                    temperature_c REAL NOT NULL,
                    gripper_closed INTEGER NOT NULL
                        CHECK (gripper_closed IN (0, 1)),
                    UNIQUE (
                        timestamp,
                        joint_position_deg,
                        temperature_c,
                        gripper_closed
                    )
                )
            """)

    print(f"Database ready: {database_path}")


def insert_readings(readings):
    """Insert readings while ignoring exact duplicates."""

    database_path = get_database_path()

    rows = [
        (
            reading["timestamp"],
            reading["joint_position_deg"],
            reading["temperature_c"],
            int(reading["gripper_closed"]),
        )
        for reading in readings
    ]

    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            cursor = connection.executemany("""
                INSERT INTO telemetry (
                    timestamp,
                    joint_position_deg,
                    temperature_c,
                    gripper_closed
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT (
                    timestamp,
                    joint_position_deg,
                    temperature_c,
                    gripper_closed
                ) DO NOTHING
            """, rows)

            inserted = cursor.rowcount

    return inserted


if __name__ == "__main__":
    create_database()
