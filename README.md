
# Robot Telemetry Monitoring Pipeline

A Python-based data pipeline that simulates robot sensor telemetry,
validates incoming readings, stores accepted records in SQLite,
and generates monitoring reports.

## Features

- Simulated robot telemetry generation
- Data validation and rejection of invalid readings
- CSV-based input and output
- SQLite database storage
- Duplicate prevention for identical readings
- Pipeline logging
- Automated unit tests
- Temperature and gripper monitoring reports

## Tech Stack

- Python
- SQLite
- CSV
- Git
- unittest

## Project Structure

```text
robot-telemetry-pipeline/
├── src/
│   ├── telemetry_simulator.py
│   ├── validator.py
│   ├── pipeline.py
│   ├── database.py
│   ├── migrate_database.py
│   ├── logger_config.py
│   ├── query_database.py
│   └── monitoring_report.py
├── tests/
│   ├── test_validator.py
│   └── test_database.py
├── data/
├── README.md
└── .gitignore
```

## Setup

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No third-party Python packages are required for the current implementation.

## Run the Pipeline

Generate simulated telemetry:

```powershell
python src/telemetry_simulator.py
```

Process and validate the data:

```powershell
python src/pipeline.py
```

Generate a monitoring report:

```powershell
python src/monitoring_report.py
```

Run automated tests:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Outputs

The application generates CSV files, an SQLite database,
a pipeline log, and a text monitoring report under `data/`.

These files are generated locally and are not committed by default.

## Limitations

- Sensor readings are simulated.
- Temperature and joint-position limits are configurable
  assumptions, not real robot safety specifications.
- The current pipeline is a local batch-processing prototype.
- Real robot hardware and live streaming are not implemented.

## Future Improvements

- Stronger schema and input validation
- Improved monitoring and error recovery
- More comprehensive automated tests
- Live telemetry ingestion
- Dashboard visualization
- Deployment and continuous integration
