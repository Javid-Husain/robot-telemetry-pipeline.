
import sqlite3
from database import get_database_path


def main():
    with sqlite3.connect(get_database_path()) as connection:
        cursor = connection.execute("""
            SELECT
                COUNT(*),
                ROUND(AVG(temperature_c), 2),
                ROUND(MAX(temperature_c), 2)
            FROM telemetry
        """)

        total, average_temperature, max_temperature = cursor.fetchone()

    print(f"Total stored readings: {total}")
    print(f"Average temperature: {average_temperature} C")
    print(f"Maximum temperature: {max_temperature} C")


if __name__ == "__main__":
    main()
