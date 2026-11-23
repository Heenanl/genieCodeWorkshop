---
name: table-governance
description: Enforce table and column documentation standards across all tables. Use for every table you create or modify, including Delta tables written by notebooks and jobs. Covers COMMENT, TBLPROPERTIES, column descriptions, PII labeling at the table level, and Unity Catalog tags. This is the baseline governance skill; apply it before any other skill.
---

# Table and Column Governance Standards

Source: `skills/table-governance` in [genie-code-skills-demo](https://github.com/databricks-solutions/genie-code-skills-demo), adapted so the DDL works for tables written by PySpark jobs (not only SDP).

## Table COMMENT (required)

| Layer | Pattern |
| --- | --- |
| Bronze | `Raw <entity> data ingested from <source>` |
| Silver | `Cleaned and validated <entity> with derived metrics from bronze_<entity>` |
| Gold | `Business aggregation: <metric> by <dimensions>` |
| PII | Append ` - CONTAINS PII: <column_list>` |

## TBLPROPERTIES (required)

At minimum `quality` (`bronze`/`silver`/`gold`) and `domain`. Add:

| Condition | Properties |
| --- | --- |
| Contains PII | `contains_pii = "true"`, `pii_columns = "<list>"` |
| Silver/Gold | `delta.enableChangeDataFeed = "true"` |
| Retention | `retention_days = "<n>"` |

Do not set `owner` in TBLPROPERTIES (reserved) or fake ownership with tags.

## Column comments

Document primary/foreign keys, derived columns (formula + units), PII columns (type + risk + masking), DQ flags, audit columns (`audit_timestamp`: "Job execution timestamp", `source_system`: "Upstream source system identifier").

## Template (run after each write in the job notebook)

```sql
COMMENT ON TABLE {catalog}.{schema}.gold_property_health_daily IS
  'Business aggregation: review count and average rating by property';

ALTER TABLE {catalog}.{schema}.gold_property_health_daily SET TBLPROPERTIES (
  'quality' = 'gold', 'domain' = 'guest_experience', 'delta.enableChangeDataFeed' = 'true');

ALTER TABLE {catalog}.{schema}.gold_property_health_daily
  ALTER COLUMN property_id COMMENT 'References samples.wanderbricks.properties.property_id',
  ALTER COLUMN avg_rating COMMENT 'Calculated as AVG(rating) over non-deleted reviews. Units: stars 1-5',
  ALTER COLUMN audit_timestamp COMMENT 'Job execution timestamp',
  ALTER COLUMN source_system COMMENT 'Upstream source system identifier';

ALTER TABLE {catalog}.{schema}.gold_property_health_daily
  SET TAGS ('quality' = 'gold', 'domain' = 'guest_experience', 'pii' = 'false', 'data_classification' = 'internal');
```

## UC tags

| Tag | Values |
| --- | --- |
| `quality` | bronze, silver, gold |
| `domain` | business domain |
| `pii` | true, false |
| `data_classification` | public, internal, confidential, restricted |
| `sla` | daily, hourly, real-time |

## Checklist

- [ ] COMMENT present and descriptive (mentions CONTAINS PII if applicable)
- [ ] TBLPROPERTIES has `quality` and `domain`; no `owner`
- [ ] PII: `contains_pii` + `pii_columns`
- [ ] Column comments for keys, derived, PII, DQ and audit columns
- [ ] UC tags applied
- [ ] `audit_timestamp`, `source_system` are the last two columns
