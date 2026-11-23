# AGENTS.md: WanderBricks property health (team project memory)

Genie Code automatically reads `AGENTS.md` files in the folder you work in and its parents. This file holds always-on team decisions for this project. Pattern from [genie-code-skills-demo](https://github.com/databricks-solutions/genie-code-skills-demo).

## Read first

Before making changes, read `docs/project_context.md` (owners, SLAs, tables, metric definitions, decisions).

## Always

- Build with PySpark notebooks + Lakeflow Jobs, not SDP.
- Target `genie_code_workshop.asml_demo`; source `samples.wanderbricks` (read-only).
- Exclude soft-deleted reviews (`is_deleted = true`) and cancelled bookings (`status = 'cancelled'`) from every metric.
- Tables: `bronze_` / `silver_` / `gold_` prefixes, `audit_timestamp` + `source_system` last.
- Apply `job-standards` and `table-governance` skills; `pii-management` for `users` / `hosts` / review text.
- Record every new architectural decision in `docs/project_context.md` under Decisions, in the same merge request.
