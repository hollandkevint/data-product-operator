---
name: strategy-review
description: Quarterly loop that reads the Team Loop decision log, groups the quarter's decisions by outcome, and asks the operator one question per decision, keep, change or stop. Use at the end of each quarter, or when asked what the team should keep, change or stop. The operator owns the calls. The loop prepares the review and never decides.
metadata:
  version: "0.1.0"
---

# Strategy review

Strategy is the sum of the decisions a team made and kept. Once a quarter, look at all of them together. This loop sets up that review. It follows the shared [loop pattern](../../docs/loop-pattern.md).

Its input is the [Team Loop](../team-loop/SKILL.md) decision log, `decisions/LOG.md`. It also reads the newest output of [decision-follow-up](../decision-follow-up/SKILL.md) for what happened after each decision.

The operator owns this loop. The operator is the named person who runs the data product, and must appear as a decider in the log. The maker prepares. The operator makes every call.

## Maker

1. Pick the quarter that just ended, for example `2026-Q3`. Read `decisions/LOG.md`. Keep rows dated in that quarter whose status is `decided` or `superseded`. Skip `pending`.
2. Give each kept decision one outcome:

| Outcome | Source |
|---|---|
| `keep`, `reverse`, `extend`, `no-outcome` | The disposition in the newest decision follow-up output |
| `superseded` | The log status. A newer record owns the question. |
| `not-reviewed` | A decided record that follow-up has not covered |

3. Copy the decision text and decider from the log exactly. Do not invent an outcome. If follow-up has not run, the outcome is `not-reviewed`.
4. Write `loops/strategy-review/<today>.md`. Put `As of`, `Quarter`, `Operator` and `Input: decisions/LOG.md` each on its own line. Add a `Groups` line with the count for every outcome. List rows grouped in this order: keep, reverse, extend, no-outcome, superseded, not-reviewed.
5. Every row asks `Keep, change or stop?` and starts with the call `pending`. A `superseded` row gets `n/a` and a note that names the record that replaced it.
6. The operator fills the calls. Rules for the operator's calls: `change` and `stop` need a note that says what changes. `keep` against a `reverse` outcome needs a note that says why. A `change` or `stop` becomes a new decision record by the Team Loop route. This loop does not write it.

## Checker

Run `python3 skills/strategy-review/check.py <workspace-dir>` from the library root. It is stdlib only and calls no model. It rejects the review when:

- The input line does not name `decisions/LOG.md`.
- A decided or superseded decision from the quarter is missing, or a row is not in the log for that quarter.
- Decision text, decider or outcome differs from the log and the follow-up output.
- The groups line, or the row order, does not match the rows.
- The operator is not a decider in the log, or differs from the state file.
- A call is not `pending`, `keep`, `change`, `stop` or `n/a`, or a required note is empty.
- The quarter has not ended, or `next_run` is under 60 days away.
- The state file disagrees with the review.

When the checker rejects, fix the review and run it again. Do not hand over a rejected review.

## State

`loops/strategy-review/state.json` holds `last_run`, `next_run`, `quarter`, `operator`, `reviewed` (records covered) and `open` (records whose call is still `pending`). An open record carries into the next review.

## Trigger

Quarterly, in the first month after a quarter ends. The next run is at least 60 days out.

## Demo data

`demo/` is a fake Team Loop workspace for a made-up product, the Synthetic Readmissions Feed. It holds the decision log, its records and one decision follow-up output. Run `python3 skills/strategy-review/check.py skills/strategy-review/demo`. It passes. The repo check also breaks seven things in a copy and confirms the checker rejects each one. See `loop.json`.

## Limits

The checker proves the review is complete and follows the log. It does not tell you which decisions matter most. A named operator still decides, and a decision stays in force until a new record replaces it.
