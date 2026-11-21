# Engineering-commitment gate

## Purpose

Decide whether the team can commit engineering effort to a bounded first release.

## Required evidence

| Evidence | Acceptance owner | Status |
| --- | --- | --- |
| First-release boundary written in [../context/product.md](../context/product.md) |  |  |
| Data contract complete in [../context/data-contract.md](../context/data-contract.md), gaps stated |  |  |
| Quality thresholds and acceptance owner set in [../context/metrics-and-quality.md](../context/metrics-and-quality.md) |  |  |
| Feasibility accepted by the engineering feasibility owner |  |  |
| Claims and non-claims listed in [../context/commercial-and-access-boundaries.md](../context/commercial-and-access-boundaries.md) |  |  |
| Open decisions have deciders and dates in [../decisions/LOG.md](../decisions/LOG.md) |  |  |

## Pass condition

Every row is `accepted` by its named owner. The data acceptance owner has accepted definitions and limitations in writing.

## Fail action

Return to intake if the problem moved. Return to discovery if the evidence is thin. Never commit on a data contract that fails.

## Gate record

Create a decision record from [../decisions/_SCHEMA.md](../decisions/_SCHEMA.md) with the outcome (`commit`, `revise`, or `return`). Append one row to [../decisions/LOG.md](../decisions/LOG.md) linking the record.
