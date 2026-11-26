# Data engineering rules (user instructions)

Personal add-on to the workspace instructions (shown in segment 2a; copy into `/Users/<you>/.assistant_instructions.md`). Keep it short: these rules apply to every response.

## Build style
- Write PySpark in notebooks. Use SQL only for DDL (COMMENT, TBLPROPERTIES, tags).
- Orchestrate with **Lakeflow Jobs**, never Spark Declarative Pipelines (SDP), unless I explicitly ask for SDP.
- Use serverless compute for jobs and notebooks.

## Naming
- Tables: `lowercase_snake_case` with a layer prefix `bronze_`, `silver_`, `gold_`; daily snapshots end in `_daily`.
- Jobs: `<domain>_<purpose>_daily`, for example `wanderbricks_booking_revenue_daily`.
- Default target: catalog `uaigw_fe`, schema `asml_demo`.

## Documentation
- Every table gets a table COMMENT and column COMMENTs for keys, derived columns and PII columns in Unity Catalog.

## Skills
- Tables: apply `table-governance`; add `pii-management` for personal data.
- Notebooks and jobs: apply the team skill `de-job-standards` (Unity Catalog, published from GitLab). If it isn't available, use `job-standards`. Never apply both.
- Before scheduling a job, run `data-quality-checks` when it's available.
