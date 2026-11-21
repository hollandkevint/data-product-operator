---
name: metric-glossary
version: 0.1.0
adapted_from: Matt Pocock, mattpocock/skills, domain-modeling
description: >
  Build and sharpen the team's METRICS glossary: one definition, one owner and one
  grain per metric, with the avoided names listed. Extends metrics-definition: that
  skill sets what a full metric spec holds, this one runs the live session that
  settles the words, challenges fuzzy names, tests edge cases and writes the glossary
  as terms are resolved. Use when metric names overlap, two reports use one name for
  two numbers, or someone asks "what exactly do we mean by active?" Reads GLOSSARY.md
  for the repo terms.
user-invocable: false
---

## What this is for

`metrics-definition` tells you what a metric spec must hold: SQL logic, time window, cadence. This skill does the earlier, human step. It gets the team to agree on the word, the one definition, the one owner and the grain, and it writes that down as it goes.

Run `metrics-definition` after this to fill in the SQL and the cadence for each term you settled. Do not repeat its template here.

## Before you start

1. Read `GLOSSARY.md` at the repo root. Its terms are fixed. A metric term must not reuse a glossary term for a different thing, and must not use a word that glossary lists under `_Avoid_`. Say so at once: "GLOSSARY.md uses 'consumer' for the person whose decision a data product improves. You mean the account here. Which word do you want?"
2. Look for `METRICS.md` at the repo root. If it exists, read it and extend it. If not, create it when the first term is settled, not before.
3. Ask what decision the metric informs and who the named consumer is. If there is none, stop and run `data-consumer-discovery`.

## During the session

### Challenge against the glossary

When a name conflicts with `METRICS.md` or `GLOSSARY.md`, call it out right away. "METRICS.md defines 'active patient' as one visit in 12 months. You just described 3 months. Which is it?"

### Sharpen fuzzy names

When a name is vague or overloaded, propose one precise term. "You say 'revenue'. Do you mean billed amount, paid amount, or recognized revenue? Those are three metrics with three owners."

Name test: could two people read this name and compute two different numbers? If yes, it is fuzzy. Fix the name or split it.

### One definition, one owner, one grain

Every term gets exactly one of each:

- **Definition**: one or two sentences a non-technical person can read. What it is, not how it is built.
- **Owner**: one named role or person who decides changes. A team is not an owner.
- **Grain**: what one row or one count is. "One patient per calendar month" is a grain. "Monthly" alone is not.

If two people claim to own a metric, ask who is paged when the number is wrong. If two definitions seem right, you have two metrics. Give each its own name.

### Run edge-case scenarios

Invent concrete cases that probe the boundary and force a ruling. Use made-up or public-dataset data (OMOP, synthetic data). Examples:

- A patient is seen on the last day of the window. In or out?
- A record is corrected after the month closes. Does last month's number change?
- One person has two ids. Count once or twice?
- A claim is paid, then reversed. Is it in "paid amount"?
- A test account makes ten visits. Excluded where, and by whose rule?

Ask one scenario at a time. Record each ruling under the term as a one-line edge case.

### Cross-reference with the query

When the user says how the number is computed, check the SQL or the report if it is available. If it contradicts the definition, surface it: "Your query counts rows, but you defined the metric per patient. Which is right?"

### Write METRICS.md inline

When a term is settled, write it to `METRICS.md` that moment. Do not batch. Use this format:

```md
# Metrics

{One or two sentences: which data product or team these metrics serve.}

## Language

**Active patient**:
A patient with at least one completed visit in the 12 months before the report date.
Owner: Clinical analytics lead
Grain: one patient per report date
Edge cases: a visit on the report date counts. A cancelled visit does not.
_Avoid_: Active member, engaged patient, MAU
```

Rules:

- Be opinionated. Pick the best name and list the others under `_Avoid_`.
- Keep the definition to one or two sentences. No SQL, no table names, no tool names. Those belong in the metric spec from `metrics-definition`.
- Only include terms this team computes or reports. General words do not belong.
- Group terms under subheadings when clusters appear: for example, volume, quality, cost.
- `METRICS.md` is a glossary and nothing else. It is not a spec or a scratch pad.

### Offer a decision record sparingly

When a definition change is hard to reverse, surprising without context, and the result of a real trade-off, offer to record it in the team's decision log (see [Team Loop](../team-loop/SKILL.md)). Example: moving "active patient" from 12 months to 6 changes every trend line. If one of the three is missing, skip it.

## Done

The session is done when every metric the user named has a definition, an owner, a grain and its avoided names in `METRICS.md`, and every scenario has a ruling. List the terms still open, each with the question that would close it.

Source: Matt Pocock, [mattpocock/skills](https://github.com/mattpocock/skills) (domain-modeling), MIT license. Adapted for metric glossaries.
