---
name: data-product-validation
version: 0.1.0
description: >
  Score whether a data product idea is worth building before committing resources.
  Validation scorecard, experiment design, and go/kill decisions. Use when evaluating
  feasibility, making go/no-go decisions, validating demand, sizing bets, or when
  someone asks "is this worth building?" or "should we invest in this?"
user-invocable: false
---

## Validation Scorecard

Score each dimension 1-5. Multiply all five for a composite score (max 3,125).

### 1. Demand Frequency

How often do consumers need this answer?

| Score | Frequency | Example |
|-------|-----------|---------|
| 5 | Daily or real-time | ICU readmission risk scores |
| 4 | Weekly | Regional performance reports |
| 3 | Monthly | Quarterly business reviews |
| 2 | Quarterly | Annual planning data |
| 1 | Rarely or once | Ad-hoc executive request |

### 2. Decision Impact

What happens when consumers don't have this data?

| Score | Impact | Example |
|-------|--------|---------|
| 5 | Critical decision blocked | Can't discharge patients without risk assessment |
| 4 | Significant delay or cost | Team spends 20+ hours/week on manual workaround |
| 3 | Moderate inconvenience | Report takes 3 hours instead of 5 minutes |
| 2 | Minor friction | Slightly slower process, acceptable workaround exists |
| 1 | Mild inconvenience | Nice to have, nobody changes behavior without it |

### 3. Workaround Effort

What are consumers doing today instead?

| Score | Effort | Example |
|-------|--------|---------|
| 5 | Custom tooling built | Analyst maintains a 47-tab Excel model updated daily |
| 4 | Significant manual process | 3 people spend 2 days/week compiling reports |
| 3 | Partial automation | Script exists but breaks frequently, needs babysitting |
| 2 | Simple workaround | Quick Excel export, takes 30 minutes |
| 1 | Haven't tried | Nobody has attempted to solve this yet |

### 4. Data Feasibility

Can we actually build this with available data?

| Score | Feasibility | Example |
|-------|-------------|---------|
| 5 | Data exists, quality verified | Source audited, passes `data-quality-assessment` checks |
| 4 | Data exists, quality unknown | Source available but no quality baseline established |
| 3 | Data exists, known issues | Source has gaps or accuracy problems that need fixing first |
| 2 | Data partially exists | Need to combine 3+ sources, some missing |
| 1 | Data doesn't exist | Would need new data collection or acquisition |

Cross-reference `data-quality-assessment` for the 5-dimension scoring. A Data Feasibility score of 1 kills the idea regardless of other scores.

### 5. Schema Risk

How locked-in are consumers once we ship?

| Score | Risk | Example |
|-------|------|---------|
| 5 | Easily re-modeled | Internal API, few consumers, versioning supported |
| 4 | Moderate coupling | Dashboard consumed by 5-10 users, change is disruptive but manageable |
| 3 | Significant coupling | 20+ downstream queries depend on current schema |
| 2 | High coupling | External consumers or contractual SLAs on schema shape |
| 1 | Breaking change impossible | Regulated output, schema changes require compliance review |

## Thresholds

| Composite Score | Decision | Action |
|----------------|----------|--------|
| 250+ | **Build** | Shape a pitch, allocate a cycle |
| 100-249 | **Investigate** | Run a 1-week experiment to de-risk the lowest-scoring dimension |
| <100 | **Kill** | Document why and move on. Revisit only if new evidence surfaces |

CRITICAL: A Data Feasibility score of 1 kills the idea at any composite score. You can't build a data product without data.

## Experiment Types

When the scorecard says "Investigate," pick the cheapest experiment that addresses the weakest dimension:

**Sample Query (1 day):** Write the SQL. Run it against production data. Does the result answer the consumer's question? Tests Data Feasibility and reveals quality issues fast. If the query returns garbage, kill early.

**Manual Pipeline (1 week):** Build the transformation by hand for one consumer. Deliver a spreadsheet or flat file. Measure: did they use it? Did it change a decision? Tests Demand Frequency and Decision Impact with real behavior.

**Schema Prototype (2-3 weeks):** Build a minimal star schema with one fact table and 2-3 dimensions. Load a month of data. Let 2-3 consumers query it. Tests Schema Risk and reveals modeling assumptions before they calcify.

## Type 1 vs Type 2 Decisions

Not all data product decisions are equal:

**Type 1 (irreversible):** Schema design decisions. Data source commitments. Terminology mappings published to external consumers. SCD strategies once historical data accumulates. These deserve full validation and the scorecard process.

**Type 2 (reversible):** Adding a metric to an existing dashboard. New filters on an existing report. Feature additions to established products. These don't need a scorecard. Just build and measure.

Discovery budget should match decision type. Spend 2 weeks validating a Type 1. Spend 2 hours on a Type 2.
