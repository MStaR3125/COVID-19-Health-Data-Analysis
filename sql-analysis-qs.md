# COVID-19 Data Analysis - SQL Queries

## 30+ Analytical SQL Queries for COVID-19 Health Data

This document contains comprehensive SQL queries to analyze COVID-19 data, answer critical questions, and extract meaningful insights from the pandemic dataset.

---

## 📋 Table of Contents

1. [Basic Data Exploration](#1-basic-data-exploration)
2. [Trend Analysis](#2-trend-analysis)
3. [Country Comparisons](#3-country-comparisons)
4. [Hotspot Identification](#4-hotspot-identification)
5. [Infection & Recovery Rates](#5-infection--recovery-rates)
6. [Hospital & Healthcare Analysis](#6-hospital--healthcare-analysis)
7. [Vaccination Analysis](#7-vaccination-analysis)
8. [Advanced Analytics](#8-advanced-analytics)

---

## 1. Basic Data Exploration

### Query 1.1: Overview of Total Cases and Deaths Globally

```sql
-- Get global COVID-19 summary
SELECT 
    MAX(date) AS latest_date,
    SUM(daily_cases) AS total_cases_reported,
    SUM(daily_deaths) AS total_deaths_reported,
    ROUND(SUM(daily_deaths) * 100.0 / NULLIF(SUM(daily_cases), 0), 2) AS global_fatality_rate_pct
FROM covid_cases;
```

**Purpose:** Get an overall snapshot of the pandemic's global impact.

---

### Query 1.2: List All Countries in Dataset

```sql
-- Get list of all countries with their latest statistics
SELECT DISTINCT 
    c.country,
    d.population,
    d.median_age,
    d.gdp_per_capita,
    d.hospital_beds_per_1000
FROM covid_cases c
LEFT JOIN country_demographics d ON c.country = d.country
ORDER BY c.country;
```

---

### Query 1.3: Date Range of Available Data

```sql
-- Check data availability period
SELECT 
    country,
    MIN(date) AS first_record_date,
    MAX(date) AS last_record_date,
    DATEDIFF(MAX(date), MIN(date)) AS days_of_data
FROM covid_cases
GROUP BY country
ORDER BY country;
```

---

## 2. Trend Analysis

### Query 2.1: Daily Cases Trend for India (Last 30 Days)

```sql
-- Show recent daily trend for India
SELECT 
    date,
    daily_cases,
    daily_deaths,
    daily_recovered,
    active_cases,
    ROUND(daily_deaths * 100.0 / NULLIF(daily_cases, 0), 2) AS daily_fatality_rate_pct
FROM covid_cases
WHERE country = 'India' 
  AND date >= DATE_SUB((SELECT MAX(date) FROM covid_cases), INTERVAL 30 DAY)
ORDER BY date DESC;
```

---

### Query 2.2: Monthly Case Trends by Country

```sql
-- Aggregate cases by month for trend analysis
SELECT 
    country,
    DATE_FORMAT(date, '%Y-%m') AS year_month,
    SUM(daily_cases) AS monthly_cases,
    SUM(daily_deaths) AS monthly_deaths,
    ROUND(SUM(daily_deaths) * 100.0 / NULLIF(SUM(daily_cases), 0), 2) AS monthly_fatality_rate
FROM covid_cases
WHERE country IN ('India', 'USA', 'Brazil', 'UK', 'France')
GROUP BY country, DATE_FORMAT(date, '%Y-%m')
ORDER BY country, year_month;
```

---

### Query 2.3: Peak Infection Days by Country

```sql
-- Find the day with highest cases for each country
WITH RankedDays AS (
    SELECT 
        country,
        date,
        daily_cases,
        RANK() OVER (PARTITION BY country ORDER BY daily_cases DESC) AS case_rank
    FROM covid_cases
)
SELECT 
    country,
    date AS peak_date,
    daily_cases AS peak_daily_cases
FROM RankedDays
WHERE case_rank = 1
ORDER BY peak_daily_cases DESC;
```

---

### Query 2.4: Year-over-Year Growth Analysis

```sql
-- Compare total cases year by year
SELECT 
    country,
    YEAR(date) AS year,
    SUM(daily_cases) AS total_cases,
    SUM(daily_deaths) AS total_deaths,
    ROUND(SUM(daily_deaths) * 100.0 / NULLIF(SUM(daily_cases), 0), 2) AS fatality_rate
FROM covid_cases
WHERE country = 'India'
GROUP BY country, YEAR(date)
ORDER BY year;
```

---

## 3. Country Comparisons

### Query 3.1: Top 10 Countries by Total Cases

```sql
-- Rank countries by cumulative cases
SELECT 
    country,
    MAX(cumulative_cases) AS total_cases,
    MAX(cumulative_deaths) AS total_deaths,
    ROUND(MAX(cumulative_deaths) * 100.0 / NULLIF(MAX(cumulative_cases), 0), 2) AS overall_fatality_rate
FROM covid_cases
GROUP BY country
ORDER BY total_cases DESC
LIMIT 10;
```

---

### Query 3.2: Cases Per Capita Analysis

```sql
-- Compare impact adjusted for population size
SELECT 
    c.country,
    MAX(c.cumulative_cases) AS total_cases,
    d.population,
    ROUND(MAX(c.cumulative_cases) * 100000.0 / d.population, 2) AS cases_per_100k_population,
    ROUND(MAX(c.cumulative_deaths) * 100000.0 / d.population, 2) AS deaths_per_100k_population
FROM covid_cases c
JOIN country_demographics d ON c.country = d.country
GROUP BY c.country, d.population
ORDER BY cases_per_100k_population DESC;
```

---

### Query 3.3: Countries with Highest Fatality Rates

```sql
-- Identify countries with highest death rates
SELECT 
    country,
    MAX(cumulative_cases) AS total_cases,
    MAX(cumulative_deaths) AS total_deaths,
    ROUND(MAX(cumulative_deaths) * 100.0 / NULLIF(MAX(cumulative_cases), 0), 2) AS fatality_rate_pct
FROM covid_cases
GROUP BY country
HAVING MAX(cumulative_cases) > 100000  -- Filter countries with significant cases
ORDER BY fatality_rate_pct DESC
LIMIT 10;
```

---

### Query 3.4: Recovery Rate Comparison

```sql
-- Compare recovery rates across countries
SELECT 
    country,
    MAX(cumulative_cases) AS total_cases,
    MAX(cumulative_recovered) AS total_recovered,
    ROUND(MAX(cumulative_recovered) * 100.0 / NULLIF(MAX(cumulative_cases), 0), 2) AS recovery_rate_pct
FROM covid_cases
GROUP BY country
HAVING MAX(cumulative_cases) > 50000
ORDER BY recovery_rate_pct DESC;
```

---

## 4. Hotspot Identification

### Query 4.1: Identify COVID-19 Hotspots in 2024

```sql
-- Find regions with highest cases in 2024
SELECT 
    country,
    DATE_FORMAT(date, '%Y-%m') AS month,
    SUM(daily_cases) AS monthly_cases,
    AVG(daily_cases) AS avg_daily_cases
FROM covid_cases
WHERE YEAR(date) = 2024
GROUP BY country, DATE_FORMAT(date, '%Y-%m')
HAVING SUM(daily_cases) > 10000  -- Threshold for hotspot
ORDER BY monthly_cases DESC
LIMIT 20;
```

---

### Query 4.2: State-wise Hotspots in India (Hospital Data)

```sql
-- Identify states with highest hospital admissions
SELECT 
    state,
    DATE_FORMAT(date, '%Y-%m') AS month,
    SUM(hospital_admissions) AS total_admissions,
    AVG(hospital_admissions) AS avg_daily_admissions,
    SUM(icu_admissions) AS total_icu_admissions
FROM hospital_data
WHERE country = 'India' 
  AND YEAR(date) >= 2024
GROUP BY state, DATE_FORMAT(date, '%Y-%m')
ORDER BY total_admissions DESC;
```

---

### Query 4.3: Moving Average to Identify Surges

```sql
-- Use 7-day moving average to identify case surges
SELECT 
    country,
    date,
    daily_cases,
    AVG(daily_cases) OVER (
        PARTITION BY country 
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_day_avg
FROM covid_cases
WHERE country = 'India' 
  AND date >= '2024-01-01'
ORDER BY date DESC
LIMIT 30;
```

---

### Query 4.4: Rapid Growth Detection

```sql
-- Find periods of exponential growth (>50% week-over-week)
WITH WeeklyData AS (
    SELECT 
        country,
        DATE_FORMAT(date, '%Y-%u') AS year_week,
        SUM(daily_cases) AS weekly_cases
    FROM covid_cases
    GROUP BY country, DATE_FORMAT(date, '%Y-%u')
),
GrowthRates AS (
    SELECT 
        country,
        year_week,
        weekly_cases,
        LAG(weekly_cases) OVER (PARTITION BY country ORDER BY year_week) AS prev_week_cases,
        ROUND((weekly_cases - LAG(weekly_cases) OVER (PARTITION BY country ORDER BY year_week)) 
              * 100.0 / NULLIF(LAG(weekly_cases) OVER (PARTITION BY country ORDER BY year_week), 0), 2) AS growth_rate_pct
    FROM WeeklyData
)
SELECT *
FROM GrowthRates
WHERE growth_rate_pct > 50  -- 50% growth threshold
  AND weekly_cases > 1000    -- Minimum case threshold
ORDER BY growth_rate_pct DESC
LIMIT 20;
```

---

## 5. Infection & Recovery Rates

### Query 5.1: Calculate Daily Infection Rate

```sql
-- Infection rate = (new cases / tests) * 100
SELECT 
    c.date,
    c.country,
    c.daily_cases,
    t.daily_tests,
    ROUND(c.daily_cases * 100.0 / NULLIF(t.daily_tests, 0), 2) AS infection_rate_pct,
    ROUND(t.daily_tests * 1.0 / NULLIF(c.daily_cases, 0), 2) AS tests_per_case
FROM covid_cases c
JOIN testing_data t ON c.country = t.country AND c.date = t.date
WHERE c.country = 'India' 
  AND c.date >= '2024-01-01'
ORDER BY c.date DESC
LIMIT 30;
```

---

### Query 5.2: Recovery Rate Analysis

```sql
-- Calculate recovery rates over time
SELECT 
    country,
    date,
    cumulative_cases,
    cumulative_recovered,
    cumulative_deaths,
    ROUND(cumulative_recovered * 100.0 / NULLIF(cumulative_cases, 0), 2) AS recovery_rate_pct,
    ROUND(cumulative_deaths * 100.0 / NULLIF(cumulative_cases, 0), 2) AS fatality_rate_pct
FROM covid_cases
WHERE country = 'India' 
  AND date >= '2024-01-01'
ORDER BY date DESC
LIMIT 30;
```

---

### Query 5.3: Case Fatality Rate (CFR) by Country

```sql
-- Compare CFR across countries with demographics
SELECT 
    c.country,
    MAX(c.cumulative_cases) AS total_cases,
    MAX(c.cumulative_deaths) AS total_deaths,
    ROUND(MAX(c.cumulative_deaths) * 100.0 / NULLIF(MAX(c.cumulative_cases), 0), 2) AS cfr_pct,
    d.median_age,
    d.hospital_beds_per_1000,
    d.gdp_per_capita
FROM covid_cases c
JOIN country_demographics d ON c.country = d.country
GROUP BY c.country, d.median_age, d.hospital_beds_per_1000, d.gdp_per_capita
HAVING total_cases > 100000
ORDER BY cfr_pct DESC;
```

---

### Query 5.4: Active Case Rate

```sql
-- Proportion of active cases to total cases
SELECT 
    country,
    date,
    active_cases,
    cumulative_cases,
    ROUND(active_cases * 100.0 / NULLIF(cumulative_cases, 0), 2) AS active_rate_pct
FROM covid_cases
WHERE date = (SELECT MAX(date) FROM covid_cases)
ORDER BY active_rate_pct DESC
LIMIT 20;
```

---

## 6. Hospital & Healthcare Analysis

### Query 6.1: Hospital Capacity Analysis

```sql
-- Analyze hospital bed availability vs admissions
SELECT 
    state,
    DATE_FORMAT(date, '%Y-%m') AS month,
    AVG(hospital_admissions) AS avg_daily_admissions,
    AVG(available_beds) AS avg_available_beds,
    ROUND(AVG(hospital_admissions) * 100.0 / NULLIF(AVG(available_beds), 0), 2) AS capacity_utilization_pct,
    AVG(icu_admissions) AS avg_icu_admissions,
    AVG(available_icu_beds) AS avg_available_icu_beds
FROM hospital_data
WHERE country = 'India' 
  AND YEAR(date) = 2024
GROUP BY state, DATE_FORMAT(date, '%Y-%m')
ORDER BY capacity_utilization_pct DESC;
```

---

### Query 6.2: ICU Utilization Rates

```sql
-- Track ICU capacity stress
SELECT 
    state,
    date,
    icu_admissions,
    available_icu_beds,
    ROUND(icu_admissions * 100.0 / NULLIF(available_icu_beds, 0), 2) AS icu_utilization_pct,
    ventilator_usage
FROM hospital_data
WHERE country = 'India'
  AND date >= DATE_SUB((SELECT MAX(date) FROM hospital_data), INTERVAL 30 DAY)
ORDER BY icu_utilization_pct DESC
LIMIT 50;
```

---

### Query 6.3: States Exceeding Hospital Capacity

```sql
-- Identify healthcare system stress points
SELECT 
    state,
    date,
    hospital_admissions,
    available_beds,
    CASE 
        WHEN hospital_admissions > available_beds THEN 'OVERCAPACITY'
        WHEN hospital_admissions > available_beds * 0.8 THEN 'CRITICAL'
        WHEN hospital_admissions > available_beds * 0.6 THEN 'HIGH'
        ELSE 'MANAGEABLE'
    END AS capacity_status
FROM hospital_data
WHERE country = 'India'
  AND hospital_admissions > available_beds * 0.6
ORDER BY date DESC, hospital_admissions DESC
LIMIT 100;
```

---

### Query 6.4: Ventilator Demand Analysis

```sql
-- Analyze critical care equipment usage
SELECT 
    state,
    AVG(ventilator_usage) AS avg_ventilators_used,
    MAX(ventilator_usage) AS max_ventilators_used,
    SUM(ventilator_usage) AS total_ventilator_days
FROM hospital_data
WHERE country = 'India' 
  AND YEAR(date) = 2024
GROUP BY state
ORDER BY avg_ventilators_used DESC;
```

---

## 7. Vaccination Analysis

### Query 7.1: Vaccination Progress by Country

```sql
-- Track vaccination rollout progress
SELECT 
    v.country,
    MAX(v.cumulative_dose1) AS total_dose1,
    MAX(v.cumulative_dose2) AS total_dose2,
    MAX(v.cumulative_booster) AS total_boosters,
    MAX(v.total_vaccinations) AS total_all_doses,
    d.population,
    ROUND(MAX(v.cumulative_dose1) * 100.0 / d.population, 2) AS pct_dose1_coverage,
    ROUND(MAX(v.cumulative_dose2) * 100.0 / d.population, 2) AS pct_fully_vaccinated
FROM vaccination_data v
JOIN country_demographics d ON v.country = d.country
GROUP BY v.country, d.population
ORDER BY pct_fully_vaccinated DESC;
```

---

### Query 7.2: Daily Vaccination Rate

```sql
-- Monitor vaccination speed
SELECT 
    country,
    date,
    daily_vaccinations_dose1 + daily_vaccinations_dose2 + daily_vaccinations_booster AS total_daily_doses,
    AVG(daily_vaccinations_dose1 + daily_vaccinations_dose2 + daily_vaccinations_booster) 
        OVER (PARTITION BY country ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS seven_day_avg_doses
FROM vaccination_data
WHERE country = 'India'
  AND date >= '2024-01-01'
ORDER BY date DESC
LIMIT 30;
```

---

### Query 7.3: Vaccination Impact on Cases

```sql
-- Correlate vaccination with case reduction
WITH VaxAndCases AS (
    SELECT 
        c.country,
        DATE_FORMAT(c.date, '%Y-%m') AS month,
        AVG(c.daily_cases) AS avg_daily_cases,
        MAX(v.cumulative_dose1) AS cumulative_dose1,
        MAX(d.population) AS population,
        ROUND(MAX(v.cumulative_dose1) * 100.0 / MAX(d.population), 2) AS vaccination_coverage_pct
    FROM covid_cases c
    JOIN vaccination_data v ON c.country = v.country AND c.date = v.date
    JOIN country_demographics d ON c.country = d.country
    WHERE c.country = 'India'
    GROUP BY c.country, DATE_FORMAT(c.date, '%Y-%m')
)
SELECT 
    month,
    avg_daily_cases,
    vaccination_coverage_pct,
    LAG(avg_daily_cases) OVER (ORDER BY month) AS prev_month_cases,
    ROUND((avg_daily_cases - LAG(avg_daily_cases) OVER (ORDER BY month)) 
          * 100.0 / NULLIF(LAG(avg_daily_cases) OVER (ORDER BY month), 0), 2) AS case_growth_rate
FROM VaxAndCases
ORDER BY month;
```

---

### Query 7.4: Booster Dose Adoption

```sql
-- Analyze booster uptake
SELECT 
    country,
    MAX(cumulative_dose2) AS fully_vaccinated,
    MAX(cumulative_booster) AS booster_doses,
    ROUND(MAX(cumulative_booster) * 100.0 / NULLIF(MAX(cumulative_dose2), 0), 2) AS booster_uptake_pct
FROM vaccination_data
GROUP BY country
HAVING fully_vaccinated > 1000000
ORDER BY booster_uptake_pct DESC;
```

---

## 8. Advanced Analytics

### Query 8.1: Comprehensive Country Dashboard

```sql
-- All key metrics in one view
SELECT 
    c.country,
    d.population,
    d.median_age,
    d.gdp_per_capita,
    MAX(c.cumulative_cases) AS total_cases,
    MAX(c.cumulative_deaths) AS total_deaths,
    MAX(c.active_cases) AS current_active_cases,
    ROUND(MAX(c.cumulative_deaths) * 100.0 / NULLIF(MAX(c.cumulative_cases), 0), 2) AS fatality_rate,
    ROUND(MAX(c.cumulative_cases) * 100000.0 / d.population, 2) AS cases_per_100k,
    MAX(v.cumulative_dose2) AS fully_vaccinated,
    ROUND(MAX(v.cumulative_dose2) * 100.0 / d.population, 2) AS vaccination_rate,
    MAX(t.cumulative_tests) AS total_tests,
    ROUND(MAX(t.cumulative_tests) * 1.0 / d.population, 2) AS tests_per_capita
FROM covid_cases c
LEFT JOIN country_demographics d ON c.country = d.country
LEFT JOIN vaccination_data v ON c.country = v.country AND c.date = v.date
LEFT JOIN testing_data t ON c.country = t.country AND c.date = t.date
WHERE c.date = (SELECT MAX(date) FROM covid_cases)
GROUP BY c.country, d.population, d.median_age, d.gdp_per_capita
ORDER BY total_cases DESC;
```

---

### Query 8.2: Time Series Analysis with Windows

```sql
-- Advanced time series analysis
SELECT 
    country,
    date,
    daily_cases,
    AVG(daily_cases) OVER (PARTITION BY country ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7day,
    AVG(daily_cases) OVER (PARTITION BY country ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS ma_30day,
    daily_cases - AVG(daily_cases) OVER (PARTITION BY country ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS deviation_from_avg
FROM covid_cases
WHERE country = 'India'
  AND date >= '2024-01-01'
ORDER BY date DESC
LIMIT 90;
```

---

### Query 8.3: Cohort Analysis - Waves Comparison

```sql
-- Compare different pandemic waves
WITH WaveDefinitions AS (
    SELECT 
        country,
        date,
        daily_cases,
        CASE 
            WHEN date BETWEEN '2020-03-01' AND '2020-09-30' THEN 'Wave 1'
            WHEN date BETWEEN '2021-03-01' AND '2021-07-31' THEN 'Wave 2'
            WHEN date BETWEEN '2022-01-01' AND '2022-03-31' THEN 'Wave 3'
            WHEN date BETWEEN '2024-01-01' AND '2024-06-30' THEN 'Wave 4'
        END AS wave
    FROM covid_cases
    WHERE country = 'India'
)
SELECT 
    wave,
    COUNT(DISTINCT date) AS days_in_wave,
    SUM(daily_cases) AS total_cases_in_wave,
    AVG(daily_cases) AS avg_daily_cases,
    MAX(daily_cases) AS peak_daily_cases
FROM WaveDefinitions
WHERE wave IS NOT NULL
GROUP BY wave
ORDER BY wave;
```

---

### Query 8.4: Predictive Indicators

```sql
-- Create leading indicators for outbreak prediction
SELECT 
    c.country,
    c.date,
    c.daily_cases,
    t.daily_tests,
    ROUND(c.daily_cases * 100.0 / NULLIF(t.daily_tests, 0), 2) AS positivity_rate,
    LAG(c.daily_cases, 7) OVER (PARTITION BY c.country ORDER BY c.date) AS cases_1week_ago,
    ROUND((c.daily_cases - LAG(c.daily_cases, 7) OVER (PARTITION BY c.country ORDER BY c.date)) 
          * 100.0 / NULLIF(LAG(c.daily_cases, 7) OVER (PARTITION BY c.country ORDER BY c.date), 0), 2) AS weekly_growth_rate,
    CASE 
        WHEN (c.daily_cases - LAG(c.daily_cases, 7) OVER (PARTITION BY c.country ORDER BY c.date)) 
             * 100.0 / NULLIF(LAG(c.daily_cases, 7) OVER (PARTITION BY c.country ORDER BY c.date), 0) > 20
             AND c.daily_cases * 100.0 / NULLIF(t.daily_tests, 0) > 5
        THEN 'HIGH RISK'
        WHEN (c.daily_cases - LAG(c.daily_cases, 7) OVER (PARTITION BY c.country ORDER BY c.date)) 
             * 100.0 / NULLIF(LAG(c.daily_cases, 7) OVER (PARTITION BY c.country ORDER BY c.date), 0) > 10
        THEN 'ELEVATED RISK'
        ELSE 'STABLE'
    END AS outbreak_risk_level
FROM covid_cases c
JOIN testing_data t ON c.country = t.country AND c.date = t.date
WHERE c.country = 'India'
  AND c.date >= DATE_SUB((SELECT MAX(date) FROM covid_cases), INTERVAL 60 DAY)
ORDER BY c.date DESC;
```

---

### Query 8.5: Healthcare System Stress Index

```sql
-- Create composite stress index
SELECT 
    h.state,
    h.date,
    ROUND(
        (h.hospital_admissions * 100.0 / NULLIF(h.available_beds, 0) * 0.4) +
        (h.icu_admissions * 100.0 / NULLIF(h.available_icu_beds, 0) * 0.4) +
        (c.active_cases * 0.01 * 0.2),
        2
    ) AS healthcare_stress_index,
    CASE 
        WHEN ROUND((h.hospital_admissions * 100.0 / NULLIF(h.available_beds, 0) * 0.4) +
                   (h.icu_admissions * 100.0 / NULLIF(h.available_icu_beds, 0) * 0.4) +
                   (c.active_cases * 0.01 * 0.2), 2) > 80 THEN 'CRITICAL'
        WHEN ROUND((h.hospital_admissions * 100.0 / NULLIF(h.available_beds, 0) * 0.4) +
                   (h.icu_admissions * 100.0 / NULLIF(h.available_icu_beds, 0) * 0.4) +
                   (c.active_cases * 0.01 * 0.2), 2) > 60 THEN 'HIGH'
        WHEN ROUND((h.hospital_admissions * 100.0 / NULLIF(h.available_beds, 0) * 0.4) +
                   (h.icu_admissions * 100.0 / NULLIF(h.available_icu_beds, 0) * 0.4) +
                   (c.active_cases * 0.01 * 0.2), 2) > 40 THEN 'MODERATE'
        ELSE 'LOW'
    END AS stress_level
FROM hospital_data h
JOIN covid_cases c ON h.date = c.date AND h.country = c.country
WHERE h.country = 'India'
  AND h.date >= DATE_SUB((SELECT MAX(date) FROM hospital_data), INTERVAL 30 DAY)
ORDER BY healthcare_stress_index DESC
LIMIT 50;
```

---

## 🎯 Summary

These 30+ SQL queries provide comprehensive analysis covering:

✅ **Basic Exploration** - Understanding the data structure and scope
✅ **Trend Analysis** - Identifying patterns over time
✅ **Country Comparisons** - Benchmarking impact across nations
✅ **Hotspot Identification** - Finding areas of concern
✅ **Rate Calculations** - Infection, recovery, and fatality metrics
✅ **Healthcare Analysis** - Hospital capacity and stress assessment
✅ **Vaccination Tracking** - Monitoring immunization progress
✅ **Advanced Analytics** - Predictive indicators and composite metrics

---

## 💡 Tips for Analysis

1. **Always filter NULL values** using `NULLIF()` in divisions
2. **Use indexes** on date and country columns for performance
3. **Apply date ranges** to focus on relevant time periods
4. **Validate results** by cross-checking with multiple queries
5. **Document assumptions** especially for calculated metrics

---

## 📊 Visualization Recommendations

Export query results to:
- **Excel/Google Sheets** - For pivot tables and charts
- **Power BI / Tableau** - For interactive dashboards
- **Python (Pandas/Matplotlib)** - For advanced visualizations
- **R (ggplot2)** - For statistical graphics

---

## 🔄 Next Steps

1. Create views for frequently used queries
2. Build stored procedures for automated reporting
3. Set up scheduled jobs for daily updates
4. Develop dashboards for stakeholders
5. Implement alerting for threshold breaches
