---
description: Synthesize raw discovery notes into a structured problem brief with ranked problems, evidence chains, and consumer maps
argument-hint: <file paths to discovery notes, or paste raw notes>
allowed-tools: Read, Write, AskUserQuestion, Bash
---

# Write a Problem Brief

Convert raw discovery inputs (interview notes, Slack exports, meeting notes, support tickets, query logs) into a structured problem brief using the atomic research method adapted for data products.

## Gather Inputs

If `$ARGUMENTS` provides file paths, read them. Accept any combination of:
- Interview transcripts or notes
- Slack thread exports
- Meeting notes (Granola, manual, or any format)
- Support tickets or bug reports
- Query log summaries
- Previous discovery briefs
- Raw pasted text

If no arguments provided, ask:

**Question 1:** What discovery inputs do you have? Provide file paths, paste text, or describe what you've gathered.

**Question 2:** What problem area are these inputs about? (1 sentence to anchor the synthesis)

## Extract Nuggets

Read all inputs and extract atomic observations. One fact per nugget.

Format each nugget:
```
[Source type: Name, Role, Date] Observation
```

Tag each nugget with:
- **Source type**: interview, log, ticket, observation, slack, meeting
- **Consumer segment**: Explorer, Reporter, Decision-maker, Builder (see `data-consumer-discovery`)
- **Topic**: short keyword for grouping

CRITICAL: Preserve specifics. "Spends 4 hours every Monday" not "spends significant time." "$2,847 per incident" not "costly errors." Numbers and names make evidence credible.

## Find Patterns

Group nuggets by topic. A pattern requires 3+ nuggets from independent sources.

For each pattern:
- State the pattern in one sentence
- List the supporting nuggets (with source attribution)
- Note the consumer segments affected
- Flag any contradictory evidence (see `research-synthesis-data` contradictory evidence rules)

Patterns with fewer than 3 sources are flagged as "Emerging" and excluded from the top problems.

## Derive Insights

For each pattern, answer "so what?" in the context of data product decisions.

Connect each insight to a downstream action:
- Problem to solve → feeds `/dpo:write-data-prd`
- Data source to audit → feeds `/dpo:review-data-quality`
- Consumer need to validate → feeds `/dpo:run-discovery` on a specific sub-problem
- Stakeholder to align → feeds `/dpo:write-stakeholder-brief`

## Write the Problem Brief

Write to `problem-brief-<name>.md` where `<name>` is a kebab-case identifier.

Use this structure:

```markdown
# Problem Brief: [Problem Area]

**Date:** [today]
**Sources:** [count] inputs ([list source types])
**Confidence:** [High / Medium / Low] (High = 5+ strong patterns, Medium = 3-4 patterns, Low = <3 or mostly Emerging)

## Top 3 Problems

Ranked by evidence strength (see `research-synthesis-data` evidence hierarchy).

### 1. [Problem Name]

**Evidence strength:** [Strong / Moderate]
**Affected segments:** [list consumer segments]
**Estimated impact:** [specific: hours/week, $/year, decisions delayed]

[2-3 sentence problem statement]

**Supporting evidence:**
- [Nugget 1 with source]
- [Nugget 2 with source]
- [Nugget 3 with source]

**Existing workarounds:** [what consumers do today]

---

### 2. [Problem Name]
[Same structure]

---

### 3. [Problem Name]
[Same structure]

## Data Landscape

For each relevant data source identified during synthesis:

| Source | Exists? | Quality Baseline | Gaps | Access |
|--------|---------|-----------------|------|--------|
| [name] | [yes/no/partial] | [score or "unknown"] | [specific gaps] | [how to access] |

## Consumer Map

| Segment | Count | Primary Need | Current Workaround | Trust Level |
|---------|-------|-------------|-------------------|-------------|
| [segment] | [#] | [decision they make] | [what they do today] | [High/Med/Low] |

## Contradictions

[List any conflicting evidence with both sides stated. Note which evidence ranks higher per the hierarchy. Recommend specific follow-ups to resolve.]

If no contradictions: "No contradictory evidence identified."

## Confidence Assessment

**Overall:** [High / Medium / Low]

**Gaps in evidence:**
- [What we don't know yet]
- [What would change the ranking if we learned it]

**Recommended follow-ups:**
- [Specific next action to strengthen evidence]
```

## Final Check

Before saving, verify:
- [ ] Every problem has 3+ supporting nuggets from independent sources
- [ ] Evidence is specific (numbers, names, dates) not vague ("significant," "many")
- [ ] Problems are ranked by evidence strength, not assumed importance
- [ ] Contradictions are flagged, not smoothed over
- [ ] Consumer map covers all segments found in the data
- [ ] Confidence assessment is honest about gaps
- [ ] At least one recommended follow-up is specific enough to act on immediately
