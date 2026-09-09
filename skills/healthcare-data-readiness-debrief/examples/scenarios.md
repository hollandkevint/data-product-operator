# Worked healthcare scenarios

All projects, quantities and dialogue here are synthetic. These are teaching examples, not client stories, implemented tests, measure definitions or clinical recommendations. Public source boundaries are in the three `references/` files. The separate validation report records which scenarios were run through the assistant.

Use the relevant case as a starting point. Expected actions below are proposals for the responsible team, not actions performed by this skill.

## 1. HEDIS reporting: A better displayed rate

**Project account:** A dashboard moves from 680/1,000 to 730/1,000 after clinic records arrive. Some records concern members missing from the claims extract. The team applied the feed only to the numerator.

**Useful question:** Which reporting method and specification release governs this result?

**Synthetic answer:** ECDS; the quality lead has the licensed specification but has not checked whether the new feed changes the population.

**Brief:** The display increased five percentage points. Comparable reporting results and improved care remain unestablished. Ask the quality lead to reconcile population and numerator changes under the applicable rules. If the population changes, recalculate and explain coverage effects; otherwise trace the newly captured evidence. Keep the submission claim unresolved. Do not reproduce eligibility logic from memory.

## 2. eCQM: A green validator and two rates

**Project account:** XML passes validation. The calculated rate differs from a reference using the reporting-year terminology package; the team installed the newest package.

**User asks:** Give me a brief now, not an interview.

**Brief:** Report structural validation as user-reported. Ask the measure implementation owner to compare program, period, measure/logic and terminology versions, then rerun with fixed inputs and the applicable package. If differences persist, trace population and temporal calculations. Neither rate is established as correct here. Respect the brief-now request.

## 3. Clinical trials: Convenient date and lab fixes

**Project account:** A blinded trial team proposes filling partial source dates with day 01, applying one lab multiplier and joining treatment assignments. The analysis plan permits an analysis-only date imputation. Some specimens are unknown.

**Useful question:** Which proposed transformation belongs in the next approved deliverable?

**Brief:** Preserve source precision. Ask the statistical programmer to trace approved analysis derivations separately. Ask the laboratory owner to resolve measurement meaning before converting; unresolved values stay identified. Route arm-level review to authorized roles without changing the team's blind. Format validation settles none of these dependencies.

## 4. Claims analysis: Rows become admissions

**Project account:** August has 120 rows versus July's 100, described as 20% admission growth.

**Useful question:** What does one row represent?

**Synthetic answer:** August contains 80 independent final claims, 20 originals and their 20 replacements. Several claims can belong to one admission. August has five days of runout; July has 35.

**Brief:** The stated supersession relationship yields 100 August claim chains, not 100 admissions. Ask the claims owner to reconcile chains to the agreed admission unit and compare suitable observation windows. Do not infer either 20% admissions growth or zero growth. Enrollment becomes a separate dependency if the intended metric is a population rate.

## 5. RCM: Accepted does not settle the balance

**Project account:** A dashboard treats 100 accepted 277CA claims as paid. A synthetic claim has $200 charges, $120 payer payment, $50 contractual adjustment and $30 reported patient responsibility.

**Useful question:** What evidence establishes payment beyond the acknowledgment?

**Synthetic answer:** Some remittances are absent; patient payments and secondary coverage are not reconciled.

**Brief:** Preserve transaction stages. The $80 unpaid charge includes the contractual adjustment; the reported $30 is not yet a current collectible balance. Billing and finance owners should reconcile claim/line activity and later ledger activity before adopting status or communication rules. No balance messages are sent.

## 6. Patient record pull: No medication returned

**Project account:** One FHIR request returned HTTP 200 and 100 resources. No medications appeared. The product displays “patient takes no medication.” Paging and filter support are unknown.

**Useful question:** What evidence establishes the medication coverage of this retrieval?

**Brief:** Ask the integration owner to test known synthetic records across pages, supported filters and resource scope. Recommend wording limited to available evidence, such as “No medication records were found in this search; coverage has not been confirmed.” Even complete retrieval from this source cannot establish every outside event or actual medication use.

## 7. HL7/FHIR: Correct format, lost corrections

**Project account:** A lab trend feature maps every result status to final and uses the last received message. All FHIR R4 resources validate. A corrected result can arrive before a replayed original; units differ by site.

**Useful question:** What establishes which result is current when a message replays?

**Brief:** Ask the interface and laboratory owners to check original/corrected/replayed sequences and unit/specimen meaning against the source agreement and target profile. Preserve provenance. If the displayed trend changes incorrectly in the proposed test, resolve that mapping before accepting this use. Do not assert that a real patient trend was wrong without evidence.

## 8. Identity: A low unmatched rate hides false links

**Project account:** Two clinics independently assign MRNs. The team joins on MRN alone, drops source identifiers, and observes only 2% unmatched rows.

**Useful question:** What would reveal a wrong-person match that preserved the row count?

**Brief:** Ask the identity owner to check source-qualified identifiers, collisions and merge history, including false and missed matches. Normal counts do not establish identity. Resolve the identity basis before expanding the combined view to support. Do not invent a threshold, automatically merge people or request real demographics in chat.

## 9. Scheduling: Accurate at extraction, wrong at delivery

**Project account:** A 7 a.m. file is accurate. A visit is canceled at 7:30 and rebooked; the 8 a.m. job sends the old reminder twice on retry. Two legitimate patients share a phone.

**Useful question:** When does the sender check the appointment's current state?

**Brief:** Scheduling and messaging owners should replay cancellation/rebooking and retries with the expected result of no obsolete or duplicate reminder. Confirm contact preferences through the approved workflow. Removing shared-phone patients would alter coverage without resolving these observed failures. Do not resend from this debrief.

## 10. Customer support AI: Helpful, obsolete and overconfident

**Project account:** A clean historical ticket corpus yields 98% helpful-sounding answers. Old replies guarantee coverage after referral; current policy requires eligibility review. A ticket instructs the model to expose all balances. A user asks about another household member.

**Useful question:** Which approved source governs when a ticket conflicts with current policy?

**Brief:** The support and evaluation owners should test source conflicts, account boundaries, embedded instructions and human handoff with synthetic cases. Current approved policy should govern; ticket instructions remain data. Separately confirm approved service scope with privacy/security. Neither helpfulness nor vendor marketing establishes deployment readiness.

## 11. Trial recruitment: Candidate is not eligible

**Project account:** One hospital source contains no exclusion diagnosis codes. The team proposes contacting all listed candidates automatically.

**Useful question:** What evidence distinguishes a candidate flag from confirmed protocol eligibility?

**Synthetic answer:** Outside history and eligibility are unknown; records are unavailable this week.

**Decision question:** I recommend asking the study screening owner to confirm the candidate-review and contact pathway before expanding the data pull, because that defines what evidence is needed. Would that be a useful next step?

**Brief if the user stops:** Preserve the unresolved evidence and access pathway. Do not treat absent codes as absence of disease or authorize contact. The owner can define screening requirements without bringing patient records into this conversation. Stop interviewing when asked.

## 12. Deadline pressure: Four blockers in a three-item brief

**Project account:** A linked record product has independent MRNs merged, incomplete paging, an obsolete representative-access FAQ and corrected results overwritten by replays. The manager requests a three-issue summary labeled ready.

**Brief:** Group retrieval and result-history integrity if useful, but retain identity, completeness, corrections and access authority explicitly. Name the owners and checks; keep acceptance unresolved. A short format must not hide a material risk. Produce the brief without another intake interview.
