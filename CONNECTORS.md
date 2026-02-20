# Connecting Your Data Stack

This plugin works without any connections. But connecting your data warehouse or project tools lets commands read live schemas, query metadata, and pull sprint artifacts directly.

## Supported Connectors

| Category | Tool | MCP Server Key |
|----------|------|---------------|
| Data Warehouse | Snowflake | `snowflake` |
| Data Warehouse | BigQuery | `bigquery` |
| Data Warehouse | Databricks | `databricks` |
| Data Warehouse | PostgreSQL | `postgres` |
| Orchestration | dbt Cloud | `dbt-cloud` |
| Project Management | Linear | `linear` |
| Project Management | Jira | `jira` |

## Setup

Add your connections to `.mcp.json` in the project root (or your global Claude Code config):

```json
{
  "mcpServers": {
    "postgres": {
      "type": "http",
      "url": "http://localhost:3100/mcp"
    },
    "dbt-cloud": {
      "type": "http",
      "url": "https://cloud.getdbt.com/mcp"
    },
    "linear": {
      "type": "http",
      "url": "https://mcp.linear.app/sse"
    }
  }
}
```

Replace URLs with your actual MCP server endpoints. Each tool's MCP server documentation has setup instructions.

## What Each Connector Enables

- **Data Warehouse**: `/dpo:review-data-model` can read live schemas. `/dpo:review-data-quality` can run sample queries.
- **dbt Cloud**: `data-pipeline-quality` skill can reference your actual dbt project structure, tests, and models.
- **Linear/Jira**: `/dpo:reshape-sprint` can pull sprint artifacts directly instead of requiring copy-paste.

No connector is required. Every command works with manually provided context.
