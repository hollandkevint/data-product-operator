# Example: Device dashboard preparation

This is a fictional example. No client or patient data was used.

## Supplied account

“We expected a device feed we could group by brand for a hospital dashboard. What arrived was charge-line data with free-text descriptions. One procedure can have multiple lines. An analyst suggested dropping descriptions we can't map. We haven't checked whether unmapped descriptions are concentrated in particular hospitals. The product lead needs to decide what the first dashboard can claim.”

## Example debrief

**Intended use:** Help the product lead define supportable brand comparisons for the first hospital dashboard. The intended counting unit still needs confirmation.

**What happened:** According to the supplied account, the team expected brand-ready data and received charge lines requiring interpretation. Multiple lines per procedure create a counting question. Dropping unmapped descriptions is a proposal; its effect has not been checked.

| Issue | Evidence and uncertainty | Next check | Owner to confirm | What the result changes |
|---|---|---|---|---|
| Counting unit | The account says procedures can have multiple charge lines. The desired metric is unspecified. | Agree whether the dashboard counts charge lines, units, or procedures. Review linkage and counting logic against that definition. | Analytics owner and product lead | Determines which metric the dashboard can describe |
| Mapping ambiguity | Free-text descriptions need mapping. No mapping review was supplied. | Separate exact, ambiguous, and unmapped descriptions and review categories with someone who knows the source. | Domain/data owner | Determines which brand assignments have supporting evidence |
| Exclusion bias | Hospital concentration of unmapped records is unknown. | Compare mapping coverage by hospital before and after proposed exclusions. | Analytics owner | Determines whether hospital comparisons need narrower scope or explicit limitations |

**Next decision:** Confirm the counting unit first. If reliable procedure linkage exists and the intended metric counts procedures, evaluate a procedure-based aggregation. If it does not, assess whether a clearly labeled charge-line metric serves the intended use or whether that comparison must wait. Mapping and coverage checks still apply.

These are proposed checks based on a narrative. No dataset was inspected and no readiness verdict is established.
