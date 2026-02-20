---
name: data-consumer-discovery
version: 0.1.0
description: >
  Discover what internal data consumers actually need. Adapted Mom Test and JTBD
  for data teams. Use when conducting user research, interviewing stakeholders,
  gathering consumer requirements, running discovery sessions, or when someone asks
  "what do they need?" or "how do I figure out what to build?"
user-invocable: false
---

## Five Discovery Questions

Ask these in order. Each builds on the prior answer:

1. **"What decision are you trying to make?"** Not "what data do you need?" Data requests are solutions. Decisions are the actual problem. If they say "I need a dashboard," ask what decision the dashboard enables.

2. **"Walk me through the last time you made this decision."** Concrete past behavior beats hypothetical future needs. Listen for: where the data came from, how long it took, what they trusted, what they second-guessed.

3. **"Where did the data come from? How much did you trust it?"** Trust is the adoption barrier for data products. A perfect pipeline that nobody trusts is useless. Map their trust signals: source familiarity, recency, whether they cross-checked.

4. **"What did you end up doing?"** The action reveals the real need. "I exported to Excel and manually combined three reports" tells you more than any requirements document.

5. **"If you could get this answer in under a minute, what changes?"** Gauges impact. If the answer is "nothing much," the problem isn't painful enough to build for. If it's "we could catch billing errors before they go out," you have a validated need.

NEVER ask "what data do you want?" or "what would you like us to build?" These questions produce wish lists, not validated needs. The Mom Test applies to data teams: talk about their life, not your product.

## Workaround Archaeology

The strongest discovery signal is existing workarounds. If an analyst built a 47-tab Excel workbook, that's a validated need with proven demand.

For every workaround you find, document:
- **Tool**: What they built it in (Excel, Python script, manual process)
- **Frequency**: How often they use it (daily = high demand)
- **Time cost**: Hours per week maintaining it
- **Trust level**: Do they trust their own workaround? Why or why not?
- **Downstream dependents**: Who else uses the output?

Workarounds with daily frequency and downstream dependents are the highest-signal discovery findings. Build for these first.

## Consumer Segments

Data consumers fall into four segments. Each needs different product shapes:

| Segment | Need | Product Shape |
|---------|------|---------------|
| **Explorers** | Flexible query access, iterate fast | Self-serve query tools, semantic layer |
| **Reporters** | Scheduled, consistent outputs | Automated reports, dashboards with alerts |
| **Decision-makers** | One number with context | Executive summaries, scorecards, red/yellow/green |
| **Builders** | Reliable APIs and tables | Documented APIs, data contracts, SLAs |

ALWAYS identify which segment you're building for before writing requirements. A product that tries to serve all four serves none.

## Trust Barrier Assessment

Ask: "What would make you NOT trust this output?"

Common trust barriers in data products:
- **Source opacity**: "I don't know where the numbers come from"
- **Stale data**: "This was true yesterday but what about right now?"
- **Conflicting numbers**: "Your dashboard says 10K, the other report says 12K"
- **No validation path**: "I can't check if this is right"
- **Past incidents**: "Last time we used this, the numbers were wrong"

Map each barrier to a specific `data-quality-assessment` dimension. Trust barriers are quality problems experienced from the consumer's perspective.

## Signal Strength

Rank evidence before acting on it:

- **Strong** (build): Observed workarounds with time investment + multiple consumers reporting same pain. Requires: workaround documentation + 3 independent data points.
- **Moderate** (investigate): 3+ quotes describing same problem, or usage data showing repeated manual queries. Requires: pattern across sources, not just one loud voice.
- **Emerging** (watch): 1-2 mentions, no observed behavior change. Requires: nothing yet.

NEVER build on Emerging signals. Moderate signals justify a 1-day experiment (see `data-product-validation`). Strong signals justify a shaped pitch.
