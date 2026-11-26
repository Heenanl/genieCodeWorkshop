# AGENTS.md: WanderBricks booking revenue (team project memory)

Genie Code automatically reads `AGENTS.md` files in the folder you work in and its parents. This file holds always-on team decisions for this project. Pattern from [genie-code-skills-demo](https://github.com/databricks-solutions/genie-code-skills-demo).

## Read first

Before making changes, read `docs/project_context.md` (owners, SLAs, tables, metric definitions, decisions).

## Always

- Build with PySpark notebooks + Lakeflow Jobs, not SDP. Prefer SQL for simple transformations.
- Target `uaigw_fe.asml_demo`; source `samples.wanderbricks` (read-only).
- Net revenue excludes cancelled bookings (`status = 'cancelled'`); use the latest status from `booking_updates`.
- Tables: `bronze_` / `silver_` / `gold_` prefixes, `audit_timestamp` + `source_system` last. Every new table gets table and column comments.
- For naming conventions and data-quality rules, call the `mcp-data-standards` MCP tools if connected; otherwise follow the `de-job-standards` and `data-quality-checks` skills. Apply `table-governance`; `pii-management` for `users` / `hosts`.
- For structured data access, use Genie Ontology (direct prompting) rather than creating Genie Agents.
- Ask for approval before overwriting or dropping an existing table. Explain the plan first, then generate code.
- Record every new architectural decision in `docs/project_context.md` under Decisions, in the same merge request.
