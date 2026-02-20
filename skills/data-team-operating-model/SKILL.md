---
name: data-team-operating-model
version: 0.1.0
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

Data products need four co-equal roles, not a hierarchy:

| Role | Owns | Veto Authority |
|------|------|---------------|
| Product Manager | Strategy, prioritization, stakeholder alignment | Business viability |
| Tech Lead | Architecture, infrastructure, technical feasibility | Technical direction |
| Design Lead | UX, usability, information design | User experience |
| Data Lead | Data quality, ethics, data engineering | Ethical concerns |

CRITICAL: The Data Lead is co-equal to the PM, not subordinate. They have veto authority on ethical data concerns. This is what distinguishes data product teams from software product teams.

## Shape Up for Data Teams

Six-week cycles replace two-week sprints. Data work has more unknowns than typical software — discovery doesn't stop when building starts.

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
- Quality gates: Problem validated with 3+ customer data points, no blocking constraints
- Trigger: Shaping session scheduled

NEVER hand off without context documentation. "I'll explain it in the meeting" is how context dies.

## Common Anti-Patterns

- **Engineering-first culture**: Tools and pipelines get prioritized over product outcomes. Fix by requiring a problem brief before any technical work starts.
- **Everything is urgent**: No prioritization framework means the loudest voice wins. Fix with a betting table and explicit appetite setting.
- **Tribal knowledge**: 1-2 people hold all context. When they leave, months of onboarding follow. Fix with handoff contracts and ADRs.
- **40 hours/week firefighting**: Quality issues consume all engineering capacity. Fix with circuit breakers and quality-first pipeline design (see `data-quality-assessment`).
