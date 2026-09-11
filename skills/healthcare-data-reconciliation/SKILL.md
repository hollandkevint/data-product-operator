---
name: healthcare-data-reconciliation
description: Investigate disagreements between healthcare source records and downstream outputs. Use for claims/RCM totals, HL7/FHIR record pulls, mappings, clinical-result routing or patient-operations state. Produce an evidence trace and discriminating checks without assuming a root cause or authorizing data changes.
metadata:
  version: "0.1.0"
---

# Healthcare Data Reconciliation

Trace a discrepancy from source to intended use and identify the next check that separates plausible explanations.
Use approved schemas, aggregate summaries and synthetic cases. Keep record-level review inside the authorized environment.

## Bound the disagreement

Record expected and observed behavior, affected period/population, grain, versions and consequence.
Distinguish event, receipt, processing and discovery time. A later snapshot may legitimately differ.
Ask who owns source interpretation and who can accept the downstream result.
Separate confirmed impact from possible harm. Follow the organization's incident process if patient safety may be affected.

## Trace the path

Follow source capture, extraction, delivery, identity matching, mapping, transformation, display and downstream action.
At each transition record input/output identifiers, version, inclusion rule, rejected records and the available evidence.
Find the last point of agreement. Compare an affected example with a relevant unaffected example.
Compare rows and distinct entities as well as totals; equal totals can conceal wrong-patient links or offsetting errors.
Never treat a successful transport acknowledgment as proof of downstream acceptance, payment or clinical follow-up.

## Select the relevant branch

| Workflow | Checks that change the conclusion |
|---|---|
| Claims analysis / RCM | Claim versus line grain, correction chain, voids/reversals, payer and adjudication stage, mature comparison period; reconcile billed, allowed, paid and patient responsibility separately |
| Patient record pull | Authorized patient scope, requested filters, server-supported behavior, pagination, resources omitted by permissions, status and correction handling |
| HL7/FHIR mapping | Sending-system identity, code system/version, units, null semantics, repeated values, preliminary/final/corrected status and resource provenance |
| Clinical result routing | Source result, receipt, correct patient and clinician, review queue, acknowledgment and follow-up; technical delivery alone does not close the workflow |
| Scheduling / referrals | Current state and state history, cancellation/rebooking, duplicate delivery, appointment linkage, contact permission and send-time recheck |
| Customer support AI | Source authority and freshness, account/patient isolation, unsupported answers, human escalation and whether any action occurred |

Pin the relevant profile, payer feed, measure or interface contract. Do not invent universal HL7 acknowledgment or payer-processing semantics.

## Maintain competing explanations

For each candidate explanation, record supporting evidence, contradictory evidence and a check that could reject it.
Distinguish source absence, extraction loss, access filtering, transformation error and changed consumer definitions.
Do not call the first plausible explanation the root cause. A fix that passes one fixture proves only the behavior exercised.
Separate original-failure reproduction from verification of the proposed correction.

## Synthetic case

An interface reports successful receipt, but a laboratory result is absent from a clinician's queue.
Possible explanations include identity mismatch, provider routing, status filtering, delayed processing or a later workflow failure.
The next check follows the same result through each stage using approved internal evidence.
Do not resend patient messages or change routing rules while investigating without authorization.
Closure requires evidence of the intended follow-up, not only a green interface status.

## Return a reconciliation brief

Include the discrepancy, timeline, source-to-output trace, competing explanations and next discriminating checks.
For each proposed correction, identify the owner, affected scope, acceptance cases, side effects and rollback or recovery limit.
Test a historical failure, an unaffected case and a boundary case in an approved environment before widening use.
Plan recurrence observation over relevant exposure, with a balancing check for wrongly excluded or duplicated work.
Fewer tickets alone cannot prove prevention. Do not invent a universal number of cycles or a success threshold.
Keep containment, correction and prevention separate. State what remains unresolved.

## Sources and limits

Reviewed September 10, 2026. The checks above are proposed workflow adaptations.

- [FHIR R4 search](https://hl7.org/fhir/R4/search.html): Version-pinned search behavior; inspect the actual server/profile.
- [CMS claims manual, Chapter 1](https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Downloads/clm104c01.pdf): Medicare processing context; not every payer feed.
- [ONC SAFER test-result follow-up](https://healthit.gov/wp-content/uploads/2025/06/SAFER-Guide-8.-Test-Results-Reporting-Final.pdf): Clinical workflow assessment guidance, not proof of safety.
- [AHRQ root cause analysis](https://psnet.ahrq.gov/primer/root-cause-analysis): Systems investigation and limitations of causal conclusions.
