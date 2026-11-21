# Interview

Ask in batches of three or four questions. Short and direct. In migration mode, skip what the sources already answer.

## Batch A — Product and decision
1. Product line, one-line description, accountable owner.
2. The first user, and the decision they make today that this product should improve.
3. The buyer, if different from the user.
4. The current alternative and what it costs.

## Batch B — Owners and decision rights
1. Executive sponsor, final release decider, working owner.
2. Data acceptance owner and engineering feasibility owner.
3. The weekly cadence: packet day, session day, review window.
4. Who resolves a scope or authority conflict.

## Batch C — Data and contract
1. Data sources, and who owns each.
2. Grain, coverage, freshness, and the known gaps.
3. The one outcome metric, with grain and window.
4. Quality thresholds the release must meet, and who accepts them.

## Batch D — Access, claims, and boundaries
1. What the team can claim now, and what it cannot claim yet.
2. Licensing, privacy, and naming rules (partners that stay unnamed, regulated data).
3. The delivery surface and what it may not do.
4. Anything off-limits beyond the defaults in `CLAUDE.md`.

## After the interview

Summarize back in six to ten bullets. Surface contradictions. Confirm before scaffolding.

## What the answers feed

| Batch | Question | Populates |
| --- | --- | --- |
| A | 1 | `context/product.md` § Product line and owner; `README.md` |
| A | 2, 3, 4 | `context/consumers.md` |
| B | 1, 2 | `context/team-and-decision-rights.md` § Roles |
| B | 3 | `context/team-and-decision-rights.md` § Cadence |
| B | 4 | `context/team-and-decision-rights.md` § Escalation path |
| C | 1, 2 | `context/data-contract.md` |
| C | 3, 4 | `context/metrics-and-quality.md` |
| D | 1 | `context/commercial-and-access-boundaries.md` § Claims |
| D | 2, 3 | `context/commercial-and-access-boundaries.md` § Access and § Delivery surface |
| D | 4 | `CLAUDE.md` § Off-limits |

Claims born in this interview carry `(stakeholder-verbal, <name>, <date>)`. Never fabricate a source.
