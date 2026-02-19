---
name: data-model-design
version: 0.1.0
description: >
  Dimensional modeling and schema design for data products. Star schema patterns,
  slowly changing dimensions, denormalization decisions, and architecture decision
  records. Use when designing data models, reviewing schema designs, choosing between
  normalization strategies, or when someone asks "how should I model this data?" or
  "should I denormalize?" For OMOP CDM patterns specifically, see healthcare-data-domain.
user-invocable: false
---

## Star Schema as Default

For analytics data products, default to star schema with strategic denormalization:

**Fact tables** contain events at the lowest useful grain:
- One row per event (transaction, visit, measurement, interaction)
- Foreign keys to dimension tables
- Numeric measures (amount, count, duration)
- Timestamps at the grain of the analysis

**Dimension tables** contain context:
- Descriptive attributes for filtering and grouping
- Human-readable labels alongside codes
- Hierarchies for drill-down (region -> state -> city)

NEVER fully denormalize into One Big Table. Many-to-many relationships cause exponential row growth. A patient with 10 conditions and 5 medications creates 50 rows instead of 15.

ALWAYS start with the query patterns. What questions will consumers ask? Design the schema to make those queries simple. If 80% of queries filter by date and group by category, those should be the primary dimensions.

## Slowly Changing Dimensions (SCD)

**Type 1** - Overwrite the old value. Use when history doesn't matter (correcting a typo in a name).

**Type 2** - Add a new row with effective dates. Use when you need to track what was true at a point in time (patient address at time of visit, product price at time of sale). Add `effective_start_date`, `effective_end_date`, and `is_current` flag.

**Type 3** - Add a column for the previous value. Use when you only need one level of history (current_category, previous_category).

Default to Type 2 for any dimension where the business asks "what was it at the time of X?" Start with Type 1 for everything else and upgrade when the need emerges.

## Architecture Decision Records

For every non-obvious modeling decision, write a lightweight ADR:
- **Context**: What situation prompted the decision?
- **Options**: What alternatives were considered?
- **Decision**: What was chosen and why?
- **Consequences**: What are the tradeoffs?

Keep ADRs in the repo alongside the schema. Future team members will ask "why is it modeled this way?" The ADR answers before they have to ask.

## Design Validation

Before building, validate with limited data:
1. Load a representative sample (1-5% of volume)
2. Run the top 10 expected queries
3. Verify results match expectations
4. Check query performance against SLA
5. Confirm grain is correct (no unexpected row multiplication)

See `schema-patterns.md` for common dimensional modeling patterns.
