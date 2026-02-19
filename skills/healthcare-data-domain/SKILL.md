---
name: healthcare-data-domain
version: 0.1.0
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
| RxNorm | Medications | 197361 (Sertraline 50mg tablet) |
| NDC | Drug packages | National Drug Code for specific manufacturer/package |

ALWAYS use standard terminology codes rather than free-text descriptions. Map to the appropriate code system for the use case.

## OMOP Analytics Patterns

The 30-40 normalized OMOP tables are wrong for analytics dashboards. Transform to star schema with strategic denormalization:
- Fact tables: Drug exposures, visits, conditions (events become facts)
- Dimension tables: Patient, drug, diagnosis
- Pre-calculated cohort definitions for common queries
- NEVER fully denormalize (One Big Table). Healthcare's many-to-many relationships cause exponential row growth.

See `domain-reference.md` for detailed OMOP table relationships and FHIR resource mappings.

## HIPAA Awareness

CRITICAL: Any data product handling patient data must consider the 18 HIPAA identifiers. See `domain-reference.md` for the full list. De-identification is required before data leaves a HIPAA-governed environment.

This skill provides general domain context, not compliance advice. Involve your privacy officer and legal team for HIPAA compliance decisions.
