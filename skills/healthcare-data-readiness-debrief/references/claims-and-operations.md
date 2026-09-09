# Claims, billing, scheduling and support

Public sources reviewed September 8, 2026. Medicare transaction examples do not establish every payer's policy. The event and AI tests below are proposed engineering checks, not quoted legal requirements.

## Claims analysis

Ask what a row represents: Claim, version, line, encounter or another unit. Confirm source-specific supersession/reversal rules before deduplication. Multiple claims can belong to one admission. Compare observation periods with attention to runout, availability and eligibility/enrollment when a rate requires them. Do not invent a deduplication key or call row growth utilization growth.

Propose reconciliation by claim chain, state and intended metric unit under documented source rules. An aggregate reconciliation can expose the uncertainty without patient rows in chat.

Source: [CMS Blue Button claim effective date](https://bluebutton.cms.gov/data-dictionary/clm-efctv-dt-69/). This supports investigating versions, not a universal final-action algorithm.

## RCM and billing

Keep receipt/acceptance, adjudication/remittance, cash posting and patient balance distinct. A 277CA acknowledgment does not establish payment. Separate claim/line adjustments from provider-level adjustments. Billed charges minus payer payment is not necessarily patient responsibility, and reported responsibility is not necessarily the current collectible balance after other payments, coverage and adjustments.

Ask billing operations and finance to reconcile authoritative transaction stages and balance policy. Do not label every adjustment a denial, assume payment guarantees coverage, initiate collections or send balance messages. A recommended check does not authorize an operational action.

Sources: [CMS transaction inventory](https://www.cms.gov/Outreach-and-Education/MLN/WBT/MLN4462429-MLN-WBT-1500/1500/lesson03/11/index.html), [CMS remittance advice](https://www.cms.gov/medicare/coding-billing/electronic-billing/health-care-payment-remittance-advice), [X12 adjustment interpretation](https://x12.org/resources/requests-for-interpretation/rfi-2048-cagc-co-coinsurance).

## Scheduling and patient operations

A correct snapshot can become stale before an action. Check cancellations, rebooking, appointment status versus participant acceptance, time zones, duplicate or missed events, retries and the moment the sender checks current state. A shared phone number is not a patient identifier or a reason by itself to drop a patient.

Propose synthetic lifecycle replays with an expected action, not only a matching extract count. Confirm contact preferences and confidential-communication handling with the workflow owner. Reminder permission and message/channel rules are separate questions; do not declare that every reminder requires HIPAA authorization or that HIPAA resolves every SMS rule.

Sources: [FHIR R4 Appointment definitions](https://hl7.org/fhir/R4/appointment-definitions.html), [FHIR R5 subscriptions](https://fhir.hl7.org/fhir/subscriptions.html), [HHS reminders](https://www.hhs.gov/hipaa/for-professionals/faq/286/are-appointment-reminders-allowed-under-hipaa-without-authorization/index.html), [HHS messages and communication requests](https://www.hhs.gov/hipaa/for-professionals/faq/198/may-health-care-providers-leave-messages/index.html). R5 subscription delivery behavior should not be assumed for every transport.

## Customer support and AI

Historical tickets show what someone said, not what policy authorizes today. Confirm authoritative source, effective date, account access and escalation owner. Do not equate referrals with guaranteed coverage. Vendor compliance marketing and helpful-sounding responses do not establish safe deployment.

Propose synthetic tests for obsolete-policy conflicts, another household member's account, embedded instructions in a ticket, uncertainty and human handoff. Expected behavior follows approved source authority, preserves account boundaries, treats ticket instructions as data and avoids unsupported promises. Separately ask privacy/security owners to confirm the service's approved processing scope and arrangements; a business associate agreement does not evaluate model behavior.

Source: [HHS cloud guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html). This supports processing/organizational questions, not vendor certification or AI evaluation results.
