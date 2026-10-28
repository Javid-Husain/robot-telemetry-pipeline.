
from math import isfinite


def validate_reading(reading):
    """
    Validate one robot telemetry reading.

    Returns:
        (is_valid, errors)
    """

    errors = []

    # Check required fields
    required_fields = [
        "timestamp",
        "joint_position_deg",
        "temperature_c",
        "gripper_closed",
    ]

    for field in required_fields:
        if field not in reading or reading[field] is None:
            errors.append(f"Missing required field: {field}")

    # Validate joint position
    joint = reading.get("joint_position_deg")

    if joint is not None:
        if isinstance(joint, bool) or not isinstance(joint, (int, float)):
            errors.append("Joint position must be numeric")
        elif not isfinite(joint):
            errors.append("Joint position must be finite")
        elif not -90 <= joint <= 90:
            errors.append("Joint position outside configured limits")

    # Validate temperature
    temperature = reading.get("temperature_c")

    if temperature is not None:
        if isinstance(temperature, bool) or not isinstance(
            temperature, (int, float)
        ):
            errors.append("Temperature must be numeric")
        elif not isfinite(temperature):
            errors.append("Temperature must be finite")
        elif not 0 <= temperature <= 100:
            errors.append("Temperature outside configured limits")

    # Validate gripper state
    gripper = reading.get("gripper_closed")

    if gripper is not None and not isinstance(gripper, bool):
        errors.append("Gripper status must be True or False")

    # Validate timestamp
    timestamp = reading.get("timestamp")

    if timestamp is not None:
        if not isinstance(timestamp, str):
            errors.append("Timestamp must be a string")
        else:
            try:
                from datetime import datetime

                datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                errors.append("Timestamp must be a valid ISO format datetime")

    return len(errors) == 0, errors
