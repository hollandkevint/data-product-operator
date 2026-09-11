# Data Product Operator

An operating system for data leaders and data product managers: Decide what is worth building, help a team deliver it, and check whether it changed the outcome.

Built by [Kevin Holland](https://kevintholland.com), from his Data Product Operating System (DPOS) practices. Start with one decision. Grow into a repeatable way to manage products, evidence, team handoffs and portfolio choices.

**[Start with Data Product Operator](skills/data-product-operator/SKILL.md)** · [Explore the skills](#core-skills) · [Choose a domain pack](#domain-application-packs)

This OS is a set of reusable instructions and linked work records. It does not require a new database or replace your project tracker. Use it as a worksheet or with an approved AI assistant; your company context and decisions stay in your own workspace.

## Start where your work is stuck

| You need to… | Start with | Leave with |
|---|---|---|
| Turn an incoming request into a product decision | [Data Product Operator](skills/data-product-operator/SKILL.md) | Intended outcome, consumer, evidence gap and next decision |
| Understand what consumers need | [Consumer discovery](skills/data-consumer-discovery/SKILL.md) | Observed workflow, attempted alternatives and an evidence-backed problem |
| Decide whether to invest | [Product validation](skills/data-product-validation/SKILL.md), [question a plan](skills/grill-me-data/SKILL.md) | Assumptions, constraints and a bounded next bet |
| Know whether an analysis supports a conclusion | [Analyst](skills/analyst/SKILL.md) | A linked path from definitions and sources to checks and decisions |
| Improve ownership and handoffs | [Team operating model](skills/data-team-operating-model/SKILL.md) | Accountabilities and handoff conditions fitted to your team |
| Explain what changed and what to do next | [Stakeholder alignment](skills/stakeholder-alignment/SKILL.md), [storytelling](skills/data-storytelling/SKILL.md) | A decision brief with evidence, limits and an owner |

## An OS you can grow into

Adopt the next layer when coordination requires it. These are ways to use the library, not maturity scores or a required rollout.

| Scope | Keep track of | Add when needed |
|---|---|---|
| One decision | Consumer, intended outcome, next question and owner | One relevant skill and a short brief |
| One data product | Definitions, source versions, checks, decisions and follow-up | Analyst evidence graph and a product handoff |
| One team | Current bets, capacity, receiving owners and recurring problems | A review cadence and agreed stop/rework conditions |
| A portfolio | Product owners, consumers, outcomes, cost and dependencies | A comparison of which products to invest in, maintain or retire |

Keep the operating loop visible:

**Understand the need → choose a bounded bet → define and build → verify and hand off → observe use → revise or retire.**

For each handoff, name the trigger, receiving owner, evidence needed and what happens if it is missing. A scheduled meeting is not a completed loop. Close a loop when someone has reviewed the result and made the next decision.

## Core skills

A skill is a Markdown file of instructions. Choose the job first, then add domain and platform guidance. Links open the skill directly; no installation is needed to read it.

| Job | Skills |
|---|---|
| Understand the problem | [Consumer discovery](skills/data-consumer-discovery/SKILL.md), [research synthesis](skills/research-synthesis-data/SKILL.md), [dashboards to decisions](skills/dashboards-to-decisions/SKILL.md) |
| Decide what to build | [Data product thinking](skills/data-product-thinking/SKILL.md), [product validation](skills/data-product-validation/SKILL.md), [question a data-product plan](skills/grill-me-data/SKILL.md), [market advantage review](skills/arbitrage-audit-data/SKILL.md) |
| Define and check the data | [Metric definitions](skills/metrics-definition/SKILL.md), [quality assessment](skills/data-quality-assessment/SKILL.md), [model design](skills/data-model-design/SKILL.md), [pipeline quality](skills/data-pipeline-quality/SKILL.md), [ethical risk assessment](skills/ethical-risk-assessment/SKILL.md) |
| Coordinate and explain | [Stakeholder alignment](skills/stakeholder-alignment/SKILL.md), [team operating model](skills/data-team-operating-model/SKILL.md), [team positioning](skills/data-team-positioning/SKILL.md), [storytelling](skills/data-storytelling/SKILL.md) |

Some older skills contain domain examples and scoring rubrics. Use the consumer's domain and intended-use criteria. Scores are discussion aids, not validated readiness measures or universal release thresholds.

### Connect evidence with Analyst

[Analyst](skills/analyst/SKILL.md) links a question to its definition, source snapshots, checks, findings, owner decision and follow-up observation. It routes to existing skills as needed.

Use Markdown records or the included JSON shape. A small checker validates references and selected state rules and identifies downstream records to review when an input changes. It does not verify evidence contents or approve release.

[Read the graph instructions](skills/analyst/SKILL.md) · [See a fictional graph](skills/analyst/example.json) · [Run the checks and read the limits](docs/analyst-testing.md)

## Domain application packs

The operating model stays the same. Domain packs add the definitions, edge cases and review boundaries that change a decision.

| Domain | Applications | Current depth |
|---|---|---|
| [Healthcare](docs/healthcare-applications.md) | Quality reporting, trial feasibility, claims, billing, record pulls, mapping and patient operations | Dedicated skills, ten application routes and worked examples |
| [Marketing data](docs/domain-applications.md#marketing-data) | Campaign measurement, funnel definitions, attribution and audience delivery | Application guide using core skills |
| [Logistics and operations](docs/domain-applications.md#logistics-and-operations) | Delivery performance, shipment events, inventory and service operations | Application guide using core skills |
| [Ecommerce](docs/domain-applications.md#ecommerce) | Revenue, orders, returns, conversion and customer cohorts | Application guide using core skills |

The newer application guides are proposed workflows, not claims of domain validation. Add a dedicated skill when repeated use reveals instructions that the core library cannot cover.

### Healthcare pack

| Start when… | Skill | What you get |
|---|---|---|
| Data preparation took more work than expected | [Readiness debrief](skills/healthcare-data-readiness-debrief/SKILL.md) | What happened, unresolved questions and next checks |
| A population or denominator needs a precise definition | [Cohort design](skills/healthcare-cohort-design/SKILL.md) | Inclusion rules, time windows, coverage and acceptance cases |
| Source records and downstream results disagree | [Data reconciliation](skills/healthcare-data-reconciliation/SKILL.md) | Source-to-output trace, competing explanations and a correction test plan |
| Clinical meaning or mapping needs review | [Healthcare data domain](skills/healthcare-data-domain/SKILL.md) | FHIR, HL7, OMOP and terminology checks with version boundaries |

**Sharing the free debrief? [Send this SKILL.md link](https://github.com/hollandkevint/data-product-operator/blob/main/skills/healthcare-data-readiness-debrief/SKILL.md).** It can be used as a worksheet or with an approved assistant. No patient records, database access or conversation with Kevin is required.

[Complete fictional brief](skills/healthcare-data-readiness-debrief/example.md) · [Twelve synthetic scenarios](skills/healthcare-data-readiness-debrief/examples/scenarios.md) · [Install the standalone debrief](docs/healthcare-data-readiness.md) · [Healthcare applications](docs/healthcare-applications.md)

This pack does not supply licensed measure logic, certify clinical validity or authorize patient-facing actions. Use approved summaries or synthetic examples and involve the responsible professional for consequential decisions.

## Platform skills

| Platform | Skill | What you get |
|---|---|---|
| Databricks | [Data-product review](skills/databricks-data-product-review/SKILL.md) | Version-qualified inputs, access checks, update/replay checks and a release evidence record |
| DuckDB | [Data profiling](skills/duckdb-data-profiling/SKILL.md) | Reproducible local profiling, explicit types, join checks and bounded exports |

Neither skill connects to a system or grants access. Add platform guidance to the chosen workflow without changing its business definition.

## Use it your way

### Read it or use an approved assistant

Open [Data Product Operator](skills/data-product-operator/SKILL.md), describe one decision and supply an approved summary. Ask for the smallest next step. Follow reference links only when needed.

Give an assistant the selected skill and its supporting files. If it cannot open a reference, supply that file separately. A link does not install a skill or prove the assistant read it. The Operator and Analyst entry points compose the library; copying only their entry file omits those linked skills.

### Install the Claude Code library

Run these commands in Claude Code:

```text
/plugin marketplace add hollandkevint/data-product-operator
/plugin install data-product-operator@data-product-operator
```

Start a fresh session and confirm the skills are available. For local development:

```bash
claude --plugin-dir /path/to/data-product-operator
```

Other assistants can read the same Markdown. Host discovery and command registration vary. The standalone healthcare debrief has separate [Codex and Claude instructions](docs/healthcare-data-readiness.md).

## Commands for longer workflows

| Workflow | Expected output |
|---|---|
| [Run discovery](commands/run-discovery.md) | Consumer needs, assumptions and a next experiment |
| [Write a problem brief](commands/write-problem-brief.md) | Ranked problems with supporting evidence |
| [Write a data PRD](commands/write-data-prd.md) | Product requirements, consumer expectations and data requirements |
| [Review data quality](commands/review-data-quality.md) | Quality review and proposed improvements |
| [Review a data model](commands/review-data-model.md) | Schema critique |
| [Write a stakeholder brief](commands/write-stakeholder-brief.md) | A one-page explanation and next decision |
| [Reshape a sprint](commands/reshape-sprint.md) | A bounded project proposal |

In Claude Code, select the installed command from the command menu. Other assistants can read the files as workflow instructions. This repository does not automatically run the operating loop or maintain private memory.

## Repository layout

```text
skills/
  data-product-operator/        Leader/DPM entry point and operating loop
  analyst/                      Evidence graph, example and structural checker
  ...                           Core, domain and platform skills
commands/                       Longer workflow entry points
docs/
  domain-applications.md        Marketing, logistics/ops and ecommerce routes
  healthcare-applications.md    Healthcare application pack
  analyst-testing.md            Checks and explicit limits
.claude-plugin/                 Claude plugin and marketplace metadata
CONNECTORS.md                   Optional integrations
CLAUDE.md                       Contributor and agent guidance
```

The library owns reusable methods. Your existing private workspace owns company context, product records and decisions. Keep personal data, credentials, confidential contracts and restricted materials out of this public repository. [Connectors](CONNECTORS.md) need separate setup and authorization.

## Testing and limits

The Analyst structural checks and five synthetic DuckDB assertions passed locally; see the [recorded checks](docs/analyst-testing.md). Databricks has not been tested against a live workspace. The new Operator entry point and domain application guides have not had independent host-level validation.

The healthcare debrief has [separate invocation tests and limits](skills/healthcare-data-readiness-debrief/CONTEXT.md). No test here establishes production readiness, regulatory acceptance or measured team performance.

## Design references

The organization draws on [PM OS](https://github.com/mohammadrizvi624/pm-os) for separating company context from reusable methods, [PM Skills](https://github.com/phuryn/pm-skills) for job-based catalogs, [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin) for workflow handoffs, [Compound Writing](https://github.com/EveryInc/compound-writing) for a context-first entry point, and [Matt Pocock's skills](https://github.com/mattpocock/skills) for problem-led questioning. These are design references, not dependencies or endorsements.

## Contributing and license

Open an issue describing the task, expected behavior and observed gap. Use synthetic examples. Follow [CLAUDE.md](CLAUDE.md), keep guidance beside its skill, and state what was tested and what remains unverified.

[MIT license](LICENSE).
