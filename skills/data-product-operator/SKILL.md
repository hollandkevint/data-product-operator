---
name: data-product-operator
description: Help a data leader or data product manager choose the next decision, coordinate delivery and review outcomes across one product or a portfolio. Use to establish or improve a data-product operating rhythm, connect existing skills and preserve decision context. Domain agnostic; does not replace the team's tools or grant execution authority.
metadata:
  version: "0.1.0"
---

# Data Product Operator

Start with the leader's decision, not a tool or a domain checklist.
Ask what someone should be able to do differently because this data product exists.
Read existing product briefs, priorities and constraints before asking for more context.
Keep company-specific work in its existing approved home. Do not create another tracker or copy private records into this repository.

## Choose the scope

Work at the requested level: One decision, one product, one team or a portfolio.
Do not turn a small request into an OS installation. Add structure when a recurring handoff or missing decision justifies it.

| Scope | Minimum working context | Decision to support |
|---|---|---|
| Decision | Consumer, intended outcome, evidence and owner | What should happen next? |
| Product | Purpose, consumers, definition, dependencies and accepting owner | Build, change, hand off or investigate? |
| Team | Current bets, capacity, ownership and blocked handoffs | What should the team finish, stop or renegotiate? |
| Portfolio | Products, owners, consumers, outcome evidence, costs and dependencies | Invest, maintain, consolidate or retire? |

Treat reported demand, estimated benefit and observed outcomes as different evidence. Do not infer adoption from meetings, praise or a delivered dataset.
When context is missing, ask the single question that most affects the decision. Offer a bounded next step with its tradeoff; leave historical facts neutral.

## Run the relevant part of the loop

Read the selected skill before using it. If it is missing, name that limitation and do not claim it ran.

| Step | Route | Required handoff |
|---|---|---|
| Understand the need | [Consumer discovery](../data-consumer-discovery/SKILL.md), [dashboards to decisions](../dashboards-to-decisions/SKILL.md) | Consumer task, consequence, attempted alternatives and unresolved question |
| Choose a bounded bet | [Product thinking](../data-product-thinking/SKILL.md), [validation](../data-product-validation/SKILL.md), [grill me](../grill-me-data/SKILL.md) | Expected outcome, appetite, assumption, scope and stop condition |
| Define and shape delivery | [Metrics](../metrics-definition/SKILL.md), [model design](../data-model-design/SKILL.md), [write a PRD](../../commands/write-data-prd.md) when useful | Agreed definitions, dependencies, acceptance cases and receiving owner |
| Verify and hand off | [Analyst](../analyst/SKILL.md), [pipeline quality](../data-pipeline-quality/SKILL.md) | Versioned evidence, unresolved risks and scoped owner decision |
| Observe use and outcomes | [Stakeholder alignment](../stakeholder-alignment/SKILL.md), [storytelling](../data-storytelling/SKILL.md) | What was observed, what remains uncertain and the next decision |
| Revise or retire | [Research synthesis](../research-synthesis-data/SKILL.md), [team operating model](../data-team-operating-model/SKILL.md) | Verified lesson, proposed change or retirement plan with dependency review |

Start at the unresolved step; do not replay completed discovery. An urgent incident may need containment through the organization's incident process before product planning.
For each handoff, record the trigger, receiving owner, needed evidence and disposition if it is absent. Follow up over an agreed observation period. A calendar event alone does not close the loop.

## Grow the operating rhythm

For one product, keep a brief and link decisions to evidence with Analyst. Reuse existing definitions and source references.
For a team, add a review of current bets, blocked handoffs and results since the last review. Fit the cadence and role assignments to the team; do not impose six-week cycles or a new organizational chart.
For a portfolio, compare intended value, observed use/outcomes, cost, risk and downstream dependencies. Mark unknowns. Before recommending retirement, identify affected consumers, migration obligations and the owner who can approve it. Never decommission a product as a side effect of review.
Use scorecards only as discussion aids. Do not fabricate ROI, maturity ratings or universal investment thresholds.

## Add domain and platform guidance last

Choose a [domain application](../../docs/domain-applications.md) or the [healthcare pack](../../docs/healthcare-applications.md) only when the task calls for it. The core OS does not assume healthcare, marketing, operations or commerce.
Add [Databricks](../databricks-data-product-review/SKILL.md) or [DuckDB](../duckdb-data-profiling/SKILL.md) only for the selected execution environment. Preserve the business definition across platforms.
Keep access, technical fitness, domain review and authority to act separate. No linked skill grants permission to change data, publish a result, contact a customer or spend money.

## Return the decision record

State the intended outcome, current decision, supporting evidence, unresolved constraints, next action and owner. Distinguish recommendations from decisions the owner has made.
If a rule in the library appears wrong, propose a correction tied to observed evidence and a regression case. Update shared skills only when authorized; keep private examples private.
Use the user's existing tracker or document format. Do not create empty plans or a folder hierarchy for hypothetical future products.
