
import csv
from pathlib import Path

from validator import validate_reading


def parse_reading(row):
    """Convert CSV strings into correctly typed values."""

    return {
        "timestamp": row["timestamp"],
        "joint_position_deg": float(row["joint_position_deg"]),
        "temperature_c": float(row["temperature_c"]),
        "gripper_closed": row["gripper_closed"].strip().lower() == "true",
    }


def main():
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"

    input_file = data_dir / "robot_telemetry.csv"
    valid_file = data_dir / "valid_telemetry.csv"
    rejected_file = data_dir / "rejected_telemetry.csv"

    accepted = 0
    rejected = 0

    with (
        input_file.open("r", newline="", encoding="utf-8") as source,
        valid_file.open("w", newline="", encoding="utf-8") as valid_output,
        rejected_file.open("w", newline="", encoding="utf-8") as rejected_output,
    ):
        reader = csv.DictReader(source)

        valid_fields = reader.fieldnames
        rejected_fields = (valid_fields or []) + ["validation_errors"]

        valid_writer = csv.DictWriter(
            valid_output, fieldnames=valid_fields
        )
        rejected_writer = csv.DictWriter(
            rejected_output, fieldnames=rejected_fields
        )

        valid_writer.writeheader()
        rejected_writer.writeheader()

        for row in reader:
            try:
                reading = parse_reading(row)
                is_valid, errors = validate_reading(reading)

                if is_valid:
                    valid_writer.writerow(row)
                    accepted += 1
                else:
                    row["validation_errors"] = "; ".join(errors)
                    rejected_writer.writerow(row)
                    rejected += 1

            except (ValueError, KeyError) as error:
                row["validation_errors"] = f"Parsing error: {error}"
                rejected_writer.writerow(row)
                rejected += 1

    print("\n--- Pipeline Summary ---")
    print(f"Accepted records: {accepted}")
    print(f"Rejected records: {rejected}")
    print(f"Total processed: {accepted + rejected}")
    print(f"Valid output: {valid_file}")
    print(f"Rejected output: {rejected_file}")


if __name__ == "__main__":
    main()
