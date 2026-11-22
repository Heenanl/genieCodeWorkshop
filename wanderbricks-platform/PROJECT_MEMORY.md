# PROJECT_MEMORY.md — wanderbricks-platform

> Last updated: 2026-11-22
> Owner: heena.refai@databricks.com

## Project Identity
Student bundle for the Genie Code workshop (WanderBricks Intelligence Platform). Grows across vibe sessions:
infra (this scaffold) -> AI Search -> AppKit app. Repo-level plan: `../PROJECT_MEMORY.md`.

## Architecture
* Source data: `samples.wanderbricks` (16 tables, read-only). Read directly; no raw-file volume / Auto Loader.
* Target catalog: `genie_code_workshop` (`var.catalog`).
* Schemas (`resources/schemas/`): `<prefix>_bronze`, `<prefix>_silver`, `<prefix>_gold` (prefix `var.schema_prefix` = `wanderbricks`).
* Volume (`resources/volumes/`): `reference_docs` in bronze — analytics handbook PDF for the flywheel.
* Pipeline `wanderbricks_medallion` (serverless SDP, Python `dp` API), `src/pipelines/wanderbricks_medallion/transformations/`:
  * bronze.py — metadata-driven MVs, one per table in the `bronze_tables` pipeline config.
  * silver.py — bookings (+nights_count), properties (+destination), reviews (non-deleted), support_messages (flattened).
  * gold.py — destination_revenue_monthly, property_performance (handbook GBV / net revenue / ADR rules).
* Job `wanderbricks_platform_refresh`: daily 06:00 UTC pipeline refresh (paused in dev mode).

## Targets & Environments
* dev (default, development mode — resource names prefixed `[dev <user>]`, schedules paused).
* prod (production mode, root_path under /Users/heena.refai@databricks.com, run_as heena.refai).

## Conventions
* Reference schemas via `${resources.schemas.<key>.*}`, never raw vars.
* One resource per `resources/<type>/<name>.<type>.yml` file.
* Business definitions come from `docs/reference/wanderbricks-analytics-handbook.md`.

## Next (Vibe Session 1 remainder)
* Metric views (revenue, occupancy, guest satisfaction) on gold.
* Genie agent over gold; Lakebase project for app state; feature tables; secret scope.
* Job tasks for data dictionary + handbook ingestion/index.

## Open Questions
* Superhost / occupancy need available-nights logic — implement in metric views or gold?
