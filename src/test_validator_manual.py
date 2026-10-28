
from validator import validate_reading


valid_reading = {
    "timestamp": "2026-10-28T10:30:00+00:00",
    "joint_position_deg": 35.0,
    "temperature_c": 42.0,
    "gripper_closed": True,
}

invalid_reading = {
    "timestamp": "not-a-timestamp",
    "joint_position_deg": 150.0,
    "temperature_c": 250.0,
    "gripper_closed": "closed",
}

for name, reading in [
    ("Valid reading", valid_reading),
    ("Invalid reading", invalid_reading),
]:
    is_valid, errors = validate_reading(reading)

    print(f"\n{name}: {'PASS' if is_valid else 'FAIL'}")

    for error in errors:
        print(f"  - {error}")
