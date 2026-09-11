---
name: databricks-data-product-review
description: Review a Databricks data product or proposed release using approved metadata and query evidence. Use for Unity Catalog scope, Delta change handling, reconciliation, or a release handoff. Does not provision infrastructure or authorize production writes.
metadata:
  version: "0.1.0"
---

# Databricks Data-Product Review

Produce a release evidence record tied to one intended use, source version and consumer.
Use approved metadata or synthetic evidence when live access is unavailable. Do not invent execution results.

## Establish the boundary

- Confirm the workspace, cloud, principal, SQL warehouse or compute, runtime and permitted task.
- Resolve the actual `catalog.schema.table` names and relevant table versions. Do not guess a release from a familiar name or mix releases silently.
- Record the population, grain, business time window, freshness expectation and accepting owner.
- Inspect the existing query runner and its restrictions before using another execution path.
- Keep credentials out of prompts and artifacts. Do not broaden grants, create shares, enable features or export records as a side effect of review.
- Draft queries by default. Execute only authorized reads through the approved connection; bound scan cost and returned data. A row limit does not bound bytes scanned.

## Review the contract

1. Confirm which governed tables or views the principal can access. Include row filters, masks and downstream sharing where relevant. A catalog's existence does not prove the configuration is safe for the use.
2. Identify keys and expected join cardinality. Check uniqueness at the declared grain before joining. Keep patient identifiers scoped to their source or tenant.
3. Reconcile rows, distinct entities, missing keys, date coverage and relevant subgroup counts before and after each meaningful transformation.
4. Distinguish source-event time, arrival time and table commit time. Record the snapshot used by each query; separate statements against changing tables can disagree legitimately.
5. Review corrections, deletes and late arrivals. Decide which outputs should change and which must remain frozen as a historical release.

## Review Delta changes

- Before a proposed `MERGE`, check duplicate source matches and document a business-supported ordering rule. Do not keep an arbitrary row to silence an error.
- Verify the runtime's duplicate-match semantics. Review `WHEN NOT MATCHED BY SOURCE` carefully: An incremental subset is not evidence that absent target records should be deleted.
- Identify the applicable change data feed implementation, table format, runtime support and available history. Do not assume all change feeds have the same enablement behavior.
- Handle insert, update and delete semantics explicitly. Do not count both update images as new clinical events.
- Record the last processed version, retention limits and recovery plan. Change feed availability is not a permanent audit archive.
- Propose a bounded replay test in an approved nonproduction target. Production writes, checkpoint resets, retention changes and `VACUUM` require separate authority.

## Synthetic review case

A feed has two corrections for the same claim key. An engineer proposes a merge followed by deletion of all unmatched target rows.
Check whether the feed is a complete snapshot or an incremental delivery; resolve correction ordering from source semantics.
The expected review flags both duplicate matching and unintended deletion risk. It does not execute the merge.
A passing staged replay supports only the tested versions and cases, not the original failure's cause or every downstream consumer.

## Return the decision record

Include intended use; principal and object scope; source/table versions; query identifiers; aggregate observations; unresolved explanations; proposed checks with owners; and whether evidence supports the named handoff.
Label each check proposed, executed or independently confirmed. Leave unavailable evidence unresolved.
Separate data fitness from model evaluation, permissions to act and operational supervision.
For healthcare, preserve clinical definitions and ask qualified owners to accept residual risk. Do not turn a technical pass into a clinical or compliance approval.

## Sources and applicability

Official AWS documentation reviewed September 10, 2026; verify the deployed cloud/runtime before using syntax or feature claims.

- [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/): Object scope and governance capabilities; inspect actual configuration.
- [Delta MERGE](https://docs.databricks.com/aws/en/delta/merge): Match semantics and conditional changes vary by runtime.
- [Change data feed](https://docs.databricks.com/aws/en/tables/features/change-data-feed): Implementation requirements, retained history and replay boundaries.

This workflow is proposed operating guidance, not a Databricks certification. No live-workspace validation is claimed.
