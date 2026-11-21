---
name: data-product-retro
metadata:
  version: "0.1.0"
adapted_from: Matt Pocock, mattpocock/skills, retro
description: >
  Look back at a shipped data product decision and ask two questions: did the
  decision change, and did the data hold up? Reads the Team Loop decision log and
  the decision follow-up state if they exist, and returns actions tied to decision
  log entries. Use after a launch, at the end of a quarter, after an incident, or
  when someone asks "what did we learn from this data product?"
user-invocable: false
---

## What this is for

A retro that ends in "we should communicate better" changes nothing. This one ends in actions, and each action points at a row in the decision log. If an action has no row, either the decision was never logged, or the action is not about a decision.

Matt Pocock's retro looks back at a coding session and proposes changes to the environment, ranked by severity. This skill keeps that shape for a data product: read the primary sources, find candidates, present them in order of severity. The subject changes from a coding session to a decision and the data under it.

## The two core questions

Ask both for every decision in scope. Do not merge them. A decision can hold while the data fails, and the reverse.

1. **Did the decision change?** Compare what was decided with what the team does now. Check the reverse condition recorded with the decision (`## What would reverse this`). Did it happen? Was the decision reversed, superseded, extended or quietly dropped?
2. **Did the data hold up?** Compare what the decision assumed about the data with what the data did. Check the definition, grain, freshness, quality and consumer use the decision relied on. Did any of them break, drift or never get measured?

## Before you start

1. Name the scope: one data product, one launch or one period. Ask only if the user has not said.
2. Read `decisions/LOG.md` in the Team Loop workspace (see [Team Loop](../team-loop/SKILL.md)). Keep the rows in scope. Open each record under `decisions/`.
3. Read the decision follow-up state if present: `loops/decision-follow-up/state.json` and the latest `loops/decision-follow-up/<date>.md` (see [decision follow-up](../decision-follow-up/SKILL.md)). Its dispositions (`keep`, `reverse`, `extend`, `no-outcome`) are evidence, not the answer. Re-read the record behind each one.
4. If there is no log, say so first. That is the first finding. Run the retro from the sources the user names, and mark each action `no log entry`.
5. Finding facts is your job. Look up metrics, quality results and consumer notes in the files and queries the team already has. Do not ask the user for what you can read. Do not invent evidence. Use a provenance tag from `decisions/_SCHEMA.md`, or `Unknown`.

## Find candidates

For each decision, look for these. Each is a candidate action.

- **Reverse condition met, no superseding record.** The decision should be superseded and nobody wrote it.
- **No outcome check.** Past its review date with no follow-up. Ask why, then set a new date.
- **Data assumption never measured.** The decision relied on a definition, grain or freshness figure with no check. Add a check: a test, a quality rule or a metric entry (`metric-glossary`).
- **Data broke after the decision.** Link the failure to the decision it affected. Use `data-quality-assessment` to score it.
- **Consumers did not use it.** Adoption fell short of the decision's premise. Use `launch-and-adoption`.
- **Decision never logged.** The team acted without a record. Log it now, with evidence or `Unknown`.
- **Wrong owner or no owner.** The decider left, or the action has no named person.

Rank candidates by severity: a decision reversed by events with no record first, a missing check last.

## Output

Present the candidates in order of severity. Report this, in this order:

- **Did the decision change?** One line per decision in scope: the log row, the answer (`held`, `changed`, `superseded`, `unknown`) and the evidence.
- **Did the data hold up?** One line per decision: the log row, the answer (`held`, `drifted`, `broke`, `unmeasured`) and the evidence.
- **Actions tied to the decision log:** a table. Each row has the action, the decision log entry it ties to (date and decision text from `decisions/LOG.md`, or `no log entry`), the owner, a due date and the check that shows it is done. No action without an owner and a due date.
- **Open:** what needs an answer, and who can give it.

This skill reports. It does not edit the log or any decision record. A named decider writes the superseding record.

Source: Matt Pocock, [mattpocock/skills](https://github.com/mattpocock/skills) (retro), MIT license. Adapted for data product decisions.
