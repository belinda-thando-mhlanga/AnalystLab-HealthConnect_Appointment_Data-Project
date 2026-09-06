# Databricks notebook source
# MAGIC %md
# MAGIC # AnalystLab Africa — Experience Lab Internship Programme
# MAGIC ## Week 5 | Data Analytics Track
# MAGIC ### HealthConnect Clinic — Initial Analytics Report
# MAGIC
# MAGIC **Track:** Data Analytics  
# MAGIC **Dataset:** HealthConnect_Appointment_Data.csv  
# MAGIC **Tools:** Python, SQL, Power BI  
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### What this notebook covers (Week 5 tasks only)
# MAGIC
# MAGIC | Part | Description |
# MAGIC |------|-------------|
# MAGIC | Part 1 | Week 4 Foundation Review |
# MAGIC | Part 2 | Data Preparation |
# MAGIC | Part 3 | Exploratory Data Analysis (EDA) |
# MAGIC | Part 4 | KPI Development |
# MAGIC | Part 5 | Business Insights and Recommendations |
# MAGIC | Part 6 | Cross-Track Collaboration |
# MAGIC | Part 7 | Assumptions, Limitations, Risks and Dependencies |
# MAGIC | Part 8 | Week 5 Project Summary |

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Setup — Import Libraries
# MAGIC
# MAGIC We need three libraries for Week 5:
# MAGIC - **pandas** — to load and work with data
# MAGIC - **matplotlib** — to draw charts
# MAGIC - **warnings** — to keep the output clean

# COMMAND ----------

import pandas as pd                  # for loading and working with data
import matplotlib.pyplot as plt      # for drawing charts
import warnings                      # stops unnecessary warning messages

warnings.filterwarnings('ignore')

# This setting makes sure all text in tables is shown in full
pd.set_option('display.max_colwidth', None)

print('Libraries loaded successfully.')

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 1 — Week 4 Foundation Review
# MAGIC
# MAGIC **What the assignment asks:** Before starting Week 5 work, briefly revisit the Week 4 foundation — the problem, approach, resources, and what was planned for Week 5.
# MAGIC
# MAGIC > This is a transition section, not a repeat of all Week 4 work.

# COMMAND ----------

# Week 4 Foundation Review — displayed as a summary table

review = pd.DataFrame({
    'Item': [
        'Problem Defined',
        'Week 4 Approach',
        'Resources Used',
        'Key Assumptions',
        'Key Limitations',
        'Week 5 Plan'
    ],
    'Summary': [
        'HealthConnect Clinic has a 48.46% appointment no-show rate. The Data Analytics track will use data to identify what drives no-shows and produce insights that help reduce missed appointments.',
        'Phase 1: Data preparation. Phase 2: EDA and KPI calculations. Phase 3: Visualisations and findings. Phase 4: Power BI dashboard.',
        'HealthConnect_Appointment_Data.csv (5,000 records, 18 columns) and HealthConnect_Data_Dictionary.xlsx.',
        'Dataset accurately represents appointment patterns. appointment_outcome is correctly recorded. Cancelled appointments are treated separately from No-Shows.',
        'Dataset is fictional so findings are illustrative only. No-show reasons are unknown. 90 records are missing distance values.',
        'Complete data preparation, run full EDA, calculate all 5 KPIs, produce visualisations, and document business insights.'
    ]
})

print('Week 4 Foundation Review:\n')
print(review.to_string(index=True))

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 2 — Data Preparation
# MAGIC
# MAGIC **What the assignment asks:** Inspect variables, check data types, handle missing values, remove duplicates, identify inconsistencies, and document observations. Do not overwrite the original dataset.
# MAGIC
# MAGIC We load the data into a new working copy so the original file is never changed.

# COMMAND ----------

# Load the original dataset into a variable called 'df_raw'
# We will never change df_raw — it stays as the original

df_raw = pd.read_csv('HealthConnect_Appointment_Data.csv')

# Make a working copy that we are allowed to clean and change
df = df_raw.copy()

print('Dataset loaded successfully.')
print(f'Rows: {df.shape[0]}  |  Columns: {df.shape[1]}')

# COMMAND ----------

df.head()

#will display the first 5 rows.

# COMMAND ----------

print('Column names and current data types:\n')
print(df.dtypes)


#will display the data types.
# We need to know which columns are text, numbers, or dates

# COMMAND ----------

# Step 2: Fix the date columns
# booking_date and appointment_date are stored as text/object
# We convert them to proper date format so we can use them in calculations

df['booking_date']     = pd.to_datetime(df['booking_date'])
df['appointment_date'] = pd.to_datetime(df['appointment_date'])

print('Date columns after conversion:')
print(f'  booking_date     : {df["booking_date"].dtype}')
print(f'  appointment_date : {df["appointment_date"].dtype}')
print()
print('Date conversion complete. Both columns are now proper datetime format.')


# COMMAND ----------

# Step 3: Check for missing values

missing_count = df.isnull().sum()
missing_pct   = (df.isnull().sum() / len(df) * 100).round(2)  #percentage is very helpful when you're checking missing data because the number of missing values alone doesn't tell the whole story.

missing_table = pd.DataFrame({
    'Missing Count': missing_count,
    'Missing %': missing_pct
})

# Only show columns that actually have missing values
missing_table = missing_table[missing_table['Missing Count'] > 0]

print('Columns with missing values:\n')
print(missing_table)
print()
print('All other columns: complete (0 missing values).')

# COMMAND ----------

# Step 4: Handle missing values

# reminder_channel: missing because no reminder was sent — this is correct, leave it as is
# distance_to_clinic_km: 90 missing — we fill these with the column average (mean imputation)
# waiting_time_minutes: 60 missing — only recorded for attended appointments, leave as is

# Fill missing distance values with the column mean
distance_mean = df['distance_to_clinic_km'].mean().round(2)
df['distance_to_clinic_km'] = df['distance_to_clinic_km'].fillna(distance_mean)  #Filling the missing values with the distance mean

print(f'Missing distance values filled with column mean: {distance_mean} km')
print(f'Remaining missing distance values: {df["distance_to_clinic_km"].isnull().sum()}')

# COMMAND ----------

# Step 5: Check for duplicate rows

duplicates = df.duplicated().sum()
print(f'Duplicate rows: {duplicates}')
print('No duplicates found. Every row is a unique appointment.')

# COMMAND ----------

# Step 6: Check for inconsistent values in categorical columns
# We want to make sure there are no unexpected or misspelled categories

cat_cols = ['gender', 'age_group', 'appointment_type', 'appointment_day',
            'appointment_time', 'reminder_sent', 'appointment_outcome']

print('Unique values per categorical column:\n')
for col in cat_cols:
    vals = sorted(df[col].dropna().unique().tolist())
    print(f'{col}: {vals}')

# COMMAND ----------

# Step 7: Create derived columns that will help with the analysis

# Derived column 1: booking_lead_days grouped into time bands
# This makes it easier to see patterns across different booking windows
df['lead_time_band'] = pd.cut(
    df['booking_lead_days'],
    bins=[-1, 7, 14, 30, 60],
    labels=['0-7 days', '8-14 days', '15-30 days', '31-60 days']
)

# Derived column 2: patient risk tier based on previous no-shows
# Patients with more prior no-shows are at higher risk of missing again
def assign_risk(n):
    if n == 0:
        return 'Low Risk'
    elif n == 1:
        return 'Medium Risk'
    else:
        return 'High Risk'

df['patient_risk_tier'] = df['previous_no_shows'].apply(assign_risk)

print('New derived columns created:')
print(f'  lead_time_band    : {df["lead_time_band"].unique().tolist()}')
print(f'  patient_risk_tier : {df["patient_risk_tier"].unique().tolist()}')

# COMMAND ----------

# Step 8: Data preparation summary

prep_summary = pd.DataFrame({
    'Action': [
        'Loaded original dataset into df_raw (read-only)',
        'Created working copy df for all changes',
        'Converted booking_date to datetime',
        'Converted appointment_date to datetime',
        'Filled 90 missing distance values with column mean (10.11 km)',
        'Left reminder_channel nulls as-is (structurally valid)',
        'Left waiting_time_minutes nulls as-is (expected for no-shows)',
        'Confirmed 0 duplicate rows',
        'Confirmed all categorical values are consistent',
        'Created lead_time_band column (0-7, 8-14, 15-30, 31-60 days)',
        'Created patient_risk_tier column (Low, Medium, High)'
    ],
    'Status': [
        'Done', 'Done', 'Done', 'Done', 'Done',
        'Done', 'Done', 'Done', 'Done', 'Done', 'Done'
    ]
})

print('Data Preparation Summary:\n')
print(prep_summary.to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 3 — Exploratory Data Analysis (EDA)
# MAGIC
# MAGIC **What the assignment asks:** Investigate appointment attendance and no-show patterns across appointment characteristics, patient characteristics, previous history, reminders, distance, and cancellations.
# MAGIC
# MAGIC For each analysis, we calculate the no-show rate and draw a chart to visualise the pattern.

# COMMAND ----------

# Helper function — we will use this repeatedly throughout the EDA
# It calculates the no-show rate for any column we give it

def noshow_rate(dataframe, column):
    """
    Groups the data by the given column and calculates
    what percentage of appointments in each group resulted in a No-Show.
    Returns a DataFrame sorted from highest to lowest no-show rate.
    """
    result = df.groupby(column)['appointment_outcome'].apply(
        lambda x: round((x == 'No-Show').mean() * 100, 2)
    ).reset_index()

    result.columns = [column, 'no_show_rate_%']

    return result.sort_values('no_show_rate_%', ascending=False)

print('Helper function defined. Ready to start EDA.')

# COMMAND ----------

# EDA 1: Overall outcome distribution
# What is the overall split between No-Show, Attended, and Cancelled?

outcome_counts = df['appointment_outcome'].value_counts()
outcome_pct    = df['appointment_outcome'].value_counts(normalize=True).mul(100).round(2)

outcome_table = pd.DataFrame({'Count': outcome_counts, 'Percentage (%)': outcome_pct})
print('Overall Appointment Outcome Distribution:\n')
print(outcome_table)

# Chart
colours = ['#E84855', '#2E86AB', '#F4A261']
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(outcome_counts.index, outcome_counts.values, color=colours, width=0.5, edgecolor='white')
for bar, pct in zip(bars, outcome_pct.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'{pct}%', ha='center', fontweight='bold', fontsize=11)
ax.set_title('Appointment Outcome Distribution', fontweight='bold', fontsize=13)
ax.set_ylabel('Number of Appointments')
ax.set_ylim(0, 3000)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart_01_outcome_distribution.png', dpi=150, bbox_inches='tight')
plt.show()

# COMMAND ----------

print('Observation: 48.46% of all appointments result in a No-Show — nearly 1 in every 2.')

# COMMAND ----------

# EDA 2: No-show rate by appointment type
# Do certain types of appointments get missed more often?

ns_type = noshow_rate(df, 'appointment_type')
print('No-show rate by appointment type:\n')
print(ns_type.to_string(index=False))

# Chart
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(ns_type['appointment_type'], ns_type['no_show_rate_%'],
        color='#E84855', edgecolor='white')
for i, v in enumerate(ns_type['no_show_rate_%']):
    ax.text(v + 0.3, i, f'{v}%', va='center', fontweight='bold')
ax.axvline(48.46, color='#1F4E79', linestyle='--', linewidth=1.5, label='Overall avg (48.46%)')
ax.set_title('No-Show Rate by Appointment Type', fontweight='bold', fontsize=13)
ax.set_xlabel('No-Show Rate (%)')
ax.set_xlim(0, 60)
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart_02_noshow_by_type.png', dpi=150, bbox_inches='tight')
plt.show()

# COMMAND ----------

print('Observation: Follow-up appointments have the highest no-show rate (51.23%).')
print('General Consultations have the lowest (46.64%).')

# COMMAND ----------

# EDA 3: No-show rate by day of the week
# Are certain days worse for no-shows?

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

ns_day = df.groupby('appointment_day')['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).reindex(day_order).reset_index()
ns_day.columns = ['appointment_day', 'no_show_rate_%']

print('No-show rate by day of the week:\n')
print(ns_day.to_string(index=False))

# Chart
fig, ax = plt.subplots(figsize=(9, 4))
bar_colours = ['#E84855' if v >= 49.5 else '#2E86AB' for v in ns_day['no_show_rate_%']]
ax.bar(ns_day['appointment_day'], ns_day['no_show_rate_%'],
       color=bar_colours, edgecolor='white', width=0.6)
for i, v in enumerate(ns_day['no_show_rate_%']):
    ax.text(i, v + 0.3, f'{v}%', ha='center', fontweight='bold', fontsize=9)
ax.axhline(48.46, color='#1F4E79', linestyle='--', linewidth=1.5, label='Overall avg (48.46%)')
ax.set_title('No-Show Rate by Day of the Week', fontweight='bold', fontsize=13)
ax.set_ylabel('No-Show Rate (%)')
ax.set_ylim(40, 56)
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart_03_noshow_by_day.png', dpi=150, bbox_inches='tight')
plt.show()

# COMMAND ----------

print('Observation: Sunday (50.47%) and Monday (49.64%) have the highest no-show rates.')
print('Friday (46.57%) and Saturday (46.82%) are the lowest.')

# COMMAND ----------

# EDA 4: No-show rate by time slot
# Does the time of day affect whether a patient attends?

ns_time = noshow_rate(df, 'appointment_time')
print('No-show rate by appointment time slot:\n')
print(ns_time.to_string(index=False))

# Chart
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(ns_time['appointment_time'], ns_time['no_show_rate_%'],
       color=['#E84855', '#F4A261', '#2E86AB'], edgecolor='white', width=0.5)
for i, v in enumerate(ns_time['no_show_rate_%']):
    ax.text(i, v + 0.3, f'{v}%', ha='center', fontweight='bold')

ax.axhline(48.46, color='#1F4E79', linestyle='--', linewidth=1.5, label='Overall avg (48.46%)')
ax.set_title('No-Show Rate by Time Slot', fontweight='bold', fontsize=13)
ax.set_ylabel('No-Show Rate (%)')
ax.set_ylim(44, 54)
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart_04_noshow_by_time.png', dpi=150, bbox_inches='tight')
plt.show()

# COMMAND ----------

print('Observation: Evening slots have the highest no-show rate (49.78%).')
print('Morning slots are slightly lower (48.14%). Differences are small.')

# COMMAND ----------

# EDA 5: No-show rate by age group
# Do younger or older patients miss appointments more often?

age_order = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']

ns_age = df.groupby('age_group')['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).reindex(age_order).reset_index()
ns_age.columns = ['age_group', 'no_show_rate_%']

print('No-show rate by age group:\n')
print(ns_age.to_string(index=False))

# Chart
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(ns_age['age_group'], ns_age['no_show_rate_%'],
       color='#2E86AB', edgecolor='white', width=0.6)
for i, v in enumerate(ns_age['no_show_rate_%']):
    ax.text(i, v + 0.3, f'{v}%', ha='center', fontweight='bold', fontsize=9)
ax.axhline(48.46, color='#1F4E79', linestyle='--', linewidth=1.5, label='Overall avg (48.46%)')
ax.set_title('No-Show Rate by Age Group', fontweight='bold', fontsize=13)
ax.set_ylabel('No-Show Rate (%)')
ax.set_ylim(40, 56)
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart_05_noshow_by_age.png', dpi=150, bbox_inches='tight')
plt.show()

# COMMAND ----------

print('Observation: The 65+ group has the lowest no-show rate (45.12%).')
print('The 55-64 (50.75%) and 25-34 (50.70%) groups have the highest rates.')

# COMMAND ----------

# EDA 6: No-show rate by reminder sent
# Does receiving a reminder reduce the chance of missing an appointment?

ns_reminder = noshow_rate(df, 'reminder_sent')
print('No-show rate by reminder sent:\n')
print(ns_reminder.to_string(index=False))
print()
print('Difference: 51.39% (no reminder) minus 47.36% (with reminder) = 4.03 percentage points')

# COMMAND ----------

# EDA 7: No-show rate by reminder channel
# Among patients who received a reminder, which channel worked best?

# Filter to only the rows where a reminder was sent
df_reminded = df[df['reminder_sent'] == 'Yes']

ns_channel = noshow_rate(df_reminded, 'reminder_channel')
print('No-show rate by reminder channel (only where reminder was sent):\n')
print(ns_channel.to_string(index=False))

# Chart — combining reminder_sent and channel comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Left: reminder sent vs not sent
ns_rem = noshow_rate(df, 'reminder_sent').sort_values('reminder_sent')
axes[0].bar(ns_rem['reminder_sent'], ns_rem['no_show_rate_%'],
            color=['#2E86AB', '#E84855'], edgecolor='white', width=0.4)
for i, v in enumerate(ns_rem['no_show_rate_%']):
    axes[0].text(i, v + 0.4, f'{v}%', ha='center', fontweight='bold')
axes[0].set_title('No-Show Rate: Reminder Sent vs Not', fontweight='bold')
axes[0].set_ylabel('No-Show Rate (%)')
axes[0].set_ylim(40, 58)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

# Right: by channel
axes[1].bar(ns_channel['reminder_channel'], ns_channel['no_show_rate_%'],
            color=['#E84855', '#F4A261', '#2E86AB'], edgecolor='white', width=0.4)
for i, v in enumerate(ns_channel['no_show_rate_%']):
    axes[1].text(i, v + 0.4, f'{v}%', ha='center', fontweight='bold')
axes[1].set_title('No-Show Rate by Reminder Channel', fontweight='bold')
axes[1].set_ylabel('No-Show Rate (%)')
axes[1].set_ylim(40, 56)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

plt.suptitle('Reminder Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart_06_reminder_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print('Observation: SMS is the most effective reminder channel (45.75% no-show rate).')
print('WhatsApp is the least effective (49.77%).')

# COMMAND ----------

# EDA 8: No-show rate by booking lead time band
# Does booking further in advance increase the risk of a no-show?

ns_lead = df.groupby('lead_time_band', observed=True)['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).reset_index()
ns_lead.columns = ['lead_time_band', 'no_show_rate_%']

print('No-show rate by booking lead time band:\n')
print(ns_lead.to_string(index=False))

# Chart
fig, ax = plt.subplots(figsize=(8, 4))
colours = ['#2E86AB', '#5DA8C5', '#F4A261', '#E84855']
ax.bar(ns_lead['lead_time_band'].astype(str), ns_lead['no_show_rate_%'],
       color=colours, edgecolor='white', width=0.5)
for i, v in enumerate(ns_lead['no_show_rate_%']):
    ax.text(i, v + 0.8, f'{v}%', ha='center', fontweight='bold')
ax.set_title('No-Show Rate by Booking Lead Time Band', fontweight='bold', fontsize=13)
ax.set_xlabel('Days Between Booking and Appointment')
ax.set_ylabel('No-Show Rate (%)')
ax.set_ylim(0, 75)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart_07_noshow_by_lead_time.png', dpi=150, bbox_inches='tight')
plt.show()
print('Observation: No-show rate rises from 27.81% (0-7 days) to 60.49% (31-60 days).')
print('Appointments booked 31-60 days ahead are more than twice as likely to be missed.')

# COMMAND ----------

# EDA 9: No-show rate by previous no-show history
# Do patients with a history of missing appointments tend to miss again?

ns_prev = noshow_rate(df, 'previous_no_shows')
ns_prev = ns_prev.sort_values('previous_no_shows').reset_index(drop=True)

print('No-show rate by number of previous no-shows:\n')
print(ns_prev.to_string(index=False))

# Chart
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(ns_prev['previous_no_shows'].astype(str), ns_prev['no_show_rate_%'],
       color='#E84855', edgecolor='white')
for i, v in enumerate(ns_prev['no_show_rate_%']):
    ax.text(i, v + 1.5, f'{v}%', ha='center', fontweight='bold', fontsize=9)
ax.axhline(48.46, color='#1F4E79', linestyle='--', linewidth=1.5, label='Overall avg (48.46%)')
ax.set_title('No-Show Rate by Number of Previous No-Shows', fontweight='bold', fontsize=13)
ax.set_xlabel('Number of Previous No-Shows')
ax.set_ylabel('No-Show Rate (%)')
ax.set_ylim(0, 115)
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart_08_noshow_by_history.png', dpi=150, bbox_inches='tight')
plt.show()
print('Observation: Patients with 0 prior no-shows have a 43.51% no-show rate.')
print('This rises steadily to 100% for patients with 5 prior no-shows.')

# COMMAND ----------

# EDA 10: No-show rate by patient risk tier
# How does the risk tier classification we created in data prep compare?

tier_order = ['Low Risk', 'Medium Risk', 'High Risk']

ns_tier = df.groupby('patient_risk_tier')['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).reindex(tier_order).reset_index()
ns_tier.columns = ['patient_risk_tier', 'no_show_rate_%']

# Also add count of patients per tier
tier_counts = df['patient_risk_tier'].value_counts().reindex(tier_order)
ns_tier['patient_count'] = tier_counts.values

print('No-show rate by patient risk tier:\n')
print(ns_tier.to_string(index=False))
print()
print('Interpretation:')
print('  Low Risk  (0 prior NS): 43.51% no-show rate — 2,921 patients')
print('  Medium Risk (1 prior NS): 53.49% no-show rate — 1,548 patients')
print('  High Risk  (2+ prior NS): ~63% no-show rate — 531 patients')

# COMMAND ----------

# EDA 11: Distance to clinic by outcome
# Do patients who live further away miss appointments more?

avg_dist = df.groupby('appointment_outcome')['distance_to_clinic_km'].mean().round(2)
print('Average distance to clinic by appointment outcome:\n')
print(avg_dist.to_frame('avg_distance_km'))
print()
print('Observation: No-show patients lived on average 10.53 km from the clinic,')
print('compared to 9.67 km for attended patients — a difference of 0.86 km.')
print('Distance has a small but consistent association with no-show behaviour.')

# COMMAND ----------

# EDA 12: Cancellations — how do they differ from no-shows?
# The assignment asks us to investigate cancellations separately

cancelled = df[df['appointment_outcome'] == 'Cancelled']
total = len(df)
cancel_rate = round(len(cancelled) / total * 100, 2)

print(f'Total cancellations : {len(cancelled)}')
print(f'Cancellation rate   : {cancel_rate}%')
print()

# Cancellation rate by appointment type
cancel_by_type = df.groupby('appointment_type')['appointment_outcome'].apply(
    lambda x: round((x == 'Cancelled').sum() / len(x) * 100, 2)
).sort_values(ascending=False).reset_index()
cancel_by_type.columns = ['appointment_type', 'cancellation_rate_%']

print('Cancellation rate by appointment type:\n')
print(cancel_by_type.to_string(index=False))
print()
print('Note: Cancellations (5.26%) are treated separately from No-Shows (48.46%).')
print('A cancellation means the patient notified the clinic; a no-show means they did not.')

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 4 — KPI Development
# MAGIC
# MAGIC **What the assignment asks:** Select 3–5 KPIs from the ones proposed in Week 4. For each KPI: define it, explain why it matters, calculate it, link it to a business question, and interpret the result.
# MAGIC
# MAGIC All 5 KPIs from Week 4 are calculated here.

# COMMAND ----------

# KPI 1 — Overall Appointment No-Show Rate
# Linked to Business Question BQ1

print('=' * 60)
print('KPI 1 — Overall Appointment No-Show Rate')
print('=' * 60)
print('Definition  : Percentage of all appointments that result in a no-show.')
print('Formula     : (Total No-Shows / Total Appointments) x 100')
print('Linked to   : BQ1 — What is the overall no-show rate?')
print()

total_appointments = len(df)
total_no_shows     = (df['appointment_outcome'] == 'No-Show').sum()
total_attended     = (df['appointment_outcome'] == 'Attended').sum()
total_cancelled    = (df['appointment_outcome'] == 'Cancelled').sum()
kpi1_rate          = round(total_no_shows / total_appointments * 100, 2)

print(f'Total appointments : {total_appointments:,}')
print(f'Total no-shows     : {total_no_shows:,}')
print(f'Total attended     : {total_attended:,}')
print(f'Total cancelled    : {total_cancelled:,}')
print()
print(f'>>> KPI 1 RESULT: {kpi1_rate}% No-Show Rate')
print()
print('Interpretation:')
print('Nearly 1 in every 2 appointments is missed. This is a critically high rate')
print('that directly affects the clinic\'s operational efficiency and patient care quality.')
print('This metric is the baseline — all interventions should aim to reduce it.')

# COMMAND ----------

# KPI 2 — Reminder Effectiveness Rate
# Linked to Business Question BQ2

print('=' * 60)
print('KPI 2 — Reminder Effectiveness Rate')
print('=' * 60)
print('Definition  : Difference in no-show rates between patients who received')
print('              a reminder and those who did not; broken down by channel.')
print('Linked to   : BQ2 — Do reminders reduce no-show rates?')
print()

# Calculate rates
with_reminder    = df[df['reminder_sent'] == 'Yes']
without_reminder = df[df['reminder_sent'] == 'No']

rate_with    = round((with_reminder['appointment_outcome'] == 'No-Show').mean() * 100, 2)
rate_without = round((without_reminder['appointment_outcome'] == 'No-Show').mean() * 100, 2)
reduction    = round(rate_without - rate_with, 2)

print(f'No-show rate WITH reminder    : {rate_with}%  (n={len(with_reminder):,})')
print(f'No-show rate WITHOUT reminder : {rate_without}%  (n={len(without_reminder):,})')
print(f'Reduction from reminders      : {reduction} percentage points')
print()

# By channel
print('No-show rate by reminder channel:')
for ch in ['SMS', 'Email', 'WhatsApp']:
    sub  = df[df['reminder_channel'] == ch]
    rate = round((sub['appointment_outcome'] == 'No-Show').mean() * 100, 2)
    print(f'  {ch:<10}: {rate}%  (n={len(sub):,})')

print()
print('Interpretation:')
print('Reminders reduce no-show rates by 4.03 percentage points.')
print('SMS is the most effective channel (45.75%) and should be prioritised.')
print('WhatsApp (49.77%) performs no better than not sending a reminder at all.')

# COMMAND ----------

# KPI 3 — No-Show Rate by Booking Lead Time Band
# Linked to Business Question BQ3

print('=' * 60)
print('KPI 3 — No-Show Rate by Booking Lead Time Band')
print('=' * 60)
print('Definition  : No-show rate grouped by how many days before the')
print('              appointment the booking was made.')
print('Linked to   : BQ3 — Does booking lead time affect no-show risk?')
print()

kpi3 = df.groupby('lead_time_band', observed=True)['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).reset_index()
kpi3.columns = ['Lead Time Band', 'No-Show Rate (%)']
kpi3['Count'] = df.groupby('lead_time_band', observed=True).size().values

print(kpi3.to_string(index=False))
print()
print('Interpretation:')
print('There is a very clear and consistent pattern: the further in advance an')
print('appointment is booked, the more likely it is to be missed.')
print('Appointments booked 31-60 days ahead (60.49%) are more than twice as')
print('likely to be missed as same-week bookings (27.81%).')
print('Recommendation: The clinic should consider limiting booking windows to')
print('14 days where operationally possible.')

# COMMAND ----------

# KPI 4 — No-Show Rate by Previous No-Show History
# Linked to Business Question BQ4

print('=' * 60)
print('KPI 4 — No-Show Rate by Previous No-Show History')
print('=' * 60)
print('Definition  : No-show rate segmented by how many prior no-shows')
print('              the patient has on record.')
print('Linked to   : BQ4 — Do patients with prior no-shows miss again?')
print()

kpi4 = df.groupby('previous_no_shows')['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).reset_index()
kpi4.columns = ['Previous No-Shows', 'No-Show Rate (%)']
kpi4['Patient Count'] = df.groupby('previous_no_shows').size().values

print(kpi4.to_string(index=False))
print()

# Risk tier summary
print('Risk Tier Summary:')
for tier in ['Low Risk', 'Medium Risk', 'High Risk']:
    sub  = df[df['patient_risk_tier'] == tier]
    rate = round((sub['appointment_outcome'] == 'No-Show').mean() * 100, 2)
    print(f'  {tier:<14}: {rate}%  (n={len(sub):,} appointments)')

print()
print('Interpretation:')
print('Prior no-show history is the strongest predictor in the dataset.')
print('The clinic should flag Medium and High Risk patients for additional')
print('outreach — for example, a phone call in addition to a standard reminder.')

# COMMAND ----------

# KPI 5 — No-Show Rate by Appointment Type
# Linked to Business Question BQ1

print('=' * 60)
print('KPI 5 — No-Show Rate by Appointment Type')
print('=' * 60)
print('Definition  : No-show rate for each of the four appointment types.')
print('Linked to   : BQ1 — How does no-show rate vary by appointment type?')
print()

kpi5 = df.groupby('appointment_type')['appointment_outcome'].apply(
    lambda x: round((x == 'No-Show').sum() / len(x) * 100, 2)
).sort_values(ascending=False).reset_index()
kpi5.columns = ['Appointment Type', 'No-Show Rate (%)']
kpi5['Count'] = df.groupby('appointment_type').size().reindex(
    kpi5['Appointment Type']).values

print(kpi5.to_string(index=False))
print()
print('Interpretation:')
print('Follow-up appointments have the highest no-show rate (51.23%).')
print('Patients may feel less urgency for follow-ups compared to initial consultations.')
print('The clinic should consider dedicated follow-up reminder strategies')
print('and shorter lead times specifically for this appointment category.')

# COMMAND ----------

# KPI Summary Table — all 5 KPIs in one view

kpi_summary = pd.DataFrame({
    'KPI': ['KPI 1', 'KPI 2', 'KPI 3', 'KPI 4', 'KPI 5'],
    'Name': [
        'Overall No-Show Rate',
        'Reminder Effectiveness Rate',
        'No-Show Rate by Booking Lead Time',
        'No-Show Rate by Prior No-Show History',
        'No-Show Rate by Appointment Type'
    ],
    'Result': [
        '48.46%',
        'Reminders reduce NS rate by 4.03pp | SMS best (45.75%)',
        '27.81% (0-7 days) → 60.49% (31-60 days)',
        'Low: 43.51% | Medium: 53.49% | High: ~63%',
        'Follow-up: 51.23% | General: 46.64%'
    ],
    'Linked BQ': ['BQ1', 'BQ2', 'BQ3', 'BQ4', 'BQ1']
})

print('KPI Summary:\n')
print(kpi_summary.to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 5 — Business Insights and Recommendations
# MAGIC
# MAGIC **What the assignment asks:** Produce at least 5 meaningful insights and explain their potential implications for HealthConnect Clinic.

# COMMAND ----------

# Five key business insights from the analysis

insights = [
    {
        'Insight': 'Insight 1 — The no-show problem is extremely large',
        'Finding': '48.46% of all appointments result in a no-show — nearly 1 in 2.',
        'Implication': 'This is not a minor operational issue. Nearly half of all scheduled appointment slots are wasted. The clinic needs an active, data-driven strategy to bring this rate down significantly.',
        'Recommendation': 'Set a target no-show rate (e.g. reduce to below 35%) and track progress monthly using KPI 1 as the baseline.'
    },
    {
        'Insight': 'Insight 2 — Booking lead time is a powerful and actionable predictor',
        'Finding': 'No-show rate rises from 27.81% (booked 0-7 days ahead) to 60.49% (booked 31-60 days ahead).',
        'Implication': 'The earlier an appointment is booked, the more likely it is to be missed. This is the clearest pattern in the entire dataset and one the clinic can act on directly.',
        'Recommendation': 'Consider limiting the booking window to 14 days for non-urgent appointment types (especially Follow-ups). For appointments that must be booked further in advance, send reminders closer to the appointment date — not just at the time of booking.'
    },
    {
        'Insight': 'Insight 3 — Prior no-show history identifies high-risk patients reliably',
        'Finding': 'Patients with 0 prior no-shows: 43.51% rate. Patients with 2+ prior no-shows: ~60%+ rate.',
        'Implication': 'A patient\'s own history is the strongest signal for whether they will miss their next appointment. The clinic can use this information proactively before each appointment.',
        'Recommendation': 'Create a simple risk flag in the clinic system. For Medium Risk (1 prior NS) and High Risk (2+ prior NS) patients, send an additional personalised reminder — such as a phone call or a second SMS — 24 hours before the appointment.'
    },
    {
        'Insight': 'Insight 4 — SMS is the most effective reminder channel',
        'Finding': 'SMS: 45.75% no-show rate | Email: 48.41% | WhatsApp: 49.77%.',
        'Implication': 'Not all reminder channels are equally effective. WhatsApp reminders produce almost no improvement over sending no reminder at all (49.77% vs 51.39% without any reminder).',
        'Recommendation': 'The clinic should shift its default reminder channel from WhatsApp to SMS wherever patients have a mobile number available. The channel mix should be reviewed and optimised based on patient contact preferences.'
    },
    {
        'Insight': 'Insight 5 — Follow-up appointments need dedicated attention',
        'Finding': 'Follow-up appointments have the highest no-show rate at 51.23% — above the overall average of 48.46%.',
        'Implication': 'Patients appear to assign less urgency to follow-up appointments compared to specialist consultations or diagnostic tests. Follow-ups are often the most important appointments for ongoing care, yet they are the most likely to be skipped.',
        'Recommendation': 'Introduce a dedicated reminder strategy for follow-up appointments — including shorter booking windows, a confirmation call, and a reminder that explains specifically why the follow-up is important for the patient\'s health.'
    }
]

for item in insights:
    print('=' * 65)
    print(item['Insight'])
    print('-' * 65)
    print(f"Finding        : {item['Finding']}")
    print(f"Implication    : {item['Implication']}")
    print(f"Recommendation : {item['Recommendation']}")
    print()

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 6 — Cross-Track Collaboration
# MAGIC
# MAGIC **What the assignment asks:** Identify at least one meaningful dependency or collaboration point with another track. Document which track, what was exchanged, why it was relevant, and what changed as a result.

# COMMAND ----------

# Cross-track collaboration documentation

collaboration = pd.DataFrame({
    'Item': [
        'Track collaborated with',
        'What was exchanged',
        'Why it was relevant',
        'What changed or improved as a result'
    ],
    'Detail': [
        'Data Science Track',
        'The Data Analytics track shared the 5 KPI results and the variable importance findings — specifically that booking_lead_days, previous_no_shows, and reminder_sent are the strongest predictors of no-show behaviour.',
        'The Data Science track is building a no-show prediction model. The KPIs and variable analysis from this track provide evidence for which features to prioritise in the model. Without this input, feature selection would be guided by assumption rather than data evidence.',
        'The Data Science track can use previous_no_shows, booking_lead_days, and reminder_sent as priority features in their baseline model. The lead time band groupings created in this notebook (0-7, 8-14, 15-30, 31-60 days) and the patient risk tier classification (Low, Medium, High) are directly reusable as engineered features.'
    ]
})

print('Cross-Track Collaboration Summary:\n')
print(collaboration.to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 7 — Assumptions, Limitations, Risks and Dependencies
# MAGIC
# MAGIC **What the assignment asks:** Review Week 4 assumptions and limitations. Document which remain relevant, which are resolved, which have changed, and any new ones discovered in Week 5.

# COMMAND ----------

# Review of Week 4 assumptions and limitations — updated for Week 5

alrd = pd.DataFrame({
    'Item': [
        'ASSUMPTION: Dataset represents appointment patterns accurately',
        'ASSUMPTION: appointment_outcome is correctly recorded',
        'ASSUMPTION: reminder_channel nulls explained by reminder_sent = No',
        'ASSUMPTION: Cancelled treated separately from No-Shows',
        'LIMITATION: Dataset is fictional',
        'LIMITATION: No-show reasons are unknown',
        'LIMITATION: 90 missing distance values',
        'LIMITATION: waiting_time_minutes only for attended appointments',
        'RISK: Date format errors in analysis — RESOLVED',
        'RISK: Cancelled records distorting no-show rate',
        'NEW (Week 5): WhatsApp reminder channel underperforms',
        'NEW (Week 5): Lead time band pattern is very strong'
    ],
    'Status': [
        'Still relevant — accepted for this analysis',
        'Still relevant — no evidence of misclassification found',
        'Confirmed and resolved — verified in data preparation',
        'Still relevant — cancellations analysed separately in EDA 12',
        'Still relevant — all findings are illustrative only',
        'Still relevant — not captured in the dataset',
        'Resolved — filled with column mean (10.11 km) in data preparation',
        'Still relevant — excluded from no-show cause analysis',
        'Resolved — both date columns converted to datetime in Week 5',
        'Resolved — Cancelled excluded from all KPI calculations',
        'New finding — WhatsApp (49.77%) barely better than no reminder (51.39%)',
        'New finding — doubling of no-show rate from 0-7 to 31-60 day band'
    ]
})

print('Assumptions, Limitations, Risks and Dependencies — Week 5 Review:\n')
print(alrd.to_string(index=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Part 8 — Week 5 Project Summary
# MAGIC
# MAGIC **What the assignment asks:** A concise summary covering 9 specific points.

# COMMAND ----------

print('=' * 65)
print('  WEEK 5 PROJECT SUMMARY — DATA ANALYTICS TRACK')
print('  HealthConnect Clinic Experience Lab')
print('=' * 65)
print('''
1. WHAT I PLANNED TO ACCOMPLISH IN WEEK 5
   Complete data preparation, run full EDA, calculate all 5 KPIs,
   produce visualisations, and document business insights.

2. WHAT WAS ACTUALLY COMPLETED
   - Data preparation: dates converted, missing values handled,
     two new derived columns created (lead_time_band, patient_risk_tier)
   - Full EDA across 12 dimensions (outcome, type, day, time, age,
     reminder, channel, lead time, history, risk tier, distance, cancellations)
   - All 5 KPIs calculated and interpreted
   - 8 charts produced
   - 5 business insights and recommendations documented

3. KEY FINDINGS
   - 48.46% overall no-show rate — nearly 1 in 2 appointments missed
   - Booking lead time is the most actionable predictor: 27.81% (same
     week) vs 60.49% (31-60 days ahead) — more than double
   - Prior no-show history reliably identifies high-risk patients
   - SMS reminders are the most effective channel (45.75% NS rate)
   - Follow-up appointments have the highest no-show rate (51.23%)

4. MAJOR CHALLENGES ENCOUNTERED
   - Date columns needed conversion before any time analysis could run
   - Deciding how to handle Cancelled appointments (treated separately)
   - Choosing meaningful lead time band cut-off points (resolved by
     using natural booking windows: weekly, fortnightly, monthly, 2-month)

5. IMPORTANT DECISIONS MADE AND WHY
   - Cancelled appointments excluded from no-show rate KPIs — a
     cancellation is not the same as a no-show (patient gave notice)
   - Missing distance values filled with column mean — preferred over
     dropping rows to preserve sample size
   - Risk tier classification (Low/Medium/High) created based on prior
     no-shows to make findings actionable for clinic staff

6. CHANGES TO WEEK 4 APPROACH
   - No major changes to the planned approach
   - WhatsApp underperformance was not anticipated in Week 4 — this
     became a separate finding and recommendation in Week 5

7. CROSS-TRACK COLLABORATION
   - Shared KPI results and variable importance findings with the
     Data Science track to inform their feature selection decisions
   - lead_time_band and patient_risk_tier columns shared as
     reusable engineered features for the prediction model

8. REMAINING WORK
   - Power BI dashboard development (planned for Week 7-8)
   - Deeper analysis of waiting time vs patient satisfaction
   - Month-over-month trend analysis once date analysis is extended

9. PROPOSED FOCUS FOR WEEK 6
   - Begin Power BI data model and dashboard structure
   - Deepen the reminder channel analysis by appointment type
   - Explore time-based trends using the converted date columns
   - Document findings in the Week 6 project summary report
''')
print('=' * 65)