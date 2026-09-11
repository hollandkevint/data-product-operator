# Data Product Operator

An operating system for data leaders and data product managers, with reusable skills, decision records and workflow handoffs. Keep the top-level positioning domain agnostic.

Skill discovery depends on the host. Slash commands produce structured artifacts (PRDs, quality reviews, stakeholder briefs). Core data-product skills apply across domains; use healthcare-specific skills when the project calls for them.

## Voice

Write like a practitioner, not a consultant. Use supported numbers, sourced or clearly synthetic examples, and concrete checks. Use the reader's domain; do not default to healthcare.

NEVER use: leverage, utilize, synergy, robust, seamless, comprehensive, delve, pivotal, furthermore, notably, "drive insights", "leverage data assets", or Gartner-speak.

ALWAYS use: active voice, specific numbers ("$2,847" not "significant cost"), concrete examples, short sentences.

## DPOS Framework Context

The Data Product Operating System (DPOS) covers people, process, product and platform. Start with [Data Product Operator](skills/data-product-operator/SKILL.md) for leader/DPM decisions and a repeatable operating loop. Grow from one decision to a product, team or portfolio only when needed. Shape Up is one process option, not a required cadence. The library supports operating work; it does not autonomously run a company or replace its tracker. Learn more at kevintholland.com.

## Domain and platform context

Keep domain packs below the core OS in navigation. [Domain applications](docs/domain-applications.md) covers marketing data, logistics/operations and ecommerce using core skills. [Healthcare applications](docs/healthcare-applications.md) has additional dedicated skills. State differences in pack depth and testing; do not imply equal maturity.

The healthcare pack includes `healthcare-data-readiness-debrief`, `healthcare-cohort-design`, `healthcare-data-reconciliation`, `healthcare-data-domain` and relevant portions of `ethical-risk-assessment`. Choose the specific job; do not load every healthcare skill automatically.

Platform guidance lives in `databricks-data-product-review` and `duckdb-data-profiling`. Keep the clinical definition separate from execution details. Confirm the environment and authorization before running queries, changing data or exporting results.

Healthcare-specific skills stay inactive for non-healthcare work. Core skills may retain healthcare examples as historical illustrations; adapt them to the current domain without importing clinical assumptions.

## Workflow Chain

The skills compose in this natural sequence:

```
discover consumers -> synthesize findings -> validate demand -> scope problem -> write PRD -> define metrics -> review model -> test pipeline -> tell the story -> write stakeholder brief
```

Each step builds on the prior. Commands write output files that downstream steps can reference:
- `/run-discovery` writes `discovery-brief-<name>.md`
- `/write-problem-brief` writes `problem-brief-<name>.md`
- `/write-data-prd` writes `data-prd-<name>.md`
- `/review-data-quality` writes `quality-review-<name>.md`
- `/write-stakeholder-brief` writes `stakeholder-brief-<name>.md`
- `/reshape-sprint` writes `shaped-pitch-<name>.md`
- `/review-data-model` provides conversational critique

## Skill Composition

Use [Analyst](skills/analyst/SKILL.md) for an explicit evidence graph across skills. Route from the unresolved decision; record definition/source versions, proposed versus executed checks, findings, owner decisions and follow-up observations. [Healthcare applications](docs/healthcare-applications.md) provide domain routes. Keep project evidence outside the public repository. Test graph changes with `python3 skills/analyst/scripts/check_graph.py --self-test`.

Hosts may select several skills or require explicit invocation. They cross-reference instead of duplicating. `ethical-risk-assessment` points to `data-quality-assessment` for scoring details rather than repeating the 5-dimension model.

Quick map:
- **Discovery**: `data-consumer-discovery` (Mom Test for data, workaround archaeology, consumer segments)
- **Validation**: `data-product-validation` (5-dimension scorecard, experiment types, Type 1/2 decisions)
- **Synthesis**: `research-synthesis-data` (atomic research chain, evidence hierarchy, 3 outputs)
- **Team positioning**: `data-team-positioning` (3 stances, evidence as currency, betting table pitches)
- **Decision framing**: `data-product-thinking` (5-risk model, outcome trees)
- **Quality**: `data-quality-assessment` (5 dimensions, circuit breakers)
- **Metrics**: `metrics-definition` (naming rules, grain, trust metrics)
- **Translation**: `stakeholder-alignment` (jargon to outcomes, shaping requests)
- **Team ops**: `data-team-operating-model` (squads, Shape Up cycles)
- **Schema**: `data-model-design` (star schema, SCDs, ADRs)
- **Clinical data**: `healthcare-data-domain` (FHIR, OMOP, terminology)
- **Storytelling**: `data-storytelling` (headlines, narrative arcs, chart selection)
- **Pipeline quality**: `data-pipeline-quality` (dbt tests, contracts, circuit breakers)
- **Ethics**: `ethical-risk-assessment` (bias testing, phased rollout)

## Skill Writing Rules

The standalone `healthcare-data-readiness-debrief` is directly invocable and portable across Codex and Claude. Its frontmatter uses `name`, `description`, and `metadata.version`; do not add `user-invocable: false`. Its longer entrypoint preserves interview and safety boundaries, with domain detail in references. Do not impose maturity scores or dataset access from adjacent skills on this debrief.

For contributors adding or modifying skills:

- New portable skills use `name`, a task-specific `description`, and `metadata.version`. Keep them directly invocable and discoverable. Preserve existing invocation policy unless deliberately changing it.
- Body: 50-80 lines for foundational skills, 80-100 lines for domain skills
- Imperative voice: "Write", "Avoid", "Include"
- Use ALWAYS/NEVER/CRITICAL for non-negotiable rules
- Cross-reference related skills by name instead of duplicating content
- Include concrete examples. Name real products, cite specific numbers
