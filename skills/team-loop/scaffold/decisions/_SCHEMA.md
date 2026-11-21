# Decision record schema

> Read this before writing a decision file. The validator rejects a record that is missing a required heading or that has an untagged evidence row.

**Pre-save self-check:**

1. Count the rows under `## Evidence` and `## Explicitly NOT doing`. Count the provenance tags in those rows. The numbers match.
2. `## Status` is one of `pending`, `decided`, `superseded`.
3. `## Decider` names one person.
4. `## What would reverse this` is specific and observable: a metric threshold, a named signal, a date.
5. `## Review date` is a real date.
6. Commentary and gaps go under `## Remaining ambiguities`, never under `## Evidence`.

Filename: `YYYY-MM-DD-<slug>.md`

```markdown
# Decision: <one-line statement>

## Status
pending | decided | superseded

## Date
YYYY-MM-DD

## Decider
<named person>

## Context
<!-- Two to four sentences. The fork in the road. -->

## Options considered
1.
2.

## Decision
<!-- What was picked. Empty for pending. -->

## Why
<!-- The reasoning. Specific. -->

## Evidence
- <claim>  `<provenance-tag>`

## Explicitly NOT doing
- <not-doing>  `<provenance-tag>`

## What would reverse this
<!-- Observable condition. -->

## Review date
YYYY-MM-DD

## Remaining ambiguities
<!-- What is still unknown. -->

## Linked
- Context: `../context/<file>.md`
- Packet: `../packets/<file>.md`
- Gate: `../rules/<file>.md`
```

## Provenance enum

Every row under `## Evidence` and `## Explicitly NOT doing` ends with exactly one of:

- `[source/...](../source/...)` — direct citation of a verbatim input
- `[ingestion/...](../ingestion/...)` — a synthesized note that cites source/
- `(stakeholder-verbal, <name>, <YYYY-MM-DD>)`
- `(intuition, <name>, <YYYY-MM-DD>)`
- `(industry-knowledge)`
- `(chat, no artifact)`
- `(hub, <name>, <YYYY-MM-DD>)` — an engagement hub or shared working document
- `Unknown` — the claim is recorded but has no source yet

A record built from mixed-trust evidence wears that mix on its face.
