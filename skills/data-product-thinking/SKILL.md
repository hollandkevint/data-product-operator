---
name: data-product-thinking
version: 0.1.0
description: >
  First-principles reasoning for data product decisions. Frames problems as data
  products, not dashboards or pipelines. Use when evaluating data product strategy,
  making build-vs-buy decisions, scoping data product features, assessing product-market
  fit for data offerings, or when someone asks "should we build this data product?"
user-invocable: false
---

## Core Principles

Apply these when making data product decisions:

1. **Trust over features.** A single data quality incident can destroy months of trust. One bad number in a board deck costs more than a delayed feature. Protect data accuracy before adding capabilities.

2. **Outcomes over outputs.** "47 dashboards and no answers" is the failure mode. Define what decisions the data product enables before defining what data it needs. Measure decisions enabled, revenue generated, time saved. Not models deployed or dashboards built.

3. **Teams over tools.** Technology is 20% of data product success. The other 80% is people, process, and product thinking. Don't lead with tool selection.

4. **Uncertainty over certainty.** Fix the time, vary the scope. Six-week cycles with variable scope beat two-week sprints with fixed scope for data products, where discovery is continuous.

5. **Ownership over handoffs.** Every handoff loses context. The team that discovers the problem should own it through delivery.

## Five-Risk Evaluation Model

Before committing to any data product bet, evaluate all five risks:

1. **Value risk** - Will customers actually use this? (Validate with 3+ customer data points)
2. **Usability risk** - Can they figure it out without training?
3. **Feasibility risk** - Can we build it with available data and infrastructure?
4. **Business viability risk** - Does it work for the business model?
5. **Ethical data risk** - Can we build it without bias, privacy violations, or unintended harm? (This is the 5th risk unique to data products. See `ethical-risk-assessment` for the full framework.)

CRITICAL: Never skip ethical data risk. A technically correct model that produces biased outcomes is worse than no model.

## Decision Framing

ALWAYS start with the problem, not the data. "Payers need to reduce readmissions" before "we have claims data."

ALWAYS define success metrics before data requirements. Build an outcome metric tree:
- Business outcome (reduce readmissions 10%)
- Product outcome (clinical decisions 3x faster)
- Feature outcome (risk scores updated real-time)
- Leading indicator (query latency under 1 second)

NEVER confuse data availability with product viability. Having the data doesn't mean there's a product.

AVOID "we could also..." scope expansion. If it doesn't serve the defined outcome, it waits.

## Upstream Discovery

Before applying the Five-Risk Evaluation, validate that the problem is worth solving. Use `data-consumer-discovery` to gather evidence from actual consumers. Use `data-product-validation` to score demand, feasibility, and schema risk. Use `research-synthesis-data` to convert raw findings into ranked problems with traceable evidence chains.

The sequence: discover consumers → synthesize findings → validate demand → then scope and evaluate risks here.

## Build vs Buy

Ask: "How good would this solution have to be if we were charging users to use it?" If the answer requires custom work, build. If an off-the-shelf tool meets 80% of the bar, buy and customize.
