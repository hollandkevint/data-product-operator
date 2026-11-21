---
name: agent-eval-regression
description: Loop that replays a golden-question set against an analytics agent after a change, rescores the answers against a pinned answer key, and flags any item the agent used to get right and now gets wrong. Use after a model, prompt, context or schema change, and weekly, or when asked whether an agent got worse. Reads and reports only. It never edits a question, a key or a run.
metadata:
  version: "0.1.0"
---

# Agent eval regression

A total score can stay flat while the agent breaks something that worked. This loop looks at items, not totals. It follows the shared [loop pattern](../../docs/loop-pattern.md) and applies the ship rule from [analytics-agent](../analytics-agent/SKILL.md).

The set has the shape of the [Team Loop grader](../../team-loop/grader/): a question file with a slice and a scoring rule per question, an answer key with a pinned data identifier, and one answers file per run. Copy the shape for your own data. Do not point this loop at the grader's files.

## Maker

1. Keep three things under `eval/`: `questions.json` (an `owner` and the questions, each with `id`, `slice`, `question` and `scoring`), `answer_key.json` (a `data_pin` and one answer per id), and `runs/` with one answers file per run.
2. Scoring rules: `exact` for counts, `tolerance` with an `abs` band for rates, `abstain` for questions the agent must decline. An abstain item has a `null` key. A number on an abstain question is wrong.
3. Replay every question through the changed agent. Save the answers as `eval/runs/<today>.json`: `harness`, `data_pin` and `answers` (a value, or `null` when the agent declines). A query that errors is a missing answer. A missing answer is wrong.
4. Keep the last accepted run as `eval/runs/baseline.json`.
5. Score both runs. An item is regressed when the baseline got it right and the candidate gets it wrong. It is fixed in the other direction.
6. Verdict: `HOLD` when any item regressed, in any slice. Otherwise `PASS`. A gain in another slice does not cancel a regression. That is a trade, and the owner makes it on purpose.
7. Write `loops/agent-eval-regression/<today>.md` with the score table by slice and in total, `Verdict`, `Regressed`, `Fixed` and `Owner` lines, and a `Next step` line on a `HOLD`. Use the demo output as the format.

## Checker

Run `python3 skills/agent-eval-regression/check.py <workspace-dir>` from the library root. It is stdlib only and calls no model. It rescores both runs itself and rejects the report when:

- A slice or total score differs from the rescore.
- The verdict is not `HOLD` when an item regressed, or `PASS` when none did.
- The `Regressed` or `Fixed` list differs from the rescore.
- A run was scored against a different `data_pin` than the key.
- A `HOLD` does not name the set's owner and a decision date after today.
- A run answers an unknown question, or the key and the scoring rules disagree.
- The state file disagrees with the report.

When the checker rejects, fix the report and run it again. Do not hand over a rejected report.

## State

`loops/agent-eval-regression/state.json` holds `last_run`, `next_run`, `baseline` and `candidate` (run files), `verdict` and `regressed`. A `PASS` run becomes the next baseline. A `HOLD` run does not.

## Trigger

On every change to the model, prompt, context, semantic layer or schema. Also weekly, because data and vendor models move without you.

## Demo data

`demo/` is a fake workspace with ten made-up questions in three slices: counts, rates and abstain. The candidate run fixes two items and breaks two, so the total stays at eight of ten and the verdict is `HOLD`. Run `python3 skills/agent-eval-regression/check.py skills/agent-eval-regression/demo`. It passes. The repo check also breaks six things in a copy and confirms the checker rejects each one. See `loop.json`.

## Limits

The checker rescores recorded answers. It does not call the agent, so the maker must record real answers. A good score on thirty questions is still thirty questions. Every wrong answer found in real use becomes a new question. Never delete a failing question to raise the score.
