---
description: Guided discovery session for a new data product idea — interviews, validation scorecard, and go/investigate/kill recommendation
argument-hint: <product idea or problem area>
allowed-tools: Read, Write, AskUserQuestion
---

# Run a Data Product Discovery Session

Guide a structured discovery conversation for a new data product idea. This command combines consumer discovery questions with a validation scorecard to produce a go/investigate/kill recommendation.

## Gather Context

If `$ARGUMENTS` provides a product idea or problem area, use it as the starting point. Otherwise, ask:

**Question 1:** What problem area are you exploring? Describe it in terms of the decision someone needs to make, not the data they want.

## Run Discovery Questions

Ask these questions one at a time. Wait for each answer before proceeding. Each question builds on the prior answer.

**Question 2:** Who are the consumers of this data? What decisions do they make with it? (Reference `data-consumer-discovery` consumer segments: Explorers, Reporters, Decision-makers, Builders.)

**Question 3:** Walk me through the last time someone needed this data. Where did it come from? How long did it take? What did they trust or distrust about it?

**Question 4:** What workarounds exist today? Describe any manual processes, Excel files, scripts, or tools people have built to solve this problem. For each workaround, capture: tool used, frequency, time cost per use, trust level, downstream dependents.

**Question 5:** What would make consumers NOT trust this output? List specific concerns: source opacity, staleness, conflicting numbers, past incidents, no validation path.

**Question 6:** If consumers could get this answer in under a minute, what changes? Describe the business impact in specific terms: decisions made faster, costs avoided, risks caught earlier.

## Score the Validation Scorecard

After collecting discovery answers, score each dimension 1-5 based on the evidence gathered. Reference `data-product-validation` for scoring criteria.

Explain your reasoning for each score in 1-2 sentences.

1. **Demand Frequency** (1-5): How often do consumers need this answer?
2. **Decision Impact** (1-5): What happens when they don't have it?
3. **Workaround Effort** (1-5): What are they doing today instead?
4. **Data Feasibility** (1-5): Can we build this with available data?
5. **Schema Risk** (1-5): How locked-in are consumers once we ship?

Calculate the composite score (multiply all five).

## Assess Signal Strength

Based on the discovery conversation, classify the evidence:

- **Strong**: Observed workarounds with time investment + 3 independent data points on the same pain
- **Moderate**: 3+ quotes describing same problem, or usage data showing repeated manual effort
- **Emerging**: 1-2 mentions, no observed behavior change

## Write the Discovery Brief

Write to `discovery-brief-<name>.md` where `<name>` is a kebab-case identifier for the product idea.

Use this structure:

```markdown
# Discovery Brief: [Product Idea Name]

**Date:** [today]
**Facilitator:** [name or "AI-assisted"]
**Signal Strength:** [Strong / Moderate / Emerging]

## Problem Statement

[2-3 sentences: the decision consumers need to make, the current pain, the evidence it's real]

## Consumer Evidence

### Who Needs This
[Consumer segments identified, with count and roles]

### Current Workarounds
[For each workaround: tool, frequency, time cost, trust level, downstream dependents]

### Trust Barriers
[Specific concerns raised, mapped to data quality dimensions]

## Data Feasibility

[Current state of required data sources. Known quality issues. Access constraints.]

## Validation Scorecard

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Demand Frequency | [1-5] | [1-2 sentences] |
| Decision Impact | [1-5] | [1-2 sentences] |
| Workaround Effort | [1-5] | [1-2 sentences] |
| Data Feasibility | [1-5] | [1-2 sentences] |
| Schema Risk | [1-5] | [1-2 sentences] |
| **Composite** | **[product]** | |

## Recommendation

**[BUILD / INVESTIGATE / KILL]**

[2-3 sentences explaining the recommendation. If INVESTIGATE, specify which experiment type (Sample Query, Manual Pipeline, or Schema Prototype) and what it would test. If KILL, state what new evidence would reopen the idea.]

## Next Steps

[2-3 specific actions with owners if known]
```

## Final Check

Before saving, verify:
- [ ] Problem statement describes a decision, not a data request
- [ ] At least one workaround is documented with specific time costs
- [ ] All 5 scorecard dimensions are scored with reasoning
- [ ] Recommendation matches the composite score thresholds (250+ = Build, 100-249 = Investigate, <100 = Kill)
- [ ] Data Feasibility score of 1 results in Kill regardless of composite
- [ ] Next steps are specific and actionable
