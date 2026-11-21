# Route: build your own

> **As of 2026-11-21. Vendor products change fast. Check vendor docs before you rely on anything here.** Names, features, plans and release status below come from vendor pages read on that date. Items marked unverified were not confirmed on a primary page.

Use this route when you need control over the agent loop, the tools and the eval, or when no single platform holds your data. You assemble four things: an agent framework, data access tools, a semantic layer or curated views, and your own eval suite. Cost: you own the glue, the upgrades and the on-call. The parts map to the [reference architecture](reference-architecture.md).

## Agent framework

- Claude Agent SDK: Claude Code's agent loop as a library, in Python and TypeScript. It brings built-in tools, hooks, subagents, MCP, permissions, sessions and skills. It has no semantic layer and no text-to-SQL of its own. You supply data access and context. The docs page read had no eval harness, so build one. Releases move fast, so pin versions. Third parties may not offer claude.ai login in their products, so plan on API keys. [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)

## Data access and meaning

- dbt semantic layer and dbt MCP server: an MCP server that exposes dbt assets to an agent. Tool groups cover the Semantic Layer, SQL, metadata discovery, the admin API, codegen and dbt commands. Metrics are queried by name through MetricFlow, with no free-form joins. A text-to-SQL tool exists and admins can hide it. You can run it yourself or use a remote server on dbt platform plans. The server is read-only. It has no built-in eval. The Semantic Layer API needs a dbt platform plan, and the exact tiers are unverified. [dbt MCP docs](https://docs.getdbt.com/docs/dbt-ai/about-mcp), [dbt-mcp repo](https://github.com/dbt-labs/dbt-mcp)
- MotherDuck and DuckDB MCP server: a local MCP server for DuckDB and MotherDuck with tools to run queries and list databases, tables and columns. It is raw SQL with catalog discovery and no semantic layer. It is read-only by default, but its README warns that read-only is not enough when third parties get access. Results are capped. Good for cheap local prototypes. [mcp-server-motherduck repo](https://github.com/motherduckdb/mcp-server-motherduck)

## A sketch of the build

1. Pick one domain and one consumer. Write the metric definitions first.
2. Expose the definitions through a semantic layer, or through curated views if you have no layer yet.
3. Give the agent a small tool set: list metrics, query a metric, run read-only SQL on approved views, show the SQL.
4. Put identity and row rules at the data layer, not in the prompt.
5. Log every conversation with the question, the SQL, the answer and the identity.
6. Build the eval harness at the same time as the agent. See the [analytics-agent skill](../../skills/analytics-agent/SKILL.md) and the worked set in [`team-loop/grader/`](../../team-loop/grader/).

## Public benchmarks for model choice

- Spider 2.0: enterprise text-to-SQL tasks scored by execution. It has Snowflake, BigQuery and SQLite variants and a DuckDB variant of repo-level dbt tasks. Use the dbt variant to test agents that build pipelines. [Spider 2.0](https://spider2-sql.github.io/), [repo](https://github.com/xlang-ai/Spider2)
- BIRD: question and SQL pairs across many databases, scored on execution accuracy, with interactive and agentic modes. [BIRD](https://bird-bench.github.io/)

Both benchmarks are public and clean. They do not test your schema, your metric definitions or your ambiguity. Use them to compare models. Do not use them to approve your agent.
