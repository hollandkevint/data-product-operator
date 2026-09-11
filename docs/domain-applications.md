# Domain application packs

Start with [Data Product Operator](../skills/data-product-operator/SKILL.md). Keep the same operating loop across domains; add the definitions and failure cases that change the decision. These guides compose existing skills and do not install separate plugins.

| Domain | Start here | Typical owner decision |
|---|---|---|
| Healthcare | [Dedicated application pack](healthcare-applications.md) | Whether evidence supports a named reporting, research or operational use |
| Marketing data | [Marketing guide](#marketing-data) | Whether to change a measurement definition, audience or budget recommendation |
| Logistics / operations | [Operations guide](#logistics-and-operations) | Whether a service metric or operational signal is fit for the intended action |
| Ecommerce | [Commerce guide](#ecommerce) | Whether orders, customers and financial outcomes reconcile for the proposed use |

These are proposed applications with synthetic examples. They have not been independently validated on live business systems. Do not treat a listed route as domain certification or a claim that all four packs have the same depth.

## Shared evidence path

[Discovery](../skills/data-consumer-discovery/SKILL.md) defines the consumer decision. [Metrics](../skills/metrics-definition/SKILL.md) fixes the unit, time window and exclusions. [Analyst](../skills/analyst/SKILL.md) links definitions and source snapshots to checks, findings and owner decisions. Add [quality](../skills/data-quality-assessment/SKILL.md), [model design](../skills/data-model-design/SKILL.md) or platform guidance only where needed.

Use source-specific contracts and approved summaries. Record system/tenant scope, identifiers, business-event and processing times, correction handling, and what the source cannot observe. Keep proposed checks separate from executed evidence.

## Marketing data

| Application | Skills | Checks to agree with the owner |
|---|---|---|
| Campaign and funnel measurement | [Metrics](../skills/metrics-definition/SKILL.md), [Analyst](../skills/analyst/SKILL.md) | Exposure/click/session/person grain, qualification rules, time window, deduplication, source coverage and event loss |
| Attribution and budget recommendations | [Product validation](../skills/data-product-validation/SKILL.md), [quality](../skills/data-quality-assessment/SKILL.md), [storytelling](../skills/data-storytelling/SKILL.md) | Attribution model/version, conversion window, cross-channel overlap, spend reconciliation and uncertainty about causal lift |
| Audience delivery | [Model design](../skills/data-model-design/SKILL.md), [pipeline quality](../skills/data-pipeline-quality/SKILL.md), [ethical risk](../skills/ethical-risk-assessment/SKILL.md) | Identity scope, applicable permissions/suppression rules from responsible owners, destination count and stale-membership handling |

**Synthetic case:** A campaign dashboard reports twice as many conversions after a customer table join. Route through metric definition, key-cardinality checks and source-to-output reconciliation. Keep attribution changes and join multiplication as separate hypotheses. Do not recommend budget increases from the inflated total or call attributed conversions incremental lift.

**Handoff:** The marketing owner reviews the reconciled definition and limitations before changing the budget recommendation. Audience upload, spend changes and customer contact require separate authority. This guide does not determine applicable consent law or infer that a marketing identifier is unrestricted.

## Logistics and operations

| Application | Skills | Checks to agree with the owner |
|---|---|---|
| On-time delivery / service performance | [Metrics](../skills/metrics-definition/SKILL.md), [Analyst](../skills/analyst/SKILL.md) | Order, shipment, package or stop grain; promised versus revised time; timezone; partial completion; exception and cancellation rules |
| Shipment-event feeds | [Model design](../skills/data-model-design/SKILL.md), [pipeline quality](../skills/data-pipeline-quality/SKILL.md) | Duplicate and out-of-order events, provider event semantics, clock precision, receipt time and late corrections |
| Inventory / service operations | [Quality](../skills/data-quality-assessment/SKILL.md), [stakeholder alignment](../skills/stakeholder-alignment/SKILL.md) | SKU/location/unit scope, reservations, adjustments, delayed scans and reconciliation against the applicable system of record |

**Synthetic case:** The source records a delivery time before midnight, while the dashboard assigns it to the next day. Pin the source and definition versions; inspect timezone conversion, business-day cutoff and arrival time before blaming the carrier. Test a boundary case on each side of the cutoff.

**Handoff:** The operations owner decides whether to correct the metric or change the service response. A received scan does not establish physical delivery or inventory availability. Do not reroute shipments, release inventory or message recipients during analysis without authorization.

## Ecommerce

| Application | Skills | Checks to agree with the owner |
|---|---|---|
| Revenue / order reconciliation | [Metrics](../skills/metrics-definition/SKILL.md), [Analyst](../skills/analyst/SKILL.md), [quality](../skills/data-quality-assessment/SKILL.md) | Order/line/payment grain; currency and conversion date; discounts, tax, shipping, refunds, cancellations and payment stage |
| Conversion and customer cohorts | [Discovery](../skills/data-consumer-discovery/SKILL.md), [metrics](../skills/metrics-definition/SKILL.md), [model design](../skills/data-model-design/SKILL.md) | Session versus customer denominator, guest identities, bots/test traffic, first-purchase definition, observation window and channel coverage |
| Returns / retention | [Analyst](../skills/analyst/SKILL.md), [pipeline quality](../skills/data-pipeline-quality/SKILL.md), [storytelling](../skills/data-storytelling/SKILL.md) | Return request versus receipt versus refund, partial returns, late events, mature follow-up and cohort attrition |

**Synthetic case:** A daily sales report subtracts a refund twice because payment and order-line tables both carry it. Define the financial event grain and trace the same synthetic refund through both paths. Reconcile amounts before and after joining. Do not silently remove duplicate-looking rows without confirming their business meaning.

**Handoff:** The commerce or finance owner accepts the scoped reconciliation. Revenue recognition and financial reporting definitions come from responsible finance owners; this guide does not establish accounting treatment. Analysis does not authorize refunds, order cancellations or customer messages.

## Add another domain

Name the consumer decision, terms that differ from the core library, source/version boundaries, a discriminating check and the accepting owner. Link to existing skills first. Add a dedicated skill only when repeated use establishes a distinct workflow. Keep private field mappings and operational evidence in the team's approved workspace.
