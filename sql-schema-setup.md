# COVID-19 Health Data Analysis - SQL Project

## Complete Working SQL Project for Health Data Analysis

This is a comprehensive, production-ready SQL project for analyzing COVID-19 health data. The project includes complete database setup, data import, and 30+ analytical queries to extract meaningful insights from global pandemic data.

---

## 📊 Project Overview

**Project Focus:** Global COVID-19 Health Data Analysis (2020-2024)

**Data Scope:**
- 20 countries including India, USA, Brazil, UK, and more
- Time period: January 2020 - November 2024
- 116,860+ total records across 5 comprehensive datasets

**Key Features:**
- ✅ Real-world data structure based on WHO/OWID standards
- ✅ Complete SQL schema with proper constraints
- ✅ Data import scripts for all tables
- ✅ 30+ analytical queries with explanations
- ✅ Advanced SQL techniques (CTEs, Window Functions, Joins)
- ✅ Trend analysis, hotspot identification, rate calculations

---

## 📁 Dataset Structure

### 1. **covid_cases** (35,560 records)
Daily COVID-19 case data by country

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of record |
| country | VARCHAR(100) | Country name |
| daily_cases | INT | New confirmed cases |
| daily_deaths | INT | New deaths |
| daily_recovered | INT | New recoveries |
| cumulative_cases | BIGINT | Total confirmed cases |
| cumulative_deaths | INT | Total deaths |
| cumulative_recovered | BIGINT | Total recovered |
| active_cases | BIGINT | Currently active cases |

### 2. **hospital_data** (17,780 records)
Hospital admission and capacity data for Indian states

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of record |
| state | VARCHAR(100) | State/region name |
| country | VARCHAR(100) | Country name |
| hospital_admissions | INT | Daily hospital admissions |
| icu_admissions | INT | ICU admissions |
| ventilator_usage | INT | Ventilators in use |
| available_beds | INT | Available hospital beds |
| available_icu_beds | INT | Available ICU beds |

### 3. **vaccination_data** (27,940 records)
Daily vaccination statistics by country

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of record |
| country | VARCHAR(100) | Country name |
| daily_vaccinations_dose1 | INT | First dose administered |
| daily_vaccinations_dose2 | INT | Second dose administered |
| daily_vaccinations_booster | INT | Booster doses administered |
| cumulative_dose1 | BIGINT | Total first doses |
| cumulative_dose2 | BIGINT | Total second doses |
| cumulative_booster | BIGINT | Total boosters |
| total_vaccinations | BIGINT | All vaccinations combined |

### 4. **country_demographics** (20 records)
Static demographic and health system data

| Column | Type | Description |
|--------|------|-------------|
| country | VARCHAR(100) | Country name |
| population | BIGINT | Total population |
| median_age | DECIMAL(4,1) | Median age of population |
| gdp_per_capita | INT | GDP per capita (USD) |
| population_density | INT | People per sq km |
| hospital_beds_per_1000 | DECIMAL(4,1) | Hospital beds per 1,000 people |

### 5. **testing_data** (35,560 records)
COVID-19 testing statistics by country

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of record |
| country | VARCHAR(100) | Country name |
| daily_tests | INT | Tests conducted daily |
| cumulative_tests | BIGINT | Total tests conducted |

---

## 🛠️ Database Setup

### Step 1: Create Database

```sql
-- Create the COVID-19 database
CREATE DATABASE covid19_analysis;

-- Use the database
USE covid19_analysis;
```

---

### Step 2: Create Tables

```sql
-- ============================================
-- TABLE 1: COVID Cases
-- ============================================
CREATE TABLE covid_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR(100) NOT NULL,
    daily_cases INT DEFAULT 0,
    daily_deaths INT DEFAULT 0,
    daily_recovered INT DEFAULT 0,
    cumulative_cases BIGINT DEFAULT 0,
    cumulative_deaths INT DEFAULT 0,
    cumulative_recovered BIGINT DEFAULT 0,
    active_cases BIGINT DEFAULT 0,
    INDEX idx_date (date),
    INDEX idx_country (country),
    INDEX idx_date_country (date, country)
);

-- ============================================
-- TABLE 2: Hospital Data
-- ============================================
CREATE TABLE hospital_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    hospital_admissions INT DEFAULT 0,
    icu_admissions INT DEFAULT 0,
    ventilator_usage INT DEFAULT 0,
    available_beds INT DEFAULT 0,
    available_icu_beds INT DEFAULT 0,
    INDEX idx_date (date),
    INDEX idx_state (state),
    INDEX idx_date_state (date, state)
);

-- ============================================
-- TABLE 3: Vaccination Data
-- ============================================
CREATE TABLE vaccination_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR(100) NOT NULL,
    daily_vaccinations_dose1 INT DEFAULT 0,
    daily_vaccinations_dose2 INT DEFAULT 0,
    daily_vaccinations_booster INT DEFAULT 0,
    cumulative_dose1 BIGINT DEFAULT 0,
    cumulative_dose2 BIGINT DEFAULT 0,
    cumulative_booster BIGINT DEFAULT 0,
    total_vaccinations BIGINT DEFAULT 0,
    INDEX idx_date (date),
    INDEX idx_country (country),
    INDEX idx_date_country (date, country)
);

-- ============================================
-- TABLE 4: Country Demographics
-- ============================================
CREATE TABLE country_demographics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100) NOT NULL UNIQUE,
    population BIGINT NOT NULL,
    median_age DECIMAL(4,1),
    gdp_per_capita INT,
    population_density INT,
    hospital_beds_per_1000 DECIMAL(4,1),
    INDEX idx_country (country)
);

-- ============================================
-- TABLE 5: Testing Data
-- ============================================
CREATE TABLE testing_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    country VARCHAR(100) NOT NULL,
    daily_tests INT DEFAULT 0,
    cumulative_tests BIGINT DEFAULT 0,
    INDEX idx_date (date),
    INDEX idx_country (country),
    INDEX idx_date_country (date, country)
);
```

---

### Step 3: Import Data

**Option A: Using MySQL LOAD DATA INFILE (Fastest)**

```sql
-- Import COVID Cases
LOAD DATA INFILE 'covid_cases.csv'
INTO TABLE covid_cases
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, country, daily_cases, daily_deaths, daily_recovered, 
 cumulative_cases, cumulative_deaths, cumulative_recovered, active_cases);

-- Import Hospital Data
LOAD DATA INFILE 'hospital_data.csv'
INTO TABLE hospital_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, state, country, hospital_admissions, icu_admissions, 
 ventilator_usage, available_beds, available_icu_beds);

-- Import Vaccination Data
LOAD DATA INFILE 'vaccination_data.csv'
INTO TABLE vaccination_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, country, daily_vaccinations_dose1, daily_vaccinations_dose2, 
 daily_vaccinations_booster, cumulative_dose1, cumulative_dose2, 
 cumulative_booster, total_vaccinations);

-- Import Demographics
LOAD DATA INFILE 'country_demographics.csv'
INTO TABLE country_demographics
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(country, population, median_age, gdp_per_capita, 
 population_density, hospital_beds_per_1000);

-- Import Testing Data
LOAD DATA INFILE 'testing_data.csv'
INTO TABLE testing_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, country, daily_tests, cumulative_tests);
```

**Option B: Using MySQL Workbench GUI**

1. Right-click on table → "Table Data Import Wizard"
2. Select the CSV file
3. Map columns automatically
4. Click "Next" and "Finish"

**Option C: Using Python/Scripts (Cross-platform)**

```python
import pandas as pd
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='covid19_analysis'
)

# Read and import data
tables = {
    'covid_cases': 'covid_cases.csv',
    'hospital_data': 'hospital_data.csv',
    'vaccination_data': 'vaccination_data.csv',
    'country_demographics': 'country_demographics.csv',
    'testing_data': 'testing_data.csv'
}

for table_name, file_name in tables.items():
    df = pd.read_csv(file_name)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    print(f"✓ Imported {table_name}")

conn.close()
```

---

### Step 4: Verify Data Import

```sql
-- Check record counts
SELECT 'covid_cases' AS table_name, COUNT(*) AS records FROM covid_cases
UNION ALL
SELECT 'hospital_data', COUNT(*) FROM hospital_data
UNION ALL
SELECT 'vaccination_data', COUNT(*) FROM vaccination_data
UNION ALL
SELECT 'country_demographics', COUNT(*) FROM country_demographics
UNION ALL
SELECT 'testing_data', COUNT(*) FROM testing_data;

-- Sample data from each table
SELECT * FROM covid_cases LIMIT 5;
SELECT * FROM hospital_data LIMIT 5;
SELECT * FROM vaccination_data LIMIT 5;
SELECT * FROM country_demographics LIMIT 5;
SELECT * FROM testing_data LIMIT 5;
```

---

## ✅ Ready to Analyze!

Your database is now set up with:
- ✓ 5 comprehensive tables
- ✓ 116,860+ records
- ✓ Proper indexes for fast queries
- ✓ Data from 2020-2024

**Next Step:** Proceed to the analytical queries document to start analyzing the data!

---

## 🔧 Troubleshooting

**Error: "File not found"**
- Ensure CSV files are in MySQL's secure file directory
- Use full file paths: `'C:/path/to/covid_cases.csv'`
- Or use GUI import method

**Error: "Access denied"**
- Grant file privileges: `GRANT FILE ON *.* TO 'username'@'localhost';`

**Error: "Data truncated"**
- Check CSV data format matches table schema
- Verify date format is YYYY-MM-DD

---

## 📚 Resources

- CSV files: Provided with this project
- MySQL Documentation: https://dev.mysql.com/doc/
- Project Repository: Contains all scripts and data files
