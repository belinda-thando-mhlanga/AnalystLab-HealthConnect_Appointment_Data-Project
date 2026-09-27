# HealthConnect Clinic — No-Show Analysis
### AnalystLab Africa | Experience Lab | Data Analytics Track | Odendaal

---

## Project Overview

HealthConnect Clinic is an appointment-based fictional healthcare provider experiencing a critical operational challenge: **48.46% of all scheduled appointments result in a missed visit** — nearly one in two.

This project analyses 5,000 appointment records spanning January 2025 to June 2026, using Python, SQL, and an interactive dashboard to identify the behavioural, logistical, and temporal factors driving no-shows and to provide evidence-based recommendations for reducing them.

**Central Project Question:**
> *How can HealthConnect Clinic use data and AI to reduce missed appointments and improve the patient support experience?*

---

## Final Results at a Glance

| Metric | Value |
|--------|-------|
| Overall No-Show Rate | **48.46%** (2,423 of 5,000) |
| Best Segment (Low Risk + 0–7 days + SMS) | **23.18%** (n=151) |
| Worst Segment (High Risk + 31–60 days + No Reminder) | **72.31%** (n=65) |
| Segment Gap | **49.13 percentage points** |
| High Risk Best Case (High Risk + 0–7 days + SMS) | **37.93%** (n=29) |
| SMS vs. No Reminder Improvement | **5.64 pp** |
| Worst Month | December 2025: **53.85%** |
| Best Month | November 2025: **42.17%** |

---

## Five Validated KPIs

### KPI 1 — Overall No-Show Rate
`48.46%` — Attended 46.28% | Cancelled 5.26%

### KPI 2 — Reminder Effectiveness

| Channel | No-Show Rate | vs. No Reminder |
|---------|-------------|-----------------|
| SMS | 45.75% | −5.64 pp |
| Email | 48.41% | −2.98 pp |
| WhatsApp | 49.77% | −1.62 pp |
| No Reminder | 51.39% | Baseline |

### KPI 3 — No-Show Rate by Booking Lead Time

| Lead Time Band | No-Show Rate | n |
|----------------|-------------|---|
| 0–7 days | **27.81%** | 640 |
| 8–14 days | 33.55% | 602 |
| 15–30 days | 43.21% | 1,333 |
| 31–60 days | **60.49%** | 2,425 |

### KPI 4 — No-Show Rate by Patient Risk Tier

| Risk Tier | No-Show Rate | n |
|-----------|-------------|---|
| Low Risk (0 prior no-shows) | 43.51% | 2,921 |
| Medium Risk (1 prior no-show) | 53.49% | 1,548 |
| High Risk (2+ prior no-shows) | **61.02%** | 531 |

### KPI 5 — No-Show Rate by Appointment Type

| Type | No-Show Rate | n |
|------|-------------|---|
| Follow-up | **51.23%** | 1,421 |
| Diagnostic Test | 49.75% | 593 |
| Specialist Consultation | 47.44% | 900 |
| General Consultation | 46.64% | 2,086 |

---

## Key Findings

1. **Lead time is the dominant predictor** — patients booking 31–60 days ahead miss 60.49% of appointments vs. 27.81% for same-week bookings (32.68 pp difference)
2. **High Risk patients need two-step intervention** — 61.02% overall, but 37.93% under SMS + same-week booking conditions (30+ pp reduction)
3. **SMS is the optimal reminder channel** — outperforms WhatsApp by ~4 pp and no reminder by 5.64 pp across all risk tiers
4. **December seasonal spike** — 53.85% driven by Follow-up (56.63%) and Specialist Consultation (55.10%), not Diagnostic Tests (44.00%)
5. **Distance is a logistical barrier** — patients over 20 km from the clinic miss 57.76% of appointments (9.30 pp above average)

---

## Five Business Recommendations

| # | Recommendation | Target | Expected Impact |
|---|----------------|--------|----------------|
| R1 | Cap Follow-up and General booking windows at 14 days | Follow-up + General | ~15 pp reduction |
| R2 | Two-step engagement: SMS 3 days before + phone call 24 hours before | High Risk patients | Up to 30 pp improvement |
| R3 | Set SMS as default reminder channel | All patients | 4–10 pp improvement |
| R4 | Flag patients >20 km for telehealth or transport options | Distance > 20 km | Reduces 9.30 pp gap |
| R5 | Increase reminder intensity Nov–Jan | Seasonal peak period | Addresses Dec 53.85% / Jan 52.96% |

---

## Cross-Track Integration — Data Science

| Item | Detail |
|------|--------|
| **Provided to Data Science** | Feature importance table (7 variables), cross-variable charts, worst/best segment definitions (72.31% / 23.18%), December breakdown, High Risk benchmark (37.93%) |
| **Received from Data Science** | Feature importance confirmation: booking_lead_days #1, previous_no_shows #2, reminder_sent #3. Categorical bands (lead_time_band, patient_risk_tier) improved model precision and recall |
| **What changed** | 37.93% adopted as model evaluation benchmark. Data Science model uses engineered categorical features from Data Analytics |

---

## Testing & Validation (Week 7)

All 8 formal tests passed:

| Test | What Was Verified | Result |
|------|-------------------|--------|
| T1 | KPI 1 = 2,423 ÷ 5,000 × 100 = 48.46% | ✅ PASS |
| T2 | KPI 2 = 51.39% − 47.36% = 4.03 pp | ✅ PASS |
| T3 | Lead time bands: 27.81% / 33.55% / 43.21% / 60.49% | ✅ PASS |
| T4 | Low Risk < Medium Risk < High Risk (monotonic) | ✅ PASS |
| T5 | KPI 5 weighted avg = 48.46% | ✅ PASS |
| T6 | Age group rates identical across two independent methods | ✅ PASS |
| T7 | 0 reminder channel values where reminder_sent = No | ✅ PASS |
| T8 | 640 + 602 + 1,333 + 2,425 = 5,000 (no unassigned records) | ✅ PASS |

---

## Repository Structure

```
├── data/
│   ├── raw/                          # Original, unaltered dataset (read-only)
│   └── processed/                    # Cleaned and feature-engineered data
├── notebooks/
│   ├── Week4_HealthConnect_DataAnalytics.ipynb
│   ├── Week5_HealthConnect_DataAnalytics.ipynb
│   ├── Week6_HealthConnect_DataAnalytics.ipynb
│   └── Week7_HealthConnect_DataAnalytics.ipynb
├── scripts/
│   └── Week4_HealthConnect_SQL_Queries.sql
├── reports/
│   ├── Week4_DataAnalytics_HealthConnect.docx
│   ├── Week5_ProjectSummaryReport_HealthConnect.docx
│   ├── Week6_ProjectReport_HealthConnect.docx
│   ├── Week7_ProjectReport_HealthConnect.docx
│   └── Week8_HealthConnect_FinalReport.docx
├── dashboard/
│   └── HealthConnect_Dashboard.html  # Interactive 5-page dashboard
└── README.md
```

---

## How to Run the Notebooks

1. Download any `.ipynb` file from the `notebooks/` folder
2. Place `HealthConnect_Appointment_Data.csv` in the same folder
3. Open in [Google Colab](https://colab.research.google.com)
4. Run cells top to bottom using **Shift + Enter**

```python
# Required libraries — both pre-installed in Google Colab
import pandas as pd
import matplotlib.pyplot as plt
```

Each notebook's setup cell re-applies all prior cleaning steps automatically.

---

## Interactive Dashboard

`HealthConnect_Dashboard.html` — open in any modern browser. No installation required.

| Page | Content |
|------|---------|
| 1 — Executive Overview | KPI 1, outcome summary, extreme segment cards |
| 2 — No-Show Patterns | KPI 5 by appointment type, day, time, age group |
| 3 — Reminders Analysis | KPI 2 channel comparison, benefit by type |
| 4 — Booking Lead Time | KPI 3 band bars, 18-month trend line |
| 5 — Patient Risk | KPI 4 risk tier bars, risk × channel table |

---

## Project Timeline

| Week | Focus | Status |
|------|-------|--------|
| Week 4 | Problem Understanding, KPI Proposal, Data Quality Audit | ✅ Complete |
| Week 5 | EDA, KPI Calculations, Business Insights | ✅ Complete |
| Week 6 | Advanced Analytics, Cross-Variable Analysis, Integration | ✅ Complete |
| Week 7 | Testing, Refinement, End-to-End Validation | ✅ Complete |
| Week 8 | Final Integration, Executive Summary, Presentation | ✅ Complete |

---

## Tools & Technologies

`Python 3` · `Pandas` · `Matplotlib` · `SQL` · `HTML / CSS / JavaScript`

---

*AnalystLab Africa Experience Lab | Data Analytics Track | HealthConnect Clinic*
