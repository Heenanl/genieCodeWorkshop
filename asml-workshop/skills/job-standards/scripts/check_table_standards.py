"""Check a Delta table against the job-standards + table-governance rules.

Usage in a notebook (Spark session available):

    %run ./check_table_standards   # or paste this function into a cell
    check_table_standards("genie_code_workshop.asml_demo.gold_property_health_daily")

Returns a list of failure messages (empty list = pass) and prints a summary.
Only reads metadata; never modifies the table.
"""

import re

LAYER_PREFIXES = ("bronze_", "silver_", "gold_")
REQUIRED_PROPS = ("quality", "domain")
AUDIT_COLUMNS = ["audit_timestamp", "source_system"]
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def check_table_standards(full_name: str) -> list:
    failures = []
    parts = full_name.split(".")
    if len(parts) != 3:
        return [f"Use a fully qualified name catalog.schema.table, got: {full_name}"]
    table = parts[2]

    # 1. Naming
    if not NAME_PATTERN.match(table):
        failures.append(f"Table name '{table}' is not lowercase_snake_case")
    if not table.startswith(LAYER_PREFIXES):
        failures.append(f"Table name '{table}' has no layer prefix {LAYER_PREFIXES}")

    # 2. Table comment
    detail = spark.sql(f"DESCRIBE DETAIL {full_name}").first()
    if not detail["description"]:
        failures.append("Missing table COMMENT")

    # 3. TBLPROPERTIES
    props = {r["key"]: r["value"] for r in spark.sql(f"SHOW TBLPROPERTIES {full_name}").collect()}
    for p in REQUIRED_PROPS:
        if p not in props:
            failures.append(f"Missing TBLPROPERTY '{p}'")
    if props.get("contains_pii") == "true" and not props.get("pii_columns"):
        failures.append("contains_pii=true but 'pii_columns' is not set")

    # 4. Audit columns last, and column comments
    fields = spark.table(full_name).schema.fields
    names = [f.name for f in fields]
    if names[-2:] != AUDIT_COLUMNS:
        failures.append(f"Last two columns must be {AUDIT_COLUMNS}, got {names[-2:]}")
    undocumented = [f.name for f in fields if not f.metadata.get("comment")]
    if undocumented:
        failures.append(f"Columns without COMMENT: {undocumented}")

    status = "PASS" if not failures else f"FAIL ({len(failures)})"
    print(f"[{status}] {full_name}")
    for f in failures:
        print(f"  - {f}")
    return failures
