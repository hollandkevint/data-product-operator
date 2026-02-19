---
name: ethical-risk-assessment
version: 0.1.0
description: >
  Ethical data risk evaluation, bias testing protocols, and governance practices for
  data products. Use when evaluating ML/AI features for fairness, designing bias
  testing protocols, planning phased rollouts for high-risk changes, reviewing
  data governance practices, or when someone asks "could this model be biased?" or
  "how do we ship AI features responsibly?" For HIPAA-specific guidance, see
  healthcare-data-domain.
user-invocable: false
---

## The Fifth Risk

Standard product risk frameworks cover four risks: value, usability, feasibility, and business viability (see `data-product-thinking`). Data products add a fifth: **ethical data risk**.

Ethical data risk asks: Can we build this without bias, privacy violations, or unintended harm?

This risk is owned by the Data Lead, who has veto authority. A technically correct model that produces biased outcomes is worse than no model. This is not optional and not delegated to a compliance review.

## Ethics Canvas

Before committing to any ML/AI feature, complete this structured evaluation:

1. **Training data**: What are the sources? What biases exist in the collection method? Which populations are overrepresented or underrepresented?
2. **Features used**: Which input variables could proxy for protected classes? (ZIP code proxies for race; insurance type proxies for income)
3. **Accuracy by group**: Does model performance vary across demographic groups? Test across race, gender, age, and geography at minimum.
4. **Known limitations**: What does the model NOT do well? Document before shipping, not after complaints.
5. **Transparency requirements**: Can you explain to a user how the model reached its conclusion? If not, the model should not make autonomous decisions.

CRITICAL: Complete the ethics canvas before writing a line of model code. Discovering bias after deployment is 10x more expensive than preventing it.

## Bias Testing Protocol

Run bias audits quarterly or before any model update:

1. Define protected classes for your domain (race, gender, age, geography, insurance status, language)
2. Split test data by each protected class
3. Compare model accuracy, false positive rate, and false negative rate across groups
4. Flag any disparity greater than a defined threshold (e.g., 5% accuracy difference)
5. If flagged, investigate root cause and apply calibration before production

Real example: A propensity scoring model showed 8% accuracy disparity for Black patients. Root cause was underrepresentation in training data. Calibration layer added before production deployment.

## Phased Rollout Protocol

Non-negotiable for high-risk changes (new ML models, major algorithm updates, data source migrations):

1. **Internal**: Team uses the output for 1-2 weeks. Catch obvious bugs.
2. **Pilot customer**: One trusted customer validates with real workflows.
3. **5% traffic**: Monitor quality metrics, bias metrics, and user feedback.
4. **25% traffic**: Expand if metrics hold. Investigate any anomalies.
5. **Full rollout**: Only after all stages pass quality and bias thresholds.

NEVER skip phased rollout for ML features. "It tested well in staging" is not evidence it works in production. Production data is messier, more diverse, and more adversarial than test data.

## Governance Practices

**Privacy by design**: Data minimization, anonymization, and access controls from day one. Not added later. Not optional for sensitive data.

**Transparency reports**: Published documentation on how ML models work, what data they use, what decisions they make, and what biases are known. Update quarterly.

**Incident response playbook**: Detect (monitoring alert) -> Assess (severity, scope) -> Contain (disable feature if needed) -> Fix (root cause) -> Communicate (affected users) -> Learn (update practices). Have the playbook before you need it.

**Ethical sign-off**: Data Lead reviews bias test results, approves transparency report, validates privacy-preserving deployment. Required before any ML/AI feature ships. This is a gate, not a suggestion.

## Data Quality SLAs as Governance

Quality thresholds are governance instruments:
- 99.9% accuracy verified against gold standard
- Data freshness within 24 hours
- 99.5% uptime
- Zero known algorithmic bias incidents

When SLAs breach, the circuit breaker fires (see `data-quality-assessment`). This is how governance becomes operational rather than bureaucratic.
