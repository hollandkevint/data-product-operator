---
name: grill-me-data
version: 0.1.0
adapted_from: Matt Pocock, mattpocock/skills, grilling
description: >
  Decision tree exploration for data product plans. Interview relentlessly about
  schema decisions, consumer contracts, quality SLAs, and delivery choices. Use when
  planning a data product, designing a schema, choosing a delivery method, or when
  someone asks "grill me on this data product" or "what am I missing in this design?"
user-invocable: false
---

## Core Instruction

Interview the user relentlessly about their data product plan until you reach a shared understanding. Map the plan as a **design tree**: every decision branches into the decisions that hang off it. The branches below are the data-specific ones.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled, so you can ask it now without guessing at answers you have not heard. Ask the whole frontier in one round. Number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like this:

```
Q1. <short title>: <the question, with choices if there are any>

Recommended: <your answer>

---

Q2. <short title>: ...
```

Word each question so "yes" accepts your recommendation. When the recommendation is obvious, the user says "yes" and you move on.

Each round reshapes the tree. A settled grain unblocks the questions about joins and SCD strategy that depended on it. A question whose answer depends on another open question in the same round waits for a later round.

Finding facts is your job. If a fact sits in a schema, a file or a query, look it up. Do not ask the user for it. Do not block on the lookup: ask the rest of the frontier now, and hold only the questions that depend on the fact. The decisions are the user's. Put each one to them and wait.

The session is done when the frontier is empty: every branch visited, nothing left silently assumed. Do not act on the plan until the user confirms you share one understanding.

To check a plan's words and fields against the data dictionary, use `data-dictionary-grill`. This skill shapes the plan. That one checks it.

## Data Product Decision Branches

Round 1 starts with the root: "What data product are you planning? Who consumes it and what decision does it inform?" Ask both as numbered questions with your recommended answer drawn from what you already know.

Then walk the tree. These are the branches specific to data products. Each bullet is a question for a round, asked once its prerequisites are settled:

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

A typical data product grill session runs 20-40 questions over several rounds. Don't shortcut the schema and quality branches, those are where undiscovered complexity hides.

When the user says "I don't know yet": record it as an open question with a suggested investigation step.

When the user wants to skip a branch: let them, but note it. "You skipped the SCD strategy decision. That will come back when historical data accumulates."

## Output

At the end, produce:

- **Decisions made:** Numbered list with branch labels, keeping the Q numbers from the rounds
- **Open questions:** What still needs answering
- **Schema risks:** Decisions that are hard to reverse once data accumulates
- **Quality gaps:** Where SLAs are undefined or unrealistic
- **Recommended next step:** The single most important thing to resolve first

---

Part of the [Data Product Operator](https://github.com/hollandkevint/data-product-operator) plugin.
Decision architecture skills: [decision-architecture](https://github.com/hollandkevint/decision-architecture)

Source: Matt Pocock, [mattpocock/skills](https://github.com/mattpocock/skills) (grilling), MIT license. Adapted for data products. For checking a plan against the data dictionary, see `data-dictionary-grill`.
