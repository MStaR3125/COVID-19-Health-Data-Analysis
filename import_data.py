#!/usr/bin/env python3
"""Import all CSV files into the MySQL database with safety controls."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Iterable

import pandas as pd
import mysql.connector
from mysql.connector import Error

try:  # Optional; falls back silently if python-dotenv isn't installed.
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - best effort import
    load_dotenv = lambda *args, **kwargs: None

CSV_FILES = {
    'covid_cases': 'covid_cases.csv',
    'hospital_data': 'hospital_data.csv',
    'vaccination_data': 'vaccination_data.csv',
    'country_demographics': 'country_demographics.csv',
    'testing_data': 'testing_data.csv',
}


def load_db_config() -> Dict[str, str]:
    """Load database credentials from environment variables."""
    load_dotenv()
    config = {
        'host': os.getenv('COVID_DB_HOST', 'localhost'),
        'user': os.getenv('COVID_DB_USER', 'root'),
        'password': os.getenv('COVID_DB_PASSWORD', ''),
        'database': os.getenv('COVID_DB_NAME', 'covid19_analysis'),
    }
    missing = [key for key, value in config.items() if value == '' and key != 'password']
    if missing:
        print(
            "⚠ Using default DB config for: " + ', '.join(missing) +
            ". Set COVID_DB_* env vars or a .env file to override."
        )
    return config


def create_connection(config: Dict[str, str]):
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("✓ Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        sys.exit(1)

def import_csv_to_table(connection, table_name, csv_file, *, reset=False, batch_size=1000):
    """Import CSV file into database table"""
    try:
        # Check if file exists
        if not os.path.exists(csv_file):
            print(f"✗ File not found: {csv_file}")
            return False

        # Read CSV file
        print(f"\nReading {csv_file}...")
        df = pd.read_csv(csv_file)
        print(f"  Found {len(df)} records")

        cursor = connection.cursor()

        if reset:
            cursor.execute(f"TRUNCATE TABLE {table_name}")
            print(f"  Cleared existing data in {table_name}")
        else:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            existing = cursor.fetchone()[0]
            if existing:
                print(f"  Retaining {existing:,} existing rows (append mode)")

        # Prepare insert statement
        cols = ','.join(df.columns)
        placeholders = ','.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        total_inserted = 0

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            values = [tuple(x) for x in batch.values]
            cursor.executemany(insert_query, values)
            connection.commit()
            total_inserted += len(batch)
            print(f"  Inserted {total_inserted}/{len(df)} records...", end='\r')

        print(f"\n✓ Successfully imported {total_inserted} records into {table_name}")
        cursor.close()
        return True

    except Error as e:
        print(f"\n✗ Error importing {csv_file}: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

def verify_import(connection, tables: Iterable[str]):
    """Verify data was imported correctly"""
    try:
        cursor = connection.cursor()
        print("\n" + "="*60)
        print("VERIFICATION: Record counts in each table")
        print("="*60)

        for table_name in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"{table_name:25s} : {count:,} records")

        print("="*60)
        cursor.close()

    except Error as e:
        print(f"✗ Error during verification: {e}")

def parse_args(argv: Iterable[str] | None = None):
    parser = argparse.ArgumentParser(description="Import project CSVs into MySQL.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Truncate each table before loading (destructive).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Number of rows to insert per batch (default: 1000).",
    )
    parser.add_argument(
        "--tables",
        nargs="*",
        choices=sorted(CSV_FILES.keys()),
        help="Subset of tables to import (defaults to all).",
    )
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory containing the CSV files (default: current directory).",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None):
    """Main import process"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  COVID-19 Data Import Script                            ║")
    print("╚══════════════════════════════════════════════════════════╝")

    args = parse_args(argv)
    tables = args.tables or list(CSV_FILES.keys())
    csv_dir = args.csv_dir

    # Check if CSV files exist
    missing_files = []
    for table in tables:
        csv_file = csv_dir / CSV_FILES[table]
        if not csv_file.exists():
            missing_files.append(str(csv_file))

    if missing_files:
        print("\n✗ Missing CSV files:")
        for f in missing_files:
            print(f"  - {f}")
        print("\nPlease ensure all CSV files are present or specify --csv-dir correctly.")
        sys.exit(1)

    connection = create_connection(load_db_config())

    success_count = 0
    for table_name in tables:
        csv_file = csv_dir / CSV_FILES[table_name]
        print(f"\n--- Importing {table_name} ---")
        if import_csv_to_table(
            connection,
            table_name,
            str(csv_file),
            reset=args.reset,
            batch_size=args.batch_size,
        ):
            success_count += 1

    verify_import(connection, tables)

    connection.close()

    print("\n" + "="*60)
    print(f"IMPORT COMPLETE: {success_count}/{len(tables)} tables imported successfully")
    print("="*60)

    if success_count == len(CSV_FILES):
        print("\n✓ All data imported successfully!")
        print("\nNext steps:")
        print("  1. Open MySQL Workbench or command line")
        print("  2. Run: USE covid19_analysis;")
        print("  3. Start running queries from sql-analysis-qs.md")
    else:
        print("\n⚠ Some imports failed. Check error messages above.")

if __name__ == "__main__":
    try:
        import pandas  # noqa: F401  (import check for helpful error)
        import mysql.connector  # noqa: F401
    except ImportError:
        print("✗ Missing required packages. Install them with:\n  pip install -r requirements.txt")
        sys.exit(1)

    main()
