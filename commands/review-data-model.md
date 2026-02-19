---
name: review-data-model
description: Evaluate a data model or schema design for normalization, naming, relationships, and extensibility
disable-model-invocation: true
argument-hint: <file path, DDL, or schema description>
allowed-tools: Read, Bash, AskUserQuestion
---

# Review a Data Model

Evaluate a schema design for a data product. This review covers normalization strategy, naming conventions, relationship design, grain correctness, and extensibility. Output is conversational critique with specific recommendations.

## Gather Context

If `$ARGUMENTS` provides a file path, read it. If it provides DDL or a description, use it directly. Otherwise, ask:

**Question 1:** Share your schema. Options: paste DDL, provide a file path, describe the tables and relationships.

**Question 2:** What is this data product used for? (analytics, reporting, ML features, API serving, operational data store)

**Question 3:** What query patterns matter most? (what questions will consumers ask this data?)

## Review Checklist

Evaluate each area and provide specific feedback:

### 1. Grain Check
- Is the grain of each fact table clearly defined?
- Is there unexpected row multiplication from joins?
- Does the grain match the intended query patterns?

Flag: "This table has one row per [X]. Is that correct? Your query pattern suggests you need one row per [Y] instead."

### 2. Normalization Strategy
- Is the normalization level appropriate for the use case? (OLTP needs 3NF; analytics needs star schema)
- Are there unnecessary joins that could be eliminated with strategic denormalization?
- Are there One Big Table anti-patterns (full denormalization causing row explosion)?

Flag: "This many-to-many relationship between patients and diagnoses will cause [N]x row multiplication if fully denormalized. Use a bridge table instead."

### 3. Naming Conventions
- Are table and column names consistent? (snake_case, no abbreviations unless standard)
- Do fact tables use `fact_` prefix and dimension tables use `dim_` prefix?
- Do column names include units when ambiguous? (`duration_days` not `duration`)
- Are foreign keys named consistently? (`<dimension>_id`)

Flag specific violations. Don't say "naming could be improved." Say "`ptnt_id` should be `patient_id`. `los` should be `length_of_stay_days`."

### 4. Relationships
- Are foreign keys defined and enforced?
- Are many-to-many relationships handled via bridge tables?
- Are there orphaned tables with no relationships?
- Are slowly changing dimensions handled appropriately (Type 1, 2, or 3)?

### 5. Extensibility
- Can new data sources be added without restructuring existing tables?
- Are there hardcoded values that should be in dimension tables?
- Is the schema prepared for the next likely feature request?
- Are there Architecture Decision Records for non-obvious choices?

### 6. Query Performance (if volume info available)
- Will the primary query patterns perform well at expected scale?
- Are partition keys or clustering keys appropriate?
- Are there opportunities for pre-aggregation or materialized views?

## Output Format

Provide conversational feedback organized by severity:

**Must fix** - Issues that will cause incorrect results or major performance problems
**Should fix** - Issues that will cause confusion, maintenance burden, or minor performance impact
**Consider** - Suggestions for improvement that aren't blocking

For each issue:
1. What the problem is (specific table/column)
2. Why it matters (consequence if not fixed)
3. How to fix it (concrete recommendation)

End with a summary: "This schema is [assessment]. The [N] must-fix items should be resolved before building pipelines on top of it."
