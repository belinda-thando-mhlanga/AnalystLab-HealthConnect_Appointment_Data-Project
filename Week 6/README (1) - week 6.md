# HealthConnect Clinic — Week 6: Advanced Analytics & Integration
### AnalystLab Africa | Experience Lab | Data Analytics Track

---

## What This Week Was About

Week 6 moved from calculating KPIs to **going deeper**. Instead of looking at one variable at a time, this week combined variables to find more meaningful patterns, validated all 5 KPIs from Week 5, and collaborated with the Data Science track to share analytical evidence for their prediction model.

**Week 6 focus:** Integration → Advanced Development → Validation

---

## Files in This Week's Submission

| File | Description |
|------|-------------|
| `Week6_HealthConnect_DataAnalytics.ipynb` | Main Week 6 analysis notebook |
| `Week6_ProjectReport_HealthConnect.docx` | 18-page project report |
| `chart_w6_01_type_x_leadtime.png` | Appointment type × booking lead time |
| `chart_w6_02_risktier_x_reminder.png` | Risk tier × reminder sent |
| `chart_w6_03_risktier_x_channel.png` | Risk tier × reminder channel |
| `chart_w6_04_distance_band.png` | No-show rate by distance band |
| `chart_w6_05_monthly_trend.png` | Monthly no-show trend (Jan 2025 – Jun 2026) |
| `chart_w6_06_segments.png` | Best vs average vs worst patient segment |

---

## Key Findings

### Worst and Best Patient Segments

| Segment | Who | No-Show Rate |
|---------|-----|-------------|
| Worst case | High Risk + booked 31–60 days ahead + no reminder | **72.31%** |
| Overall average | All 5,000 appointments | 48.46% |
| Best case | Low Risk + booked same week + SMS reminder | **23.18%** |

The gap between worst and best is **49 percentage points** — that is how much improvement is available through the right interventions.

---

### New Findings from Cross-Variable Analysis

| Finding | Detail |
|---------|--------|
| Worst appointment combination | Follow-up + booked 31–60 days ahead = **65.14%** no-show rate |
| High Risk patients with a reminder | Still **58.22%** — a standard reminder is not enough |
| SMS vs WhatsApp for Medium Risk | SMS: 48.64% vs WhatsApp: 58.59% — a 9.95 pp gap |
| Patients living over 20 km away | **57.76%** no-show rate — nearly 10 pp above average |
| Worst month | December 2025: **53.85%** |
| Best month | November 2025: **42.17%** |
| Seasonal range | **11.68 percentage points** between best and worst month |

---

### KPI Validation Results

All 5 KPIs from Week 5 were tested across subgroups. None required revision.

| KPI | Result | Validated |
|-----|--------|-----------|
| Overall No-Show Rate | 48.46% | ✅ |
| Reminder Effectiveness | SMS best across every risk tier | ✅ |
| No-Show Rate by Lead Time | Pattern holds in all appointment types | ✅ |
| No-Show Rate by Risk Tier | High Risk always above Low Risk | ✅ |
| No-Show Rate by Appointment Type | Follow-up worst in every lead time band | ✅ |

---

## Cross-Track Integration — Data Science Track

| | Detail |
|--|--------|
| **Provided to Data Science** | Feature importance ranking table, cross-variable charts, worst-case segment (72.31%) and best-case segment (23.18%) definitions |
| **Received from Data Science** | Model feature importance from their Week 5 baseline confirming booking lead time and prior no-show history as the two strongest predictors |
| **What changed** | Data Science will use `lead_time_band` and `patient_risk_tier` as engineered features. The 72.31% worst-case rate is now the model evaluation benchmark |

---

## How to Run the Notebook

1. Download `Week6_HealthConnect_DataAnalytics.ipynb`
2. Place `HealthConnect_Appointment_Data.csv` in the same folder
3. Open in [Google Colab](https://colab.research.google.com)
4. Run each cell top to bottom using **Shift + Enter**

The setup cell automatically re-applies all Week 5 data preparations — no need to run the Week 5 notebook first.

```python
# Libraries needed (both pre-installed in Google Colab)
import pandas as pd
import matplotlib.pyplot as plt
```

---

## Tools Used This Week

`Python` · `Pandas` · `Matplotlib` · `SQL` · `Power BI (planned for Week 7)`

---

*AnalystLab Africa Experience Lab | Data Analytics Track | HealthConnect Clinic*
