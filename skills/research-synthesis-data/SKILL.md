---
name: research-synthesis-data
version: 0.1.0
description: >
  Convert raw discovery notes into structured insights using atomic research methods
  adapted for data products. Use when synthesizing findings, reviewing evidence,
  summarizing research, writing problem briefs, or when someone asks "what did we
  learn?" or "what does the evidence say?"
user-invocable: false
---

## Evidence Hierarchy

Not all evidence is equal. Rank sources in this order:

1. **Observed workarounds** (strongest) — Someone built something to solve this problem. Documented in `data-consumer-discovery` workaround archaeology format. Time invested = validated demand.
2. **Usage data** — Query logs, dashboard access patterns, API call frequency. Behavior over opinions.
3. **Quality incidents** — Support tickets, data bug reports, escalations. Pain that generated action.
4. **Consumer quotes** — Direct statements from interviews. 3+ independent quotes on the same theme = a pattern.
5. **Stakeholder requests** (weakest) — What someone asked for. Often a solution masking a different problem.

CRITICAL: When usage data contradicts interview data, usage data wins. People describe aspirational workflows. Logs show actual ones.

## Atomic Research Chain

Build insights from the bottom up. Every level must trace to the one below it.

### Nuggets

Raw observations tagged with source and date. One fact per nugget.

Example: `[Interview: Sarah, Analytics Lead, 2024-01-15] Spends 4 hours every Monday rebuilding the regional performance report from 3 separate data exports.`

Tag each nugget: source type (interview, log, ticket, observation), consumer segment (Explorer, Reporter, Decision-maker, Builder), and topic.

### Patterns

Three or more nuggets from independent sources pointing to the same conclusion. Less than three is anecdotal.

Example: `3 of 5 analytics leads manually combine data from 3+ sources weekly. Average time: 3.5 hours. All distrust the automated report because "the numbers don't match what I pull manually."`

### Insights

Patterns interpreted in context. Answers "so what?"

Example: `Regional reporting is the highest-pain workaround across analytics. The root cause is inconsistent metric definitions across source systems, not missing data. Fixing the semantic layer would eliminate 15+ hours/week of manual reconciliation.`

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
2. Check the evidence hierarchy. Higher-ranked evidence wins.
3. If same-rank evidence conflicts, note the split and recommend a targeted follow-up (specific question, specific data pull).

Example: "Interview data suggests daily demand, but query logs show weekly access. Recommend monitoring actual usage for 2 weeks before committing to real-time refresh SLA."

NEVER present a clean narrative when the evidence is messy. Stakeholders deserve honest uncertainty over false confidence.
