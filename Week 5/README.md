# HealthConnect Clinic Experience Lab
### AnalystLab Africa — Experience Lab Internship Programme
**Track:** Data Analytics | **Tools:** Python · SQL · Power BI

---

## Project Overview

HealthConnect Clinic is a fictional healthcare provider that manages appointment-based services. The clinic is experiencing a critically high appointment no-show rate and needs data-driven insights to understand and reduce missed appointments.

This repository contains all Data Analytics track deliverables produced during the AnalystLab Africa Experience Lab Internship Programme.

**Central Project Question:**
> How can HealthConnect Clinic use data to reduce missed appointments and improve the patient support experience?

---

## The Problem

| Metric | Value |
|--------|-------|
| Total appointment records | 5,000 |
| Overall no-show rate | **48.46%** |
| Attended rate | 46.28% |
| Cancellation rate | 5.26% |

Nearly 1 in every 2 scheduled appointments is missed — causing wasted slots, reduced efficiency, and lower quality of patient care.

---

## Repository Structure

```
healthconnect-experience-lab/
│
├── data/
│   └── HealthConnect_Appointment_Data.csv        # Original dataset (do not modify)
│
├── notebooks/
│   ├── Week4_HealthConnect_DataAnalytics.ipynb   # Week 4 — Initial analysis document
│   └── Week5_HealthConnect_DataAnalytics.ipynb   # Week 5 — EDA, KPIs, insights
│
├── sql/
│   └── Week4_HealthConnect_SQL_Queries.sql       # SQL queries for KPI calculations
│
├── reports/
│   ├── Week4_ProjectSummaryReport_HealthConnect.docx  # Week 4 project summary report
│   └── Week5_ProjectSummaryReport_HealthConnect.docx  # Week 5 project summary report
│
└── README.md
```

---

## Weekly Progress

### ✅ Week 4 — Project Kickoff and Problem Understanding

**Objective:** Establish a clear understanding of the HealthConnect business problem and define how the Data Analytics track will contribute.

**Completed:**
- Reviewed the dataset structure (5,000 records, 18 columns)
- Conducted initial data quality assessment
- Identified important variables relevant to no-show behaviour
- Defined 5 business questions
- Proposed and justified 5 KPIs
- Developed an initial analysis approach
- Documented assumptions, limitations, risks and dependencies

**Key observation from Week 4:**
The dataset is of good quality. The no-show rate of 48.46% confirms the problem is significant and worth investigating further.

**Deliverables:**
- `Week4_HealthConnect_DataAnalytics.ipynb`
- `Week4_HealthConnect_SQL_Queries.sql`
- `Week4_ProjectSummaryReport_HealthConnect.docx`

---

### ✅ Week 5 — Exploratory Analysis, KPI Development and Business Insights

**Objective:** Move from planning into practical implementation — clean the data, run full EDA, calculate KPIs, and produce business insights.

**Completed:**
- Data preparation — converted date columns, handled missing values, created derived columns
- Exploratory data analysis across 12 dimensions
- Calculated all 5 KPIs with full interpretation
- Produced 8 charts
- Documented 5 business insights and recommendations
- Completed cross-track collaboration with the Data Science track

**Key findings from Week 5:**

| Finding | Detail |
|---------|--------|
| Booking lead time | No-show rate doubles from 27.81% (0–7 days) to 60.49% (31–60 days) |
| Prior no-show history | Patients with 2+ prior no-shows have a ~63% no-show rate |
| SMS reminders | Most effective channel at 45.75% no-show rate |
| Follow-up appointments | Highest no-show rate at 51.23% |
| WhatsApp reminders | Barely more effective than no reminder (49.77% vs 51.39%) |

**Deliverables:**
- `Week5_HealthConnect_DataAnalytics.ipynb`
- `Week5_ProjectSummaryReport_HealthConnect.docx`

---

## KPI Summary

| KPI | Name | Result | Business Question |
|-----|------|--------|-------------------|
| KPI 1 | Overall No-Show Rate | 48.46% | BQ1 |
| KPI 2 | Reminder Effectiveness Rate | SMS: 45.75% \| WhatsApp: 49.77% \| Email: 48.41% | BQ2 |
| KPI 3 | No-Show Rate by Booking Lead Time | 27.81% (0–7 days) → 60.49% (31–60 days) | BQ3 |
| KPI 4 | No-Show Rate by Prior History | Low: 43.51% \| Medium: 53.49% \| High: ~63% | BQ4 |
| KPI 5 | No-Show Rate by Appointment Type | Follow-up: 51.23% \| General: 46.64% | BQ1 |

---

## Business Questions

| ID | Question |
|----|----------|
| BQ1 | What is the overall no-show rate and how does it vary by appointment type, day, and time slot? |
| BQ2 | Do reminders reduce no-show rates? Does the channel (SMS, WhatsApp, Email) make a difference? |
| BQ3 | Is there a relationship between booking lead time and the likelihood of a no-show? |
| BQ4 | Do patients with a history of previous no-shows have higher future no-show rates? |
| BQ5 | Does patient distance from the clinic affect appointment attendance? |

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Python (Pandas, Matplotlib) | Data loading, preparation, EDA, KPI calculations, visualisations |
| SQL | KPI queries and data quality checks |
| Power BI | Dashboard development (planned — Week 7) |
| Jupyter Notebook | Analysis documentation |

---

## How to Run the Notebooks

1. Clone or download this repository
2. Place `HealthConnect_Appointment_Data.csv` in the same folder as the notebook you want to run
3. Open the notebook in [Google Colab](https://colab.research.google.com) or Jupyter Notebook
4. Run each cell from top to bottom using **Shift + Enter**

**Required Python libraries:**
```python
import pandas as pd
import matplotlib.pyplot as plt
```
Both are pre-installed in Google Colab. No additional installation needed.

---

## Dataset

| Property | Detail |
|----------|--------|
| File | HealthConnect_Appointment_Data.csv |
| Records | 5,000 appointment records |
| Columns | 18 variables |
| Unique patients | 1,696 |
| Source | Fictional and anonymised — provided by AnalystLab Africa |

> **Important:** The original dataset must not be overwritten. All cleaning and transformations are applied to a working copy inside the notebooks.

---

## Upcoming Work

- [ ] Week 6 — Time-based trend analysis and deeper reminder channel investigation
- [ ] Week 7 — Power BI dashboard development
- [ ] Week 8 — Final report and presentation

---

## Author

**Data Analytics Track Intern**  
AnalystLab Africa Experience Lab Internship Programme  
Project: HealthConnect Clinic Experience Lab

---

*This project is based on a fictional dataset provided by AnalystLab Africa for educational purposes. All findings are illustrative and do not represent real clinic data.*
