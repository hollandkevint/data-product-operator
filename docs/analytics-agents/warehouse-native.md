# Route: warehouse-native

> **As of 2026-11-21. Vendor products change fast. Check vendor docs before you rely on anything here.** Names, features, plans and release status below come from vendor pages read on that date. Items marked unverified were not confirmed on a primary page.

Use this route when your data already sits in one warehouse platform and you want the platform's own agent. The platform supplies the semantic layer, the query engine, governance and an agent. Fit: teams that are all in on one platform. Cost: you depend on that vendor's roadmap and pricing. Ask each vendor what its eval tooling covers. The parts map to the [reference architecture](reference-architecture.md).

## Snowflake

- Cortex Analyst: a managed text-to-SQL API over semantic views. A semantic view holds logical tables, dimensions, metrics, joins, synonyms and verified queries. Run verified queries against it to measure SQL accuracy and watch for regressions. The docs now point teams toward Cortex Agents. [Cortex Analyst docs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
- Cortex Agents: a managed loop that plans, calls tools and reflects. Tools include Cortex Analyst for structured data, Cortex Search for unstructured data, code execution, charts, custom tools, MCP connectors and web search. It offers threads, logs, traces, user feedback and an evaluations feature. Release status is not stated on the page. [Cortex Agents docs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents)
- Snowflake Intelligence: the docs URL for it returned a page about a product called CoWork, built on the Cortex Agent API. Whether CoWork is the renamed Snowflake Intelligence is unverified. [Docs page](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence)

## Databricks

- Genie Agents (formerly called Genie spaces): the data team configures datasets, sample queries, instructions, metrics and verified answers. Answers follow Unity Catalog governance. Add reviewed answers as benchmark questions and score accuracy. Test phrasing variants too. [Genie docs](https://docs.databricks.com/aws/en/genie/), [best practices](https://docs.databricks.com/aws/en/genie/best-practices)
- Agent Bricks: a platform for building and hosting agents, with tools, memory and observability. Evaluation uses MLflow tracing, LLM judges, custom scorers and expert feedback. Genie is reachable through an MCP server. The agent types Agent Bricks offers were not confirmed on the page (unverified). [Agent Bricks docs](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/)
- Release status is not stated on the pages read. Check it before you plan around a feature.

## Google Cloud

- Conversational Analytics API and data agents: agents answer questions over BigQuery, Looker Explores and Data Studio. AlloyDB, Spanner and Cloud SQL support is in Preview. Several features carry Preview tags, so check each one. The docs read had no eval section, only conversation logging for review. An older Data QnA API is deprecated. [API overview](https://docs.cloud.google.com/gemini/docs/conversational-analytics-api/overview)
- Looker route: LookML is the source of truth and Looker builds the query, so the agent does not write raw SQL. An Explore agent takes up to five Explores, instructions, verified queries and glossaries. [Looker conversational analytics](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)

## What these routes leave to you

The vendor tools score some SQL accuracy. None of them replaces a golden set built from your own questions, with abstention items and a named owner. Load the verified queries or benchmark questions from your [golden set](../../skills/analytics-agent/SKILL.md) so the vendor tool and your own harness agree.

Also check, for each vendor:

1. Does the agent run as the consumer's identity, so row and column rules apply?
2. Can you export logs and traces to your own store?
3. What does it cost per question, and who sets the budget?
4. Who owns the semantic layer inside the vendor product, and how do changes get reviewed?
