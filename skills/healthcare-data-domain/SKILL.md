---
name: healthcare-data-domain
version: 0.1.1
description: >
  Healthcare data domain context covering FHIR, HL7, OMOP CDM, real-world evidence,
  and clinical terminology systems. Use when working on clinical data pipelines,
  EHR integrations, claims data products, HIPAA-governed data, OMOP transformations,
  or when the conversation involves PHI, ICD-10, SNOMED, CPT, LOINC, or RxNorm.
  Skip this skill for non-healthcare data products.
user-invocable: false
---

## When This Skill Applies

Activate when the data product involves: electronic health records (EHR), claims/billing data, clinical terminology, patient-level data, OMOP CDM, FHIR/HL7, or any data governed by HIPAA.

Do NOT activate for: general analytics, marketing data, financial data, or non-clinical datasets.

## Core Standards

**FHIR (Fast Healthcare Interoperability Resources)** - Modern API standard for health data exchange. Resource-based (Patient, Observation, MedicationRequest, Condition, Encounter). Use for real-time integrations and patient-facing apps.

**HL7 v2** - Legacy messaging standard still dominant in hospital systems. Pipe-delimited segments (MSH, PID, OBX). Expect to encounter this in any EHR integration project.

**OMOP CDM (Common Data Model)** - Research-optimized schema for observational health data. Core tables: PERSON, VISIT_OCCURRENCE, CONDITION_OCCURRENCE, DRUG_EXPOSURE, MEASUREMENT, OBSERVATION, PROCEDURE_OCCURRENCE. Use for analytics and real-world evidence studies.

## Clinical Terminology Systems

| System | What It Codes | Example |
|--------|--------------|---------|
| ICD-10-CM | Diagnoses | F32.1 (Major depressive disorder, single episode, moderate) |
| CPT | Procedures | 99213 (Office visit, established patient) |
| SNOMED CT | Clinical concepts | 73211009 (Diabetes mellitus) |
| LOINC | Lab tests/observations | 2345-7 (Glucose, serum/plasma) |
| RxNorm | Medications | Resolve ingredient, strength and dose form against the selected release |
| NDC | Drug packages | National Drug Code for specific manufacturer/package |

Preserve original codes, text, system and version. Use the appropriate standard terminology when a supported mapping exists; keep ambiguous and unmapped values visible for review. Verify example codes against the applicable vocabulary release before implementation.

## OMOP Analytics Patterns

Choose an analytical view or serving model for the consumer's query pattern while preserving the canonical CDM and provenance. If a star schema is useful:
- Fact tables: Drug exposures, visits, conditions (events become facts)
- Dimension tables: Patient, drug, diagnosis
- Pre-calculated cohort definitions for common queries
- Check join cardinality before denormalizing. Multiple event tables can multiply rows and distort totals; aggregate at the intended grain before joining when appropriate.

See [domain-reference.md](domain-reference.md) for source types and interpretation limits. Confirm the deployed CDM version before using any mapping.

## FHIR Gotchas

Common mistakes when working with FHIR resources:

| Gotcha | What Trips You Up | Fix |
|--------|-------------------|-----|
| Coding vs CodeableConcept | A CodeableConcept can contain several codings and text. The first coding need not be the required system. | Select by the expected system and applicable version; preserve alternatives and handle text-only values. |
| Patient.identifier vs Patient.id | `.id` is the FHIR server's internal ID. `.identifier` holds MRNs, SSNs, and other business identifiers. | Query by `.identifier.value` with the correct `.identifier.system`. |
| Observation.value[x] | Polymorphic field. Could be `valueQuantity`, `valueString`, `valueCodeableConcept`, or others. | Check the resource profile or test data to know which type your source sends. |
| Bundle pagination | Page size is server-dependent. A successful first response may cover only part of the search. | Follow authorized `next` links, verify filters and scope, and distinguish complete retrieval from complete clinical history. |

## FHIR-to-OMOP Mapping

When transforming FHIR resources into OMOP CDM:

| FHIR Resource | OMOP Table | Key Mapping Notes |
|---------------|-----------|-------------------|
| Patient | person | Map `Patient.birthDate` → `year_of_birth`. Gender codes differ between systems. |
| Condition | condition_occurrence | `Condition.code` → `condition_concept_id` via SNOMED-to-OMOP vocabulary mapping. |
| Observation | measurement or another appropriate domain | Resolve the concept's domain, value type and units under the applicable vocabulary and CDM conventions; not every Observation is a measurement. |
| MedicationRequest | drug_exposure when supported by the ETL convention | Preserve the order's provenance/type and supported fields. CDM 5.4 has no generic `dose_value`/`dose_unit` fields in this table. Do not infer actual use or dose from strength. |
| Encounter | visit_occurrence | `Encounter.class` → `visit_concept_id`. Map inpatient/outpatient/emergency. |

## Common LOINC Codes for Vitals

| Vital Sign | LOINC Code | Units |
|------------|-----------|-------|
| Blood pressure, systolic | 8480-6 | mmHg |
| Blood pressure, diastolic | 8462-4 | mmHg |
| Heart rate | 8867-4 | /min |
| Body temperature | 8310-5 | Cel |
| Body weight | 29463-7 | kg |
| Body height | 8302-2 | cm |

## HIPAA Awareness

Determine applicable privacy rules, permitted purpose, recipients and agreements with the responsible owner. HIPAA permits some identifiable-data uses and disclosures under specified conditions; de-identification is one route, not a universal condition for every transfer. Do not export data based on this overview.

This skill provides general domain context, not compliance advice. Involve your privacy officer and legal team for HIPAA compliance decisions.

## Source checks

Reviewed September 10, 2026: [FHIR R4 datatypes](https://hl7.org/fhir/R4/datatypes.html#CodeableConcept), [FHIR R4 search](https://hl7.org/fhir/R4/search.html), [OMOP CDM 5.4](https://ohdsi.github.io/CommonDataModel/cdm54.html) and [HHS Privacy Rule summary](https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html). These are versioned or scope-limited sources, not automatic approval for a project.
