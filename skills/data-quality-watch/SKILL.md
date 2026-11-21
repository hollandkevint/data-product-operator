---
name: data-quality-watch
description: Daily loop that checks each declared table for freshness, volume, null rates and schema drift against written expectations, and reports every check as pass or fail with an owner for each failure. Use after the morning load, or when asked whether the data can be trusted today. Reads and reports only. It never edits an expectation or a table.
metadata:
  version: "0.1.0"
---

# Data quality watch

A data product promises quality. This loop checks the promise every day. It follows the shared [loop pattern](../../docs/loop-pattern.md). Write the expectations with [data-quality-assessment](../data-quality-assessment/SKILL.md) and [data-pipeline-quality](../data-pipeline-quality/SKILL.md).

It reads two files. `quality/expectations.json` declares, per table: `owner`, `max_age_hours`, `min_rows`, `max_rows`, `max_null_pct` per column and `columns` with their types. `quality/observed.json` holds what a profile or query found: `observed_at`, and per table `loaded_at`, `rows`, `null_pct` and `columns`. Getting those observed values is outside this loop. Use [duckdb-data-profiling](../duckdb-data-profiling/SKILL.md) or your own query.

## Maker

1. Read both files. For each declared table, make these checks:

| Check | Pass when | Expected text | Observed text |
|---|---|---|---|
| `freshness` | `observed_at - loaded_at` is at most `max_age_hours` | `<= 26 h` | `5.0 h` |
| `volume` | `rows` is between `min_rows` and `max_rows` | `900000 to 1100000 rows` | `1002345 rows` |
| `nulls:<column>` | `null_pct` is at most the column limit | `<= 1.0%` | `0.4%` |
| `schema` | The columns and types match the declaration | `patient_id:int, payer:text` | `matches`, or what differs: `missing x`, `new y`, `z int to text` |

2. Write one row per check, in the table shown in the demo output. Copy the expected and observed text in exactly this format.
3. A failing row names the table's owner and a date after today in Next step. A passing row has `-`.
4. Write `loops/data-quality-watch/<today>.md` with `As of: <today>` on its own line.
5. Do not change an expectation to make a failure pass. A new column or a new limit is a decision for the owner.

## Checker

Run `python3 skills/data-quality-watch/check.py <workspace-dir>` from the library root. It is stdlib only and calls no model. It recomputes every check from the two JSON files and rejects the report when:

- A declared check is missing, or a check was never declared.
- Expected or observed text differs from what the data gives.
- A result says `pass` when the numbers fail, or the reverse.
- A failing row has no owner from the expectations or no later date.
- `observed_at` is not on the run date, or a table has no observed data.
- The state file disagrees with the report.

When the checker rejects, fix the report and run it again. Do not hand over a rejected report.

## State

`loops/data-quality-watch/state.json` holds `last_run`, `next_run`, `checked` (tables covered) and `failing` (`table:check` for each failed check). A failing check stays on the list until a later run passes it.

## Trigger

Daily, after the morning load.

## Demo data

`demo/` is a fake workspace with two made-up tables for the Synthetic Readmissions Feed. Run `python3 skills/data-quality-watch/check.py skills/data-quality-watch/demo`. It passes, and it holds three failures on purpose. The repo check also breaks five things in a copy and confirms the checker rejects each one. See `loop.json`.

## Limits

The checker proves the report matches the numbers. It does not prove the numbers are true, and four checks do not cover every way data goes wrong. A named owner still decides what a failure means.
