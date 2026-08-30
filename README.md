# HealthConnect Clinic Appointment No-Show Analysis

## 📌 Project Overview
HealthConnect Clinic is an appointment-based healthcare provider experiencing operational and patient support challenges. This project focuses on analyzing historical appointment data to understand the underlying behavioral, situational, and logistical factors associated with patient no-shows. 

By analyzing these patterns, this project aims to support clinical decision-making, optimize resource utilization, and guide the design of targeted patient engagement and support interventions.

### 🔍 Central Project Question
> **How can HealthConnect Clinic use data and AI to reduce missed appointments and improve the patient support experience?**

---

## 👩‍💻 Intern & Track Metadata
* **Intern Name:** Belinda Thando Mhlanga
* **Role:** Data Analyst Intern
* **Programme:** AnalystLab Africa Experience Lab
* **Project Phase:** Week 4 — Problem Understanding & Solution Design
* **Submission Date:** 30 August 2026

---

## 📂 Repository Structure
```directory/
├── data/
│   ├── raw/                  # Original, unaltered project datasets
│   └── processed/            # Cleaned and engineered data (generated in Week 5)
├── notebooks/                # Jupyter Notebooks for exploratory data analysis (EDA)
├── scripts/                  # Python & SQL scripts for data quality and loading
│   ├── data_quality_assessment.py
│   └── data_quality_assessment.sql
├── reports/                  # Formatted documentation and PDF summaries
└── README.md                 # Project landing page and weekly progress log

Note: In accordance with data governance best practices, all raw datasets are kept read-only and are never directly modified or overwritten.
📈 Baseline Clinical Metrics
An initial analysis of the 5,000 scheduled appointments in the dataset reveals a highly critical operational bottleneck: nearly half of all booked consultations result in a missed visit.
Appointment Outcome
Total Count
Percentage (%)
Operational Impact
No-Show (Missed)
2,423
48.5%
Empty consulting rooms; wasted clinical resources
Attended
2,314
46.3%
Completed consultations and patient care
Cancelled
263
5.3%
Slot cancelled in advance; potential for rescheduling
Total Bookings
5,000
100.0%
Baseline clinical capacity
🕵️‍♂️ Key Discoveries & Behavioral Drivers
Early exploratory profiling has revealed distinct differences in patient behaviors and logistics between the attendance and default cohorts:
🟡 Gold Clues (High Predictive Importance)
Booking Lead Time: Patients who missed appointments booked their visits an average of 34.5 days in advance, compared to only 24.5 days for those who attended (a massive 10-day difference).
Behavioral Defaults: Attendance history is a powerful indicator. Patients who defaulted averaged 0.64 previous no-shows, whereas those who showed up averaged only 0.46.
Travel Distance: Distance serves as a tangible physical barrier. No-show patients live further away from the clinic on average (10.5 km vs. 9.7 km for attendees).
Reminder Impact: Sending a reminder resulted in a modest 4.0% reduction in no-shows (47.4% no-show rate for reminded patients vs. 51.4% for non-reminded patients), indicating significant room for reminder system optimization.
⚪ Silver Clues (Medium Predictive Importance)
Appointment Urgency: Follow-up consultations have the highest default rate at 51.2%, whereas General Consultations see a lower default rate of 46.6%.
Temporal Patterns: Sunday and Monday bookings see the highest default rates (approximately 50.0%), while Friday has the lowest (approximately 47.0%).
Age Demographics: Older patients (aged 65+) show the highest reliability with the lowest default rate (45.1%), while young adults default slightly more often.
🛠 Data Quality Audit & Preparation Strategy
Before executing calculations or building dashboards, a strict data quality audit was conducted to preserve dataset integrity:
Record Uniqueness: Checked all 5,000 records; 0 duplicates found (every appointment ID is unique and valid).
Missing Value Profiling:
reminder_channel (1,366 blank rows / 27.3% missing): Confirmed as logically valid nulls, matching records where reminder_sent was marked 'No'
.
distance_to_clinic_km (90 rows / 1.8% missing): Low risk; to be handled in Week 5 using median imputation.
waiting_time_minutes (60 rows / 1.2% missing): Expected missingness, as no-show patients never checked in at the front desk.
Date-Math Preparation: Dates are currently stored as plain text strings. Converting these into proper ISO standard datetime formats is prioritized for Week 5.
🎯 Proposed Key Performance Indicators (KPIs)
These 5 core metrics have been designed to measure operational efficiency and evaluate future interventions:
Overall Appointment No-Show Rate (%)
Formula: (Total No-Shows ÷ Total Booked Appointments) * 100
Baseline: 48.5%
Reminder Effectiveness Rate (% Variance)
Formula: No-Show Rate (No Reminder) - No-Show Rate (Reminder Sent)
Baseline: 4.0%
No-Show Rate by Booking Lead Time Band
Formula: Segments overall no-show rates into booking bands (e.g., 0-7 days, 8-14 days, 15-30 days, 31-60 days).
High-Risk Patient Re-Attendance Rate (%)
Formula: No-show rates segmented by historical default count (0, 1, 2, or 3+ past defaults).
No-Show Rate by Appointment Type (%)
Formula: Miss rates broken down by clinical department (e.g., General, Follow-up, Specialist, Diagnostics).
🛣 Experience Lab Roadmap
Phase 1: Ingestion & Data Preparation (Week 5)
[ ] Convert text date fields into standard computer-friendly datetime formats.
[ ] Impute missing physical distances and waiting times using median values.
[ ] Segment continuous lead days into distinct categorical booking bands.
[ ] Standardize categorical string entries (whitespace and casing).
Phase 2: Exploratory Data Analysis (Weeks 5–6)
[ ] Calculate final validated attendance, no-show, and cancellation rates.
[ ] Perform bivariate analyses comparing outcomes against demographics and travel metrics.
[ ] Generate early visual distributions of patient default behaviors.
Phase 3: KPI Implementation & Chart Generation (Weeks 6–7)
[ ] Write robust Python math scripts to output the 5 defined KPIs.
[ ] Produce polished, publication-quality visualizations using Matplotlib and Seaborn.
[ ] Draft data-backed recommendations for clinical operational changes.
Phase 4: Interactive Dashboard Deployment (Weeks 7–8)
[ ] Construct a clean, unified schema.
[ ] Design and deploy an interactive dashboard (Power BI or Tableau) for clinic stakeholders.
[ ] Deliver final portfolio presentation and briefing.
⚠️ Assumptions, Gaps, and Risks
Data Limitations: The dataset lacks qualitative variables explaining the exact physical reasons behind missed appointments (e.g., financial constraints, transport access, or sudden family emergencies).
Key Analytical Assumption: Historical patient records represent future clinic booking behaviors accurately.
Logistical Dependency: Waiting times are only recorded for patients who attended; this variable cannot be used to predict future no-shows but can be used to gauge historical operational delays.

***

This README structure gives your GitHub repository an incredibly clean, professional appearance that immediately shows your program mentors and future employers that you have an organized, systematic approach to data analytics.

🚀 **Would you like me to help you draft your LinkedIn post next, or are you all set for your Week 4 submission?**
