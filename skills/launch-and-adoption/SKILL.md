---
name: launch-and-adoption
metadata:
  version: "0.1.0"
description: >
  Plan the launch of a data product (see GLOSSARY.md): the named consumer, the decision it
  changes, the adoption signal, the countermetric, onboarding, channels and a retire rule.
  Use before or at release, when a data product is built but nobody uses it yet, or when
  adoption stalls. Works for internal and external consumers.
user-invocable: false
---

# Launch and adoption

A data product that ships and is not used has not launched. Adoption is an incentive problem before it is a marketing problem. Map what the consumer is measured on and what safe habit they must give up, then plan the launch.

Reuse these, do not repeat them:
- [Consumer discovery](../data-consumer-discovery/SKILL.md) for who the consumer is and what they do today.
- [Dashboards to decisions](../dashboards-to-decisions/SKILL.md) for the decision spec.
- [Stakeholder alignment](../stakeholder-alignment/SKILL.md) for sponsors and objectors.
- [Data storytelling](../data-storytelling/SKILL.md) for the launch message and demo.

## Step 1: Name the consumer and the decision

One consumer (a role or a person, not "the business"). One decision it changes. If either is missing, stop. Go back to discovery. Without both, there is nothing to launch.

## Step 2: Map incentives

Ask what the consumer is measured on, who sponsors the change, and what they give up to adopt. A consumer who must drop a trusted spreadsheet needs a reason stronger than "it is better." Pull beats push: if you must sell the product hard, the fit may be wrong.

## Step 3: Pick the adoption signal and the countermetric

Measure at the workflow or decision level, not at activity level. Logins, queries and tokens are activity. A decision made differently is value.

- **Adoption signal:** one observable behavior that shows the decision changed, with a baseline and a target date.
- **Countermetric:** one measure that would rise if people gamed or misused the signal, or if the product caused harm (for example, decisions reversed, manual rework, complaints).

## Step 4: Plan onboarding

Fit the consumer's existing workflow. Deliver where they already work. Plan the first use: who sits with the first five users, what the first session covers, what "set up" means, and who answers questions in week one.

## Step 5: Pick channels

| Consumer | Channels to consider |
|---|---|
| Internal | The team meeting where the decision is made, a named sponsor, a short demo on a real case, a message in the tool they already use |
| External | Account owner or support contact, release note, docs page, a worked example in the customer's own terms, a status or changelog page |

Marketing here means telling the right consumer what decision gets easier, in their words. Do not announce to everyone.

## Step 6: Set the retire rule

State up front: if the adoption signal is not met by the review date, the owner either fixes the named cause, narrows the consumer, or retires the product. Name the owner and the date. Unused products cost run time and trust.

## Output

Produce one page with these fields:

- **Consumer:** the named role or person.
- **Decision changed:** the decision, and what happens differently.
- **Adoption signal:** the behavior, baseline, target and date.
- **Countermetric:** the measure, and the value that triggers a stop.
- **Onboarding:** first-use plan and the week-one support owner.
- **Channels:** where and how the consumer hears of it.
- **Retire rule:** review date, owner and the three options.

If a field cannot be filled, say which one and why. Do not invent a number.

Source: ideas on measuring at the workflow level and fitting the existing workflow come from the research notes in this repo's first-principles page. No third-party text is copied here.
