---
name: review-data-quality
description: Systematic data quality assessment with 5-dimension scoring and improvement recommendations
disable-model-invocation: true
argument-hint: <data source, table name, or pipeline description>
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# Review Data Quality

Assess the quality of a data source, table, or pipeline across 5 dimensions. Produces a scored quality review with specific improvement recommendations.

## Gather Context

If `$ARGUMENTS` provides a data source or table name, use it. Otherwise, ask:

**Question 1:** What data are you assessing? (table name, pipeline name, or data source)

**Question 2:** What is this data used for? (analytics dashboard, ML model input, API response, reporting)

**Question 3:** Do you have access to the data now, or should I work from documentation/schema only?

If the user provides a file path or schema, read it. If they describe the data verbally, work from that description.

## Assess Each Dimension

Score each dimension 1-5 based on evidence. Ask clarifying questions if you can't assess a dimension.

### Scoring Rubric

For each dimension, evaluate and assign a score:

**Completeness** (are expected records and fields present?)
- 5: <1% nulls in required fields, all expected records present
- 4: 1-5% nulls, minor gaps in expected records
- 3: 5-10% nulls, some expected records missing
- 2: 10-20% nulls, significant gaps
- 1: >20% missing data or entire expected segments absent

**Accuracy** (does the data reflect reality?)
- 5: <0.1% error rate, validated against gold standard
- 4: <1% error rate, spot-checked against known values
- 3: Occasional known errors, no systematic validation
- 2: Known systematic errors, manual reconciliation required
- 1: Nobody trusts the numbers

**Timeliness** (is the data fresh enough?)
- 5: Real-time or well within SLA
- 4: Mostly within SLA, occasional delays
- 3: Frequently approaching SLA limits
- 2: Regularly exceeds SLA, consumers compensate with workarounds
- 1: Data is days or weeks stale

**Consistency** (does the same fact look the same everywhere?)
- 5: Single source of truth, no conflicting definitions
- 4: Minor inconsistencies between systems, documented and managed
- 3: Multiple definitions exist, team knows which is "right"
- 2: Conflicting definitions cause confusion, manual reconciliation needed
- 1: "Revenue" means 3 different things to 3 different teams

**Validity** (does the data conform to business rules?)
- 5: All business rules enforced at ingestion, invalid data rejected
- 4: Most rules enforced, some validated downstream
- 3: Key rules checked, but gaps in edge case handling
- 2: Minimal validation, invalid data flows through regularly
- 1: No validation, garbage in garbage out

## Write the Review

Write the assessment to `quality-review-<name>.md` where `<name>` is a kebab-case identifier for the data source.

### Output Structure

```markdown
# Data Quality Review: [Data Source Name]

**Date:** [today]
**Assessed by:** Claude (data-product-operator plugin)
**Overall Score:** [average of 5 dimensions] / 5

## Scorecard

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Completeness | X/5 | [one sentence] |
| Accuracy | X/5 | [one sentence] |
| Timeliness | X/5 | [one sentence] |
| Consistency | X/5 | [one sentence] |
| Validity | X/5 | [one sentence] |

## Detailed Findings

### Completeness
[Evidence and specific observations]

### Accuracy
[Evidence and specific observations]

### Timeliness
[Evidence and specific observations]

### Consistency
[Evidence and specific observations]

### Validity
[Evidence and specific observations]

## Circuit Breaker Recommendations

[Which thresholds should trigger an automatic pause in the pipeline?]

## Improvement Plan

### Quick Wins (this week)
- [Specific action 1]
- [Specific action 2]

### Medium-Term (this month)
- [Specific action 1]
- [Specific action 2]

### Strategic (this quarter)
- [Specific action 1]
- [Specific action 2]
```

ALWAYS provide specific, actionable improvement recommendations. "Improve data quality" is not a recommendation. "Add null check on patient_id at the ingestion layer, rejecting records where patient_id is missing" is.
