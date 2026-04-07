---
name: grill-me-data
version: 0.1.0
description: >
  Decision tree exploration for data product plans. Interview relentlessly about
  schema decisions, consumer contracts, quality SLAs, and delivery choices. Use when
  planning a data product, designing a schema, choosing a delivery method, or when
  someone asks "grill me on this data product" or "what am I missing in this design?"
user-invocable: false
---

## Core Instruction

Interview the user relentlessly about every aspect of their data product plan until you reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one by one.

For each question, provide your recommended answer based on context. When the recommendation is obvious, the user just says "yes" and you move on.

## Data Product Decision Branches

Start with: "What data product are you planning? Who consumes it and what decision does it inform?"

Then walk the tree. These are the branches specific to data products:

### Consumer Branch
- Who are the primary consumers? (Explorers, Reporters, Decision-makers, Builders)
- How do they access this today? (manual query, existing dashboard, Excel export, nothing)
- What format do they need? (dashboard, API, flat file, embedded metric)
- What's their technical sophistication? (SQL-fluent, BI-tool-only, non-technical)
- What decision does this inform? If they can't name one, stop and run `data-consumer-discovery`.

### Schema Branch
- What's the grain? (one row = what?)
- Fact or dimension? (measurable events vs. descriptive attributes)
- SCD strategy needed? (Type 1 overwrite, Type 2 history, Type 3 limited history)
- Conformed dimensions available? (shared across products, or isolated)
- Denormalization tradeoffs? (query performance vs. maintenance complexity)

Cross-reference `data-model-design` for schema pattern details.

### Quality Branch
- What accuracy SLA does this need? (99.9% for clinical, 95% for internal reporting)
- Freshness requirement? (real-time, hourly, daily, weekly)
- What happens when data is late or wrong? (circuit breaker, fallback, manual override)
- Who gets paged when quality drops?

Cross-reference `data-quality-assessment` for the 5-dimension scoring model.

### Delivery Branch
- Push or pull? (scheduled delivery vs. on-demand query)
- What system of record does this feed? (BI tool, application, API, spreadsheet)
- Schema evolution strategy? (breaking changes, versioning, consumer migration)
- Consumer contract defined? (SLA, format, access method per consumer type)

Cross-reference `data-pipeline-quality` for delivery patterns.

### Validation Branch
- Has demand been validated? (real consumer requests vs. assumed need)
- What's the validation score? Cross-reference `data-product-validation` scorecard.
- Type 1 or Type 2 decision? (irreversible schema commitment vs. reversible feature add)

## Session Dynamics

A typical data product grill session runs 20-40 questions over 30 minutes. Don't shortcut the schema and quality branches — those are where undiscovered complexity hides.

When the user says "I don't know yet": record it as an open question with a suggested investigation step.

When the user wants to skip a branch: let them, but note it. "You skipped the SCD strategy decision. That will come back when historical data accumulates."

## Output

At the end, produce:

- **Decisions made:** Numbered list with branch labels
- **Open questions:** What still needs answering
- **Schema risks:** Decisions that are hard to reverse once data accumulates
- **Quality gaps:** Where SLAs are undefined or unrealistic
- **Recommended next step:** The single most important thing to resolve first

Based on Matt Pocock's grill-me skill pattern, adapted for data products.

---

Part of the [Data Product Operator](https://github.com/hollandkevint/data-product-operator) plugin.
Decision architecture skills: [decision-architecture](https://github.com/hollandkevint/decision-architecture)
