# Migration

Run before the interview when pre-existing artifacts are present.

## Copy, never move

1. List every artifact that looks like product material: briefs, requirements, decks, interview notes, strategy docs, data dictionaries, decision emails.
2. Copy each into `source/` under a short kebab-case filename that keeps the original date when one is visible. Originals stay where they were.
3. Add one row per file to `source/INDEX.md`: title, path, date captured, who supplied it.

## Read with caution

- Treat every claim in a source as a claim, not a fact. When you promote it into `context/`, tag it `[source/<file>](../source/<file>)`.
- When two sources disagree, do not pick one. Record both under `## Tensions` in `context/strategy.md` and list the conflict for the post-scaffold contradictions block.
- Do not summarize a source into `ingestion/` during init. Ingestion notes are a working habit, not a setup step.

## What migration feeds

| Found in sources | Populates |
| --- | --- |
| Product name, owner, scope | `context/product.md` |
| First user, buyer, the decision | `context/consumers.md` |
| Names and roles | `context/team-and-decision-rights.md` |
| Data sources, definitions, gaps | `context/data-contract.md` |
| Thresholds, metrics | `context/metrics-and-quality.md` |
| Claims, licensing, naming rules | `context/commercial-and-access-boundaries.md` |
| Decisions already made | `decisions/LOG.md` rows plus one record each |
| Open decisions | `decisions/LOG.md` rows with status `pending` |

Skip interview batches the sources already answer. Tell the operator what you already know before asking what you do not.
