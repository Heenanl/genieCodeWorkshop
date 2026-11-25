# Data Services engineering standards (workspace instructions, example)

> Pasted live in segment 2a. A workspace admin saves this as `/Workspace/.assistant_workspace_instructions.md`.
> Workspace instructions apply to every user and take priority over user instructions.
> Adapted from `instructions/.assistant_workspace_instructions.md` in genie-code-skills-demo (SDP replaced by Jobs).

## Platform rules
- Build batch processing as PySpark notebooks orchestrated by Lakeflow Jobs. Do not create SDP pipelines unless asked.
- Use serverless compute. Never hard-code secrets, tokens or workspace URLs; use secret scopes.
- Never write to production catalogs from interactive sessions.

## Table documentation policy
- Every table MUST have a COMMENT and TBLPROPERTIES with at least `quality` and `domain`. Do not set `owner` (reserved).
- Tables with personal data MUST set `contains_pii = "true"` and `pii_columns`.
- Primary keys, derived columns and PII columns MUST have column comments.
- Apply UC tags `quality`, `domain`, `pii`, `data_classification`.

## Naming
- Tables `lowercase_snake_case` with `bronze_` / `silver_` / `gold_` prefixes.
- `audit_timestamp` and `source_system` are the LAST two columns of every table.

## Skills
Team standards live in the GitLab skills repo, are reviewed in merge requests, published to
Unity Catalog (`skills.data_services`) and enabled in Genie Code > Customizations. Keep **one
source per standard**; there is no precedence order between skill sources.

1. `@table-governance`: apply first, to every table. It implements the documentation policy
   above; where `uc-documentation` differs, this policy wins.
2. `@de-job-standards` (UC): notebooks, job structure and job settings. If it isn't available,
   use `@job-standards`. Never apply both.
3. `@data-quality-checks` (UC): before publishing a table or scheduling a job.
4. `@pii-management`: tables with personal data.
5. `@code-review-checklist` (UC): before a merge request, or when asked "is this production ready".

## Tools
- When the `mcp-data-standards` connector is enabled, always call `get_naming_conventions` before creating a table and `validate_table_name` before finalising the name.
- For structured data questions, use Genie Ontology (direct prompting in Genie Code) rather than creating Genie Agents.
