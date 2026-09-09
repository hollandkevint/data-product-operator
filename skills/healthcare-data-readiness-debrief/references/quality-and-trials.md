# Quality reporting and clinical trials

Public sources reviewed September 8, 2026. Use the relevant section only. None of these prompts supplies a licensed measure definition, protocol decision, or regulatory acceptance.

## HEDIS reporting

Confirm reporting method, measure identifier, measurement period, approved specification release, terminology package and updates with the quality reporting owner. Do not substitute a similar eCQM. Do not reconstruct or distribute proprietary eligibility logic or code lists from memory. Ask the owner to check the applicable licensed source and permitted use.

Reconcile population entry/removal, exclusions and other applicable population stages, denominator and numerator before interpreting a rate change. In ECDS, a clinical feed can affect any measure element, including the denominator. A displayed increase may reflect newly available evidence or changed coverage rather than improved care. Preserve the distinction.

Useful question: “How did you check whether the new source changed who belongs in the population?”

Propose aggregate counts with reasons under the approved rules. If population comparability holds, examine newly captured numerator evidence. If it does not, recalculate and explain the coverage change. If the rules are unavailable, keep the reporting claim unresolved.

Sources: [NCQA technical resources](https://www.ncqa.org/hedis/measures/), [ECDS FAQ](https://www.ncqa.org/hedis/ecds-frequently-asked-questions/), [permitted uses and licensing](https://www.ncqa.org/hedis/using-hedis-measures/). These sources support the distinctions above; the skill is not NCQA certified.

## CMS eCQM reporting

Identify program, reporting period, measure version, logic dependencies, terminology/value-set expansions and applicable updates. Structural validation and agreement with the measure calculation are different checks. Do not automatically upgrade to the newest package.

If implementations disagree, compare version manifests first, hold the approved input fixed, then trace population, temporal and mapping differences. Use synthetic boundary cases whose expected results the measure owner derives from the applicable specification. Do not invent which rate is correct.

Source: [CMS annual update implementation](https://ecqi.healthit.gov/ecqm-annual-update-implementation). Applicable versions depend on program and period.

## Clinical trials

First distinguish feasibility/recruitment, operational monitoring, tabulation, analysis and submission. Do not route every trial project through submission standards. For recruitment, distinguish a candidate flag from confirmed eligibility and authorized patient contact; the clinical study team owns protocol interpretation and screening.

For tabulation/analysis, identify the protocol, statistical analysis plan (SAP), deliverable and approved derivation versions. Preserve collected date precision and original values. Keep analysis imputation separate from source/tabulation values, with derivation flags and traceability. Do not assume a medication order or strength establishes exposure.

Before lab conversion, confirm analyte, specimen, method, units and reference-range meaning with the laboratory/domain owner. A single multiplier cannot be assumed to work across tests and sources. Unsupported conversions remain unresolved; exclusions require an owner and an account of their effect.

Maintain the stated blind. Route treatment-arm checks to authorized roles rather than joining restricted assignment data for a blinded team. Preserve correction history, who changed what, when and why. Synthetic examples do not authorize real access changes.

For a submission, the relevant owner checks FDA center, submission scope, study timing and supported standard versions. A format checker does not establish scientific fitness or regulatory acceptance.

Sources: [CDASHIG v2.1 section 3.6](https://www.cdisc.org/standards/foundational/cdashig-v2-1), [ADaM traceability examples](https://www.cdisc.org/standards/foundational/adam/adam-examples-traceability-v1-0), [FDA study-data resources](https://www.fda.gov/industry/study-data-standards-resources/study-data-submission-cder-and-cber), [FDA technical conformance guide](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/study-data-technical-conformance-guide-technical-specifications-document), [FDA electronic systems guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-systems-electronic-records-and-electronic-signatures-clinical-investigations-questions). Guidance is not itself a certification or a substitute for applicable requirements.
