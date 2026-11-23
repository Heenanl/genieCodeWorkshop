---
name: pii-management
description: Identify, label and mask PII columns in tables written by notebooks and jobs. Use when creating or modifying tables that contain customer, employee, host or other personal data (names, emails, phone numbers, addresses, IDs). Includes detection patterns, table property labeling, column annotation, layer rules and masking SQL.
---

# PII Management

Source: `skills/pii-management` in [genie-code-skills-demo](https://github.com/databricks-solutions/genie-code-skills-demo), adapted from SDP to PySpark jobs.

## Detect PII columns

| Column pattern | PII type | Risk |
| --- | --- | --- |
| `email`, `email_address` | EMAIL | HIGH |
| `phone`, `mobile`, `telephone` | PHONE | HIGH |
| `name`, `first_name`, `last_name`, `full_name` | NAME | MEDIUM |
| `date_of_birth`, `dob` | DOB | MEDIUM |
| `address`, `street`, `postal_code` | ADDRESS | MEDIUM |
| `ssn`, `national_id`, `tax_id` | NATIONAL_ID | CRITICAL |
| `account_number`, `iban` | ACCOUNT | HIGH |
| `card_number`, `cvv` | PAYMENT | CRITICAL |
| free text (`comment`, `messages`) | FREEFORM | HIGH |

In WanderBricks: `users.name`, `users.email`, `hosts.name`, `hosts.email`, `hosts.phone`, `reviews.comment`.

## Label PII tables

- TBLPROPERTIES `contains_pii = "true"` and `pii_columns = "<list>"`
- COMMENT ends with ` - CONTAINS PII: <list>`
- Column comments state type and risk, for example `[PII: EMAIL - HIGH]`
- UC tags `pii = 'true'`, `data_classification = 'confidential'`

## Rules by layer

| Layer | Rule |
| --- | --- |
| Bronze | Pass PII through, fully labeled |
| Silver | Replace raw PII with masked/derived values (`email_hash`, `phone_masked`, drop `name`) |
| Gold | Aggregates only; no individual PII |

## PySpark masking patterns (silver)

```python
from pyspark.sql import functions as F

silver = (
    spark.table("samples.wanderbricks.users")
    .withColumn("email_hash", F.sha2(F.lower(F.trim("email")), 256))
    .drop("email", "name")
)
# phone: keep last 4 digits
# F.concat(F.lit("***-***-"), F.substring(F.regexp_replace("phone", "[^0-9]", ""), -4, 4))
```

## UC column mask (when raw values must stay but be protected)

```sql
CREATE OR REPLACE FUNCTION {catalog}.{schema}.mask_email(email STRING)
RETURNS STRING
RETURN CASE WHEN is_account_group_member('pii_full_access') THEN email ELSE '***@***' END;

ALTER TABLE {catalog}.{schema}.bronze_users ALTER COLUMN email SET MASK {catalog}.{schema}.mask_email;
```

## Checklist

- [ ] Every PII column detected and annotated
- [ ] `contains_pii` / `pii_columns` / COMMENT / tags set
- [ ] Silver has no raw email, phone or name
- [ ] Gold contains aggregates only
