---
name: weekly-metric-review
description: Weekly loop that reads a metric definitions table and a week of values, recomputes each metric's week-over-week move, and flags moves that nobody has explained. Use every week before the team reads its numbers, or when asked which metric moves have no cause. Reads and reports only. It never edits a definition or a value.
metadata:
  version: "0.1.0"
---

# Weekly metric review

A number that moved for no known reason is a risk, not a result. This loop finds those numbers each week. It follows the shared [loop pattern](../../docs/loop-pattern.md).

It reads two files. `metrics/definitions.md` holds one row per metric: name, definition, grain, owner and a move threshold in percent. Write each row with [metrics-definition](../metrics-definition/SKILL.md). `metrics/values.csv` holds `metric,week_start,value`.

## Maker

1. Read `metrics/definitions.md` and `metrics/values.csv`. Take the two newest `week_start` dates. Call them last week and this week.
2. For every defined metric, copy both values exactly and compute the change: `(this - last) / last * 100`, rounded to one decimal. If last week is zero, write `n/a`.
3. A move is a change larger than the metric's threshold, up or down.
4. Pick one status per metric:

| Status | Use when | Evidence |
|---|---|---|
| `steady` | No move | `-` |
| `explained` | A move, and you found the cause | A provenance tag from the Team Loop `_SCHEMA.md` |
| `unexplained` | A move, and no cause found | `Unknown` |

5. Do not invent a cause. Ask the metric's owner, read the load log, check for a definition change. If you find nothing, the status is `unexplained`.
6. An `unexplained` row names the metric's owner and a check date after today in Next step.
7. Write `loops/weekly-metric-review/<today>.md` with the table shown in the demo output, `As of: <today>` and `Weeks compared: <last> and <this>` each on its own line.

## Checker

Run `python3 skills/weekly-metric-review/check.py <workspace-dir>` from the library root. It is stdlib only and calls no model. It rejects the output when:

- A defined metric is missing, or a metric is not in the definitions.
- A value differs from `values.csv`, or a change is not recomputed correctly.
- A move past the threshold is called `steady`, or a quiet metric is called anything else.
- `explained` has no provenance tag, or `unexplained` has evidence.
- `unexplained` does not name the owner from the definitions and a later check date.
- The state file disagrees with the output.

When the checker rejects, fix the output and run it again. Do not hand over a rejected output.

## State

`loops/weekly-metric-review/state.json` holds `last_run`, `next_run`, `reviewed` (every metric covered) and `unexplained` (metrics with no cause yet). An unexplained metric is checked again next run.

## Trigger

Weekly, before the team reads the numbers.

## Demo data

`demo/` is a fake workspace for a made-up product, the Synthetic Readmissions Feed. Run `python3 skills/weekly-metric-review/check.py skills/weekly-metric-review/demo`. It passes. The repo check also breaks five things in a copy and confirms the checker rejects each one. See `loop.json`.

## Limits

The checker proves the arithmetic and the rules. It does not prove a cause is the true cause. A named owner still explains each move.
