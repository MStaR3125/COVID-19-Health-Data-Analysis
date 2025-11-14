# 🏥 COVID-19 Health Data Analysis - Complete SQL Project

## Production-Ready SQL Project for Health Data Analysis

**A comprehensive, fully functional SQL project analyzing COVID-19 pandemic data from 2020-2024 across 20 countries with 116,860+ records.**

> ℹ️ **Synthetic but realistic data** – All CSVs are generated with the included `generate_datasets.py` script so you can reproduce the exact dataset (or customize it) at any time. The schema mirrors WHO/OWID structures while keeping the project self-contained.

[![SQL](https://img.shields.io/badge/SQL-MySQL-blue.svg)](https://www.mysql.com/)
[![Data](https://img.shields.io/badge/Records-116K+-green.svg)](/)
[![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)](/)

---

## 📊 Project Overview

This project provides a complete SQL-based analysis system for COVID-19 health data, including:

- **5 comprehensive database tables** with real-world schema
- **116,860+ records** spanning January 2020 to November 2024
- **20 countries** including India, USA, Brazil, UK, and major nations
- **30+ analytical queries** covering trends, hotspots, rates, and predictions
- **Advanced SQL techniques** including CTEs, window functions, and joins

---

## 🎯 Key Features

✅ **Real-World Data Structure** - Based on WHO/OWID COVID-19 data standards  
✅ **Comprehensive Coverage** - Cases, deaths, hospitalizations, vaccinations, testing  
✅ **Production Ready** - Properly indexed, optimized queries, follows best practices  
✅ **Educational** - Perfect for learning SQL data analysis  
✅ **Extensible** - Easy to add more data, countries, or metrics  
✅ **Well Documented** - Every query explained with business context  

---

## 📁 Project Structure

```
covid19-sql-project/
│
├── Data Files (CSV)
│   ├── covid_cases.csv              (35,560 records)
│   ├── hospital_data.csv            (17,780 records)
│   ├── vaccination_data.csv         (27,940 records)
│   ├── country_demographics.csv     (20 records)
│   └── testing_data.csv             (35,560 records)
│
├── Setup Files
│   ├── setup_database.sql           (Complete database setup)
│   ├── sql-schema-setup.md          (Detailed setup guide)
│   └── readme-quickstart.md         (Quick start instructions)
│
└── Analysis Files
    └── sql-analysis-qs.md           (30+ analytical queries)
```

---

## 🚀 Quick Start

### 0. Configure database credentials

Duplicate `.env.example` to `.env` (or set the `COVID_DB_*` environment variables) before running `import_data.py`. This keeps secrets out of source control while giving the importer everything it needs:

```
COVID_DB_HOST=localhost
COVID_DB_USER=root
COVID_DB_PASSWORD=your_password
COVID_DB_NAME=covid19_analysis
```

### Prerequisites
- MySQL 8.0+ or MariaDB 10.3+
- MySQL Workbench (recommended) or command-line access
- Basic SQL knowledge

### Setup in 3 Steps

**1. Create Database & Tables**
```bash
mysql -u root -p < setup_database.sql
```

**2. Import Data**

Using MySQL Workbench:
- Right-click each table → "Table Data Import Wizard"
- Select corresponding CSV file
- Click Next → Finish

**3. Verify Setup**
### 4. Explore and validate (recommended)

- Review generator options: `python generate_datasets.py --help`
- After importing to MySQL, double-check counts: `python validate_datasets.py --check-db`

```sql
USE covid19_analysis;

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
| table_name | records |
|------------|---------|
| covid_cases | 35,560 |
| hospital_data | 17,780 |
| vaccination_data | 27,940 |
| country_demographics | 20 |
| testing_data | 35,560 |

---

## 📊 Database Schema

### Table 1: covid_cases
Daily COVID-19 case, death, and recovery statistics by country

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

### Table 2: hospital_data
Hospital admission and capacity data for Indian states

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of record |
| state | VARCHAR(100) | State/region name |
| country | VARCHAR(100) | Country name (always `India` in v1) |
| hospital_admissions | INT | Daily hospital admissions |
| icu_admissions | INT | ICU admissions |
| ventilator_usage | INT | Ventilators in use |
| available_beds | INT | Available hospital beds |
| available_icu_beds | INT | ICU beds available |

### Table 3: vaccination_data
Daily vaccination statistics by country

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of record |
| country | VARCHAR(100) | Country name |
| daily_vaccinations_dose1 | INT | First dose administered |
| daily_vaccinations_dose2 | INT | Second dose administered |
| daily_vaccinations_booster | INT | Booster doses |
| cumulative_dose1 | BIGINT | Total first doses |
| cumulative_dose2 | BIGINT | Total second doses |
| cumulative_booster | BIGINT | Total booster doses |
| total_vaccinations | BIGINT | Aggregate of all doses |

### Table 4: country_demographics
Static demographic and health system data

| Column | Type | Description |
|--------|------|-------------|
| country | VARCHAR(100) | Country name |
| population | BIGINT | Total population |
| median_age | DECIMAL(4,1) | Median age |
| gdp_per_capita | INT | GDP per capita (USD) |
| hospital_beds_per_1000 | DECIMAL(4,1) | Hospital beds per 1,000 |

### Table 5: testing_data
COVID-19 testing statistics by country

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Date of record |
| country | VARCHAR(100) | Country name |
| daily_tests | INT | Tests conducted daily |
| cumulative_tests | BIGINT | Total tests conducted |

---

## 🔍 Sample Queries

### Global COVID-19 Summary
```sql
SELECT 
    MAX(date) AS latest_date,
    SUM(daily_cases) AS total_cases,
    SUM(daily_deaths) AS total_deaths,
    ROUND(SUM(daily_deaths) * 100.0 / SUM(daily_cases), 2) AS fatality_rate
FROM covid_cases;
```

### Top 10 Countries by Cases
```sql
SELECT 
    country,
    MAX(cumulative_cases) AS total_cases,
    MAX(cumulative_deaths) AS total_deaths
FROM covid_cases
GROUP BY country
ORDER BY total_cases DESC
LIMIT 10;
```

### Monthly Trend Analysis
```sql
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS month,
    SUM(daily_cases) AS monthly_cases,
    AVG(daily_cases) AS avg_daily_cases
FROM covid_cases
WHERE country = 'India'
GROUP BY DATE_FORMAT(date, '%Y-%m')
ORDER BY month DESC
LIMIT 12;
```

### Hospital Capacity Analysis
```sql
SELECT 
    state,
    AVG(hospital_admissions) AS avg_admissions,
    AVG(available_beds) AS avg_beds,
    ROUND(AVG(hospital_admissions) * 100.0 / AVG(available_beds), 2) AS utilization_pct
FROM hospital_data
WHERE country = 'India' AND date >= '2024-01-01'
GROUP BY state
ORDER BY utilization_pct DESC;
```

### Vaccination Progress
```sql
SELECT 
    v.country,
    MAX(v.cumulative_dose2) AS fully_vaccinated,
    d.population,
    ROUND(MAX(v.cumulative_dose2) * 100.0 / d.population, 2) AS pct_vaccinated
FROM vaccination_data v
JOIN country_demographics d ON v.country = d.country
GROUP BY v.country, d.population
ORDER BY pct_vaccinated DESC;
```

**More Queries:** See `sql-analysis-qs.md` for 30+ comprehensive analytical queries!

---

## 📈 Analysis Capabilities

This project enables analysis of:

### 1. **Trend Analysis**
- Daily, weekly, monthly case trends
- Year-over-year growth comparisons
- Peak infection period identification
- Moving averages for smoothing

### 2. **Geographic Analysis**
- Country-wise comparisons
- State-level hotspot identification (India)
- Per capita case rates
- Regional outbreak patterns

### 3. **Healthcare Analysis**
- Hospital capacity utilization
- ICU bed availability
- Ventilator demand forecasting
- Healthcare system stress assessment

### 4. **Epidemiological Metrics**
- Infection rates (positivity rates)
- Case fatality rates (CFR)
- Recovery rates
- Active case proportions
- R-effective approximations

### 5. **Vaccination Analysis**
- Vaccination coverage progress
- Dose distribution analysis
- Booster uptake rates
- Vaccination impact on case reduction

### 6. **Testing Analysis**
- Testing capacity trends
- Tests per case ratios
- Test positivity rates
- Testing strategy effectiveness

---

## 💡 Use Cases

### For Students
- Learn SQL through real-world data
- Build data analysis portfolio
- Practice advanced SQL techniques
- Understand pandemic data structures

### For Data Analysts
- Demonstrate analytical skills
- Create visualizations and dashboards
- Practice epidemiological analysis
- Showcase technical expertise

### For Researchers
- Study pandemic patterns
- Analyze intervention effectiveness
- Compare country-level responses
- Generate research insights

### For Educators
- Teaching SQL and data analysis
- Demonstrating public health informatics
- Case studies for epidemiology
- Real-world data science examples

---

## 🎓 Learning Objectives

After completing this project, you will:

✅ Understand complex database schema design  
✅ Master JOIN operations across multiple tables  
✅ Use window functions for trend analysis  
✅ Write CTEs for complex queries  
✅ Calculate rates and percentages correctly  
✅ Handle time-series data in SQL  
✅ Create meaningful aggregations  
✅ Optimize queries with proper indexing  

---

## 🔧 Advanced Features

### Create Analytical Views
```sql
-- Create a view for quick country summaries
CREATE VIEW country_summary AS
SELECT 
    c.country,
    MAX(c.cumulative_cases) AS total_cases,
    MAX(c.cumulative_deaths) AS total_deaths,
    ROUND(MAX(c.cumulative_deaths) * 100.0 / MAX(c.cumulative_cases), 2) AS cfr,
    d.population,
    ROUND(MAX(c.cumulative_cases) * 100000.0 / d.population, 2) AS cases_per_100k
FROM covid_cases c
JOIN country_demographics d ON c.country = d.country
GROUP BY c.country, d.population;

-- Use the view
SELECT * FROM country_summary ORDER BY total_cases DESC;
```

### Create Stored Procedures
```sql
-- Create procedure for date range analysis
DELIMITER //
CREATE PROCEDURE analyze_date_range(
    IN start_date DATE,
    IN end_date DATE,
    IN country_name VARCHAR(100)
)
BEGIN
    SELECT 
        date,
        daily_cases,
        daily_deaths,
        AVG(daily_cases) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7day
    FROM covid_cases
    WHERE country = country_name 
      AND date BETWEEN start_date AND end_date
    ORDER BY date;
END //
DELIMITER ;

-- Use it
CALL analyze_date_range('2024-01-01', '2024-06-30', 'India');
```

---

## 📊 Visualization Integration

Export query results to create dashboards in:

- **Tableau** - Interactive dashboards
- **Power BI** - Business intelligence reports
- **Excel** - Pivot tables and charts
- **Python** - Matplotlib, Seaborn, Plotly
- **R** - ggplot2 visualizations
- **Google Data Studio** - Web-based dashboards

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

**Issue:** "File not found" during data import  
**Solution:** Use full absolute path or place CSV files in MySQL secure directory

**Issue:** "Access denied for LOAD DATA"  
**Solution:** Grant file privileges:
```sql
GRANT FILE ON *.* TO 'your_user'@'localhost';
```

**Issue:** Date format errors  
**Solution:** Ensure dates in CSV are YYYY-MM-DD format

**Issue:** Slow query performance  
**Solution:** Verify indexes exist:
```sql
SHOW INDEX FROM covid_cases;
```

---

## 📚 Documentation

- **setup_database.sql** - Complete database setup script
- **sql-schema-setup.md** - Detailed setup instructions and data import guide
- **sql-analysis-qs.md** - 30+ analytical queries with explanations
- **readme-quickstart.md** - Quick start guide for beginners

---

## 🎯 Project Deliverables Checklist

- [ ] Database created with all 5 tables
- [ ] All CSV files imported successfully
- [ ] Run at least 10 analytical queries
- [ ] Document key findings
- [ ] Create 3-5 visualizations
- [ ] Write a summary report (optional)
- [ ] Share insights or publish to portfolio

---

## 🚀 Next Steps & Extensions

1. **Add More Data**
   - Include more countries
   - Add historical pre-2020 baseline data
   - Include climate/weather data

2. **Advanced Analysis**
   - Build predictive models
   - Perform statistical testing
   - Create machine learning pipelines

3. **Automation**
   - Schedule daily data updates
   - Automate report generation
   - Set up data quality checks

4. **Integration**
   - Connect to live COVID-19 APIs
   - Build REST API for data access
   - Create web-based dashboard

5. **Collaboration**
   - Share with research community
   - Contribute to open data projects
   - Publish findings

---

## 📖 Learning Resources

### SQL Learning
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQL Tutorial by W3Schools](https://www.w3schools.com/sql/)
- [Mode SQL Tutorial](https://mode.com/sql-tutorial/)

### COVID-19 Data Sources
- [Our World in Data](https://ourworldindata.org/coronavirus)
- [WHO COVID-19 Dashboard](https://covid19.who.int/)
- [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)

### Data Visualization
- [Tableau Public](https://public.tableau.com/)
- [Power BI Desktop](https://powerbi.microsoft.com/)
- [Python Plotly](https://plotly.com/python/)

---

## 🤝 Contributing

Contributions are welcome! You can:
- Add more analytical queries
- Improve documentation
- Fix bugs or issues
- Add new features
- Share your analyses

---

## 📝 License

This project is for educational purposes. The COVID-19 data structure is inspired by publicly available datasets from WHO, OWID, and other authoritative sources.

---

## ⭐ Acknowledgments

- Data structure inspired by Our World in Data COVID-19 dataset
- WHO for global COVID-19 data standards
- Johns Hopkins CSSE for pandemic tracking methodology
- Ministry of Health, Government of India for regional data formats

---

## 📧 Support & Feedback

If you find this project helpful:
- ⭐ Star the repository
- 🐛 Report issues
- 💡 Suggest improvements
- 📢 Share with others

---

## 🎉 Success Metrics

After completing this project, you should be able to:
- ✅ Design and implement complex database schemas
- ✅ Write advanced SQL queries with confidence
- ✅ Analyze time-series health data
- ✅ Create meaningful epidemiological metrics
- ✅ Build data-driven reports and dashboards
- ✅ Showcase professional data analysis skills

---

**Ready to start? Follow the quick start guide in `readme-quickstart.md`!**

**Questions about queries? Check out `sql-analysis-qs.md` for 30+ examples!**

**Need setup help? See `sql-schema-setup.md` for detailed instructions!**

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Records | 116,860+ |
| Tables | 5 |
| Countries | 20 |
| Time Span | Jan 2020 - Nov 2024 |
| Analytical Queries | 30+ |
| Data Points | 1,000,000+ |
| Documentation Pages | 4 |

---

## ♻️ Regenerating or Customizing the Dataset

Need fresh data or different parameters? Use the new unified generator:

1. Install dependencies once:
    ```powershell
    pip install -r requirements.txt
    ```
2. Run the generator (defaults match the bundled CSVs):
    ```powershell
    python generate_datasets.py --output-dir .
    ```
3. Tweak `--start-date`, `--end-date`, `--seed`, or `--output-dir` to explore new scenarios.

Tip: run `python generate_datasets.py --help` to view all options at any time.

Because the data is deterministic per seed, re-running with the default seed (42) recreates the published 116,860+ records exactly.

**Built with ❤️ for the data analysis community**

**Happy Analyzing! 🚀📊**
