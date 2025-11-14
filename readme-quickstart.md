# COVID-19 SQL Project - Quick Start Guide

## Get Your COVID-19 Health Data Analysis Project Running in 15 Minutes!

This is a **complete, working SQL project** that you can set up and run immediately. Follow these steps to get started.

> ✅ All five CSVs are **synthetic but realistic**, generated with the bundled `generate_datasets.py` script so you can reproduce or customize the dataset whenever you like.

---

## 🎯 What You'll Get

After setup, you'll have:
- ✅ A fully functional COVID-19 database with **116,860+ records**
- ✅ 5 comprehensive tables with real-world data structure
- ✅ 30+ ready-to-run analytical queries
- ✅ Data from 20 countries spanning 2020-2024
- ✅ Advanced analytics including trends, hotspots, rates, and predictions

---

## 📦 Project Files

You should have these 7 files:

1. **covid_cases.csv** (35,560 records) - Daily case, death, and recovery data
2. **hospital_data.csv** (17,780 records) - Hospital admissions and capacity
3. **vaccination_data.csv** (27,940 records) - Vaccination progress data
4. **country_demographics.csv** (20 records) - Population and health system data
5. **testing_data.csv** (35,560 records) - COVID testing statistics
6. **sql-schema-setup.md** - Complete database setup instructions
7. **sql-analysis-qs.md** - 30+ analytical queries with explanations

---

## 🚀 Quick Setup (3 Steps)

### Before you begin: install dependencies

```powershell
pip install -r requirements.txt
```

### Step 0: configure credentials

Copy `.env.example` to `.env` (or set the `COVID_DB_*` environment variables) and fill in your MySQL connection details:

```
COVID_DB_HOST=localhost
COVID_DB_USER=root
COVID_DB_PASSWORD=your_password
COVID_DB_NAME=covid19_analysis
```

### Step 1: Install MySQL (if not already installed)

**Windows:**
- Download from: https://dev.mysql.com/downloads/installer/
- Run installer → Choose "Developer Default"
- Set root password (remember this!)

**Mac:**
```bash
brew install mysql
brew services start mysql
```

**Linux:**
```bash
sudo apt-get install mysql-server
sudo systemctl start mysql
```

---

### Step 2: Create Database and Tables

Open MySQL command line or MySQL Workbench and run:

```sql
-- Create database
CREATE DATABASE covid19_analysis;
USE covid19_analysis;

-- Create all 5 tables
-- (Copy the CREATE TABLE statements from sql-schema-setup.md)
```

Or simply run this single command:
```bash
mysql -u root -p < setup_database.sql
```

---

### Step 3: Import Data

**Option A: MySQL Workbench (Easiest)**
1. Right-click on each table → "Table Data Import Wizard"
2. Select corresponding CSV file
3. Click Next → Finish
4. Repeat for all 5 tables

**Option B: Command Line**
```sql
LOAD DATA INFILE '/path/to/covid_cases.csv'
INTO TABLE covid_cases
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Repeat for other tables
```

**Option C: Python Script** (Cross-platform)
Run the provided importer instead of hand-writing scripts:

```powershell
python import_data.py --reset
```

It will read credentials from `COVID_DB_*` environment variables (or `.env`) and can append data safely if you omit `--reset`.

---

## ✅ Verify Setup

Run this query to confirm everything is loaded:

```sql
-- Check all tables
SELECT 'covid_cases' AS table_name, COUNT(*) AS records FROM covid_cases
UNION ALL
SELECT 'hospital_data', COUNT(*) FROM hospital_data
UNION ALL
SELECT 'vaccination_data', COUNT(*) FROM vaccination_data
UNION ALL
SELECT 'country_demographics', COUNT(*) FROM country_demographics
UNION ALL
SELECT 'testing_data', COUNT(*) FROM testing_data;
```

**Expected Output:**
```
table_name              | records
------------------------|--------
covid_cases             | 35,560
hospital_data           | 17,780
vaccination_data        | 27,940
country_demographics    | 20
testing_data            | 35,560
```

---

## 🎓 Run Your First Queries

### Query 1: Global COVID-19 Summary

```sql
SELECT 
    MAX(date) AS latest_date,
    SUM(daily_cases) AS total_cases,
    SUM(daily_deaths) AS total_deaths,
    ROUND(SUM(daily_deaths) * 100.0 / SUM(daily_cases), 2) AS fatality_rate
FROM covid_cases;
```

---

### Query 2: Top 10 Countries by Total Cases

```sql
SELECT 
    country,
    MAX(cumulative_cases) AS total_cases,
    MAX(cumulative_deaths) AS total_deaths,
    ROUND(MAX(cumulative_deaths) * 100.0 / MAX(cumulative_cases), 2) AS fatality_rate
FROM covid_cases
GROUP BY country
ORDER BY total_cases DESC
LIMIT 10;
```

---

### Query 3: India COVID-19 Trend (Last 30 Days)

```sql
SELECT 
    date,
    daily_cases,
    daily_deaths,
    active_cases,
    ROUND(daily_deaths * 100.0 / NULLIF(daily_cases, 0), 2) AS daily_fatality_rate
FROM covid_cases
WHERE country = 'India' 
  AND date >= DATE_SUB((SELECT MAX(date) FROM covid_cases), INTERVAL 30 DAY)
ORDER BY date DESC;
```

---

### Query 4: Hospital Capacity by State

```sql
SELECT 
    state,
    AVG(hospital_admissions) AS avg_admissions,
    AVG(available_beds) AS avg_available_beds,
    ROUND(AVG(hospital_admissions) * 100.0 / AVG(available_beds), 2) AS capacity_utilization
FROM hospital_data
WHERE country = 'India' 
  AND date >= '2024-01-01'
GROUP BY state
ORDER BY capacity_utilization DESC;
```

---

### Query 5: Vaccination Progress

```sql
SELECT 
    v.country,
    MAX(v.cumulative_dose1) AS first_doses,
    MAX(v.cumulative_dose2) AS fully_vaccinated,
    d.population,
    ROUND(MAX(v.cumulative_dose2) * 100.0 / d.population, 2) AS pct_fully_vaccinated
FROM vaccination_data v
JOIN country_demographics d ON v.country = d.country
GROUP BY v.country, d.population
ORDER BY pct_fully_vaccinated DESC
LIMIT 10;
```

---

## 📊 Sample Analysis Questions

Your dataset can answer these real-world questions:

1. **What were the trends of spread over every country?**
   - Use Query 2.2 (Monthly Case Trends) in sql-analysis-qs.md

2. **How many people were admitted to hospital in the last month?**
   - Use Query 6.1 (Hospital Capacity Analysis)

3. **What were the hotspots in 2024?**
   - Use Query 4.1 (Identify COVID-19 Hotspots)

4. **What are the infection and recovery rates?**
   - Use Query 5.1 (Infection Rate) and Query 5.2 (Recovery Rate)

All these queries are in the **sql-analysis-qs.md** file!

---

## 🔍 Advanced Features

### Create Views for Frequent Queries

```sql
-- Create a view for daily summary
CREATE VIEW daily_global_summary AS
SELECT 
    date,
    SUM(daily_cases) AS global_daily_cases,
    SUM(daily_deaths) AS global_daily_deaths,
    ROUND(SUM(daily_deaths) * 100.0 / NULLIF(SUM(daily_cases), 0), 2) AS daily_cfr
FROM covid_cases
GROUP BY date;

-- Use it
SELECT * FROM daily_global_summary 
WHERE date >= '2024-01-01' 
ORDER BY date DESC;
```

---

### Create Stored Procedures

```sql
-- Create procedure for country analysis
DELIMITER //
CREATE PROCEDURE analyze_country(IN country_name VARCHAR(100))
BEGIN
    SELECT 
        country,
        MAX(cumulative_cases) AS total_cases,
        MAX(cumulative_deaths) AS total_deaths,
        MAX(cumulative_recovered) AS total_recovered,
        MAX(active_cases) AS current_active
    FROM covid_cases
    WHERE country = country_name
    GROUP BY country;
END //
DELIMITER ;

-- Use it
CALL analyze_country('India');
```

---

## 📈 Visualization Ideas

Export your query results and create:

1. **Line Charts** - Case trends over time
2. **Bar Charts** - Country comparisons
3. **Heatmaps** - Geographical hotspots
4. **Pie Charts** - Case distribution
5. **Dashboards** - Combined metrics

**Tools:** Excel, Tableau, Power BI, Python (Matplotlib/Plotly), or R (ggplot2)

---

## 🛠️ Troubleshooting

### Error: "Loading local data is disabled"
**Solution:**
```sql
SET GLOBAL local_infile = 1;
```

### Error: "Access denied for LOAD DATA"
**Solution:**
```sql
GRANT FILE ON *.* TO 'your_user'@'localhost';
```

### Error: "Date format incorrect"
**Solution:** Ensure dates in CSV are in YYYY-MM-DD format

### Performance is slow
**Solution:** Make sure indexes were created:
```sql
SHOW INDEX FROM covid_cases;
```

---

## 📚 Learning Path

1. **Beginner:** Run queries 1.1 to 3.4 (Basic exploration and comparisons)
2. **Intermediate:** Run queries 4.1 to 6.4 (Trends and healthcare analysis)
3. **Advanced:** Run queries 7.1 to 8.5 (Vaccination and predictive analytics)

---

## 🎯 Project Deliverables

Your project should include:

1. ✅ **Database Schema** - All 5 tables properly created
2. ✅ **Imported Data** - All CSV files loaded successfully
3. ✅ **Query Results** - At least 10 analytical queries executed
4. ✅ **Documentation** - Query explanations and insights
5. ✅ **Visualizations** (Optional) - Charts from query results
6. ✅ **Report** (Optional) - Summary of key findings

---

## 💡 Extension Ideas

1. **Add More Countries:** Expand the dataset to include more nations
2. **Real-time Updates:** Automate daily data ingestion
3. **Machine Learning:** Build predictive models for case forecasting
4. **API Integration:** Connect to live COVID-19 APIs
5. **Web Dashboard:** Create interactive web-based visualization

---

## 📧 Support

If you encounter issues:

1. Check the **sql-schema-setup.md** for detailed setup instructions
2. Review the **sql-analysis-qs.md** for query examples
3. Verify your MySQL version: `SELECT VERSION();`
4. Check data integrity: `SELECT COUNT(*) FROM table_name;`

---

## 🎉 Congratulations!

You now have a fully functional COVID-19 health data analysis project. Start exploring the data, running queries, and discovering insights about the pandemic's global impact!

**Next Steps:**
1. ✅ Run basic exploration queries (1.1 - 1.3)
2. ✅ Analyze trends for your country of interest
3. ✅ Create visualizations from query results
4. ✅ Build a comprehensive report with your findings
5. ✅ Share insights with your portfolio or team!

---

## 📄 Quick Reference

## ♻️ Regenerate or Customize the CSVs

Want to change the time window, countries, or random seed? Run the generator:

```powershell
python generate_datasets.py --output-dir .
```

Available flags:

- `--start-date` / `--end-date` – change the time range (YYYY-MM-DD)
- `--seed` – control randomness for reproducible variations
- `--output-dir` – write CSVs somewhere else for experiments

Re-running with the defaults reproduces the exact datasets shipped in the repo.

## ✅ Recommended follow-up commands

- Inspect generator options: `python generate_datasets.py --help`
- After importing into MySQL, validate counts: `python validate_datasets.py --check-db`

**Database:** covid19_analysis  
**Tables:** 5 (covid_cases, hospital_data, vaccination_data, country_demographics, testing_data)  
**Records:** 116,860+  
**Time Period:** Jan 2020 - Nov 2024  
**Countries:** 20 major nations  
**Queries Available:** 30+  

**Key Metrics:**
- Cases, Deaths, Recoveries
- Hospital Admissions & Capacity
- Vaccination Progress
- Testing Statistics
- Infection & Recovery Rates
- Healthcare System Stress

**Ready to analyze? Start with the sql-analysis-qs.md file!**
