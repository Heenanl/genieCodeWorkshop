# Genie Code hands-on lab: starter handout

**Main track:** your own data in your own ASML environment. **Fallback track:** genieCodeWorkshop on `samples.wanderbricks` (skip the Apps modules).

## 1. Make Genie Code yours in 15 minutes

| Layer | Where | Try this |
| --- | --- | --- |
| Instructions (user) | `/Users/<you>/.assistant_instructions.md` | Start from `instructions/user_instructions_after.md`; replace naming and catalog with yours |
| Instructions (workspace, admins) | `/Workspace/.assistant_workspace_instructions.md` | `instructions/workspace_instructions_example.md`; takes priority over user instructions |
| AGENTS.md / CLAUDE.md | Any folder in your project (auto-discovered up the tree) | Reuse the files your Claude/Copilot teams already have |
| Skills (user) | `/Users/<you>/.assistant/skills/<name>/SKILL.md` | Copy `skills/job-standards`, change the job settings to your team's |
| Skills (workspace) | `/Workspace/.assistant/skills/<name>/SKILL.md` | Team standards, owned by admins |
| Skills (Unity Catalog, Beta) | `<catalog>.<schema>.<skill>`, enabled in Genie Code > Customizations | Team standards published from GitLab; access is a UC grant |
| MCP | Genie Code > Customizations > Connectors | Add a Genie Agent over your tables, or an external MCP (GitLab) |
| Memory | Just say "Remember that ..." | Business rules such as "TST- machines are test rigs, exclude them" |
| Project memory | `AGENTS.md` + `docs/project_context.md` in your Git folder | Copy `project/` and fill in your owners, SLAs, metrics |

Gotchas: start a **new chat** after editing a skill or instructions. A skill's `description` decides when it auto-loads, so make it specific. `@skill-name` forces a skill.

## 2. Skills from your GitLab AI marketplace

What we showed (segment 2c): **GitLab stays the source of truth, Unity Catalog governs, Genie Code consumes.**

1. Skills live in a GitLab repo: `skills/<name>/SKILL.md`, plus `skills.yaml` mapping each folder to `<catalog>.<schema>.<skill>`.
2. GitLab CI validates every merge request (folder name = `name:`, description present, publisher dry run).
3. A Databricks Job (Git source = the GitLab repo, run as a service principal, scheduled or Run now) runs the
   [unity-gateway `publish-skills`](https://github.com/databricks/unity-gateway/tree/main/actions/publish-skills) publisher.
   It creates, updates or skips each UC skill. The workspace pulls from GitLab, so workspace IP access lists don't get in the way.
4. Grant `USE CATALOG`, `USE SCHEMA`, `READ VOLUME` to the teams that should use them; each user enables them in **Genie Code > Customizations**.

Gotchas:
* **Storage:** the skills schema needs a `MANAGED LOCATION` on your own storage. Databricks Default Storage fails with `NotImplemented`.
* **One source per standard:** there's no precedence between user, workspace and UC skills; Genie Code picks by relevance. Don't keep a personal copy of a team skill.
* **Beta:** UC skills in Genie Code are a preview (**Settings > Previews > Unity Gateway skills in Genie**). Workspace skills (`/Workspace/.assistant/skills/`) are the GA alternative, fed from the same GitLab repo.
* Docs: [create and share UC skills](https://learn.microsoft.com/en-us/azure/databricks/agents/uc-skills/create-share-uc-skills/).

## 3. Five best practices

1. Be specific about format, library and detail. Reference assets with `@`. Seed the schema with `SELECT * FROM ...`.
2. Document tables and columns in UC (AI-generated comments). This is the biggest quality lever for machine-data tables.
3. Use one chat per task. Avoid marathon chats and overly broad exploration.
4. Set the effort level to Low for repeated simple tasks.
5. Encode standards as skills and instructions, not long prompts.

## 4. Cost (team admins)

* Pay-as-you-go since 8 Jul 2026, with a per-user free monthly allowance. Query `system.billing.usage` with `billing_origin_product = 'GENIE'` (`cost/genie_code_usage.sql`).
* Import the Genie Code events dashboard (top users, active users, heaviest tasks).
* Budgets per account, workspace, group or user, with alerts. They are an estimate, not a hard cap.
* Diagnose a cost spike: (1) find where usage is concentrated (user/surface/day), (2) find out why (task type, marathon chats, high effort), (3) fix the specific cause (skill, instructions, effort level), (4) apply a per-user budget override if needed.

Docs: [skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills/) · [instructions](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions/) · [MCP](https://learn.microsoft.com/en-us/azure/databricks/genie-code/mcp/) · [memory](https://learn.microsoft.com/en-us/azure/databricks/genie-code/memory/) · [tips](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips/) · [monitor cost](https://learn.microsoft.com/en-us/azure/databricks/genie/monitor-cost/) · [budgets](https://learn.microsoft.com/en-us/azure/databricks/genie/budgets/)
