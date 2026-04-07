---
name: arbitrage-audit-data
version: 0.1.0
description: >
  3 diagnostic questions for evaluating data product markets through the arbitrage gap
  lens. Identifies whether your data product sits on a durable or closing advantage.
  Use when assessing data product positioning, evaluating market risk, or when someone
  asks "is AI going to replace this?" or "what's our moat?"
user-invocable: false
---

## The 3 Questions (Data Product Context)

### Question 1: What inefficiency is this data product built on?

Every data product sits on top of a gap. Name it:

| Gap Type | Data Product Example | Closing Speed |
|----------|---------------------|---------------|
| **Knowledge asymmetry** | "Only our analysts know how to calculate this metric" | Fast — AI can learn metric definitions |
| **Fragmentation** | "Data lives in 5 systems nobody has connected" | Medium — integration tools accelerating |
| **Speed** | "This report takes 3 days of manual SQL" | Fast — automation and agents |
| **Discipline** | "People skip the quality checks" | Medium — AI can enforce process |
| **Judgment** | "Someone needs to decide which cohort definition is clinically valid" | Slow — requires domain expertise |
| **Relationship** | "The client trusts our interpretation, not just the numbers" | Slow — fundamentally human |

Ask: "If a competitor had the same data and unlimited AI, what would still be hard for them to replicate?"

### Question 2: How fast can AI close this gap?

**Informational data products** (reports, dashboards, automated queries) face fast closure. If your data product's value is "we run the SQL so you don't have to," the clock is ticking.

**Judgment data products** (cohort validation, clinical interpretation, business context) face slow closure. If your data product's value is "we know what this number means for YOUR situation," that's durable.

Specific data product signals:

| Signal | Gap Closing | Action |
|--------|-------------|--------|
| Consumer could get the same answer from ChatGPT + raw data | Fast | Migrate to judgment layer |
| Consumer needs your domain expertise to interpret results | Slow | Encode and protect that expertise |
| Consumer uses your output as input to another automated system | Fast | The consuming system will eventually skip you |
| Consumer uses your output to make human decisions | Slow | Double down on decision context |

### Question 3: What new gap opens when this one closes?

When AI closes the "generate the report" gap, the new gap is: "who decides if this report is answering the right question?"

When AI closes the "connect the data sources" gap, the new gap is: "who decides what the connected data means for this specific business context?"

**For data teams:** The upstream gap is always decision architecture — knowing what to measure, why, and what to do with the answer. That's where `data-team-positioning` (demand-shaper stance) lives.

## Output

```markdown
# Data Product Arbitrage Audit: [Product Name]
Date: [date]

## The Gap
[What inefficiency this product is built on]

## Gap Type & Closing Speed
[Type] — [Fast/Medium/Slow] — [rationale]

## Upstream Gap
[What becomes the new bottleneck]

## Position Assessment
[Closing gap → migrate. Durable gap → encode and protect.]

## Recommended Action
[One specific thing]
```

Based on Nate Jones' Arbitrage Gap Framework. Generic version: [decision-architecture](https://github.com/hollandkevint/decision-architecture).

---

Part of the [Data Product Operator](https://github.com/hollandkevint/data-product-operator) plugin.
