---
name: shipping-bridge
version: 0.1.0
description: >
  Map a data product decision to release gates before it ships. Connects the Team Loop
  controlled-launch gate to the ai-shipping release practices in Pawel Huryn's
  product-engineering pack. Use when a data product, model or agent is about to reach
  consumers and you need to know which gates apply and who signs them.
user-invocable: false
adapted_from: https://github.com/phuryn/product-engineering
---

# Shipping bridge

A product decision is not a release. This skill turns the decision into a short list of gates, each with an owner and evidence. It links to the shipping pack. It does not copy it. Read the pack for the full method.

Pack: [phuryn/product-engineering](https://github.com/phuryn/product-engineering), the `ai-shipping` skills: `ship-check`, `code-review`, `independent-review` and `release-gate`.

## Step 1: State the decision

Use the decision spec from [dashboards to decisions](../dashboards-to-decisions/SKILL.md). Name the consumer and the cohort that gets it first. See [launch and adoption](../launch-and-adoption/SKILL.md) for the signal and countermetric.

## Step 2: Map the gates

| Question | Gate | Where it lives |
|---|---|---|
| Is the evidence good enough for a first cohort? | Controlled-launch gate: test evidence, limitations text, cohort, stop conditions, rollback, support owner | `skills/team-loop/scaffold/rules/launch.md` |
| Does the shipped thing match what was decided? | Intended versus implemented check | `ship-check` in the pack |
| Did someone other than the author review the change? | Fresh-eyes review, repeated until clean | `code-review`, `independent-review` in the pack |
| Preview, go or no-go, promote, verify | Release steps | `release-gate` in the pack |

Pick only the gates the change needs. A metric definition change may need the launch gate and an independent review, and no more.

## Step 3: Assign owners and evidence

For each gate, name who accepts it and what evidence they need. The person who builds the change does not accept it.

## Step 4: Decide and record

Outcome is go, revise or stop. Record it with the cohort, the stop conditions and the review date, in the Team Loop decision log if the team uses one.

## Output

Produce one table with these fields for every gate:

- **Gate:** the name.
- **Source:** where the gate is defined (Team Loop rule or pack skill).
- **Owner:** who accepts it.
- **Evidence:** what must exist before acceptance.
- **Outcome:** go, revise or stop.

Add one line for the decision it serves and one for the stop conditions.

Source: Pawel Huryn, product-engineering, https://github.com/phuryn/product-engineering, MIT license. Ideas adapted, no text copied.
