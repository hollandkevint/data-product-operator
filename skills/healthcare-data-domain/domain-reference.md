# Healthcare Data Domain Reference

Detailed reference for clinical data systems, terminology codes, and regulatory requirements. The main SKILL.md provides the overview; this file provides depth when you need it.

## OMOP CDM Core Tables

### Person-Level
- **PERSON** - Demographics, gender, race, ethnicity, year of birth, location
- **OBSERVATION_PERIOD** - Time spans of available data per person
- **PAYER_PLAN_PERIOD** - Insurance coverage periods

### Clinical Events (Fact Tables for Analytics)
- **VISIT_OCCURRENCE** - Encounters (inpatient, outpatient, ER, telehealth)
- **CONDITION_OCCURRENCE** - Diagnoses (mapped to SNOMED from ICD-10)
- **DRUG_EXPOSURE** - Medication orders, administrations, dispensings
- **PROCEDURE_OCCURRENCE** - Clinical and surgical procedures
- **MEASUREMENT** - Lab results, vitals, clinical measurements
- **OBSERVATION** - Clinical observations not captured elsewhere
- **DEVICE_EXPOSURE** - Medical device usage
- **SPECIMEN** - Biological samples

### Vocabulary Tables
- **CONCEPT** - All standardized clinical concepts across vocabularies
- **CONCEPT_RELATIONSHIP** - Mappings between vocabularies (ICD-10 to SNOMED)
- **CONCEPT_ANCESTOR** - Hierarchical relationships for rollup queries

## FHIR R4 Common Resources

### Administrative
- Patient, Practitioner, Organization, Location, Encounter

### Clinical
- Condition, Observation, DiagnosticReport, MedicationRequest, Procedure, Immunization, AllergyIntolerance

### Financial
- Claim, ExplanationOfBenefit, Coverage

### Workflow
- ServiceRequest, Task, Communication

## HIPAA 18 Identifiers (PHI)

Data containing any of these requires HIPAA protections:

1. Names
2. Geographic data smaller than state
3. Dates (except year) related to an individual
4. Phone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photographs
18. Any other unique identifying number or code

## Healthcare Data Source Types

### Claims Data
- Medical claims (professional, institutional, pharmacy)
- Sources: Medicare (CMS), commercial payers, Medicaid
- Strengths: large populations, longitudinal, billing-complete
- Weaknesses: diagnosis coding driven by reimbursement, no clinical detail

### EHR Data
- Clinical notes, lab results, vitals, medications, orders
- Sources: Epic, Cerner, Allscripts, custom systems
- Strengths: clinical richness, real-time availability
- Weaknesses: documentation bias, site-specific variation, extraction complexity

### Registry Data
- Disease-specific patient registries (oncology, rare disease, behavioral health)
- Strengths: deep clinical detail, outcome tracking
- Weaknesses: selection bias, small populations, variable completeness

## Real-World Evidence (RWE) Patterns

### Study Design Components
- Study population: inclusion/exclusion criteria
- Exposure definition: drug, procedure, or intervention of interest
- Outcome measures: primary and secondary endpoints
- Confounders: variables that could bias the association
- Time windows: washout, exposure, follow-up periods

### Common Biases to Address
- **Selection bias** - Non-random entry into the study population
- **Immortal time bias** - Misclassifying unexposed person-time
- **Channeling bias** - Treatment selection based on severity
- **Confounding by indication** - The reason for treatment correlates with the outcome
