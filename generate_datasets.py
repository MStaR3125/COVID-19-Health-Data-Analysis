#!/usr/bin/env python3
"""Generate synthetic COVID-19 health datasets for the SQL project."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

DEFAULT_COUNTRIES = [
    "India",
    "USA",
    "Brazil",
    "UK",
    "France",
    "Germany",
    "Italy",
    "Spain",
    "Russia",
    "Turkey",
    "South Africa",
    "Argentina",
    "Colombia",
    "Mexico",
    "Japan",
    "South Korea",
    "Canada",
    "Australia",
    "China",
    "Indonesia",
]

INDIA_STATES = [
    "Maharashtra",
    "Karnataka",
    "Kerala",
    "Tamil Nadu",
    "Delhi",
    "Uttar Pradesh",
    "West Bengal",
    "Gujarat",
    "Rajasthan",
    "Madhya Pradesh",
]

DEFAULT_START = datetime(2020, 1, 1)
DEFAULT_END = datetime(2024, 11, 12)
DEFAULT_VACCINATION_START = datetime(2021, 1, 16)


@dataclass(frozen=True)
class DatasetBundle:
    covid_cases: pd.DataFrame
    hospital_data: pd.DataFrame
    vaccination_data: pd.DataFrame
    country_demographics: pd.DataFrame
    testing_data: pd.DataFrame

    def save(self, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        files = {
            "covid_cases.csv": self.covid_cases,
            "hospital_data.csv": self.hospital_data,
            "vaccination_data.csv": self.vaccination_data,
            "country_demographics.csv": self.country_demographics,
            "testing_data.csv": self.testing_data,
        }
        for filename, df in files.items():
            df.to_csv(output_dir / filename, index=False)


def date_range(start: datetime, end: datetime) -> pd.DatetimeIndex:
    if end < start:
        raise ValueError("End date must be on or after start date")
    return pd.date_range(start=start, end=end, freq="D")


def build_covid_cases(
    dates: Sequence[pd.Timestamp], countries: Sequence[str], rng: random.Random
) -> pd.DataFrame:
    records = []
    for country in countries:
        base_cases = rng.randint(100, 1000)
        cumulative_cases = 0
        cumulative_deaths = 0
        cumulative_recovered = 0

        for i, current_date in enumerate(dates):
            wave_factor = 1 + 0.5 * np.sin(i / 90) + 0.3 * np.sin(i / 180)
            if i < 60:
                daily_cases = int(base_cases * wave_factor * (1 + i / 100))
            elif i < 365:
                daily_cases = int(base_cases * wave_factor * (1 + i / 50))
            elif i < 730:
                daily_cases = int(base_cases * wave_factor * (2 + i / 40))
            else:
                daily_cases = int(base_cases * wave_factor * (1.5 + i / 100))

            daily_cases = max(0, int(daily_cases * rng.uniform(0.7, 1.3)))
            daily_deaths = int(daily_cases * rng.uniform(0.02, 0.03))
            daily_recovered = (
                int(daily_cases * rng.uniform(0.90, 0.95)) if i > 14 else 0
            )

            cumulative_cases += daily_cases
            cumulative_deaths += daily_deaths
            cumulative_recovered += daily_recovered
            active_cases = max(0, cumulative_cases - cumulative_deaths - cumulative_recovered)

            records.append(
                {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "country": country,
                    "daily_cases": daily_cases,
                    "daily_deaths": daily_deaths,
                    "daily_recovered": daily_recovered,
                    "cumulative_cases": cumulative_cases,
                    "cumulative_deaths": cumulative_deaths,
                    "cumulative_recovered": cumulative_recovered,
                    "active_cases": active_cases,
                }
            )
    return pd.DataFrame(records)


def build_hospital_data(
    dates: Sequence[pd.Timestamp], states: Sequence[str], rng: random.Random
) -> pd.DataFrame:
    records = []
    for i, current_date in enumerate(dates):
        wave_factor = 1 + 0.5 * np.sin(i / 90)
        for state in states:
            base_admissions = rng.randint(50, 500)
            daily_admissions = max(
                0, int(base_admissions * wave_factor * rng.uniform(0.8, 1.2))
            )
            icu_admissions = int(daily_admissions * rng.uniform(0.15, 0.25))
            ventilator_usage = int(icu_admissions * rng.uniform(0.3, 0.5))

            records.append(
                {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "state": state,
                    "country": "India",
                    "hospital_admissions": daily_admissions,
                    "icu_admissions": icu_admissions,
                    "ventilator_usage": ventilator_usage,
                    "available_beds": rng.randint(100, 1000),
                    "available_icu_beds": rng.randint(10, 100),
                }
            )
    return pd.DataFrame(records)


def build_vaccination_data(
    start_date: datetime,
    end_date: datetime,
    countries: Sequence[str],
    rng: random.Random,
) -> pd.DataFrame:
    vax_dates = date_range(max(start_date, DEFAULT_VACCINATION_START), end_date)
    records = []
    for country in countries:
        cumulative_dose1 = 0
        cumulative_dose2 = 0
        cumulative_booster = 0
        for i, current_date in enumerate(vax_dates):
            if i < 90:
                daily_dose1 = rng.randint(10_000, 100_000)
                daily_dose2 = rng.randint(5_000, 50_000) if i > 30 else 0
                daily_booster = 0
            elif i < 365:
                daily_dose1 = rng.randint(100_000, 500_000)
                daily_dose2 = rng.randint(50_000, 400_000)
                daily_booster = rng.randint(10_000, 100_000) if i > 270 else 0
            else:
                daily_dose1 = rng.randint(50_000, 200_000)
                daily_dose2 = rng.randint(40_000, 180_000)
                daily_booster = rng.randint(50_000, 150_000)

            cumulative_dose1 += daily_dose1
            cumulative_dose2 += daily_dose2
            cumulative_booster += daily_booster

            records.append(
                {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "country": country,
                    "daily_vaccinations_dose1": daily_dose1,
                    "daily_vaccinations_dose2": daily_dose2,
                    "daily_vaccinations_booster": daily_booster,
                    "cumulative_dose1": cumulative_dose1,
                    "cumulative_dose2": cumulative_dose2,
                    "cumulative_booster": cumulative_booster,
                    "total_vaccinations": cumulative_dose1
                    + cumulative_dose2
                    + cumulative_booster,
                }
            )
    return pd.DataFrame(records)


def build_demographics(countries: Sequence[str]) -> pd.DataFrame:
    data = {
        "country": countries,
        "population": [
            1393409038,
            331893745,
            214326223,
            68207114,
            67391582,
            83900471,
            60367477,
            47351567,
            145912025,
            85042738,
            60041994,
            45605826,
            51265844,
            130262216,
            125836021,
            51780579,
            38155012,
            25788215,
            1444216107,
            276361783,
        ],
        "median_age": [
            28.4,
            38.3,
            33.5,
            40.5,
            41.7,
            47.8,
            47.9,
            45.5,
            39.6,
            32.2,
            27.6,
            31.9,
            31.2,
            29.3,
            48.6,
            43.7,
            41.8,
            37.5,
            38.4,
            30.2,
        ],
        "gdp_per_capita": [
            6700,
            63051,
            14103,
            42330,
            44995,
            50795,
            42776,
            38286,
            27394,
            27956,
            12032,
            19922,
            13579,
            17336,
            42248,
            43143,
            48720,
            59934,
            16117,
            11812,
        ],
        "population_density": [
            464,
            36,
            25,
            275,
            119,
            240,
            206,
            94,
            9,
            109,
            49,
            17,
            46,
            66,
            347,
            527,
            4,
            3,
            153,
            151,
        ],
        "hospital_beds_per_1000": [
            0.5,
            2.9,
            2.1,
            2.5,
            5.9,
            8.0,
            3.2,
            2.9,
            7.1,
            2.9,
            2.3,
            5.0,
            1.7,
            1.0,
            13.0,
            12.4,
            2.5,
            3.8,
            4.3,
            1.0,
        ],
    }
    return pd.DataFrame(data)


def build_testing_data(
    dates: Sequence[pd.Timestamp], countries: Sequence[str], rng: random.Random
) -> pd.DataFrame:
    records = []
    for country in countries:
        cumulative_tests = 0
        for i, current_date in enumerate(dates):
            if i < 60:
                daily_tests = rng.randint(1_000, 10_000)
            elif i < 180:
                daily_tests = rng.randint(10_000, 100_000)
            else:
                daily_tests = rng.randint(100_000, 1_000_000)
            cumulative_tests += daily_tests
            records.append(
                {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "country": country,
                    "daily_tests": daily_tests,
                    "cumulative_tests": cumulative_tests,
                }
            )
    return pd.DataFrame(records)


def generate_bundle(
    start: datetime,
    end: datetime,
    countries: Sequence[str],
    states: Sequence[str],
    rng_seed: int,
) -> DatasetBundle:
    rng = random.Random(rng_seed)
    np.random.seed(rng_seed)

    dates = date_range(start, end)
    covid_cases = build_covid_cases(dates, countries, rng)
    hospital_data = build_hospital_data(dates, states, rng)
    vaccination_data = build_vaccination_data(start, end, countries, rng)
    demographics = build_demographics(countries)
    testing_data = build_testing_data(dates, countries, rng)

    return DatasetBundle(
        covid_cases=covid_cases,
        hospital_data=hospital_data,
        vaccination_data=vaccination_data,
        country_demographics=demographics,
        testing_data=testing_data,
    )


def print_summary(bundle: DatasetBundle) -> None:
    summary = {
        "covid_cases": len(bundle.covid_cases),
        "hospital_data": len(bundle.hospital_data),
        "vaccination_data": len(bundle.vaccination_data),
        "country_demographics": len(bundle.country_demographics),
        "testing_data": len(bundle.testing_data),
    }
    print("\n=== DATASET SUMMARY ===")
    for name, count in summary.items():
        print(f"{name:25s}: {count:,} records")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic COVID-19 datasets for the SQL project."
    )
    parser.add_argument(
        "--start-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=DEFAULT_START,
        help="Start date for the time series (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--end-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=DEFAULT_END,
        help="End date for the time series (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory where CSV files will be written.",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    bundle = generate_bundle(
        start=args.start_date,
        end=args.end_date,
        countries=DEFAULT_COUNTRIES,
        states=INDIA_STATES,
        rng_seed=args.seed,
    )
    bundle.save(args.output_dir)
    print_summary(bundle)


if __name__ == "__main__":
    main()
