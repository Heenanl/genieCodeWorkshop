# Data Services engineering standards (workspace instructions, example)

> Show-only in the demo. A workspace admin saves this as `/Workspace/.assistant_workspace_instructions.md`.
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

## Skills (Approach A: skills in the workspace)
1. `@table-governance`: apply first, to every table
2. `@job-standards`: notebooks, Delta writes, job settings
3. `@pii-management`: tables with personal data

## Skills (Approach B: skills served from GitLab/GitHub via MCP)
Before writing table or job code, fetch each required `skills/<name>/SKILL.md` with the `get_file_contents` tool on the MCP connection `<your-connection>` (owner `<org>`, repo `<repo>`, branch `main`). If the fetch fails, stop and report it; don't fall back to local skills. Remove local `.assistant/skills/` copies when using this approach, because local skills take precedence.
