"""
MCP server: Data Standards Gateway
Hosted on Databricks Apps. Exposes team data-engineering standards as tools
that Genie Code (or any MCP client) can call.

The rules mirror the team skills published from GitLab (de-job-standards,
data-quality-checks). Keep them in sync: the skills are the source of truth.

Tools:
  get_naming_conventions  - team naming rules for tables, columns, jobs and notebooks
  get_dq_checks           - the standard data-quality check catalog
  validate_table_name     - checks a proposed table name against the convention
  get_project_context     - current project decisions and known risks
"""
import os
import re

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Data Standards Gateway", stateless_http=True)

LAYERS = ("bronze", "silver", "gold")
FREQUENCIES = ("hourly", "daily", "weekly", "monthly")

NAMING = """
| Object | Pattern | Example |
|---|---|---|
| Table | <layer>_[<domain>_]<entity>[_<frequency>], lowercase snake_case | gold_booking_revenue_daily |
| Layer prefix | bronze_, silver_, gold_ | silver_guests |
| Job | <domain>_<purpose>_<frequency>, snake_case | wanderbricks_booking_revenue_daily |
| Notebook | <nn>_<step> | 01_ingest, 02_transform, 03_dq_checks, 04_publish |
| Column | snake_case, no abbreviations | net_revenue_amount |

- Booleans start with is_ / has_. Timestamps end with _timestamp, dates with _date.
- Audit columns go last in every table: audit_timestamp (load time, UTC), source_system.
- Development output goes to uaigw_fe.asml_demo.
"""

DQ_CHECKS = """
| Check | Blocking | Rule |
|---|---|---|
| Row count | yes | > 0, and within +-50% of the 7-day average |
| Primary key unique | yes | COUNT(*) = COUNT(DISTINCT <key>) |
| Not null | yes | key and measure columns have 0 nulls |
| Range | yes | amounts >= 0; dates not in the future |
| Freshness | yes | max(date column) >= current_date - 1 |
| Referential integrity | no | every foreign key exists in its dimension table |
| Reconciliation | yes | gold total vs silver total within 0.1% |

If any blocking check fails, do not publish or schedule the table.
An empty table is a FAIL, never a PASS.
"""

PROJECT_CONTEXT = """
# Project context: WanderBricks booking revenue (demo)

## Purpose
Trusted daily booking revenue per destination and property type.
(ASML analogy: property = machine, booking = production run, revenue = output KPI.)

## Decisions
- Source data: samples.wanderbricks (bookings, booking_updates, payments, properties, destinations).
- Reporting grain: day, by destination and property type.
- Output: uaigw_fe.asml_demo.gold_booking_revenue_daily,
  job wanderbricks_booking_revenue_daily (PySpark notebooks + Lakeflow Jobs, not SDP).
- All gold tables must pass the data-quality checks before a job is scheduled.

## Known risks
- Bookings can be updated after creation (see booking_updates); always use the latest status.
- Currency handling is out of scope for the demo.
"""

NAME_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")


@mcp.tool()
def get_naming_conventions() -> str:
    """Return the team naming conventions for tables, columns, jobs and notebooks.
    Use this before creating or renaming any data asset."""
    return NAMING


@mcp.tool()
def get_dq_checks() -> str:
    """Return the standard data-quality check catalog (blocking and non-blocking checks).
    Use this when building a dq_checks task or validating a table."""
    return DQ_CHECKS


@mcp.tool()
def validate_table_name(proposed_name: str) -> str:
    """Check whether a proposed table name follows the team naming convention
    <layer>_[<domain>_]<entity>[_<frequency>]. Returns OK or a specific violation."""
    name = proposed_name.strip().split(".")[-1]  # accept catalog.schema.table
    if name != name.lower():
        return f"FAIL: '{name}' must be lowercase snake_case."
    if not NAME_RE.match(name):
        return f"FAIL: '{name}' must be lowercase snake_case (letters, digits, single underscores)."
    parts = name.split("_")
    if parts[0] not in LAYERS:
        if parts[-1] in LAYERS:
            fixed = "_".join([parts[-1], *parts[:-1]])
            return f"FAIL: the layer is a prefix, not a suffix. Did you mean '{fixed}'?"
        return f"FAIL: '{name}' must start with a layer prefix: bronze_, silver_ or gold_."
    rest = parts[1:]
    frequency = rest.pop() if rest[-1] in FREQUENCIES else None
    if not rest:
        return f"FAIL: '{name}' needs an entity after the layer, e.g. gold_booking_revenue_daily."
    detail = f"layer={parts[0]}, name={'_'.join(rest)}" + (f", frequency={frequency}" if frequency else "")
    return f"OK: '{name}' follows the convention ({detail})."


@mcp.tool()
def get_project_context() -> str:
    """Return the current project decisions, purpose and known risks.
    Use this before making changes to understand the project scope."""
    return PROJECT_CONTEXT


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("DATABRICKS_APP_PORT", "8000"))
    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=port)
