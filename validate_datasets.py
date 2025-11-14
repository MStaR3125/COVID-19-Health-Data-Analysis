#!/usr/bin/env python3
"""Lightweight validation harness for the COVID SQL project."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Iterable

import pandas as pd

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = lambda *args, **kwargs: None

CSV_FILES = {
    "covid_cases": "covid_cases.csv",
    "hospital_data": "hospital_data.csv",
    "vaccination_data": "vaccination_data.csv",
    "country_demographics": "country_demographics.csv",
    "testing_data": "testing_data.csv",
}

EXPECTED_ROWS = {
    "covid_cases": 35560,
    "hospital_data": 17780,
    "vaccination_data": 27940,
    "country_demographics": 20,
    "testing_data": 35560,
}

UNIQUE_KEYS = {
    "covid_cases": ["date", "country"],
    "hospital_data": ["date", "state"],
    "vaccination_data": ["date", "country"],
    "testing_data": ["date", "country"],
    "country_demographics": ["country"],
}


def parse_args(argv: Iterable[str] | None = None):
    parser = argparse.ArgumentParser(description="Validate project CSVs and DB state.")
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory containing the CSV files (default: current directory).",
    )
    parser.add_argument(
        "--check-db",
        action="store_true",
        help="Also verify table counts in the configured MySQL database.",
    )
    return parser.parse_args(argv)


def load_db_config() -> Dict[str, str]:
    load_dotenv()
    return {
        "host": os.getenv("COVID_DB_HOST", "localhost"),
        "user": os.getenv("COVID_DB_USER", "root"),
        "password": os.getenv("COVID_DB_PASSWORD", ""),
        "database": os.getenv("COVID_DB_NAME", "covid19_analysis"),
    }


def validate_csvs(csv_dir: Path) -> bool:
    print("\n=== Validating CSV files ===")
    success = True
    for table, filename in CSV_FILES.items():
        path = csv_dir / filename
        if not path.exists():
            print(f"✗ {table}: missing file at {path}")
            success = False
            continue

        df = pd.read_csv(path)
        row_count = len(df)
        expected = EXPECTED_ROWS.get(table)
        if expected is not None and row_count != expected:
            print(f"✗ {table}: expected {expected:,} rows, found {row_count:,}")
            success = False
        else:
            print(f"✓ {table}: {row_count:,} rows")

        key = UNIQUE_KEYS.get(table)
        if key:
            dupes = int(df.duplicated(subset=key).sum())
            if dupes:
                print(f"  • WARN: {dupes} duplicate rows on key {key}")
                success = False
            else:
                print(f"  • Keys {key} are unique")
    return success


def validate_database() -> bool:
    import mysql.connector  # Imported lazily to keep optional dependency.

    config = load_db_config()
    try:
        connection = mysql.connector.connect(**config)
    except mysql.connector.Error as exc:  # type: ignore[attr-defined]
        print(f"✗ Unable to connect to MySQL: {exc}")
        return False

    cursor = connection.cursor()
    success = True
    print("\n=== Verifying MySQL table counts ===")
    for table in CSV_FILES.keys():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        (row_count,) = cursor.fetchone()
        expected = EXPECTED_ROWS.get(table)
        label = "✓" if expected == row_count else "✗"
        print(f"{label} {table:22s} : {row_count:,} rows")
        if expected is not None and row_count != expected:
            success = False
    cursor.close()
    connection.close()
    return success


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    csv_ok = validate_csvs(args.csv_dir)
    db_ok = True
    if args.check_db:
        db_ok = validate_database()
    if csv_ok and db_ok:
        print("\nValidation complete ✅")
        return 0
    print("\nValidation detected issues. See logs above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
