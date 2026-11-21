# Post-scaffold

Run after the scaffold is copied and populated.

## 1. Validate

Run `python3 scripts/validate.py .` from the instance root. Fix every finding. Re-run until exit 0.

## 2. Walk the links

Open `INDEX.md`, `CLAUDE.md`, and `rules/INDEX.md`. Follow every relative link. The validator already checked resolution; here you confirm the routing reads correctly for a human.

## 3. The three first actions

Lead the handoff with these, in order:

1. **Fill decision rights today.** `context/team-and-decision-rights.md` § Roles. Name the final release decider, the data acceptance owner, and the engineering feasibility owner. Nothing else moves until these are named.
2. **Write the first packet this week.** Copy `packets/_TEMPLATE.md` to `packets/<date>-weekly-packet.md`. Put the one decision that matters most in the first row.
3. **Log the first pending decision.** One row in `decisions/LOG.md` and one record from `decisions/_SCHEMA.md`, status `pending`, with a decider and a review date.

## 4. Contradictions

List one to three contradictions found during migration or the interview, each with the two sources that disagree and where the tension now lives in `context/`. If none were found, say so.

## 5. Gaps

Two or three concrete gaps, no more. Example: "`context/data-contract.md` has no freshness for the claims source."

## 6. Receipt

Print:

```
Self-test receipt:
- Validator: exit 0
- Links walked: N
- Context sections populated: N of 30, tagged: N, Unknown: N
- Contradictions surfaced: N
```

## 7. Hand off

Order: three first actions, contradictions, gaps, one paragraph on what was built. Do not lead with a folder map. Then stop and wait for the operator's first real task.
