---
name: analytics-agent
description: >
  Plan, build and test an analytics agent: a delivery surface that answers
  questions in natural language over a data product. Teaches the five concepts
  to settle first and a step-by-step golden-question eval method (question set,
  expected answers, scoring, regression cadence, abstention). Use when a team
  wants chat over its data, is picking a route (warehouse-native, build your
  own, open source or BI-native), or needs to know whether an agent's answers
  can be trusted. Vendor neutral.
metadata:
  version: "0.1.0"
---

# Analytics agent

An analytics agent is a delivery surface. It is not the data product. The data product is the governed data asset, its quality promise and the decision it improves. The agent is one way a consumer reaches it, next to a dashboard or an API.

So the agent inherits the quality of what sits under it. Fix the definitions first. Then pick a route. Then test the agent with questions you wrote yourself.

Route pages (each carries an as-of date, vendor products change fast):
[reference architecture](../../docs/analytics-agents/reference-architecture.md),
[warehouse-native](../../docs/analytics-agents/warehouse-native.md),
[build your own](../../docs/analytics-agents/build-your-own.md),
[open source and BI-native](../../docs/analytics-agents/open-source-and-bi-native.md).

## The five concepts

Settle these before you choose a tool.

1. **Define the metrics before the agent.** If "active patient" has three meanings, the agent picks one at random. A semantic layer, or a set of curated views, is a contract. Free-form text-to-SQL over raw tables is a guess. Use [metrics-definition](../metrics-definition/SKILL.md) to write each definition: grain, time window, owner.
2. **Build the test set first.** Collect 30 to 100 real questions with the correct answer or SQL, owned by a named person. Re-run it on every model, prompt, context or schema change. Public benchmarks do not replace it. See the method below.
3. **Governance travels with the agent.** Row-level security, column masking and identity passthrough must apply to the agent's queries. Read-only access is the minimum, not the whole control.
4. **Context is a maintained product.** Descriptions, synonyms, sample queries and glossaries decay as schemas change. Give the context an owner. Feed failed questions and downvotes back into it.
5. **Wrong answers look right.** Show the SQL and the sources. Ask a clarifying question when a term is ambiguous. Cap result sizes. Log every conversation. Start with one narrow domain and human review, then widen.

## Golden-question eval method

A golden-question set is a fixed list of questions, each with an answer you trust, that you replay against the agent and score. It is a unit-test suite for answers.

### 1. Scope one domain and one consumer

Name the consumer and the decision the agent supports. Write down which tables and metrics are in scope. A set for "everything" tests nothing.

### 2. Collect the questions

Take them from real sources: the consumer's request history, support tickets, the questions an analyst answers every week, the numbers on a board slide. Aim for 30 to 100. Write each as the consumer would type it, not as a clean spec.

Tag every question with a slice, a short label for the area it tests (population, cohorts, utilization). Slices let you see where a change helps and where it hurts. Cover the easy counts and the hard ones: joins, date logic, percentages, definitions with a catch.

### 3. Write the expected answer

For each question, write a SQL file that computes the right answer from the governed data. A person owns it and reviews it. Run it once and store the result in a key file. Pin the data too: a version, a snapshot date or a file hash. If the data moves under the key, every score after that is noise.

Keep the SQL, not only the number. When the data or a definition changes, you recompute the key from the SQL.

### 4. Pick a scoring rule per question

Do not use one blanket rule.

- **Exact** for counts and ids.
- **Tolerance** for rates and averages, with an absolute band you chose on purpose (0.1 percentage points, say).
- **Set match** for lists, if your questions return lists.
- **Judge or rubric** for prose answers. Use it only when no number fits, and have a person spot-check the judge.

Score the answer, not the SQL text. Two different queries can both be right.

### 5. Add abstention questions

Some questions should not get a number. Add them on purpose:

- The term is ambiguous ("revenue" with two definitions).
- The data is not in scope or does not exist.
- The consumer lacks permission to see it.
- The question asks for a causal claim the data cannot support.

The right answer is a clarifying question or a refusal with a reason. Score a confident number on these as wrong. Score a refusal on a question that has an answer as wrong too, and track both rates. An agent that refuses everything is safe and useless.

### 6. Run it

Run every question through the agent and capture the answer and the SQL it used. Score each item pass or fail. A query that errors is a failed item, not a crashed run. Report by slice and in total, never only the total.

### 7. Apply a ship rule to every change

A change to the model, prompt, context or semantic layer ships only if it:

1. beats the current setup on the slice it targets, and
2. breaks nothing the current setup got right, in any slice.

Otherwise the current setup stays. A change that lifts one slice and drops another is a trade. Make it on purpose, with the owner, and log the decision.

### 8. Set the regression cadence

- On every change to the model, prompt, context, semantic layer or schema: full run before release.
- On a schedule (nightly or weekly), because the data and the vendor model move without you.
- Weekly: the owner reads the failures and sorts each into a context fix, a definition fix or a wrong key.
- Every wrong answer found in real use becomes a new question. Never delete a failing question to make the score rise.
- When a metric definition changes on purpose, recompute the key from the SQL and record the decision, so a score drop later is not blamed on the agent.

### 9. Know what public benchmarks are for

Benchmarks such as Spider 2.0 and BIRD compare models on clean public schemas. They do not test your schema, your definitions or your ambiguity. Use them to shortlist models. Use your golden set to decide whether to ship.

## Worked example: the Team Loop grader

The repo already holds a small golden-question set. It lives in [`team-loop/grader/`](../../team-loop/grader/). Read it as the method above in running code.

| Method step | File in `team-loop/grader/` |
| --- | --- |
| Question set, slices, scoring rule per question | `questions.json`: 28 questions over a public synthetic OMOP dataset, in four slices (population, cohorts, utilization, medications). Each has an `exact` or `tolerance` rule. |
| Expected answer as SQL | `key/q01.sql` to `key/q28.sql` |
| Pinned data and stored key | `answer_key.json`: the computed answers plus the dataset URL and SHA-256 |
| The agent's answers | `harnesses/<name>/sql/qNN.sql`: the SQL an agent wrote under that harness |
| Scoring and ship rule | `grade.py`: replays each harness's SQL, scores it, applies the ship rule |
| Result record | `RUNS.md`: score by slice, verdicts, item detail |

A harness here is the context an agent works from: definitions plus instructions. The `base` harness is the default. Specialized harnesses override part of it.

What the committed run shows (`RUNS.md`): `base` gets 20 of 28 right. The `cohorts` harness gets 24 and breaks nothing, so it ships. The `utilization` harness fixes its own slice (7 of 7) but breaks 8 items `base` had right, so it is rejected. That is the ship rule doing its job: a harness that wins its slice and loses elsewhere does not ship.

To run it:

```bash
pip install -r team-loop/grader/requirements.txt
python3 team-loop/grader/data.py                 # downloads and verifies the dataset
python3 team-loop/grader/grade.py key            # recompute the key from key/*.sql
python3 team-loop/grader/grade.py run base       # score one harness
python3 team-loop/grader/grade.py ship cohorts   # ship-rule verdict against base
```

What the grader does not do, so add it for your own set:

- It has no abstention questions. Every question has a numeric answer.
- It scores `exact` and `tolerance` only. It has no set-match or judge scoring.
- It replays committed SQL by default. `grade.py live <harness>` asks an agent to write the SQL again, then replays it.
- It tests SQL answers, not the agent's conversation, its clarifying questions or its permissions.

Do not change the grader to cover these. Copy its shape for your own data and extend your copy.

## Build your own set from this skill

1. Name the consumer and the decision. List the tables and metrics in scope.
2. Write 30 questions in the consumer's words. Tag each with a slice.
3. For each, write the SQL that gives the right answer. Have its owner review it.
4. Run the SQL on pinned data. Store the answers in a key file with the data version.
5. Choose exact, tolerance or set match per question.
6. Add at least five abstention questions: two ambiguous, one out of scope, one no-permission, one causal.
7. Run the agent. Score by slice. Write down the baseline.
8. Set the cadence from step 8 above. Put the owner's name on the set.
9. Grow it to 100 as real failures arrive.

## Rules

- Say "analytics agent" and "delivery surface". Do not call the agent the data product.
- Never ship an agent with no golden set, however good the demo looked.
- Never put real patient or client data in a public test set. Use synthetic or public data.
- Treat vendor claims as claims. Check each against the vendor's current docs and against your own golden set.
