
import csv
import sqlite3
from pathlib import Path

from database import get_database_path


def get_rejected_count(data_dir):
    """Count rejected records in the latest pipeline output."""

    rejected_file = data_dir / "rejected_telemetry.csv"

    if not rejected_file.exists():
        return 0

    with rejected_file.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        return max(sum(1 for _ in csv.DictReader(file)), 0)


def generate_report():
    """Generate a summary of stored robot telemetry."""

    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    database_path = get_database_path()

    with sqlite3.connect(database_path) as connection:
        total, average_temp, maximum_temp, closed_count = (
            connection.execute("""
                SELECT
                    COUNT(*),
                    AVG(temperature_c),
                    MAX(temperature_c),
                    SUM(gripper_closed)
                FROM telemetry
            """).fetchone()
        )

    rejected = get_rejected_count(data_dir)

    average_temp = (
        f"{average_temp:.2f} °C"
        if average_temp is not None else "N/A"
    )
    maximum_temp = (
        f"{maximum_temp:.2f} °C"
        if maximum_temp is not None else "N/A"
    )

    report = f"""
========================================
   ROBOT TELEMETRY MONITORING REPORT
========================================

Stored telemetry readings : {total}
Rejected records (latest run): {rejected}
Average temperature       : {average_temp}
Maximum temperature       : {maximum_temp}
Gripper-closed readings   : {closed_count or 0}

Database                  : {database_path}

========================================
"""

    print(report)

    report_file = data_dir / "monitoring_report.txt"
    report_file.write_text(report, encoding="utf-8")

    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    generate_report()
