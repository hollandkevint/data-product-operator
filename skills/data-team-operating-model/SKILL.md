---
name: data-team-operating-model
version: 0.1.1
description: >
  Team structure and operating rhythm for data product teams. Product squads,
  Shape Up 6-week cycles, handoff contracts, and role assignments by lifecycle
  stage. Use when organizing a data team, planning data product development cycles,
  defining roles and responsibilities, improving team handoffs, or when someone asks
  "how should we structure our data team?" or "why do we keep losing context between
  discovery and delivery?"
user-invocable: false
---

## Product Squad Structure

Use this four-role model as one option. Fit accountabilities to the actual team and decision rights; one person may cover several roles.

| Role | Owns | Veto Authority |
|------|------|---------------|
| Product Manager | Strategy, prioritization, stakeholder alignment | Business viability |
| Tech Lead | Architecture, infrastructure, technical feasibility | Technical direction |
| Design Lead | UX, usability, information design | User experience |
| Data Lead | Data quality, ethics, data engineering | Ethical concerns |

Agree on escalation and stop-work rights with the organization. This example does not grant veto authority or replace clinical, privacy, security or operational owners.

## Shape Up for Data Teams

Consider Shape Up when bounded project bets fit the work. Keep the existing cadence when it serves the team; incident response and regulatory deadlines may need different rhythms. The following is an example, not a required schedule.

**Cycle structure:**
- 2 weeks shaping (before the cycle): PM and Data Lead define the problem, set the appetite
- 6 weeks building (the cycle): squad executes with fixed time, variable scope
- 2 weeks cooldown: bug fixes, tech debt, exploration, skill development

**Shaping artifacts:**
- Problem statement with evidence
- Appetite: how much time is this problem worth? (not an estimate, a budget)
- Solution sketch: directional, not detailed
- Rabbit holes: known risks that could blow up the timeline
- No-gos: things explicitly excluded from this cycle

**Hill Charts over burndown charts.** Track progress as "figuring it out" (uphill) vs "getting it done" (downhill). Data products spend more time uphill than software products because data surprises are constant.

**Scope hammering:** When you discover the problem is bigger than the appetite, narrow the scope. Don't extend the timeline. Ask: "What is the smallest version that delivers value?"

## Role x Lifecycle Matrix

Who leads, supports, and consults at each stage:

| Stage | PM | Tech Lead | Design Lead | Data Lead |
|-------|-----|-----------|-------------|-----------|
| Discover | Lead | Consult | Support | Support |
| Decide | Lead | Support | Support | Support |
| Build | Support | Lead | Support | Lead |
| Test | Consult | Support | Support | Lead |
| Ship | Lead | Lead | Support | Support |
| Evaluate | Lead | Consult | Support | Lead |

"Lead" means accountable for the output. "Support" means contributing work. "Consult" means providing input when asked.

## Handoff Contracts

Every stage transition requires a handoff contract:

- **From**: Which role is handing off
- **To**: Which role is receiving
- **Required context**: What information must be included
- **Quality gates**: What conditions must be met before handoff
- **Trigger**: What event initiates the next stage

Example: Discovery -> Decide handoff:
- From: PM + Data Lead
- To: Full squad
- Required: Problem brief with evidence, data availability assessment, ethical screening
- Quality gates: Decision-relevant evidence reviewed, contradictions and blocking constraints named, and an accepting owner identified; no universal interview-count threshold
- Trigger: Shaping session scheduled

NEVER hand off without context documentation. "I'll explain it in the meeting" is how context dies.

## Common Anti-Patterns

- **Engineering-first culture**: Tools and pipelines get prioritized over product outcomes. Fix by requiring a problem brief before any technical work starts.
- **Everything is urgent**: No prioritization framework means the loudest voice wins. Fix with a betting table and explicit appetite setting.
- **Tribal knowledge**: 1-2 people hold all context. When they leave, months of onboarding follow. Fix with handoff contracts and ADRs.
- **40 hours/week firefighting**: Quality issues consume all engineering capacity. Fix with circuit breakers and quality-first pipeline design (see `data-quality-assessment`).
