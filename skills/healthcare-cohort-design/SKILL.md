---
name: healthcare-cohort-design
description: Turn a healthcare population question into a reviewable cohort specification and acceptance cases. Use for claims or EHR cohorts, OMOP studies, quality-reporting denominators or trial-feasibility counts. Does not determine clinical trial eligibility or supply licensed measure logic.
metadata:
  version: "0.1.0"
---

# Healthcare Cohort Design

Define who belongs in a population, when they enter it and what the available data can establish.
Work from approved summaries, schemas and source labels. Do not request patient records or restricted protocols.

## Establish the use

Ask the most consequential unanswered question first. Read supplied context before repeating intake.
Distinguish descriptive analytics, regulated quality reporting, research, trial feasibility and patient outreach.
Record the decision owner, target population, observation unit, source coverage and reporting or study period.
Do not choose clinical definitions or causal study assumptions on behalf of qualified owners.

## Write the specification before SQL

| Element | Required definition |
|---|---|
| Unit | Person, source patient, encounter, episode, claim or claim line; key scope and duplicate policy |
| Entry | Index event, event date, qualifying evidence and tie-breaking rule |
| Observation | Lookback, enrollment or observable period, gaps and minimum follow-up only when justified |
| Criteria | Each inclusion/exclusion rule, evidence source, terminology version and handling of uncertainty |
| Time | Inclusive/exclusive boundaries, timezone, date precision, late arrivals and data cutoff |
| Exit | End event, censoring or fixed reporting endpoint, and re-entry policy |
| Output | Cohort grain, permitted fields, attrition counts and release label |

Keep unknown rules marked for confirmation. A convenient SQL expression is not a clinical definition.

## Follow the applicable branch

- **HEDIS/eCQM:** Obtain the measure identifier, measurement year, reporting method and applicable specification/value-set versions from the owner. Preserve denominator, numerator, exclusions and exceptions separately. Do not substitute one program's completeness threshold for another's.
- **Trial feasibility:** Separate observable candidate counts from confirmed eligibility, consent, recruitment access and enrollment. Preserve uncertain dates and blinding; route protocol interpretation to the study owner.
- **Claims:** Specify adjudication maturity, coverage periods, service versus payment dates and replacement/reversal handling. A claim row is not necessarily an encounter or a paid service.
- **EHR/OMOP research:** Distinguish documentation from disease occurrence and recorded medication events from actual use. Observation periods do not guarantee complete external care capture.
- **Patient operations:** Define active referral, appointment or support-case states as of a time. Separate analysis membership from authorization to contact or act on a patient.

## Protect meaning

Review source codes, standard concepts, descendants, invalid mappings and vocabulary dates with a domain owner.
Keep source values and mapping provenance. A mapped concept or high mapping percentage does not establish phenotype validity.
Do not infer dose, frequency or adherence from medication strength. Keep orders, fills and administrations distinct.
Investigate missingness by source, period and relevant subgroup before proposing exclusions.
For causal questions, surface time-related bias and confounding for methodological review; do not claim adjustment solves them.

## Define acceptance cases

Use synthetic examples covering a clear inclusion, a clear exclusion and the boundary that could change the decision.
Add ambiguous identity, uncertain date, late correction or observation gaps when relevant.
Record expected membership and reason before running SQL. Keep unresolved cases unresolved.
Compare attrition after each rule and reconcile against an independent source count where available.

Example: Two sources use the patient key `001`. Keep source scope or use an approved linkage, rather than merging people by the raw key. Absence of a recorded exclusion diagnosis does not establish absence of the condition or confirmed trial eligibility.

## Deliver and stop

Return the cohort specification, source-to-rule map, unresolved decisions, synthetic acceptance cases and proposed review owners.
Generate dialect-specific SQL only when requested, using confirmed schema names. Execution and data export require their own authorization.
Label counts observed, estimated or untested. Do not certify clinical validity, trial eligibility or regulatory acceptance.

## Sources and limits

Reviewed September 10, 2026. This workflow is a proposed method, not a mandated checklist.

- [FDA EHR/claims guidance](https://www.fda.gov/media/152503/download): July 2024, relevance/reliability for drug and biological regulatory research; broader operational use is an adaptation.
- [OMOP CDM 5.4](https://ohdsi.github.io/CommonDataModel/cdm54.html): Pinned schema and conventions; confirm the deployed CDM and vocabulary.
- [NCQA HEDIS FAQ](https://www.ncqa.org/hedis/ecds-frequently-asked-questions/): Public context; applicable licensed specifications remain necessary.
