---
name: dashboards-to-decisions
version: 0.1.0
description: >
  Convert dashboard requests into decision specifications. The missing layer between
  "build me a dashboard" and "help me decide." Use when receiving dashboard requests,
  reviewing analytics backlogs, prioritizing data team work, or when someone asks
  "what dashboard do you need?" Apply this BEFORE building anything.
user-invocable: false
---

## The Reframe

When someone asks "I need a dashboard," the first question is: "What decision will this inform?"

If they can't answer, the dashboard shouldn't exist yet. Not "never build it." Just "not yet." Get the decision clear first.

## The Process

### Step 1: Surface the Decision

Ask: "What decision will this dashboard help you make? Be specific — not 'understand performance' but 'decide whether to expand into the Southeast region this quarter.'"

If the requester struggles, use these prompts:
- "What would you DO differently after seeing this dashboard?"
- "If the number is high, what changes? If it's low, what changes?"
- "Who makes this decision, and when?"

If no decision emerges: the request is a monitoring need, not a decision need. Route to Layer 1 (dashboard craft) and move on.

### Step 2: Map the Decision Architecture

| Element | Question | Example |
|---------|----------|---------|
| **Decision** | What specifically is being decided? | "Expand to Southeast: yes/no" |
| **Decision-maker** | Who has authority? | "VP of Operations, with CFO sign-off" |
| **Timeline** | When does this decision get made? | "Q3 planning, due July 15" |
| **Metrics needed** | What data informs this? | "Market size, current penetration, operational capacity, P&L impact" |
| **Threshold** | What number triggers action? | "If projected ROI > 15% AND capacity utilization < 80%" |
| **Context** | What else does the decision-maker need to know? | "Previous expansion to Midwest failed at 12% ROI" |
| **Failure mode** | What would make the wrong decision? | "Misleading market size data (happened with Midwest)" |

### Step 3: Design the Decision Spec (Not the Dashboard)

Write a decision specification that captures:

1. **The question** (in plain language, not metric language)
2. **The answer format** (yes/no, rank order, threshold comparison)
3. **The data required** (specific metrics with definitions and sources)
4. **The context required** (what the decision-maker needs to know before looking at data)
5. **The intent** (when metrics conflict, which wins?)
6. **The failure mode** (what would lead to a wrong decision?)

### Step 4: THEN Design the Dashboard

Only after Steps 1-3 are clear, design the visualization. Now you know:
- What metrics to show (from the data requirement)
- How to organize them (around the decision, not the data model)
- What context to include (the "how to use this" layer)
- What thresholds to highlight (the intent layer)

## The Four Layers Applied

| Layer | What This Skill Adds |
|-------|---------------------|
| **Layer 1: Dashboard Craft** | The dashboard itself (this is where most teams stop) |
| **Layer 2: Decision Context** | The "what you need to know before looking at the data" document |
| **Layer 3: Decision Intent** | The thresholds and metric priorities that encode business judgment |
| **Layer 4: Decision Infrastructure** | The full spec that lets the decision-maker self-serve |

Cross-reference `stakeholder-alignment` for translating between data teams and business stakeholders.

## The Monday Morning Test

Ask your team: "Name 3 decisions that changed because of something we shipped last quarter."

If they can't, you're stuck at Layer 1. This skill moves you to Layer 2+.

## Output

```markdown
# Decision Specification: [Decision Name]
Date: [date]
Requester: [who asked for this]

## The Decision
[Plain language question]

## Decision-Maker & Timeline
[Who decides, by when]

## Metrics Required
| Metric | Definition | Source | Current Value |
|--------|-----------|--------|---------------|
| [metric] | [precise definition] | [data source] | [if known] |

## Decision Threshold
[What number triggers which action]

## Context
[What the decision-maker needs to know before looking at data]

## Intent (When Metrics Conflict)
[Which metric wins and why]

## Failure Modes
[What would lead to a wrong decision]

## Dashboard Recommendation
[Now we can spec the visualization — layout, key charts, highlights]
```

From the Decision Engineering framework. Generic decision tools: [decision-architecture](https://github.com/hollandkevint/decision-architecture).

---

Part of the [Data Product Operator](https://github.com/hollandkevint/data-product-operator) plugin.
