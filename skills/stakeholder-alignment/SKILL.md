---
name: stakeholder-alignment
version: 0.1.0
description: >
  Translates between technical data teams and business stakeholders. Use when
  preparing stakeholder updates, translating technical data work for executives,
  shaping vague business requests into buildable specs, navigating competing
  priorities across data consumers, or when someone asks "how do I explain this
  to my VP?" or "the business team wants X but that's not how data works."
user-invocable: false
---

## Core Model: Extended Squad

Data products are built by a core squad with extended stakeholder input:

**Core Squad** (day-to-day, co-equal authority):
- Product Manager: strategy and prioritization
- Tech Lead: architecture and feasibility
- Design Lead: UX and usability
- Data Lead: data quality, ethics, and engineering

**Extended Squad** (contribute expertise, not approval gates):
- Legal/Compliance: regulatory input early in shaping, not as a late blocker
- Medical Affairs / Domain SMEs: validate domain accuracy
- Commercial/Sales: pricing, GTM, customer feedback
- Finance: budget and ROI modeling
- Data Governance: policy and access control

CRITICAL: Bring extended stakeholders in during shaping (before commitment), not during delivery (as surprise reviewers). Early input prevents late vetoes.

## Translation Patterns

When translating technical data work for business audiences:

**Replace jargon with outcomes.** "We normalized the schema and added SCD Type 2" becomes "Historical changes are now tracked, so you can see how patient records evolved over time."

**Lead with the decision it enables.** Not "we built a pipeline" but "you can now see which patients are at risk of readmission within 24 hours of discharge."

**Quantify impact in business terms.** Not "query performance improved 10x" but "the report that took 45 minutes now takes under 5 seconds, saving your team 3 hours per week."

**Name the tradeoff, not just the recommendation.** "We can ship in 3 weeks with 90% accuracy, or 6 weeks with 99%. The 90% version catches the same high-risk patients but may flag 10% more false positives."

## Shaping Vague Requests

When a stakeholder says "I need a dashboard for X":

1. Ask what decision the dashboard enables (not what data it shows)
2. Ask who will use it and how often
3. Ask what they do today without it (the workaround reveals the real need)
4. Ask what "good enough" looks like (perfect is the enemy of shipped)

NEVER build what was asked for without understanding why it was asked for. The request is a symptom. The decision they need to make is the diagnosis.

## Resolving Competing Priorities

Use a Betting Table (quarterly or per-cycle):
- Each stakeholder pitches their top priority with business impact
- The squad evaluates feasibility and effort for each
- Leadership allocates fixed capacity to the highest-impact bets
- Boundaries enable autonomy: what's fixed (strategic direction) vs. flexible (implementation approach)

AVOID the loudest-voice-wins pattern. Data team capacity is finite. Every yes is an implicit no to something else. Make the tradeoffs explicit.
