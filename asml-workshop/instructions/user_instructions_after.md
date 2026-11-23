# Data engineering rules (user instructions)

Copy into `/Users/<you>/.assistant_instructions.md` for segment 2a. Keep it short: these rules apply to every response.

## Build style
- Write PySpark in notebooks. Use SQL only for DDL (COMMENT, TBLPROPERTIES, tags).
- Orchestrate with **Lakeflow Jobs**, never Spark Declarative Pipelines (SDP), unless I explicitly ask for SDP.
- Use serverless compute for jobs and notebooks.

## Naming
- Tables: `lowercase_snake_case` with a layer prefix `bronze_`, `silver_`, `gold_`; daily snapshots end in `_daily`.
- Jobs: `<domain>_<purpose>_daily`, for example `wanderbricks_property_health_daily`.
- Default target: catalog `genie_code_workshop`, schema `asml_demo`.

## Documentation
- Every table gets a table COMMENT and column COMMENTs for keys, derived columns and PII columns in Unity Catalog.

## Skills
- When writing tables or jobs, apply `job-standards` and `table-governance`. Add `pii-management` for personal data.
