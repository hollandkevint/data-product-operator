---
name: data-storytelling
version: 0.1.0
description: >
  Data presentation and storytelling for data product operators. Narrative structures,
  chart selection, headline formulas, and anti-patterns. Use when presenting data to
  stakeholders, building a data presentation, writing an executive summary of findings,
  telling a data story, or making a case with data. For stakeholder alignment process,
  see stakeholder-alignment. For metric definitions, see metrics-definition.
user-invocable: false
---

## Headline Formula

Every data finding needs a headline: **[Specific Number] + [Business Impact] + [Actionable Context]**.

"Readmission risk scores now flag 23% more high-risk patients, saving $2.1M annually." Not "We improved our model performance." Not "Results were statistically significant."

The number makes it concrete. The impact makes it relevant. The context makes it actionable.

## Narrative Structures

Pick the structure that matches the situation:

| Structure | When to Use | Shape |
|-----------|------------|-------|
| Problem-Solution | Pitching new work | "Here's the gap, here's what we built" |
| Trend | Status updates | "Here's what changed and why it matters" |
| Comparison | Trade-off decisions | "Here are two options with costs" |

## Narrative Arc for Presentations

**Hook** (the surprise or gap) → **Context** (what the audience needs to know) → **Evidence** (the data, 2-3 charts max) → **Implication** (so what?) → **Recommendation** (now what?)

Start with the finding, not the methodology. Executives care about the answer. They'll ask about the method if they want it.

## Chart Selection

Match the metric type to the right chart:

| Metric Type | Chart | Example |
|-------------|-------|---------|
| Counts | Bar chart | Monthly patient encounters |
| Rates over time | Line chart | 30-day readmission rate by quarter |
| Part-of-whole | Stacked bar | Claim denials by category |
| Distribution | Histogram or box plot | Length of stay distribution |
| Correlation | Scatter plot | Cost vs complexity score |
| Ranking | Horizontal bar | Top 10 diagnoses by volume |

NEVER use pie charts. Stacked bar does everything a pie chart does, with readable labels.

NEVER use dual Y-axes. Two metrics, two charts. Dual axes let you imply any correlation by scaling the axes.

ALWAYS label data directly on the chart. A legend across the room is useless.

## Presentation Anti-Patterns

**Charts without a "so what."** Every chart needs a headline that states the finding. "Figure 3: Revenue by Region" tells the audience nothing. "Northeast revenue dropped 12% after formulary change" tells them what to see.

**Data dumps disguised as analysis.** 47 metrics on one slide helps no one. Pick the 2-3 numbers that matter and make them big.

**Leading with methodology.** "We used a logistic regression with 47 features and cross-validated using..." Save it for the appendix. Lead with the result.

**Hiding bad news in an appendix.** If the data tells an inconvenient story, put it up front. Credibility compounds faster than any dashboard metric.

## Cross-References

For stakeholder alignment process (getting agreement on what to build), see `stakeholder-alignment`. For metric definitions (what exactly does this number mean?), see `metrics-definition`. This skill covers how to present the results.
