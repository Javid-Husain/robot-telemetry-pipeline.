
import csv
from pathlib import Path

from validator import validate_reading
from database import create_database, insert_readings
from logger_config import setup_logger


def parse_reading(row):
    """Convert CSV strings into correctly typed values."""

    gripper_value = row["gripper_closed"].strip().lower()

    if gripper_value not in ("true", "false"):
        raise ValueError("Gripper status must be True or False")

    return {
        "timestamp": row["timestamp"],
        "joint_position_deg": float(row["joint_position_deg"]),
        "temperature_c": float(row["temperature_c"]),
        "gripper_closed": gripper_value == "true",
    }


def main():
    """Process telemetry, validate it, and store accepted readings."""

    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"

    input_file = data_dir / "robot_telemetry.csv"
    valid_file = data_dir / "valid_telemetry.csv"
    rejected_file = data_dir / "rejected_telemetry.csv"

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input telemetry file not found: {input_file}. "
            "Run telemetry_simulator.py first."
        )

    create_database()
    logger = setup_logger()
    logger.info("Pipeline started")

    accepted = 0
    rejected = 0
    valid_readings = []

    with (
        input_file.open("r", newline="", encoding="utf-8") as source,
        valid_file.open("w", newline="", encoding="utf-8") as valid_output,
        rejected_file.open("w", newline="", encoding="utf-8") as rejected_output,
    ):
        reader = csv.DictReader(source)

        expected_fields = {
            "timestamp",
            "joint_position_deg",
            "temperature_c",
            "gripper_closed",
        }

        if not reader.fieldnames or not expected_fields.issubset(
            set(reader.fieldnames)
        ):
            raise ValueError(
                f"Input CSV must contain these columns: "
                f"{', '.join(sorted(expected_fields))}"
            )

        valid_writer = csv.DictWriter(
            valid_output,
            fieldnames=reader.fieldnames,
        )

        rejected_writer = csv.DictWriter(
            rejected_output,
            fieldnames=reader.fieldnames + ["validation_errors"],
        )

        valid_writer.writeheader()
        rejected_writer.writeheader()

        for row in reader:
            try:
                reading = parse_reading(row)
                is_valid, errors = validate_reading(reading)

                if is_valid:
                    valid_writer.writerow(row)
                    valid_readings.append(reading)
                    accepted += 1
                    logger.debug("Telemetry record accepted")
                else:
                    row["validation_errors"] = "; ".join(errors)
                    rejected_writer.writerow(row)
                    rejected += 1
                    logger.warning("Telemetry record rejected: %s", errors)

            except (ValueError, KeyError) as error:
                row["validation_errors"] = f"Parsing error: {error}"
                rejected_writer.writerow(row)
                rejected += 1
                logger.warning("Telemetry parsing failed: %s", error)

    # Insert accepted records into SQLite after CSV processing.
    inserted = insert_readings(valid_readings)
    logger.info(
    "Pipeline completed: accepted=%s rejected=%s inserted=%s",
    accepted,
    rejected,
    inserted,
)

    print("\n--- Pipeline Summary ---")
    print(f"Accepted records: {accepted}")
    print(f"Rejected records: {rejected}")
    print(f"Total processed: {accepted + rejected}")
    print(f"Database records inserted: {inserted}")
    print(f"Valid output: {valid_file}")
    print(f"Rejected output: {rejected_file}")


if __name__ == "__main__":
    main()
