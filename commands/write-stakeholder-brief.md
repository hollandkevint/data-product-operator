---
description: Translate technical data work into a 1-page business summary with impact metrics
argument-hint: <project or feature to summarize>
allowed-tools: Read, Write, AskUserQuestion
---

# Write a Stakeholder Brief

Translate technical data product work into a concise business-facing summary. The audience is executives, business stakeholders, or cross-functional partners who need to understand impact without technical depth.

## Gather Context

If `$ARGUMENTS` describes the project, use it. Otherwise, ask:

**Question 1:** What data product work are you summarizing? (feature shipped, project milestone, quarterly update)

**Question 2:** Who is the audience? Options: C-suite, VP-level, business partners, cross-functional team, board.

**Question 3:** What's the most important thing they need to know? (impact achieved, decision needed, risk to flag, resource request)

**Question 4:** What metrics or results can you share? (specific numbers preferred: revenue impact, time saved, adoption rate, quality improvement)

## Write the Brief

Write to `stakeholder-brief-<name>.md` where `<name>` is a kebab-case identifier.

Target length: 1 page (300-500 words). Executives skim. Every sentence must earn its place.

### Output Structure

```markdown
# [Project Name]: Stakeholder Brief

**Date:** [today]
**Status:** [On Track / At Risk / Completed / Needs Decision]
**Owner:** [team or person]

## Bottom Line

[2-3 sentences: what happened, what it means for the business, what comes next. Lead with the most important fact.]

## Impact

[Quantified results in business terms, not technical terms]
- [Metric 1]: [value] ([comparison or trend])
- [Metric 2]: [value] ([comparison or trend])
- [Metric 3]: [value] ([comparison or trend])

## What We Did

[3-5 bullet points describing the work in business language. No jargon. No architecture diagrams. Focus on what changed for the user or customer.]

## What's Next

[2-3 bullet points on upcoming milestones, decisions needed, or dependencies]

## Risks or Asks

[Only if applicable. Flag blockers, resource needs, or decisions that need escalation. Skip this section entirely if there are none.]
```

### Writing Rules

ALWAYS lead with the outcome, not the process. "Reduced report generation time from 45 minutes to 5 seconds" not "We optimized the ETL pipeline and migrated to a columnar database."

ALWAYS quantify impact in terms the audience cares about. For executives: revenue, cost savings, risk reduction, time saved. For business partners: capabilities enabled, decisions supported, customer impact.

NEVER include technical implementation details. If they need to know about the database migration, schedule a separate technical review.

NEVER use jargon without translation. "SLA" becomes "our commitment to data freshness." "Schema migration" becomes "updated the data structure to support the new reporting requirements."

ALWAYS name the tradeoff when flagging risks. "We can ship Feature X in 3 weeks with 90% coverage, or 6 weeks with 99%. Recommend the 3-week version because [reason]."

Keep paragraphs to 2-3 sentences. Use bullet points for lists. Bold the key number in each impact line.
