---
name: job-standards
description: Team standards for building batch data processing as PySpark notebooks orchestrated by Lakeflow Jobs. Use whenever you write a notebook that creates or updates Delta tables, or create, schedule or edit a Databricks Job. Covers table naming, audit columns, idempotent writes, data-quality flags and required job settings (schedule, notifications, retries, timeout, tags). Not for Spark Declarative Pipelines (SDP).
---

# Job Standards (PySpark + Lakeflow Jobs)

For teams that build with **Jobs, not SDP**. Apply together with `table-governance` (always) and `pii-management` (personal data).

## Steps

1. **Read before writing.** Inspect source tables in Unity Catalog (columns, comments) before writing transformations.
2. **Write PySpark** in a notebook with widgets `catalog` and `schema` (defaults `uaigw_fe` / `asml_demo`). No hard-coded catalog names in logic.
3. **Name tables** `lowercase_snake_case` with a layer prefix: `bronze_`, `silver_`, `gold_`. Daily snapshots end in `_daily`.
4. **Order columns:** identifiers -> dimensions -> measures -> derived -> `data_quality_flag` (silver) -> **`audit_timestamp`, `source_system` LAST**.
5. **Write idempotently.** Full refresh: `mode("overwrite")` with `overwriteSchema`. Incremental: `MERGE` on the business key, or `replaceWhere` on the date partition for daily snapshots. Never plain `append` for a daily job (re-runs would duplicate rows).
6. **Document** with `table-governance`: table COMMENT, TBLPROPERTIES (`quality`, `domain`), column comments, UC tags.
7. **Validate** by running `scripts/check_table_standards.py` against every table the notebook writes, and fix any failures.
8. **Create the Job** with the settings below.

## Data quality

- Bronze: filter only rows that are unusable (null keys); keep raw values.
- Silver: add `data_quality_flag` (`CLEAN`, `MISSING_<field>`, `INVALID_<field>`).
- Exclude soft-deleted source rows (`is_deleted = true`) from silver/gold unless asked otherwise.
- Fail the task (raise) if the output row count is 0.

## Required job settings

| Setting | Value |
| --- | --- |
| Name | `<domain>_<purpose>_daily` |
| Compute | Serverless |
| Schedule | Quartz `0 0 6 * * ?`, timezone `Europe/Amsterdam` |
| `max_concurrent_runs` | 1 |
| Task retries | `max_retries: 1`, `min_retry_interval_millis: 300000` |
| Timeout | `timeout_seconds: 3600` |
| Notifications | `email_notifications.on_failure` = the job owner |
| Tags | `project: asml_demo`, `layer: <bronze/silver/gold>`, `owner_team: data_services` |
| Parameters | `catalog`, `schema` as job parameters (map to notebook widgets) |

Multi-step work = multiple tasks with `depends_on` (bronze -> silver -> gold), not one giant notebook.

## Example (gold write)

```python
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
target = f"{catalog}.{schema}.gold_property_health_daily"

from pyspark.sql import functions as F

reviews = spark.table("samples.wanderbricks.reviews").filter(~F.col("is_deleted"))
df = (
    reviews.groupBy("property_id")
    .agg(F.count("*").alias("review_count"), F.round(F.avg("rating"), 2).alias("avg_rating"))
    .withColumn("audit_timestamp", F.current_timestamp())
    .withColumn("source_system", F.lit("samples.wanderbricks"))
)
if df.limit(1).count() == 0:
    raise ValueError(f"No rows produced for {target}")
df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(target)
```

## Edge cases

- **User explicitly asks for SDP:** follow the request and say that it deviates from team standard.
- **Source has no `is_deleted` column:** skip that filter; don't invent one.
- **Existing job:** update it in place; never create a duplicate job with the same name.
- **Schema changes on overwrite:** `overwriteSchema` replaces column comments, so re-apply the `table-governance` comments after every write (put the DDL in the same notebook).

## Checklist

- [ ] PySpark notebook with `catalog` / `schema` widgets
- [ ] Layer prefix + snake_case names
- [ ] Audit columns last
- [ ] Idempotent write (overwrite / MERGE / replaceWhere)
- [ ] Soft deletes excluded, zero-row guard
- [ ] `check_table_standards.py` passes
- [ ] Job: serverless, schedule, max 1 concurrent run, retries, timeout, failure email, tags
