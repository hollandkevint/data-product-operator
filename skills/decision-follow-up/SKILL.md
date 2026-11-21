---
name: decision-follow-up
description: Weekly loop that reads a Team Loop decision log, finds decisions whose review date has passed, and checks each against what actually happened. Use after the weekly decision packet, or when asked which decisions are overdue for an outcome check. Reads and reports only. It never edits a decision record or the log.
metadata:
  version: "0.1.0"
---

# Decision follow-up

A decision without a follow-up is a guess nobody checks. This loop closes that gap. It follows the shared [loop pattern](../../docs/loop-pattern.md).

It reads the [Team Loop](../team-loop/SKILL.md) decision log: `decisions/LOG.md` and the records under `decisions/`, in the format set by `decisions/_SCHEMA.md`.

## Maker

1. Read `decisions/LOG.md`. Keep rows with status `decided` whose review date is on or before today.
2. Skip `pending` and `superseded` rows. A superseded decision has a newer record that owns the question.
3. Open each kept record. Copy its decision text, review date and `## What would reverse this` condition exactly.
4. Look for outcome evidence for that condition. Use what the team already has: metrics, access logs, consumer notes. Do not invent evidence. Record it as a provenance tag from `_SCHEMA.md`, or `Unknown`.
5. Pick one disposition per decision:

| Disposition | Use when | Evidence |
|---|---|---|
| `keep` | The reverse condition did not happen | Required |
| `reverse` | The reverse condition happened | Required |
| `extend` | Too early to tell, with a reason | Any |
| `no-outcome` | Nobody has looked, or the evidence is missing | `Unknown` is fine |

6. Write `loops/decision-follow-up/<today>.md` with the table shown in the demo output, and `As of: <today>` on its own line. A `reverse` row says who writes the superseding record. The loop does not write it.

## Checker

Run `python3 skills/decision-follow-up/check.py <workspace-dir>` from the library root, or point it at your Team Loop workspace. It is stdlib only and calls no model. It rejects the output when:

- A due decision is missing, a not-due decision appears, or a decision is not in the log.
- The decision text, review date or reverse condition differs from the record.
- Evidence is not a valid provenance tag or `Unknown`.
- `keep` or `reverse` has no evidence.
- `extend` or `no-outcome` has no next review date after today.
- The state file disagrees with the output.

When the checker rejects, fix the output and run it again. Do not hand over a rejected output.

## State

`loops/decision-follow-up/state.json` holds `last_run`, `next_run`, `followed_up` (record filenames covered this run) and `open` (records marked `extend` or `no-outcome`). An open record is due again at its next review date.

## Trigger

Weekly, right after the decision packet. Also run it by hand before a strategy review.

## Demo data

`demo/` is a fake Team Loop workspace for a made-up product, the Synthetic Readmissions Feed. Run `python3 skills/decision-follow-up/check.py skills/decision-follow-up/demo`. It passes. The repo check also breaks four things in a copy and confirms the checker rejects each one. See `loop.json`.

## Limits

This loop reports. It does not change a decision, the log or any data. A named decider still decides what happens next.
