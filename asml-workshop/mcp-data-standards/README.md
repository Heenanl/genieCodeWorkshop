# mcp-data-standards

A custom Databricks App that serves team data-engineering standards as an MCP server
("Data Standards Gateway"). Genie Code connects to it and calls the tools when relevant.

The rules mirror the team skills published from GitLab (`de-job-standards`,
`data-quality-checks`): `gold_` / `silver_` / `bronze_` **prefix**, snake_case job names,
`audit_timestamp` + `source_system` last. The skills are the source of truth; keep this in sync.

## Tools
| Tool | What it returns |
|---|---|
| `get_naming_conventions` | Table, column, job and notebook naming rules |
| `get_dq_checks` | The standard data-quality check catalog |
| `validate_table_name` | `OK` or `FAIL` with the reason, for a proposed table name |
| `get_project_context` | Project decisions, purpose and known risks (booking revenue demo) |

`validate_table_name` examples (tested locally over MCP):

| Input | Result |
|---|---|
| `gold_booking_revenue_daily` | OK (layer=gold, name=booking_revenue, frequency=daily) |
| `booking_revenue_gold` | FAIL: the layer is a prefix, not a suffix. Did you mean `gold_booking_revenue`? |
| `Gold_Booking` | FAIL: must be lowercase snake_case |
| `gold_daily` | FAIL: needs an entity after the layer |

## Deploy
Requires Databricks Apps in the workspace.

UI: **Unity Gateway > MCPs > + MCP > Build a new MCP server**, create a custom app named
`mcp-data-standards`, sync this folder to the workspace, then **Deploy**.

CLI equivalent:
```bash
databricks apps create mcp-data-standards --profile <PROFILE>
databricks sync . /Workspace/Users/<you>/mcp-data-standards --profile <PROFILE>
databricks apps deploy mcp-data-standards \
  --source-code-path /Workspace/Users/<you>/mcp-data-standards --profile <PROFILE>
```

`requirements.txt` pins `mcp<2`: MCP 2.x renamed `FastMCP` to `MCPServer`, and `server.py`
uses the 1.x API. Unpinned, the App crashes on startup.

## Connect to Genie Code
Genie Code > **Customizations** > **Connectors** > **Add MCP server** > **Custom MCP server** >
select `mcp-data-standards` > **Save**. The MCP endpoint is `https://<app-hostname>/mcp`.

## Run locally
```bash
pip install -r requirements.txt
DATABRICKS_APP_PORT=8000 python server.py   # MCP endpoint: http://localhost:8000/mcp
```
