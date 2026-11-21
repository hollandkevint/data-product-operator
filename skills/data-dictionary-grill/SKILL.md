---
name: data-dictionary-grill
version: 0.1.0
adapted_from: Matt Pocock, mattpocock/skills, grill-with-docs
description: >
  Grill a data plan against the team's data dictionary and METRICS glossary, and call
  out every conflict. Differs from grill-me-data: that skill walks the decision tree of
  a new data product (consumer, schema, quality, delivery); this one checks a plan's
  words and fields against what the data already means. Use when a PRD, schema change,
  dashboard spec or pipeline plan names fields or metrics, or when someone asks "does
  this match our dictionary?"
user-invocable: false
---

## What this is for

Plans drift from the dictionary one word at a time. A spec says "admission" and the dictionary says "encounter". A dashboard says "active" and the glossary says 12 months. This skill finds those gaps before they ship.

It works against documents the team already has: a data dictionary, `METRICS.md` from `metric-glossary`, and `GLOSSARY.md` at the repo root. It does not replace `grill-me-data`. Run `grill-me-data` to shape the plan. Run this to check it.

## Before you start

1. Ask for the plan, and for the data dictionary or schema doc. Read both. If the user has no dictionary, say that is the first finding, then check against `METRICS.md` and `GLOSSARY.md` alone.
2. Read `GLOSSARY.md` and `METRICS.md` if present. Their terms are fixed.
3. Pull every field name, metric name and domain term out of the plan into a list. This is the checklist for the session.

Finding facts is your job. If a fact is in the dictionary, a file or a query, look it up. Do not ask the user for it.

## Run it in rounds

Map the plan as a tree: each term or field branches into the decisions that depend on it. The frontier is every item whose prerequisites are settled. Ask the whole frontier in one round, number each question, and give your recommended answer. Then wait.

Format a round like this:

```
Q1. <short title>: <the conflict or gap, with the dictionary line and the plan line side by side>

Recommended: <your answer>

---

Q2. <short title>: ...
```

Word each question so "yes" accepts your recommendation. Each answer reshapes the tree: a settled grain unblocks the questions about joins that depend on it. A question that depends on an open question waits for a later round.

## What to check

For each item on the checklist, look for:

- **Name conflict**: the plan uses a word the dictionary or glossary defines differently, or lists under `_Avoid_`. Quote both. "The plan says 'admission'. The dictionary defines 'encounter' and lists 'admission' as avoided."
- **Two names, one thing**: the plan and the dictionary name the same concept differently. Pick one.
- **One name, two things**: the plan uses one word for two concepts. Ask which, or split it.
- **Grain mismatch**: the plan counts at a different grain than the dictionary row. "The dictionary says one row per claim line. The plan counts rows as claims."
- **Missing entry**: the plan names a field or metric the dictionary lacks. Ask who owns it and settle the definition, or hand it to `metric-glossary`.
- **Owner gap**: a term has no owner, or two.
- **Edge case**: invent one scenario that tests the boundary and ask for a ruling. Use made-up or public-dataset data (OMOP, synthetic data). Example: "A claim is paid, then reversed after month end. Is it in this month's paid amount?"

## Update the docs as you go

When a term is settled, update `METRICS.md` or the dictionary at once. Use `metric-glossary` for metric entries. Do not batch. Keep the glossary free of SQL, table names and scratch notes.

Offer a decision record only when the call is hard to reverse, surprising without context, and the result of a real trade-off. Use the team's decision log (see [Team Loop](../team-loop/SKILL.md)).

## Output

When the frontier is empty, report:

- **Conflicts**: each one, with the plan line, the dictionary line and the ruling.
- **Gaps**: terms the dictionary lacks, with owner and next step.
- **Changes made**: docs you updated.
- **Open**: what still needs an answer, and who can give it.

Do not act on the plan until the user confirms you share one understanding.

Source: Matt Pocock, [mattpocock/skills](https://github.com/mattpocock/skills) (grill-with-docs and grilling), MIT license. Adapted for data dictionaries.
