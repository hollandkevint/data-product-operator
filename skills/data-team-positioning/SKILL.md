---
name: data-team-positioning
version: 0.1.0
description: >
  Position data teams as strategic partners, not order-takers. The organizational
  "why" behind doing discovery work. Use when discussing team positioning, value
  exchange, demand shaping, escaping the order-taker trap, or when someone asks
  "how do we stop being order-takers?" or "how does the data team become strategic?"
user-invocable: false
---

## Three Stances

Data teams operate in one of three positions. Most are stuck at position 1.

### 1. Request Taker

"Tell us what to build." The backlog is a queue of stakeholder requests. Prioritization is based on who asked loudest or most recently. The team is measured on throughput: stories completed, dashboards shipped, tickets closed.

**Why it fails:** The team builds what was asked for, not what's needed. No discovery means no understanding of the actual problem. Stakeholders lose trust when delivered products don't solve their real need.

### 2. Request Shaper

"You asked for X, here's why Y is better." The team pushes back on requests, translating vague asks into buildable specs. Uses `stakeholder-alignment` patterns to reframe requests around decisions and outcomes.

**Why it's not enough:** Still reactive. The team only works on problems that stakeholders bring to them. Important problems that stakeholders don't know to ask about go unsolved.

### 3. Demand Shaper

"We interviewed 15 stakeholders, here are the top 3 problems." The team runs its own discovery. Consumer evidence drives prioritization, not stakeholder politics. The team with the most evidence has the most influence.

**This is the target.** Discovery work (`data-consumer-discovery`) IS the positioning mechanism. You don't ask for a seat at the table. You bring the data that makes the table's decisions better.

## Evidence as Currency

In organizations, influence follows evidence. The team that can say "we talked to 15 consumers and the #1 pain point is X, costing $200K/year in manual workarounds" outranks the team that says "we think we should build Y."

Build evidence systematically:
- Run discovery cycles quarterly (see `data-consumer-discovery`)
- Synthesize findings into problem briefs (see `research-synthesis-data`)
- Score opportunities against the validation scorecard (see `data-product-validation`)
- Present ranked opportunities at the betting table with evidence attached

The discovery practice is not overhead. It is the single highest-leverage activity for team positioning.

## Betting Table Pitch Structure

When presenting data product opportunities to leadership:

**Problem** (2-3 sentences): State the problem with consumer quotes and workaround evidence. "Regional analytics leads spend 15+ hours/week manually reconciling reports across 3 systems. Quote from Sarah, Analytics Lead: 'I don't trust the automated numbers, so I rebuild everything in Excel.'"

**Appetite** (1 sentence): Time budget, not estimate. "We'd bet 4 weeks of one squad on this." Appetite caps investment. If it can't be solved within the appetite, reshape the scope.

**Tradeoff** (1 sentence): What you won't build to fund this. "This means we defer the executive dashboard refresh to next cycle." Every yes is a visible no to something else.

NEVER pitch without evidence. A pitch backed by "we think" loses to a pitch backed by "we observed." Discovery is the investment that makes every other investment smarter.

## Anti-Patterns

Recognize these signs that a team is stuck at position 1:

- **No discovery before sprint planning.** The team plans what to build without talking to consumers first.
- **Backlog populated entirely by requests.** Zero items originated from the data team's own research.
- **Measured on throughput, not outcomes.** Success = stories completed, not decisions enabled or time saved.
- **"Urgent" bypasses prioritization.** Any stakeholder can jump the queue by saying it's urgent. No evidence required.
- **Team can't articulate top 3 consumer problems.** If you ask the data team "what are your consumers' biggest pain points?" and they answer with their backlog instead of with evidence, they're order-takers.

Each anti-pattern has a specific remedy:
- No discovery → Schedule 3 consumer interviews this week
- Request-only backlog → Reserve 20% of capacity for team-originated work
- Throughput metrics → Add one outcome metric to the team scorecard
- Urgency bypass → Require evidence (workaround, usage data, or 3 consumer quotes) for priority overrides
- Can't name problems → Run `/dpo:run-discovery` on your most-used data product
