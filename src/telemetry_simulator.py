
import csv
import random
from datetime import datetime, timezone
from pathlib import Path


def generate_reading():
    """Generate one simulated robot sensor reading."""

    reading = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "joint_position_deg": round(random.uniform(-90, 90), 2),
        "temperature_c": round(random.uniform(25, 75), 2),
        "gripper_closed": random.choice([True, False]),
    }

    return reading


def main():
    """Generate and save 100 robot telemetry readings."""

    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    output_file = data_dir / "robot_telemetry.csv"

    fieldnames = [
        "timestamp",
        "joint_position_deg",
        "temperature_c",
        "gripper_closed",
    ]

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(100):
            reading = generate_reading()
            writer.writerow(reading)

    print("Telemetry simulation completed!")
    print(f"Total readings generated: 100")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()
