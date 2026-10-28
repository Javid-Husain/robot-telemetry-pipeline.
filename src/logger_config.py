
import logging
from pathlib import Path


def setup_logger():
    """Configure logging to write to both console and file."""

    project_root = Path(__file__).resolve().parent.parent
    log_file = project_root / "data" / "pipeline.log"

    logger = logging.getLogger("robot_telemetry")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if setup is called again.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_file, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
