# Intake gate

## Purpose

Decide whether a product problem is worth a team's time before anyone writes requirements.

## Required evidence

| Evidence | Acceptance owner | Status |
| --- | --- | --- |
| Named first user and the decision they make today |  |  |
| Named buyer |  |  |
| Current alternative and its cost |  |  |
| Why now: a dated commercial or clinical trigger |  |  |
| Highest-risk assumption named, with the test that would resolve it |  |  |
| Data sources exist and an owner can describe grain and coverage |  |  |

## Pass condition

Every row has an acceptance owner and a status of `accepted`. Any `Unknown` row has a named owner and a date.

## Fail action

Stop, or reframe the problem and re-run the gate. Do not write requirements past a failed intake.

## Gate record

Create a decision record from [../decisions/_SCHEMA.md](../decisions/_SCHEMA.md) with the outcome (`proceed`, `reframe`, or `stop`). Append one row to [../decisions/LOG.md](../decisions/LOG.md) linking the record.
