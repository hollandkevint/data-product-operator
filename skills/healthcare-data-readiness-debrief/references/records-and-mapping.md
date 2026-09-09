# Record retrieval, identity and mapping

Public sources reviewed September 8, 2026. The cited FHIR R4 behavior is version-specific; confirm the deployed server, release, profiles and local interface agreement.

## Patient record pulls

An HTTP success or an empty response does not establish complete clinical coverage. Check endpoint and resource scope, authorization scope, supported filters, warnings, pagination and time coverage. FHIR R4 search can ignore unsupported parameters. Inspect documented capabilities and returned search information rather than assuming a copied filter worked.

Propose synthetic fixtures with known records, multiple pages and unsupported filters inside the approved environment. Distinguish unavailable records from absent events. No returned medication record does not establish that a patient takes no medication; an order returned does not establish actual use.

A successful synthetic query supports only the retrieval behavior exercised by that fixture. It does not prove that source coverage, rather than filtering, permissions or another difference, caused the original absence. Compare the original request and scope before assigning a cause. Label untested explanations as hypotheses.

Source: [FHIR R4 search](https://hl7.org/fhir/R4/search.html).

## Identity and access

Confirm identifier namespace, source organization, merge history and authoritative linkage. Independently assigned medical record numbers can collide. Normal row counts and low unmatched rates do not detect all false matches. Check false and missed matches, using approved synthetic fixtures here and owner-controlled review elsewhere. Do not prescribe a universal matching threshold, name/DOB-only proof, or automatic patient merges.

Identity and permission to disclose are separate dependencies. Knowing an appointment time or demographic detail does not settle representative authority. Route record-access decisions to the applicable verification workflow and its owner. Do not assume a household relationship grants access. Do not apply a blanket “minimum necessary” rule to every individual access request; the applicable access pathway matters.

Sources: [ONC patient matching](https://healthit.gov/standards-and-technology/patient-identity-and-patient-record-matching/), [FHIR R4 Patient](https://hl7.org/fhir/R4/patient.html), [HHS representative verification](https://www.hhs.gov/hipaa/for-professionals/faq/551/how-would-a-covered-entity-know-if-someone-were-a-personal-representative/index.html), [HHS individual access guidance](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/access/index.html). These sources do not determine the legal outcome of an individual request.

## HL7 v2 / FHIR preparation and mapping

Identify source message version and local agreement, target FHIR release/profile, terminology versions and consuming use. Check source identifiers, repetitions, units, specimen/method when relevant, result status/corrections, and effective versus receipt time. Latest received is not necessarily clinically current when messages replay or arrive out of order.

Ask the interface engineer and domain owner to review synthetic original/corrected/replayed sequences and representative unit cases against the agreed contract. Preserve original values and provenance. A valid resource can still misrepresent the result or fail the consumer's intended use. Do not turn a terminology match into unsupported clinical equivalence.

Sources: [HL7 v2-to-FHIR OBX mapping](https://www.hl7.org/fhir/uv/v2mappings/ConceptMap-segment-obx-to-observation.html), [FHIR R4 Observation definitions](https://hl7.org/fhir/R4/observation-definitions.html), [FHIR R4B validation](https://hl7.org/fhir/R4B/validation.html). The mapping guide is an example reference, not the project's interface contract; the validation discussion includes constraints outside automated conformance checks.
