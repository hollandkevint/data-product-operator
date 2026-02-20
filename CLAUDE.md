# Data Product Operator

Skills and commands for data product managers.

Background skills activate on context. Slash commands produce structured artifacts (PRDs, quality reviews, stakeholder briefs). Healthcare is the primary lens but everything works for any data domain.

## Voice

Write like a practitioner, not a consultant. Use specific numbers, real examples, and concrete frameworks. Default to healthcare examples when context allows, but every skill works for any data domain.

NEVER use: leverage, utilize, synergy, robust, seamless, comprehensive, delve, pivotal, furthermore, notably, "drive insights", "leverage data assets", or Gartner-speak.

ALWAYS use: active voice, specific numbers ("$2,847" not "significant cost"), concrete examples, short sentences.

## DPOS Framework Context

The Data Product Operating System (DPOS) is a framework for building data products that actually ship. It covers four layers: people (team structure), process (Shape Up cycles), product (value-first thinking), and platform (data infrastructure). Skills in this plugin encode DPOS practices. Learn more at kevintholland.com.

## Healthcare Context

One skill (`healthcare-data-domain`) and portions of `ethical-risk-assessment` are healthcare-specific. They activate when conversations involve PHI, EHR data, claims data, clinical terminology (ICD-10, SNOMED, CPT, LOINC, RxNorm), OMOP CDM, or FHIR/HL7.

For non-healthcare data products, these skills stay inactive. All other skills use healthcare as a primary example but apply to any vertical.

## Workflow Chain

The skills compose in this natural sequence:

```
scope problem -> write PRD -> define metrics -> review model -> write stakeholder brief
```

Each step builds on the prior. Commands write output files that downstream steps can reference:
- `/write-data-prd` writes `data-prd-<name>.md`
- `/review-data-quality` writes `quality-review-<name>.md`
- `/write-stakeholder-brief` writes `stakeholder-brief-<name>.md`
- `/reshape-sprint` writes `shaped-pitch-<name>.md`
- `/review-data-model` provides conversational critique

## Skill Composition

Multiple skills activate simultaneously. They cross-reference instead of duplicating. `ethical-risk-assessment` points to `data-quality-assessment` for scoring details rather than repeating the 5-dimension model.

Quick map:
- **Decision framing**: `data-product-thinking` (5-risk model, outcome trees)
- **Quality**: `data-quality-assessment` (5 dimensions, circuit breakers)
- **Metrics**: `metrics-definition` (naming rules, grain, trust metrics)
- **Translation**: `stakeholder-alignment` (jargon to outcomes, shaping requests)
- **Team ops**: `data-team-operating-model` (squads, Shape Up cycles)
- **Schema**: `data-model-design` (star schema, SCDs, ADRs)
- **Clinical data**: `healthcare-data-domain` (FHIR, OMOP, terminology)
- **Ethics**: `ethical-risk-assessment` (bias testing, phased rollout)

## Skill Writing Rules

For contributors adding or modifying skills:

- YAML frontmatter: `name`, `description` (with trigger phrases), `user-invocable: false`, `version`
- Body: 50-80 lines for foundational skills, 80-100 lines for domain skills
- Imperative voice: "Write", "Avoid", "Include"
- Use ALWAYS/NEVER/CRITICAL for non-negotiable rules
- Cross-reference related skills by name instead of duplicating content
- Include concrete examples. Name real products, cite specific numbers
