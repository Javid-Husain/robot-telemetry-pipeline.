
import sqlite3
from database import get_database_path


def main():
    with sqlite3.connect(get_database_path()) as connection:
        connection.execute("""
            DELETE FROM telemetry
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM telemetry
                GROUP BY
                    timestamp,
                    joint_position_deg,
                    temperature_c,
                    gripper_closed
            )
        """)

        connection.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_telemetry_unique_reading
            ON telemetry (
                timestamp,
                joint_position_deg,
                temperature_c,
                gripper_closed
            )
        """)

    print("Database migration completed successfully.")


if __name__ == "__main__":
    main()
