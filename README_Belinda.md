# HealthConnect Clinic Appointment No-Show Analysis

## 📌 Project Overview

HealthConnect Clinic is an appointment-based healthcare provider experiencing operational and patient support challenges. This project focuses on analysing historical appointment data to understand the underlying behavioural, situational, and logistical factors associated with patient no-shows.

By analysing these patterns, this project aims to support clinical decision-making, optimise resource utilisation, and guide the design of targeted patient engagement and support interventions.

---

## 🔍 Central Project Question

> How can HealthConnect Clinic use data and AI to reduce missed appointments and improve the patient support experience?

---

## 👩‍💻 Intern and Track Metadata

| Field | Detail |
|-------|--------|
| Intern Name | Belinda Thando Mhlanga |
| Role | Data Analyst Intern |
| Programme | AnalystLab Africa Experience Lab |
| Project Phase | Week 4 — Problem Understanding and Solution Design |
| Submission Date | 30 August 2026 |

---

## 📂 Repository Structure

```
healthconnect-no-show-analysis/
│
├── data/
│   ├── raw/                             # Original, unaltered project datasets
│   └── processed/                       # Cleaned and engineered data (generated in Week 5)
│
├── notebooks/                           # Jupyter Notebooks for exploratory data analysis
│
├── scripts/                             # Python and SQL scripts
│   ├── data_quality_assessment.py
│   └── data_quality_assessment.sql
│
├── reports/                             # Formatted documentation and PDF summaries
│
└── README.md                            # Project landing page and weekly progress log
```

> **Note:** In accordance with data governance best practices, all raw datasets are kept read-only and are never directly modified or overwritten.

---

## 📈 Baseline Clinical Metrics

An initial analysis of the 5,000 scheduled appointments in the dataset reveals a critically high operational bottleneck — nearly half of all booked consultations result in a missed visit.

| Appointment Outcome | Total Count | Percentage (%) | Operational Impact |
|---------------------|-------------|----------------|--------------------|
| No-Show (Missed) | 2,423 | 48.5% | Empty consulting rooms; wasted clinical resources |
| Attended | 2,314 | 46.3% | Completed consultations and patient care |
| Cancelled | 263 | 5.3% | Slot cancelled in advance; potential for rescheduling |
| **Total Bookings** | **5,000** | **100%** | Baseline clinical capacity |

---

## 🕵️ Key Discoveries and Behavioural Drivers

Early exploratory profiling revealed distinct differences in patient behaviour and logistics between the attendance and no-show cohorts.

### 🟡 Gold Clues — High Predictive Importance

- **Booking Lead Time:** Patients who missed appointments booked their visits an average of 34.5 days in advance, compared to only 24.5 days for those who attended — a 10-day difference.
- **Behavioural History:** Attendance history is a powerful indicator. Patients who did not show up averaged 0.64 previous no-shows, whereas those who attended averaged only 0.46.
- **Travel Distance:** Distance serves as a tangible physical barrier. No-show patients live further from the clinic on average (10.5 km vs 9.7 km for attendees).
- **Reminder Impact:** Sending a reminder resulted in a 4.0 percentage point reduction in no-shows (47.4% with reminder vs 51.4% without), indicating significant room for reminder system optimisation.

### ⚪ Silver Clues — Medium Predictive Importance

- **Appointment Urgency:** Follow-up consultations have the highest no-show rate at 51.2%, while General Consultations are lower at 46.6%.
- **Temporal Patterns:** Sunday and Monday bookings have the highest no-show rates (approximately 50%), while Friday is the lowest (approximately 47%).
- **Age Demographics:** Older patients (65+) show the highest reliability with the lowest no-show rate (45.1%), while younger adults default slightly more often.

---

## 🛠️ Data Quality Audit and Preparation Strategy

Before executing calculations or building dashboards, a strict data quality audit was conducted to preserve dataset integrity.

| Check | Finding |
|-------|---------|
| Record uniqueness | 0 duplicates found — every appointment ID is unique and valid |
| reminder_channel missing | 1,366 rows (27.3%) — confirmed as logically valid nulls matching records where reminder_sent = No |
| distance_to_clinic_km missing | 90 rows (1.8%) — low risk; to be handled in Week 5 using median imputation |
| waiting_time_minutes missing | 60 rows (1.2%) — expected missingness; no-show patients never checked in |
| Date format issue | Both date columns stored as text strings — conversion to datetime format prioritised for Week 5 |

---

## 🎯 Proposed Key Performance Indicators (KPIs)

Five core metrics have been designed to measure operational efficiency and evaluate future interventions.

| KPI | Formula | Baseline |
|-----|---------|----------|
| **KPI 1** — Overall No-Show Rate | (Total No-Shows ÷ Total Booked Appointments) × 100 | 48.5% |
| **KPI 2** — Reminder Effectiveness Rate | No-Show Rate (No Reminder) − No-Show Rate (Reminder Sent) | 4.0 pp |
| **KPI 3** — No-Show Rate by Booking Lead Time Band | No-show rate segmented into bands: 0–7, 8–14, 15–30, 31–60 days | To be calculated in Week 5 |
| **KPI 4** — High-Risk Patient Re-Attendance Rate | No-show rates segmented by prior no-show count (0, 1, 2, 3+) | To be calculated in Week 5 |
| **KPI 5** — No-Show Rate by Appointment Type | Miss rates by appointment category (General, Follow-up, Specialist, Diagnostic) | To be calculated in Week 5 |

---

## 🛣️ Experience Lab Roadmap

### Phase 1 — Data Preparation (Week 5)
- [ ] Convert text date fields into standard datetime format
- [ ] Impute missing distance and waiting time values using median values
- [ ] Segment booking lead days into categorical bands
- [ ] Standardise categorical string entries (whitespace and casing)

### Phase 2 — Exploratory Data Analysis (Week 5–6)
- [ ] Calculate final validated attendance, no-show, and cancellation rates
- [ ] Perform bivariate analyses comparing outcomes against demographics and logistics
- [ ] Generate visual distributions of patient no-show behaviour

### Phase 3 — KPI Implementation and Visualisation (Week 6–7)
- [ ] Calculate all 5 KPIs using Python
- [ ] Produce publication-quality visualisations using Matplotlib and Seaborn
- [ ] Draft data-backed recommendations for clinical operational improvements

### Phase 4 — Interactive Dashboard Deployment (Week 7–8)
- [ ] Construct a clean, unified data schema
- [ ] Design and deploy an interactive dashboard in Power BI
- [ ] Deliver final portfolio presentation and project briefing

---

## ⚠️ Assumptions, Gaps, and Risks

| Item | Detail |
|------|--------|
| Data limitation | The dataset lacks qualitative variables explaining the exact reasons behind missed appointments (e.g. financial constraints, transport access, family emergencies) |
| Key assumption | Historical patient records accurately represent future clinic booking behaviours |
| Logistical dependency | Waiting times are only recorded for attended appointments — this variable cannot be used to predict future no-shows but can measure historical operational delays |

---

## 🚀 Upcoming Work

- [ ] Week 5 — Full data preparation, EDA, and KPI calculations
- [ ] Week 6 — Deepened analysis and visualisations
- [ ] Week 7 — Power BI dashboard development
- [ ] Week 8 — Final report and portfolio presentation

---

*This project is based on a fictional dataset provided by AnalystLab Africa for educational purposes. All findings are illustrative and do not represent real clinic data.*
