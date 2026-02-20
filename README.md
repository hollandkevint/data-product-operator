# Data Product Operator

Claude Code skills for data product managers. Discovery, validation, and delivery for data products.

## What's a Data Product?

A data product is any data asset that someone depends on to make a decision. A risk score that flags patients for readmission. A metrics dashboard that tells a VP which region is underperforming. An API that feeds claims data to a downstream system. If it has consumers, quality expectations, and a reason to exist, it's a data product.

Most data teams ship datasets. A data product operator ships data *products* — with success metrics defined before data requirements, quality built into pipelines instead of tested in after, and value delivered on a cadence instead of thrown over a wall.

## Install

From the Claude Code marketplace:

```
/plugin marketplace add hollandkevint/data-product-operator
/plugin install data-product-operator@data-product-operator
```

For local development:

```bash
claude --plugin-dir /path/to/data-product-operator
```

## Skills

Background skills activate automatically based on context.

| Skill | What It Does |
|-------|-------------|
| `data-consumer-discovery` | Discover what internal data consumers actually need. Mom Test for data teams, workaround archaeology, consumer segments, trust barrier assessment. |
| `data-product-validation` | Score whether a data product idea is worth building. 5-dimension validation scorecard, experiment types, go/investigate/kill thresholds. |
| `research-synthesis-data` | Convert raw discovery notes into structured insights. Atomic research chain, evidence hierarchy, three synthesis outputs. |
| `data-team-positioning` | Position data teams as strategic partners, not order-takers. Three stances, evidence as currency, betting table pitch structure. |
| `data-product-thinking` | Frames problems as data products. Value-first thinking, 5-risk evaluation model, outcome metric trees. |
| `data-quality-assessment` | Systematic quality evaluation across 5 dimensions: completeness, accuracy, timeliness, consistency, validity. |
| `stakeholder-alignment` | Translates between technical data teams and business stakeholders. Shapes requests into buildable specs. |
| `data-model-design` | Star schema, dimensional modeling, OMOP CDM patterns. When to denormalize, how to handle slowly changing dimensions. |
| `metrics-definition` | Defines metrics with precision: numerator/denominator, grain, time window, edge cases, naming conventions. |
| `data-team-operating-model` | Squad structure, Shape Up 6-week cycles for data teams, handoff contracts, role assignments by lifecycle stage. |
| `healthcare-data-domain` | FHIR, OMOP, HL7, clinical terminology (ICD-10, SNOMED, CPT, LOINC, RxNorm), claims data patterns. |
| `data-storytelling` | Presents data findings to stakeholders. Headline formulas, narrative structures, chart selection, anti-patterns. |
| `data-pipeline-quality` | Automated quality checks in pipelines. Testing pyramid, dbt patterns, data contracts, circuit breakers, monitoring. |
| `ethical-risk-assessment` | Bias audit protocols, phased rollout governance, ethics canvas for ML features, HIPAA scope awareness. |

## Commands

| Command | What It Does | Output |
|---------|-------------|--------|
| `/dpo:run-discovery <idea>` | Guided discovery session: consumer interviews, validation scorecard, go/investigate/kill recommendation | `discovery-brief-<name>.md` |
| `/dpo:write-problem-brief <notes>` | Synthesize raw discovery notes into ranked problems with evidence chains and consumer maps | `problem-brief-<name>.md` |
| `/dpo:write-data-prd <product>` | Guided PRD creation with data-specific sections: consumer contracts, quality SLAs, schema direction | `data-prd-<name>.md` |
| `/dpo:review-data-quality <source>` | 5-dimension quality scorecard with scoring rubric and improvement recommendations | `quality-review-<name>.md` |
| `/dpo:write-stakeholder-brief` | Translates technical data work into a 1-page business summary with impact metrics | `stakeholder-brief-<name>.md` |
| `/dpo:review-data-model <file>` | Evaluates schema design for normalization, naming, relationships, and extensibility | Conversational |
| `/dpo:reshape-sprint` | Converts sprint artifacts into a shaped pitch: problem, appetite, solution, rabbit holes, no-gos | `shaped-pitch-<name>.md` |

## Example Workflows

**Discovery to delivery (full chain):**
Start with `/dpo:run-discovery` to interview consumers and score the opportunity. Feed raw notes into `/dpo:write-problem-brief` to rank problems by evidence. The problem brief feeds `/dpo:write-data-prd` for requirements. Continue with `metrics-definition`, `/dpo:review-data-model`, `data-pipeline-quality`, and `/dpo:write-stakeholder-brief` to communicate the plan.

**New data product from scratch:**
Start with `data-product-thinking` to scope the problem, then `/dpo:write-data-prd` to capture requirements. Use `metrics-definition` to nail down success metrics, `/dpo:review-data-model` on your schema, `data-pipeline-quality` to set up tests, then `/dpo:write-stakeholder-brief` to communicate the plan.

**Escape the order-taker trap:**
Use `data-team-positioning` to assess your team's current stance. Run `/dpo:run-discovery` on your most-used data product to build consumer evidence. Use `research-synthesis-data` to structure findings into a betting table pitch. Present ranked opportunities backed by evidence, not opinions.

**Inherited dataset cleanup:**
Run `/dpo:review-data-quality` to score the current state. Use `data-model-design` to evaluate the schema, then `data-pipeline-quality` to add automated checks. Close with `data-storytelling` to present findings to leadership.

**Sprint to Shape Up conversion:**
Run `/dpo:reshape-sprint` on your backlog. The shaped pitch uses `data-product-thinking` to frame appetite and `stakeholder-alignment` to translate for the betting table.

## Connecting Your Data Stack

Commands work better when they can read your live schemas and sprint artifacts. See [CONNECTORS.md](CONNECTORS.md) for setup instructions. No connections required; every command works with manually provided context.

## For Healthcare Data Teams

`healthcare-data-domain` covers FHIR, OMOP CDM, clinical terminology (ICD-10, SNOMED, CPT, LOINC, RxNorm), and healthcare-specific quality patterns. `ethical-risk-assessment` adds HIPAA-aware governance, bias testing for clinical models, and phased rollout protocols.

Both activate only when the conversation involves clinical data. Everything else works for any data domain.

## Go Deeper

Built on the **Data Product Operating System (DPOS)** — a framework for building data products that actually ship.

- [DPOS Blog Series](https://kevintholland.com) — the thinking behind these practices
- [DPOS Assessment](https://kevintholland.com) — score your data team's maturity across 4 dimensions

Built by [Kevin Holland](https://kevintholland.com) ([LinkedIn](https://linkedin.com/in/kevintholland)). 10 years building healthcare data products across 36M patient records.

## Contributing

PRs welcome. If you build data products and have patterns that should be encoded here, open an issue or submit a skill.

Skills follow the conventions in [CLAUDE.md](CLAUDE.md): 50-100 lines, imperative voice, concrete examples, zero consultant-speak.

## License

MIT. See [LICENSE](LICENSE).

General guidance, not compliance advice. Healthcare skills reflect common patterns but are not a substitute for clinical, legal, or regulatory expertise.
