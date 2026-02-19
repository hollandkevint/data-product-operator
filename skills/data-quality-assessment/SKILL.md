---
name: data-quality-assessment
version: 0.1.0
description: >
  Systematic data quality evaluation covering completeness, accuracy, timeliness,
  consistency, and validity. Use when assessing data pipelines, reviewing data product
  quality, auditing data sources, defining quality SLAs, building data quality monitors,
  or when someone asks "is this data trustworthy?" or "how do we measure data quality?"
user-invocable: false
---

## Five Quality Dimensions

Score each dimension 1-5 when evaluating any data source or pipeline:

**1. Completeness** - What percentage of expected records and fields are present?
- Null rate per column
- Missing record detection (expected vs actual row counts)
- Required field coverage
- Score 5: <1% nulls in required fields. Score 1: >20% missing data.

**2. Accuracy** - Does the data reflect reality?
- Cross-field validation (age matches birth date, totals match line items)
- Reference data matching (codes exist in terminology tables)
- Statistical outlier detection
- Score 5: <0.1% error rate verified against gold standard. Score 1: Known systematic errors unresolved.

**3. Timeliness** - Is the data fresh enough for its intended use?
- Data freshness (time since last update vs SLA)
- Pipeline latency (ingestion to availability)
- Score 5: Real-time or within SLA. Score 1: Data is days/weeks stale.

**4. Consistency** - Does the same fact look the same everywhere?
- Format standardization (dates, codes, identifiers)
- Cross-system agreement (same patient, same record across sources)
- Naming convention compliance
- Score 5: Single source of truth, no conflicting definitions. Score 1: "Revenue" means 3 different things.

**5. Validity** - Does the data conform to business rules?
- Range checks (negative ages, future dates)
- Referential integrity (foreign keys resolve)
- Business rule compliance (diagnosis codes valid for encounter type)
- Score 5: All business rules enforced at ingestion. Score 1: Invalid data flows through unchecked.

## Circuit Breaker Protocol

CRITICAL: If data accuracy drops below threshold during development, pause deployment until the data lead investigates. Quality incidents in production destroy trust that takes months to rebuild.

Implement circuit breakers at every pipeline stage:
1. Source validation (schema, nulls, ranges)
2. Transformation validation (business rules applied correctly)
3. Output validation (against reference data or prior period)
4. If any stage fails, block promotion to the next stage

## Quality vs Eval Distinction

Traditional quality checks: Is data complete? Does it match schema? Are calculations correct?

AI/ML evaluation (evals): Is the model telling the truth? Would a domain expert agree? Is it fair across user segments? Is it helpful or harmful?

Both are required for data products with AI components. Quality gates catch data issues. Evals catch model behavior issues. Neither substitutes for the other.

## Practical Starting Point

Week 1: Audit the last 20 data quality issues. Write simple checks for the top 3 failure modes.
Week 2: Label 100 production examples. Write your first automated quality monitor. Connect to CI/CD.
Weeks 3-4: Monitor 10% of production data flow. Build the detect-fix-measure loop.

NEVER ship a data product without at least completeness and accuracy checks in the pipeline. Everything else can come later. Those two catch 80% of issues.
