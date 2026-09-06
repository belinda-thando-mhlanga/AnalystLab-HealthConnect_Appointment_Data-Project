# Databricks notebook source
# MAGIC %md
# MAGIC # AnalystLab Africa — Experience Lab Internship Programme
# MAGIC ## Week 4 | Data Analytics Track
# MAGIC ### HealthConnect Clinic — Initial Analysis Document
# MAGIC
# MAGIC **Track:** Data Analytics  
# MAGIC **Dataset:** HealthConnect_Appointment_Data.csv  
# MAGIC **Tools:** Python, SQL, Power BI  
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### What this notebook covers (Week 4 tasks only)
# MAGIC
# MAGIC | Task | Description |
# MAGIC |------|-------------|
# MAGIC | Task 1 | Dataset Overview |
# MAGIC | Task 2 | Data Quality Assessment |
# MAGIC | Task 3 | Important Variables |
# MAGIC | Task 4 | Business Questions |
# MAGIC | Task 5 | Proposed KPIs (identified and justified only — no full calculations yet) |
# MAGIC | Task 6 | Initial Analysis Approach |
# MAGIC | Task 7 | Assumptions, Limitations, Risks and Dependencies |
# MAGIC | Task 8 | Week 4 Project Summary |
# MAGIC
# MAGIC > **Note:** The Week 4 brief states you are only required to **identify and justify** the KPIs at this stage. Full KPI calculations, analysis, and visualisations will be completed in Week 5.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Setup — Import Libraries
# MAGIC
# MAGIC We only need **pandas** for Week 4. Pandas is a library that lets us load and work with data in Python — think of it like Excel but inside Python.
# MAGIC
# MAGIC We also import **warnings** just to stop unnecessary messages from appearing in our output.

# COMMAND ----------

import pandas as pd    # pandas lets us load, explore and work with data
import warnings        # stops unnecessary warning messages from printing

warnings.filterwarnings('ignore')

print('Libraries loaded successfully.')

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Task 1 — Dataset Overview
# MAGIC
# MAGIC **Questions:** Review the dataset structure and understand what data is available.
# MAGIC
# MAGIC We start by loading the CSV file into a **DataFrame**. A DataFrame is like a table — rows and columns, just like a spreadsheet.

# COMMAND ----------

# Load the dataset
# The CSV file must be in the same folder as this notebook

df = pd.read_csv('HealthConnect_Appointment_Data.csv')

print('Dataset loaded successfully!')
print()
print(f'Number of rows    : {df.shape[0]}')
print(f'Number of columns : {df.shape[1]}')

# COMMAND ----------

# Preview the first 5 rows to see what the data looks like

print('First 5 rows of the dataset:')
df.head()

# COMMAND ----------

# Check column names and their data types
# 'object' = text   |   'int64' = whole number   |   'float64' = decimal number

print('Column names and data types:')
print()
print(df.dtypes)

# COMMAND ----------

# Count unique patients and unique appointments
# One patient can have more than one appointment record

print(f'Unique appointments : {df["appointment_id"].nunique()}')
print(f'Unique patients     : {df["patient_id"].nunique()}')

# COMMAND ----------

# For columns with categories, let's see all the possible values
# This helps us understand what each column contains

categorical_columns = [
    'gender',
    'age_group',
    'appointment_type',
    'appointment_day',
    'appointment_time',
    'reminder_sent',
    'reminder_channel',
    'appointment_outcome'
]

print('Unique categories for each column:')
print()
for col in categorical_columns:
    values = df[col].dropna().unique().tolist()
    print(f'  {col}: {values}')

# COMMAND ----------

# Basic statistics for the numeric columns
# This shows min, max, average, etc. for each number column

print('Basic statistics for numeric columns:')
print()
df[['age', 'booking_lead_days', 'previous_appointments',
    'previous_no_shows', 'distance_to_clinic_km', 'waiting_time_minutes']].describe().round(2)

# COMMAND ----------

# Count how many appointments had each outcome

outcome_counts = df['appointment_outcome'].value_counts()
outcome_pct    = df['appointment_outcome'].value_counts(normalize=True).mul(100).round(2)

outcome_table = pd.DataFrame({
    'Count': outcome_counts,
    'Percentage (%)': outcome_pct
})

print('Appointment Outcome Distribution:')
print()
print(outcome_table)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1 Summary
# MAGIC
# MAGIC | Property | Detail |
# MAGIC |---|---|
# MAGIC | Total records | 5,000 |
# MAGIC | Total columns | 18 |
# MAGIC | Unique patients | 1,696 |
# MAGIC | Duplicate records | 0 |
# MAGIC
# MAGIC **Columns grouped by category:**
# MAGIC - **Patient info:** patient_id, gender, age, age_group
# MAGIC - **Appointment details:** appointment_id, appointment_type, appointment_date, appointment_day, appointment_time
# MAGIC - **Booking info:** booking_date, booking_lead_days
# MAGIC - **History and reminders:** previous_appointments, previous_no_shows, reminder_sent, reminder_channel
# MAGIC - **Logistics and outcome:** distance_to_clinic_km, waiting_time_minutes, appointment_outcome
# MAGIC
# MAGIC **Key observation:** 48.46% of all appointments result in a No-Show. Nearly 1 in every 2 appointments is missed — confirming this is a serious operational problem for the clinic.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Task 2 — Data Quality Assessment
# MAGIC
# MAGIC **Question:** Conduct an initial data quality assessment.
# MAGIC
# MAGIC We check for: missing values, duplicate rows, incorrect data types, and values that seem unrealistic.

# COMMAND ----------

# CHECK 1: Missing values
# A missing value means a cell is blank — no data was recorded for that field

missing_count = df.isnull().sum()
missing_pct   = (df.isnull().sum() / len(df) * 100).round(2)

missing_table = pd.DataFrame({
    'Missing Count': missing_count,
    'Missing (%)': missing_pct
})

print('Missing values per column:')
print()
print(missing_table)

# COMMAND ----------

# CHECK 2: Why is reminder_channel missing for 1,366 rows?
# Our theory: it should only be blank when no reminder was sent

check = df.groupby('reminder_sent')['reminder_channel'].apply(
    lambda x: x.isnull().sum()
).reset_index()
check.columns = ['reminder_sent', 'missing_reminder_channel_count']

print('Missing reminder_channel — grouped by reminder_sent:')
print()
print(check.to_string(index=False))
print()
print('Conclusion: All 1,366 missing values are from rows where reminder_sent = No.')
print('This is NOT an error — if no reminder was sent, there is no channel to record.')

# COMMAND ----------

# CHECK 3: Duplicate rows
# A duplicate means the exact same appointment appears more than once

duplicates = df.duplicated().sum()
print(f'Duplicate rows found: {duplicates}')
print()
print('No duplicate rows found. Every row is a unique appointment record.')

# COMMAND ----------

# CHECK 4: Date column data types
# Right now the date columns are stored as text, not as real dates
# We need to fix this in Week 5 before doing any date-related analysis

print('Current data type of date columns:')
print(f'  booking_date     : {df["booking_date"].dtype}  <-- stored as text, needs converting')
print(f'  appointment_date : {df["appointment_date"].dtype}  <-- stored as text, needs converting')
print()
print('What they look like right now:')
print(df['booking_date'].head(3).tolist())
print()
print('Action for Week 5: Convert using pd.to_datetime() before any date calculations.')

# COMMAND ----------

# CHECK 5: Numeric range validation
# Are there any values that seem impossible or suspicious?

print('Numeric column ranges (minimum and maximum values):')
print()

cols = ['age', 'booking_lead_days', 'previous_appointments',
        'previous_no_shows', 'distance_to_clinic_km', 'waiting_time_minutes']

for col in cols:
    col_min  = df[col].min()
    col_max  = df[col].max()
    col_mean = round(df[col].mean(), 1)
    print(f'  {col:<28}  min={col_min}  max={col_max}  avg={col_mean}')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2 Summary
# MAGIC
# MAGIC | Quality Check | Finding |
# MAGIC |---|---|
# MAGIC | Missing values | 3 columns have missing values (details below) |
# MAGIC | Duplicate rows | Zero duplicates found — dataset is clean |
# MAGIC | Date formats | booking_date and appointment_date stored as text — must convert in Week 5 |
# MAGIC | Numeric ranges | All values are within realistic and plausible bounds |
# MAGIC
# MAGIC **Missing values explained:**
# MAGIC
# MAGIC | Column | Missing | Why |
# MAGIC |---|---|---|
# MAGIC | reminder_channel | 1,366 (27.3%) | Structurally valid — only blank where reminder_sent = No |
# MAGIC | distance_to_clinic_km | 90 (1.8%) | Small gap — will be addressed following week 5 |
# MAGIC | waiting_time_minutes | 60 (1.2%) | Expected — no wait time recorded when patient did not attend |
# MAGIC
# MAGIC > **Overall:** The dataset is of good quality. The issues found are minor and manageable. No major problems that would block the analysis.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Task 3 — Important Variables
# MAGIC
# MAGIC **Question:** Identify important variables relevant to appointment attendance and no-shows.
# MAGIC
# MAGIC For each variable, we ask: *does this column help explain why a patient missed their appointment?* We check this by comparing values between patients who attended and patients who did not.

# COMMAND ----------

# Variable 1: previous_no_shows
# Question: Do patients who have missed before tend to miss again?

avg_prev = df.groupby('appointment_outcome')['previous_no_shows'].mean().round(2)

print('Average previous no-shows — by appointment outcome:')
print()
print(avg_prev)
print()
print('Finding: Patients who did not attend had a higher average of previous no-shows (0.64)')
print('than those who attended (0.46). Past behaviour predicts future behaviour.')

# COMMAND ----------

# Variable 2: booking_lead_days
# Question: Do appointments booked further in advance have higher no-show rates?

avg_lead = df.groupby('appointment_outcome')['booking_lead_days'].mean().round(2)

print('Average booking lead days — by appointment outcome:')
print()
print(avg_lead)
print()
print('Finding: No-show appointments were booked 34.5 days ahead on average,')
print('compared to 24.5 days for attended ones — a 10-day difference.')
print('The further ahead a booking is made, the higher the no-show risk.')

# COMMAND ----------

# Variable 3: reminder_sent
# Question: Does receiving a reminder reduce the chance of a no-show?

# We calculate what percentage of appointments in each group resulted in a no-show
reminder_ns = df.groupby('reminder_sent')['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).reset_index()
reminder_ns.columns = ['reminder_sent', 'no_show_rate_%']

print('No-show rate — by whether a reminder was sent:')
print()
print(reminder_ns.to_string(index=False))
print()
print('Finding: Without a reminder, 51.39% of patients did not show up.')
print('With a reminder, the rate drops to 47.36% — a 4 percentage point improvement.')

# COMMAND ----------

# Variable 4: appointment_type
# Question: Are certain appointment types more likely to be missed?

type_ns = df.groupby('appointment_type')['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).reset_index()
type_ns.columns = ['appointment_type', 'no_show_rate_%']
type_ns = type_ns.sort_values('no_show_rate_%', ascending=False)

print('No-show rate — by appointment type:')
print()
print(type_ns.to_string(index=False))
print()
print('Finding: Follow-up appointments have the highest no-show rate (51.23%).')
print('General Consultations have the lowest (46.64%).')

# COMMAND ----------

# Variable 5: distance_to_clinic_km
# Question: Do patients who live further away miss more appointments?

avg_dist = df.groupby('appointment_outcome')['distance_to_clinic_km'].mean().round(2)

print('Average distance to clinic — by appointment outcome:')
print()
print(avg_dist)
print()
print('Finding: No-show patients lived slightly further from the clinic on average (10.53 km)')
print('compared to attended patients (9.67 km). Distance may be a small barrier to attendance.')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3 Summary
# MAGIC
# MAGIC **High relevance — strongest connection to no-shows:**
# MAGIC
# MAGIC | Variable | Evidence |
# MAGIC |---|---|
# MAGIC | previous_no_shows | Avg 0.64 (No-Show) vs 0.46 (Attended) |
# MAGIC | booking_lead_days | Avg 34.5 days (No-Show) vs 24.5 days (Attended) |
# MAGIC | reminder_sent | 51.4% no-show rate without reminder vs 47.4% with reminder |
# MAGIC | distance_to_clinic_km | Avg 10.53 km (No-Show) vs 9.67 km (Attended) |
# MAGIC
# MAGIC **Moderate relevance:**
# MAGIC
# MAGIC | Variable | Evidence |
# MAGIC |---|---|
# MAGIC | appointment_type | Follow-up has highest no-show rate (51.23%) |
# MAGIC | reminder_channel | Some channels appear more effective than others |
# MAGIC | age_group | Older patients (65+) have slightly lower no-show rates |
# MAGIC | appointment_day | Sunday and Monday have slightly higher no-show rates |

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Task 4 — Business Questions
# MAGIC
# MAGIC **Question:** Define relevant business questions linked to the clinic's challenges.
# MAGIC
# MAGIC These five questions will guide the full analysis in Weeks 5 to 8.

# COMMAND ----------

# Display the business questions as a table
# We use pd.set_option to make sure the full text is visible (not cut off)

pd.set_option('display.max_colwidth', None)

business_questions = pd.DataFrame({
    'ID': ['BQ1', 'BQ2', 'BQ3', 'BQ4', 'BQ5'],
    'Business Question': [
        'What is the overall no-show rate and how does it vary by appointment type, day, and time slot?',
        'Do appointment reminders reduce no-show rates? Does the channel used (SMS, WhatsApp, Email) make a difference?',
        'Is there a relationship between how far in advance an appointment is booked and whether the patient attends?',
        'Do patients with a history of previous no-shows have significantly higher future no-show rates?',
        'Does a patient living further from the clinic increase the likelihood of a no-show?'
    ],
    'Clinic Challenge Addressed': [
        'Patients missing appointments — understand the scale of the problem and where it happens most',
        'Evaluate whether the current reminder system is effective and which channel works best',
        'Inefficient use of appointment slots — can a shorter booking window reduce no-shows?',
        'Difficulty identifying which patients are at high risk of not attending',
        'Improve patient engagement — understand if distance is a practical barrier to attendance'
    ]
})

print('Business Questions:')
print()
print(business_questions.to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Task 5 — Proposed KPIs
# MAGIC
# MAGIC **What the assignment asks:** Identify 3–5 potential KPIs linked to the business questions. Each KPI should be justified for relevance. You are NOT required to calculate, analyse, or visualise them yet — that is Week 5 work.
# MAGIC
# MAGIC A KPI (Key Performance Indicator) is a measurable value that tells us how the clinic is performing on something that matters.

# COMMAND ----------

# KPI 1 — Overall Appointment No-Show Rate

print('KPI 1 — Overall Appointment No-Show Rate')
print('-' * 55)
print('Linked Business Question : BQ1')
print()
print('Definition:')
print('  The percentage of all scheduled appointments that result in a no-show.')
print()
print('Formula:')
print('  (Total No-Shows / Total Appointments) x 100')
print()
print('Justification:')
print('  This is the headline metric for the entire project. It measures the full scale')
print('  of the missed appointment problem and sets the baseline that all other KPIs')
print('  and interventions will be measured against.')
print()
print('  An initial check shows the rate is approximately 48.46%.')
print('  Full calculation will be completed in Week 5.')

# COMMAND ----------

# KPI 2 — Reminder Effectiveness Rate

print('KPI 2 — Reminder Effectiveness Rate')
print('-' * 55)
print('Linked Business Question : BQ2')
print()
print('Definition:')
print('  The difference in no-show rates between patients who received a reminder')
print('  and those who did not. Also broken down by reminder channel.')
print()
print('Approach:')
print('  Compare no-show rate for reminder_sent = Yes vs No.')
print('  Then compare SMS vs WhatsApp vs Email.')
print()
print('Justification:')
print('  Reminders are the clinic\'s primary tool for reducing no-shows.')
print('  Measuring whether they work — and which channel works best — supports')
print('  a key operational decision for the clinic.')
print()
print('  Initial data suggests reminders reduce no-show rates by about 4 percentage points.')
print('  Full breakdown will be calculated in Week 5.')

# COMMAND ----------

# KPI 3 — No-Show Rate by Booking Lead Time Band

print('KPI 3 — No-Show Rate by Booking Lead Time Band')
print('-' * 55)
print('Linked Business Question : BQ3')
print()
print('Definition:')
print('  The no-show rate for each booking lead time band — grouped by how many days')
print('  before the appointment the booking was made.')
print()
print('Approach:')
print('  In Week 5, group booking_lead_days into four bands:')
print('    0-7 days | 8-14 days | 15-30 days | 31-60 days')
print('  Then calculate the no-show rate for each band.')
print()
print('Justification:')
print('  The data shows that no-show appointments were booked about 10 days further')
print('  in advance than attended ones. A clear pattern exists between booking lead time')
print('  and no-show risk. This KPI will help the clinic evaluate whether a shorter')
print('  booking window could reduce missed appointments.')

# COMMAND ----------

# KPI 4 — No-Show Rate by Previous No-Show History

print('KPI 4 — No-Show Rate by Previous No-Show History')
print('-' * 55)
print('Linked Business Question : BQ4')
print()
print('Definition:')
print('  The no-show rate segmented by how many prior no-shows a patient has on record.')
print()
print('Approach:')
print('  In Week 5, group records by previous_no_shows (0, 1, 2, 3+)')
print('  and calculate the no-show rate per group.')
print()
print('Justification:')
print('  Previous no-show history is the strongest variable found in the data.')
print('  Patients with prior no-shows have a meaningfully higher average previous')
print('  no-show count (0.64) than patients who attended (0.46).')
print('  This KPI will help the clinic identify high-risk patients and proactively')
print('  offer them extra support or follow-up reminders.')

# COMMAND ----------

# KPI 5 — No-Show Rate by Appointment Type

print('KPI 5 — No-Show Rate by Appointment Type')
print('-' * 55)
print('Linked Business Question : BQ1')
print()
print('Definition:')
print('  The no-show rate for each of the four appointment types.')
print()
print('Approach:')
print('  In Week 5, group appointment_outcome by appointment_type')
print('  and calculate the no-show rate per type.')
print()
print('Justification:')
print('  Different appointment types serve different patient needs and urgency levels.')
print('  Initial checks show Follow-up appointments have the highest no-show rate (51.23%)')
print('  while General Consultations are lowest (46.64%).')
print('  This KPI helps the clinic decide where to focus intervention strategies first.')

# COMMAND ----------

# Print a clean summary table of all 5 KPIs

kpi_summary = pd.DataFrame({
    'KPI': ['KPI 1', 'KPI 2', 'KPI 3', 'KPI 4', 'KPI 5'],
    'Name': [
        'Overall No-Show Rate',
        'Reminder Effectiveness Rate',
        'No-Show Rate by Booking Lead Time Band',
        'No-Show Rate by Previous No-Show History',
        'No-Show Rate by Appointment Type'
    ],
    'Linked BQ': ['BQ1', 'BQ2', 'BQ3', 'BQ4', 'BQ1'],
    'Key Variable(s)': [
        'appointment_outcome',
        'reminder_sent, reminder_channel',
        'booking_lead_days',
        'previous_no_shows',
        'appointment_type'
    ]
})

print('KPI Summary Table:')
print()
print(kpi_summary.to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Task 6 — Initial Analysis Approach
# MAGIC
# MAGIC **Question:** Develop an initial approach to the analysis work.
# MAGIC
# MAGIC This outlines what will be done from Week 5 onwards — in what order, using which tools.

# COMMAND ----------

approach = pd.DataFrame({
    'Phase': ['1', '2', '3', '4'],
    'Week': ['Week 5', 'Week 5-6', 'Week 6-7', 'Week 7-8'],
    'What Will Be Done': [
        'Data Preparation: Convert date columns, handle missing values, create lead time bands and patient risk tiers',
        'Exploratory Analysis: Calculate all 5 KPIs, analyse no-show rates across all key variables, answer all 5 business questions using Python and SQL',
        'Visualisations and Findings: Build charts for each business question, summarise key findings, write recommendations',
        'Dashboard: Build a 5-page Power BI dashboard for clinic stakeholders showing KPIs, trends, and insights'
    ],
    'Tool': ['Python (Pandas)', 'Python + SQL', 'Python + SQL', 'Power BI']
})

print('Planned Analysis Approach:')
print()
print(approach.to_string(index=False))
print()
print('Power BI Dashboard Pages (planned for Week 7-8):')
print('  Page 1 — Executive Summary: Overall no-show rate, outcome distribution')
print('  Page 2 — No-Show Patterns: By appointment type, day, and time slot')
print('  Page 3 — Reminders Analysis: Effectiveness by channel')
print('  Page 4 — Booking Lead Time: No-show rate by lead time band')
print('  Page 5 — Patient Risk: No-show rate by previous no-show history')

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Task 7 — Assumptions, Limitations, Risks and Dependencies
# MAGIC
# MAGIC **What the assignment asks:** Identify factors that may affect the proposed approach.

# COMMAND ----------

print('ASSUMPTIONS')
print('=' * 60)
print()
assumptions = [
    'The dataset accurately represents appointment patterns, even though it is fictional.',
    'The appointment_outcome column is correctly recorded with no misclassification.',
    'The 1,366 missing reminder_channel values are correctly explained by reminder_sent = No.',
    'Cancelled appointments will be treated separately from No-Shows in the analysis.',
    'Each row represents one unique appointment event.'
]
for i, item in enumerate(assumptions, 1):
    print(f'  {i}. {item}')

print()
print('LIMITATIONS')
print('=' * 60)
print()
limitations = [
    'The dataset is fictional — findings cannot be applied directly to a real clinic.',
    'We do not know WHY a patient missed their appointment (illness, transport, forgetting, etc.).',
    '90 records are missing distance values — small impact on distance analysis.',
    'waiting_time_minutes is only available for attended appointments, not useful for explaining no-shows.',
    'No socioeconomic or neighbourhood data is available beyond the distance to clinic.'
]
for i, item in enumerate(limitations, 1):
    print(f'  {i}. {item}')

print()
print('RISKS AND MITIGATIONS')
print('=' * 60)
print()
risks = [
    ('Cancelled records distorting the no-show rate if included',
     'Clearly document whether Cancelled is included or excluded in each analysis.'),
    ('Missing distance/waiting time values introducing bias',
     'Apply mean imputation or row exclusion in Week 5 — document the approach used.'),
    ('Date columns causing errors in time-based analysis',
     'Convert to datetime format in Week 5 before running any date calculations.'),
    ('Power BI data model failing due to unformatted dates',
     'Export a fully cleaned CSV from Python before importing into Power BI.')
]
for i, (risk, fix) in enumerate(risks, 1):
    print(f'  {i}. Risk       : {risk}')
    print(f'     Mitigation : {fix}')
    print()

print('DEPENDENCIES')
print('=' * 60)
print()
deps = [
    'HealthConnect_Data_Dictionary.xlsx — confirms what each column means.',
    'HealthConnect_Clinic_Knowledge_Base.docx — provides business context for interpreting findings.',
    'Week 5 data preparation must be completed before EDA and KPI calculations begin.',
    'Cleaned dataset must be exported from Python before Power BI development starts.'
]
for i, item in enumerate(deps, 1):
    print(f'  {i}. {item}')

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Task 8 — Week 4 Project Summary
# MAGIC
# MAGIC **What the assignment asks:** Prepare a concise Week 4 Project Summary covering 6 specific points.

# COMMAND ----------

print('=' * 62)
print('  WEEK 4 PROJECT SUMMARY — DATA ANALYTICS TRACK')
print('  HealthConnect Clinic Experience Lab')
print('=' * 62)
print('''
1. THE SPECIFIC PROBLEM MY TRACK WILL ADDRESS
   HealthConnect Clinic has a 48.46% appointment no-show rate.
   Nearly 1 in every 2 scheduled appointments is missed, causing
   wasted slots, reduced efficiency, and lower patient care quality.
   This track will use Python, SQL, and Power BI to identify what
   factors drive no-shows and generate data-backed insights that
   help the clinic reduce missed appointments.

2. RESOURCES USED
   - HealthConnect_Appointment_Data.csv (5,000 records, 18 columns)
   - HealthConnect_Data_Dictionary.xlsx (column definitions)
   - AnalystLab Africa Week 4 Assignment Brief
   - Python (Pandas) for data loading and initial exploration

3. KEY OBSERVATIONS FROM WEEK 4
   - Overall no-show rate is 48.46% — nearly 1 in 2 appointments missed
   - Patients with prior no-shows have higher future no-show risk
     (avg 0.64 prior no-shows vs 0.46 for patients who attended)
   - Appointments booked further ahead have higher no-show rates
     (avg 34.5 days for no-shows vs 24.5 days for attended)
   - Reminders reduce no-show rate by approximately 4 percentage points
   - Follow-up appointments have the highest no-show rate (51.23%)
   - Dataset quality is good — only minor, manageable gaps found

4. PROPOSED APPROACH
   Phase 1 (Week 5)  : Data preparation in Python
   Phase 2 (Week 5-6): Full EDA using Python and SQL
   Phase 3 (Week 6-7): KPI calculations and visualisations
   Phase 4 (Week 7-8): Power BI dashboard for stakeholders

5. KEY CONSIDERATIONS THAT MAY AFFECT THE PROJECT
   - Cancelled appointments need a clear handling decision before analysis
   - Date columns must be converted to datetime format in Week 5
   - All findings must be framed as based on fictional data
   - The 48.46% baseline is the core problem to explain and address

6. PROPOSED FOCUS FOR WEEK 5
   - Complete Python data preparation pipeline
   - Convert date columns and handle missing values
   - Create derived columns: lead time bands, patient risk tiers
   - Begin full exploratory data analysis
   - Run SQL queries for KPI calculations
   - Start building the Power BI data model
''')
print('=' * 62)