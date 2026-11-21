# Data contract

> What the data is, where it comes from, and what it cannot support. Load before any quality or feasibility claim.

## Sources

| Source | Owner | Grain | Coverage | Freshness | Known gaps |
| --- | --- | --- | --- | --- | --- |
| OMOP CDM 5.3 extract (Eunomia GiBleed, synthetic) | OHDSI community | One row per clinical event; `person` is one row per patient | 2,694 patients, events 1908 to 2019 | Static. Pinned by SHA-256 in `grader/data.py` | `visit_occurrence` holds inpatient visits only; `observation_period` has rows with no matching patient |

## Definitions

- **Patient.** A row in `person`. Count patients with `study_population`.
- **Study population.** Every patient in `person`. Defined in `definitions/10_study_population.sql`.
- **Condition cohort.** Patients with a condition record for the concept, matched on `condition_concept_id`. Defined in `definitions/20_condition_records.sql`.
- **Ingredient exposure.** A drug era for the ingredient. `drug_era` is already at ingredient level. Defined in `definitions/30_ingredient_eras.sql`.
- **Inpatient visit.** A `visit_occurrence` row with `visit_concept_id` 9201. Length of stay counts the admit day and the discharge day. Defined in `definitions/40_inpatient_visits.sql`.
- **Age on a date.** The year of the date minus `year_of_birth`.

## Mapping and layers

Raw OMOP tables load as-is into DuckDB. The definitions above are the only cleaned layer. There is no presentation layer.

## Limitations the product must state

- The data is synthetic and cleaner than a real client extract.
- Visit-based rates cover inpatient care only.

## Provenance

(hub, OHDSI CDM 5.3 documentation, 2026-10-22)
