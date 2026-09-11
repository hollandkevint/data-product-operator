# Healthcare applications

Use [Analyst](../skills/analyst/SKILL.md) to connect a definition, source snapshot, check, finding and owner decision. These are synthetic investigation routes, not executable clinical rules or validated customer outcomes. Read only the matching route and linked skills.

| Application | Skills to connect | Evidence that changes the decision | Boundary |
|---|---|---|---|
| HEDIS / eCQM reporting | [Cohort](../skills/healthcare-cohort-design/SKILL.md) → [metrics](../skills/metrics-definition/SKILL.md) → [reconciliation](../skills/healthcare-data-reconciliation/SKILL.md) | Measure/program/year and applicable specification/value-set versions; separate numerator, denominator, exclusions and exceptions; source-to-result trace | Missing licensed rules remain missing. A count match does not authorize submission. |
| Clinical trial feasibility | [Cohort](../skills/healthcare-cohort-design/SKILL.md) → [domain](../skills/healthcare-data-domain/SKILL.md) → [quality](../skills/data-quality-assessment/SKILL.md) | Approved protocol labels, observation coverage, uncertain dates, attrition and owner-reviewed boundary cases | Observable candidates are not confirmed eligible, consented or available for recruitment. |
| Claims analysis | [Metrics](../skills/metrics-definition/SKILL.md) → [reconciliation](../skills/healthcare-data-reconciliation/SKILL.md) → [DuckDB](../skills/duckdb-data-profiling/SKILL.md) | Claim/line grain, source-scoped identifiers, maturity cutoff, correction chains and join multiplicity | Paid claims do not establish complete care or disease prevalence. |
| RCM / billing | [Reconciliation](../skills/healthcare-data-reconciliation/SKILL.md) → [metrics](../skills/metrics-definition/SKILL.md) → [stakeholder alignment](../skills/stakeholder-alignment/SKILL.md) | Separate billed, allowed, paid and patient responsibility; payer stage, remittance version and reprocessing history | Transport receipt does not mean payment. Do not resubmit bills during analysis. |
| Patient record pull | [Reconciliation](../skills/healthcare-data-reconciliation/SKILL.md) → [domain](../skills/healthcare-data-domain/SKILL.md) | Authorized scope, identity namespace, requested filters, pagination, permission exclusions and corrected statuses | Retrieval completeness for a request is not a complete clinical history. |
| HL7 / FHIR preparation and mapping | [Domain](../skills/healthcare-data-domain/SKILL.md) → [model design](../skills/data-model-design/SKILL.md) → [reconciliation](../skills/healthcare-data-reconciliation/SKILL.md) | Applicable message/profile version, code system, units, null semantics, repeated values and provenance | Select a coding by system/version, not array position. Preserve uncertain mappings. |
| OMOP / real-world evidence | [Cohort](../skills/healthcare-cohort-design/SKILL.md) → [domain](../skills/healthcare-data-domain/SKILL.md) → [quality](../skills/data-quality-assessment/SKILL.md) | CDM/vocabulary release, source coverage, phenotype boundary cases and study-specific checks | General data-quality checks do not establish fitness for a particular study or a causal effect. |
| Scheduling / referrals | [Reconciliation](../skills/healthcare-data-reconciliation/SKILL.md) → [metrics](../skills/metrics-definition/SKILL.md) | State history, cancellations, rebookings, duplicate deliveries and send-time state | After a timeout, confirm actual state before retrying. Analysis does not authorize bookings or contact. |
| Customer support / support AI | [Reconciliation](../skills/healthcare-data-reconciliation/SKILL.md) → [ethical risk](../skills/ethical-risk-assessment/SKILL.md) | Versioned answer sources, tenant isolation, unsupported-answer cases, escalation and action logs | Readiness of data does not establish agent safety or authority to change accounts. |
| Laboratory result follow-up | [Reconciliation](../skills/healthcare-data-reconciliation/SKILL.md) → [domain](../skills/healthcare-data-domain/SKILL.md) | Result identity, preliminary/final/corrected status, clinician routing, review and follow-up evidence | An interface acknowledgment does not close a clinical workflow. Use the organization's incident process for possible harm. |

Add [Databricks review](../skills/databricks-data-product-review/SKILL.md) when the evidence lives in that approved environment. Use DuckDB only with explicitly selected files and an approved storage boundary. Do not change a clinical definition to make it fit a platform.

## Three worked graph applications

### Before launch: Quality-reporting denominator

**Synthetic input:** A team has a denominator query and a successful scheduled run, but the supplied summary omits the measurement year and value-set version.

**Graph:** Question `reporting-q1` → definition `measure-d1` → check `denominator-c1` → finding `coverage-f1` → decision `submission-j1`. The source snapshot also feeds the check.

**Analyst response:** Keep the definition unresolved and the check proposed. Ask the measure owner for the applicable specification labels and expected boundary cases. Do not infer the year from the current calendar or treat job success as a measure pass. The reporting owner retains the submission decision.

### Before agent access: Scheduling support

**Synthetic input:** A read-only scheduling assistant answers accurately in supplied examples. The team asks to enable booking. One proposed test simulates a timeout after the scheduling service accepts a request.

**Graph:** Intended action → appointment-state definition + API contract version → duplicate/retry and isolation checks → bounded findings → operational owner decision → observed booking outcomes.

**Analyst response:** Keep read accuracy and action safety as separate findings. Require authorized nonproduction testing of the ambiguous timeout, state recheck, patient/account isolation and escalation. No booked appointment or permission grant is inferred. Data access, tool authority, clinical/operational review and supervision each remain separate decisions.

### After a mismatch: Paid-claims report

**Synthetic input:** A report's paid total increased after joining a roster. The source includes correction records. No before/after run artifact was supplied.

**Graph:** Adapt the [core JSON example](../skills/analyst/example.json): Replace its active-account definition with the claim/line definition, bind the payer snapshot, and route the check to healthcare reconciliation. Keep the proposed reconciliation, competing hypotheses and hold decision separate.

**Analyst response:** Investigate join multiplicity and correction handling independently. Freeze source and definition versions before comparing totals. A synthetic duplicate-key test can demonstrate a failure mechanism; it cannot establish that this caused the real mismatch. Keep the handoff on hold until the named owner reviews the relevant evidence.

## Source boundaries

The linked healthcare skills contain source references and version limits. For quality reporting, [HL7 CQL](https://cql.hl7.org/) supplies computable clinical logic, but teams still need their applicable measure and terminology artifacts. [NCQA's public FAQ](https://www.ncqa.org/hedis/ecds-frequently-asked-questions/) does not replace licensed specifications. For research, [FDA's July 2024 EHR/claims guidance](https://www.fda.gov/media/152503/download) addresses intended-use relevance and reliability for drug and biological regulatory decisions; these broader operational routes are adaptations.

Never place private project graphs, patient data or restricted protocols in this public repository. See [testing and limits](analyst-testing.md) before treating the examples as evidence.
