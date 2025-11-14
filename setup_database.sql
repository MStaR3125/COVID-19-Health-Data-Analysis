-- ============================================
-- COVID-19 HEALTH DATA ANALYSIS PROJECT
-- Complete Database Setup Script
-- ============================================

-- Drop database if exists (for fresh start)
DROP DATABASE IF EXISTS covid19_analysis;

-- Create database
CREATE DATABASE covid19_analysis;
USE covid19_analysis;

-- ============================================
-- TABLE 1: COVID Cases
-- Daily COVID-19 case, death, and recovery data
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE 2: Hospital Data
-- Hospital admissions and capacity data
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE 3: Vaccination Data
-- COVID-19 vaccination progress data
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE 4: Country Demographics
-- Static demographic and health system data
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE 5: Testing Data
-- COVID-19 testing statistics
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Verify Tables Created
-- ============================================
SHOW TABLES;

-- ============================================
-- DATA IMPORT INSTRUCTIONS
-- ============================================
-- After creating tables, import data using one of these methods:
--
-- METHOD 1: MySQL Workbench GUI
-- Right-click each table -> "Table Data Import Wizard" -> Select CSV file
--
-- METHOD 2: LOAD DATA INFILE (Replace paths with your actual file paths)
/*
LOAD DATA INFILE '/path/to/covid_cases.csv'
INTO TABLE covid_cases
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, country, daily_cases, daily_deaths, daily_recovered, 
 cumulative_cases, cumulative_deaths, cumulative_recovered, active_cases);

LOAD DATA INFILE '/path/to/hospital_data.csv'
INTO TABLE hospital_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, state, country, hospital_admissions, icu_admissions, 
 ventilator_usage, available_beds, available_icu_beds);

LOAD DATA INFILE '/path/to/vaccination_data.csv'
INTO TABLE vaccination_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, country, daily_vaccinations_dose1, daily_vaccinations_dose2, 
 daily_vaccinations_booster, cumulative_dose1, cumulative_dose2, 
 cumulative_booster, total_vaccinations);

LOAD DATA INFILE '/path/to/country_demographics.csv'
INTO TABLE country_demographics
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(country, population, median_age, gdp_per_capita, 
 population_density, hospital_beds_per_1000);

LOAD DATA INFILE '/path/to/testing_data.csv'
INTO TABLE testing_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date, country, daily_tests, cumulative_tests);
*/

-- ============================================
-- VERIFICATION QUERIES
-- Run these after data import to verify
-- ============================================

-- Check record counts
/*
SELECT 'covid_cases' AS table_name, COUNT(*) AS records FROM covid_cases
UNION ALL
SELECT 'hospital_data', COUNT(*) FROM hospital_data
UNION ALL
SELECT 'vaccination_data', COUNT(*) FROM vaccination_data
UNION ALL
SELECT 'country_demographics', COUNT(*) FROM country_demographics
UNION ALL
SELECT 'testing_data', COUNT(*) FROM testing_data;
*/

-- Sample data from each table
/*
SELECT * FROM covid_cases LIMIT 5;
SELECT * FROM hospital_data LIMIT 5;
SELECT * FROM vaccination_data LIMIT 5;
SELECT * FROM country_demographics LIMIT 5;
SELECT * FROM testing_data LIMIT 5;
*/

-- ============================================
-- SETUP COMPLETE
-- Next: Import CSV files and run analytical queries
-- ============================================
