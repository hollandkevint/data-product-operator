# Controlled-launch gate

## Purpose

Decide go, revise, or stop for a first cohort.

## Required evidence

| Evidence | Acceptance owner | Status |
| --- | --- | --- |
| Test evidence against the thresholds in [../context/metrics-and-quality.md](../context/metrics-and-quality.md) |  |  |
| Approved limitations text for customer-facing material |  |  |
| Rollout cohort named and sized |  |  |
| Stop conditions and the person who can call them |  |  |
| Rollback or containment path |  |  |
| Support owner and review date |  |  |

## Pass condition

Every row is `accepted`. The final release decider has signed the decision record.

## Fail action

`revise` sends the packet back with the failing rows named. `stop` records why and what would reopen it.

## Gate record

Create a decision record from [../decisions/_SCHEMA.md](../decisions/_SCHEMA.md) with the outcome (`go`, `revise`, or `stop`), the cohort, the stop conditions, and the review date. Append one row to [../decisions/LOG.md](../decisions/LOG.md) linking the record.
