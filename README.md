# Data Product Operator

Claude Code skills for data product managers. Product thinking meets data engineering.

## What's a Data Product Operator?

A data product operator treats data like a product, not a project. That means defining success metrics before data requirements, building quality into pipelines instead of testing it in, and shipping value to consumers on a cadence. This plugin gives Claude the domain knowledge to help you do that.

## Install

```bash
claude plugins add hollandkevint/data-product-operator
```

## Skills

Background skills activate automatically when Claude detects relevant context. You don't invoke them directly.

| Skill | What It Does |
|-------|-------------|
| `data-product-thinking` | Frames problems as data products. Value-first thinking, 5-risk evaluation model, outcome metric trees. |
| `data-quality-assessment` | Systematic quality evaluation across 5 dimensions: completeness, accuracy, timeliness, consistency, validity. |
| `stakeholder-alignment` | Translates between technical data teams and business stakeholders. Shapes requests into buildable specs. |
| `data-model-design` | Star schema, dimensional modeling, OMOP CDM patterns. When to denormalize, how to handle slowly changing dimensions. |
| `metrics-definition` | Defines metrics with precision: numerator/denominator, grain, time window, edge cases, naming conventions. |
| `data-team-operating-model` | Squad structure, Shape Up 6-week cycles for data teams, handoff contracts, role assignments by lifecycle stage. |
| `healthcare-data-domain` | FHIR, OMOP, HL7, clinical terminology (ICD-10, SNOMED, CPT, LOINC, RxNorm), claims data patterns. |
| `ethical-risk-assessment` | Bias audit protocols, phased rollout governance, ethics canvas for ML features, HIPAA scope awareness. |

## Commands

Slash commands are explicit workflows you invoke when you need structured output.

| Command | What It Does | Output |
|---------|-------------|--------|
| `/dpo:write-data-prd <product>` | Guided PRD creation with data-specific sections: consumer contracts, quality SLAs, schema direction | `data-prd-<name>.md` |
| `/dpo:review-data-quality <source>` | 5-dimension quality scorecard with scoring rubric and improvement recommendations | `quality-review-<name>.md` |
| `/dpo:write-stakeholder-brief` | Translates technical data work into a 1-page business summary with impact metrics | `stakeholder-brief-<name>.md` |
| `/dpo:review-data-model <file>` | Evaluates schema design for normalization, naming, relationships, and extensibility | Conversational |
| `/dpo:reshape-sprint` | Converts sprint artifacts into a shaped pitch: problem, appetite, solution, rabbit holes, no-gos | `shaped-pitch-<name>.md` |

## For Healthcare Data Teams

Two skills are built specifically for healthcare data products:

**`healthcare-data-domain`** covers FHIR resource types, OMOP CDM table relationships, clinical terminology systems, and healthcare-specific data quality patterns. It activates when your conversation involves EHR data, claims, clinical terminology, or OMOP.

**`ethical-risk-assessment`** includes HIPAA-aware governance patterns, algorithmic bias testing for clinical models, and phased rollout protocols for healthcare AI features.

Both skills stay inactive for non-healthcare data products. Every other skill uses healthcare as a primary example but works for any data domain.

## Go Deeper

This plugin encodes practices from the **Data Product Operating System (DPOS)**, a framework for building data products that actually ship.

- [DPOS Blog Series](https://kevintholland.com) - The thinking behind the practices
- [DPOS Assessment](https://kevintholland.com) - Score your data team's maturity across 4 dimensions

Built by [Kevin Holland](https://kevintholland.com) ([LinkedIn](https://linkedin.com/in/kevintholland)) - data product leader, healthcare data nerd.

## Contributing

PRs welcome. If you build data products and have patterns that should be encoded here, open an issue or submit a skill.

Skills should follow the conventions in [CLAUDE.md](CLAUDE.md): 50-100 lines, imperative voice, concrete examples, no consultant-speak.

## License

MIT. See [LICENSE](LICENSE).

This plugin provides general guidance for data product management. It is not a substitute for clinical, legal, or regulatory expertise. Healthcare-specific skills reflect common patterns but do not constitute compliance advice.
