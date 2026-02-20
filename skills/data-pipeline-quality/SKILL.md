---
name: data-pipeline-quality
version: 0.1.0
description: >
  Automated data quality checks for pipelines. Testing pyramids, dbt test patterns,
  data contracts, circuit breakers, and monitoring. Use when implementing data quality
  checks, writing dbt tests, defining data contracts, setting up pipeline validation,
  building automated quality monitoring, or when someone asks "how do I test my data
  pipeline?" For quality scoring methodology (the 5-dimension rubric), see
  data-quality-assessment.
user-invocable: false
---

## Testing Pyramid for Data

Run tests in this order. Cheapest and fastest first:

| Layer | What It Catches | Examples |
|-------|----------------|---------|
| Schema tests (run first) | Structural failures | Column types, not-null, uniqueness, accepted values |
| Business rule tests | Logic errors | Cross-field validation, referential integrity, range checks |
| Integration tests (run last) | System-level drift | Cross-system reconciliation, end-to-end row counts |

Schema tests are cheap. Run them on every pipeline execution. Business rule tests are mid-tier — run them on staging and production. Integration tests are expensive — run them on a schedule (daily or pre-release).

## dbt Test Patterns

**Generic tests** for reusable checks. Apply across models:

```yaml
models:
  - name: fct_encounters
    columns:
      - name: encounter_id
        tests: [not_null, unique]
      - name: encounter_type
        tests:
          - accepted_values:
              values: ['inpatient', 'outpatient', 'emergency', 'observation']
      - name: patient_id
        tests:
          - relationships:
              to: ref('dim_patient')
              field: patient_id
```

**Custom generic test** for row count tolerance:

```sql
{% test row_count_within_tolerance(model, min_count, max_count) %}
select count(*) as row_count
from {{ model }}
having count(*) < {{ min_count }} or count(*) > {{ max_count }}
{% endtest %}
```

**Singular tests** for business logic specific to one model. Use singular tests when the logic doesn't generalize.

## Data Contracts

A data contract is a product spec for your data. It defines what consumers can depend on.

```yaml
contract:
  name: fct_encounters
  version: 2
  owner: data-platform-team
  sla:
    freshness: "< 4 hours from source update"
    completeness: ">= 99.5% of expected rows"
    accuracy: ">= 99.9% match to source of record"
  schema:
    encounter_id: {type: bigint, nullable: false, unique: true}
    patient_id: {type: bigint, nullable: false}
    encounter_date: {type: date, nullable: false}
```

**Producer responsibilities**: Meet the SLA, notify consumers before breaking changes, version the schema.

**Consumer expectations**: Query only contracted fields, respect the grain, report quality issues.

## Circuit Breakers

Wire quality gates into pipeline stages. When a check fails, block the pipeline and alert.

- **Schema violation**: Block immediately. Bad schema corrupts everything downstream.
- **Row count outside tolerance**: Block and alert. Investigate before proceeding.
- **Freshness SLA breach**: Alert the on-call. Don't block unless downstream consumers can't tolerate stale data.
- **Business rule failure**: Block if the failure rate exceeds threshold (e.g., >1% of rows). Alert if below.

Cross-reference `data-quality-assessment` for the 4-stage quality model (detect → assess → respond → prevent).

CRITICAL: Never auto-heal data quality issues in production. Alert, block, investigate. Auto-fixes mask root causes and erode trust faster than stale data.

## Monitoring

Track quality over time, not just point-in-time pass/fail:

- **Row count trends**: Expected vs actual with tolerance bands. A sudden 40% drop is a pipeline failure. A gradual 5% weekly decline is a source issue.
- **Freshness**: Time since last successful pipeline run. Track P50 and P95, not just "last run."
- **Anomaly detection**: Statistical thresholds beat static thresholds. A metric that normally ranges 1,000-1,200 firing at 950 is more useful than a static "alert below 500" that never triggers.

## Cross-References

For quality scoring methodology (the 5-dimension rubric and maturity model), see `data-quality-assessment`. This skill covers how to automate those checks in your pipeline.
