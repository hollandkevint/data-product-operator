# Data Product Operator

Skills and commands for data product managers working in Claude Code.

This plugin encodes practitioner knowledge for building data products, with a focus on healthcare data. It provides background skills (auto-activated) and slash commands (user-invoked) that cover the full data product lifecycle.

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

Multiple skills may activate simultaneously. They reinforce each other:

- `data-product-thinking` provides the decision framework (value-first, 5-risk model)
- `data-quality-assessment` provides quality scoring (5 dimensions)
- `metrics-definition` provides metric precision (outcome trees, naming rules)
- `stakeholder-alignment` provides translation patterns (technical to business)
- `data-team-operating-model` provides team structure (squads, cycles, handoffs)
- `data-model-design` provides schema guidance (star schema, dimensional modeling)
- `healthcare-data-domain` provides clinical data context (FHIR, OMOP, terminology)
- `ethical-risk-assessment` provides governance practices (bias testing, phased rollout)

When skills overlap, they cross-reference rather than duplicate. For example, `ethical-risk-assessment` says "For quality scoring details, see `data-quality-assessment`" rather than repeating the 5-dimension model.

## Skill Writing Rules

For contributors adding or modifying skills:

- YAML frontmatter: `name`, `description` (with trigger phrases), `user-invocable: false`, `version`
- Body: 50-80 lines for foundational skills, 80-100 lines for domain skills
- Imperative voice: "Write", "Avoid", "Include"
- Use ALWAYS/NEVER/CRITICAL for non-negotiable rules
- Cross-reference related skills by name instead of duplicating content
- Include concrete examples. Name real products, cite specific numbers
