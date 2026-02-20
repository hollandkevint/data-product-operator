---
description: Generate a complete data product requirements document with data-specific sections
argument-hint: <product name or brief description>
allowed-tools: Read, Write, AskUserQuestion
---

# Write a Data Product PRD

Generate a requirements document for a data product. This is not a standard software PRD. Data products require sections for data lineage, quality SLAs, consumer contracts, and ethical considerations that typical PRDs skip.

## Gather Context

If `$ARGUMENTS` provides a product name or description, use it. Otherwise, ask:

**Question 1:** What data product are you building? Describe the problem it solves.

**Question 2:** Who consumes the output? Options: analysts, clinicians, executives, data scientists, external API consumers, end users.

**Question 3:** What data sources are involved? List the databases, APIs, files, or systems this product depends on.

**Question 4:** What are the quality requirements? Consider: maximum acceptable latency, accuracy threshold, data freshness SLA, uptime requirement.

## Write the PRD

Write the document to `data-prd-<name>.md` where `<name>` is a kebab-case version of the product name.

Use this structure:

### 1. Problem Statement

State the problem in one paragraph. Include:
- Who has this problem (specific role, not "users")
- What they currently do (the workaround)
- Evidence the problem is real (customer quotes, usage data, support tickets)
- What success looks like (measurable outcome)

NEVER write a problem statement without evidence. "We think users want X" is not a problem statement.

### 2. Data Sources and Lineage

For each data source:
- Source system name and type (database, API, file, stream)
- Refresh frequency (real-time, hourly, daily, batch)
- Volume estimate (rows/day, GB)
- Known quality issues
- Access method and credentials needed

Include a lineage diagram showing source -> transformation -> output flow.

### 3. Consumer Contracts

For each consumer of this data product:
- Who they are (role or system name)
- What format they need (API, file, dashboard, embedded)
- What SLA they expect (latency, freshness, uptime)
- What schema/fields they require
- How they access it (pull vs push, auth method)

### 4. Quality Requirements

Score targets across 5 dimensions (see `data-quality-assessment` skill):
- Completeness target (e.g., <1% null rate in required fields)
- Accuracy target (e.g., 99.9% match against gold standard)
- Timeliness target (e.g., data available within 15 minutes of source update)
- Consistency target (e.g., single metric definition across all consumers)
- Validity target (e.g., all business rules enforced at ingestion)

Include circuit breaker thresholds: at what quality level does the pipeline stop and alert?

### 5. Schema Design Direction

Describe the target data model at a high level:
- Key entities and relationships
- Fact vs dimension table split (if star schema)
- Grain of the primary fact table
- Slowly changing dimension strategy
- Denormalization decisions and rationale

Do not write DDL at this stage. Directional guidance only.

### 6. Success Metrics

Build an outcome metric tree:
- **Business outcome** - The organizational goal this serves (e.g., reduce readmissions 10%)
- **Product outcome** - What the data product enables (e.g., clinical decisions 3x faster)
- **Feature outcome** - What the feature delivers (e.g., risk scores updated in real-time)
- **Leading indicator** - What you can measure early (e.g., query latency under 1 second)

Include trust metrics: data accuracy rate, query response time, support response time.

### 7. Risks and Mitigations

Evaluate all 5 risks (see `data-product-thinking` skill):
- **Value risk** - Will consumers actually use this? What evidence do we have?
- **Usability risk** - Can consumers find and understand the data without training?
- **Feasibility risk** - Can we build this with current infrastructure and data access?
- **Business viability risk** - Does this justify the investment?
- **Ethical data risk** - Any bias, privacy, or fairness concerns?

For each risk rated Medium or High, include a specific mitigation.

### 8. Ethical Considerations

If the data product involves personal data, ML models, or decision support:
- What bias could exist in the training data or source data?
- What demographic groups could be affected differently?
- What transparency is required (explain how the model works)?
- What privacy protections are needed (de-identification, access controls)?
- Who has veto authority if ethical concerns arise?

If none of these apply, state "No ethical considerations identified" with a brief justification.

## Final Check

Before saving, verify:
- [ ] Problem statement has evidence, not assumptions
- [ ] Every data source has a quality assessment
- [ ] Every consumer has a defined contract
- [ ] Quality targets are numeric, not vague ("high quality")
- [ ] Success metrics trace from business outcome to leading indicator
- [ ] All 5 risks are evaluated
- [ ] Ethical section is present (even if minimal)
