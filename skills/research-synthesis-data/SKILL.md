---
name: research-synthesis-data
version: 0.1.1
description: >
  Convert raw discovery notes into structured insights using atomic research methods
  adapted for data products. Use when synthesizing findings, reviewing evidence,
  summarizing research, writing problem briefs, or when someone asks "what did we
  learn?" or "what does the evidence say?"
user-invocable: false
---

## Evidence Hierarchy

Assess evidence for the specific question, coverage, independence and recency. These source types offer different signals, not a universal ranking:

1. **Observed workarounds**: Record the task, cost and alternatives using `data-consumer-discovery`. Investment shows effort, not validated demand or willingness to buy.
2. **Usage data**: Query logs, dashboard access and API calls show recorded behavior within instrumentation and access limits.
3. **Quality incidents**: Tickets and escalations show reported problems; silence does not establish absence of harm.
4. **Consumer quotes**: Preserve wording, context and independence. Repeated quotes can suggest a pattern, not a fixed validation threshold.
5. **Stakeholder requests**: Separate the requested solution from the decision, constraints and authority behind it.

When usage and interviews conflict, check identity, coverage, period, permissions and workflow definitions. Logs may miss off-platform work; interviews may describe intended rather than observed behavior. Preserve unresolved contradictions.

## Atomic Research Chain

Build insights from the bottom up. Every level must trace to the one below it.

### Nuggets

Raw observations tagged with source and date. One fact per nugget.

Synthetic example: `[Fictional interview: Sarah, Analytics Lead, 2024-01-15] Spends 4 hours every Monday rebuilding the regional performance report from 3 separate data exports.`

Tag each nugget: source type (interview, log, ticket, observation), consumer segment (Explorer, Reporter, Decision-maker, Builder), and topic.

### Patterns

Group observations that support the same explanation. Report the sample, independence and contrary cases. No universal count establishes a pattern; a single well-supported safety event can still require action.

Synthetic example: `3 of 5 analytics leads manually combine data from 3+ sources weekly. Average reported time: 3.5 hours. They report distrust of the automated totals. The sample does not establish demand across the organization.`

### Insights

Patterns interpreted in context. Answers "so what?"

Synthetic interpretation: `Definition differences may explain the regional reporting mismatch. Compare the same population and period under each definition before claiming a cause or forecasting time saved.`

### Recommendations

Insights translated into action. Each recommendation links to a specific skill or command:

- Problem Brief → feeds `data-product-validation` scorecard
- Data Landscape Assessment → feeds `data-quality-assessment` audit
- Consumer Map → feeds `stakeholder-alignment` prioritization

## Three Synthesis Outputs

Every discovery effort produces three artifacts:

**1. Problem Brief** — The top 3 problems ranked by evidence strength. For each: problem statement, evidence summary (nuggets and patterns), affected consumer segments, estimated impact. Feeds directly into `/dpo:write-data-prd`.

**2. Data Landscape Assessment** — Current state of relevant data sources. For each: what exists, quality baseline (cross-ref `data-quality-assessment`), gaps, access constraints. Feeds into `data-product-validation` Data Feasibility scoring.

**3. Consumer Map** — Who needs what, segmented by type (see `data-consumer-discovery` segments). Includes: frequency of need, current workaround, trust level, downstream dependents. Feeds into `stakeholder-alignment` prioritization.

## Contradictory Evidence

When evidence conflicts:

1. Flag the contradiction explicitly. Do not smooth it over or pick the more convenient interpretation.
2. Compare scope, timing, source reliability and independence. Do not choose a winner by source type alone.
3. Record competing explanations and a targeted follow-up that could distinguish them.

Example: "Interview data suggests daily demand, but query logs show weekly access. Recommend monitoring actual usage for 2 weeks before committing to real-time refresh SLA."

NEVER present a clean narrative when the evidence is messy. Stakeholders deserve honest uncertainty over false confidence.
