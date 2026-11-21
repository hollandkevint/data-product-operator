# Route: open source and BI-native

> **As of 2026-11-21. Vendor products change fast. Check vendor docs before you rely on anything here.** Names, features, plans and release status below come from vendor pages read on that date. Items marked unverified were not confirmed on a primary page.

Two routes sit here. Pick open source when you want a self-hosted agent that reads context you keep in files. Pick BI-native when your team already runs a BI tool and wants its agent on top of the semantic model you built there. Both are less work than building your own and give you less control than building your own. The parts map to the [reference architecture](reference-architecture.md).

## Open source

- nao: an open-source agent for chat over data. The data team builds a context folder with a command-line tool. It pulls warehouse metadata, dbt assets, docs and rules into files. Users ask questions from the nao app, Slack, Teams or an MCP client. Answers show the SQL and the source files. It reads context as files and has the model write SQL. The page does not mention a semantic layer. Tests are YAML files with a question and expected SQL. A test command scores them offline. Chat replay and context recommendations feed failures back into the context. The core is Apache 2.0, but some files are under a commercial licence, so read the licence mix before you adopt it. The release read was pre-1.0, so expect change. [nao on GitHub](https://github.com/getnao/nao), [nao site](https://getnao.io)

nao's test format is a small golden-question set. The [analytics-agent skill](../../skills/analytics-agent/SKILL.md) shows how to fill it well: real questions, owned answers, abstention items and a regression cadence.

## BI-native

- Hex Threads and Notebook Agent: Threads is chat over your data connections. It prefers semantic models and endorsed data over raw tables, and a governed mode can limit it to semantic models only. A thread can be saved as a notebook project. The page read had no eval section, and the rest of the Hex docs were not checked (unverified). Release date is unverified. [Threads docs](https://learn.hex.tech/docs/explore-data/threads), [Notebook Agent docs](https://learn.hex.tech/docs/explore-data/notebook-view/notebook-agent)
- Looker and Google's data agents are covered on the [warehouse-native page](warehouse-native.md).

## What to check

1. Does the agent answer from the semantic model only, or can it fall back to raw tables?
2. Where do definition changes get reviewed, and who approves them?
3. Can you replay your own golden set against it, in bulk, on a schedule?
4. Does it show the query behind each answer?
5. What happens when a question is ambiguous or out of scope: a clarifying question, a refusal or a guess?

A vendor's built-in eval is a start. Keep your own golden set as the check that does not depend on the vendor.
