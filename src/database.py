
import sqlite3
from pathlib import Path


def create_database():
    """Create the database and telemetry table."""

    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "data" / "robot_telemetry.db"

    with sqlite3.connect(database_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                joint_position_deg REAL NOT NULL,
                temperature_c REAL NOT NULL,
                gripper_closed INTEGER NOT NULL
                    CHECK (gripper_closed IN (0, 1))
            )
        """)

    print(f"Database ready: {database_path}")


if __name__ == "__main__":
    create_database()
