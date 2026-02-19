# Schema Patterns Reference

Common dimensional modeling patterns for data products. Reference this when designing or reviewing data models.

## Pattern: Event Fact Table

The most common pattern for data products. One row per event.

```
fact_patient_visit
├── visit_id (PK)
├── patient_id (FK -> dim_patient)
├── provider_id (FK -> dim_provider)
├── facility_id (FK -> dim_facility)
├── visit_date_id (FK -> dim_date)
├── diagnosis_id (FK -> dim_diagnosis)
├── visit_type (inpatient, outpatient, ER, telehealth)
├── length_of_stay_days
├── total_charge_amount
└── claim_paid_amount
```

Grain: one row per visit. If a visit has multiple diagnoses, the primary diagnosis goes here. Secondary diagnoses go in a bridge table.

## Pattern: Periodic Snapshot

Use when you need "state at a point in time" rather than individual events.

```
fact_patient_monthly_snapshot
├── patient_id (FK)
├── snapshot_month_id (FK -> dim_date)
├── active_medication_count
├── open_condition_count
├── days_since_last_visit
├── risk_score
└── care_gap_count
```

Grain: one row per patient per month. Useful for trend analysis and cohort tracking.

## Pattern: Accumulating Snapshot

Use for processes with defined stages (claims processing, referral management).

```
fact_claim_lifecycle
├── claim_id (PK)
├── submitted_date_id (FK)
├── adjudicated_date_id (FK)
├── paid_date_id (FK)
├── denied_date_id (FK, nullable)
├── days_to_adjudicate
├── days_to_pay
├── claim_amount
└── paid_amount
```

Grain: one row per claim, updated as it progresses through stages.

## Pattern: Bridge Table for Many-to-Many

When a fact has multiple values for a dimension (patient with multiple diagnoses per visit):

```
bridge_visit_diagnosis
├── visit_id (FK -> fact_patient_visit)
├── diagnosis_id (FK -> dim_diagnosis)
├── diagnosis_rank (primary=1, secondary=2, ...)
└── present_on_admission_flag
```

NEVER flatten many-to-many into the fact table. Use a bridge.

## Pattern: Junk Dimension

Collect low-cardinality flags and indicators into a single dimension rather than cluttering the fact table:

```
dim_visit_profile
├── visit_profile_id (PK)
├── is_emergency (Y/N)
├── is_readmission (Y/N)
├── is_telehealth (Y/N)
├── insurance_type (commercial, medicare, medicaid, self-pay)
└── discharge_disposition (home, SNF, AMA, expired)
```

## Pattern: Conformed Dimensions

Dimensions shared across multiple fact tables must use identical keys and attributes:

- `dim_patient` used by visit facts, claim facts, and medication facts
- `dim_date` used by every fact table
- `dim_provider` used by visit and claim facts

ALWAYS build conformed dimensions first. They are the backbone of a data product that needs to answer questions across domains.

## Naming Conventions

- Fact tables: `fact_<subject>` or `fact_<subject>_<grain>`
- Dimension tables: `dim_<subject>`
- Bridge tables: `bridge_<left>_<right>`
- Columns: snake_case, descriptive, include unit where ambiguous (`length_of_stay_days`, not `los`)
- Keys: `<table>_id` for surrogate keys, `<source>_<table>_id` for natural keys
- Dates: `<event>_date` for actual dates, `<event>_date_id` for foreign keys to dim_date
