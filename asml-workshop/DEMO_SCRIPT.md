# Demo Script: ASML Genie Code Hackathon (max 20 min)

One storyline: **WanderBricks guest reviews -> daily property-health Job**, on `samples.wanderbricks`.
Output lands in `genie_code_workshop.asml_demo` (run `setup/00_setup_and_reset.sql` first).

ASML mapping to say out loud once: *property = machine, review = sensor reading, rating = health KPI, soft-deleted review = test rig.*

To keep to time: every prompt is **pre-run**. Keep a second tab with the finished result for each segment. Show the **job definition**; don't wait for a job run.

| # | Segment | Min |
|---|---|---|
| 0 | Framing | 1 |
| 1 | Built-in skills + baseline | 3 |
| 2a | Instructions | 2 |
| 2b | Skills (personal, built live) | 3 |
| 2c | **Team skills: GitLab -> Unity Catalog** | 3 |
| 2d | MCP: Genie Agent as a tool | 2 |
| 2e | Memory + project memory | 2 |
| 3 | Best practices | 1 |
| 4 | Cost and usage | 2 |
| 5 | Handoff | 1 |

---

## 0. Framing (1 min)

**Show:** Catalog Explorer -> `samples.wanderbricks` (`reviews`, `properties`, `bookings`, `users`) and the empty `genie_code_workshop.asml_demo` schema.

**Say:** "You already know Genie Code. Today is about two things: making it *yours* (your standards, your context) and keeping it *governed* (cost, control). We'll run one prompt, then add one layer at a time and re-run it."

---

## 1. Built-in skills + baseline (3 min)

**Pre-check:**
- No `/Users/<you>/.assistant_instructions.md`.
- No demo skills in `/Users/<you>/.assistant/skills/`.
- No saved memories about WanderBricks.
- **The demo user has no `READ VOLUME` on the `skills.data_services.*` skills.** The team skills from GitLab must stay invisible until 2c (see the reset steps).
- No `WanderBricks Reviews` server in Genie Code **Settings > MCP Servers**.
- Work from a notebook in `asml-workshop/demo/`.

**Prompt 1a (agent mode, new chat):**

> @samples.wanderbricks.reviews profile this table, find properties whose average rating is dropping month over month, and show the distribution of ratings.

**Point out:** it explores UC metadata itself (built-in EDA / Unity Catalog exploration skills), samples the data and builds a chart.

**Prompt 1b:**

> Turn this into a notebook that writes a daily property health table, and schedule it as a Databricks Job that runs daily.

**Point out:** the data engineering + jobs skills, the way ASML actually works.

**Save** the notebook as `demo/baseline_property_health` and screenshot the job settings. **This is the baseline.**

What the baseline usually lacks (check during the pre-run and keep only what you actually saw):

* [ ] Table naming convention (`gold_` prefix, snake_case)
* [ ] Table and column COMMENTs, TBLPROPERTIES
* [ ] Audit columns (`audit_timestamp`, `source_system`)
* [ ] Soft-deleted reviews (`is_deleted = true`) excluded
* [ ] Job: failure notifications, timeout, retries, tags, max concurrent runs = 1

**One sentence:** "Pipelines/SDP, Lakeflow Designer, dashboards and MLflow also ship as built-in skills. We stay on Jobs because that's how you build."

---

## 2a. Instructions (2 min)

**Show:** the two files side by side:

* User: `/Users/<you>/.assistant_instructions.md`
* Workspace: `/Workspace/.assistant_workspace_instructions.md` (admins only; takes priority over user instructions)

**Do:** paste [`instructions/user_instructions_after.md`](instructions/user_instructions_after.md) into the user file (pre-staged; just open it). Open [`workspace_instructions_example.md`](instructions/workspace_instructions_example.md) as "this is what your platform team would own".

**New chat, re-run Prompt 1b** (with 1a's context, or say "Build a notebook from @samples.wanderbricks.reviews that writes a daily property health table and schedule it as a daily Databricks Job").

**Side-by-side with baseline. Point out:** PySpark, `gold_property_health_daily` naming, UC comments, Job not SDP, serverless.

**Say:** "Instructions are always on: short global rules. They're not the place for a 3-page standard. That's what skills are for."

*(handout)* `AGENTS.md` / `CLAUDE.md` are also picked up automatically, which is useful for teams already on Claude or Copilot.

---

## 2b. Skills: personal, built live (3 min)

**Build live** (paste from pre-staged [`skills/job-standards/SKILL.md`](skills/job-standards/SKILL.md)):

1. Create `/Users/<you>/.assistant/skills/job-standards/SKILL.md`. Walk through the anatomy: frontmatter `name` + `description` (the description is what triggers auto-load), rules, an example, edge cases.
2. Add `scripts/check_table_standards.py`: "skills can ship code, not just prose."
3. Also copy `table-governance/` and `pii-management/`: "these two come straight from the public genie-code-skills-demo repo, adapted from SDP to Jobs."

**New chat** (gotcha: skills load at chat start, so always start a new chat after editing one).

**Prompt 2b-1 (auto-load):**

> Build a daily Job that writes a gold table of guest satisfaction per property from samples.wanderbricks.reviews and properties.

**Point out:** in the reasoning panel, `job-standards` + `table-governance` load **without being mentioned**; output has audit columns last, TBLPROPERTIES, idempotent write, job with notifications/timeout/retries/tags, and it runs the checker script.

**Prompt 2b-2 (explicit):**

> @pii-management @job-standards add a silver guest table from samples.wanderbricks.users to this job.

**Point out:** `email` hashed, `name` dropped/masked, `contains_pii` properties.

**Bridge to 2c:** "That's *my* skill, in *my* folder. Nice for prototyping, but 500 engineers won't each copy a folder. Your standards live in GitLab. So let's put GitLab in charge."

---

## 2c. Team skills: GitLab -> Unity Catalog -> Genie Code (3 min)

**The architecture (one slide, 20 s):**

```
GitLab repo (source of truth)  ──git fetch──▶  Databricks Job "skills-sync-uc"  ──▶  UC skills  ──▶  Genie Code
merge request + CI validation                  (runs inside the workspace,           skills.data_services.*     (Unity Gateway
                                               as a service principal)               GRANT = who can use it     skills preview)
```

**Pre-stage (before the session):**
- Preview **Unity Gateway skills in Genie** is on.
- Job `skills-sync-uc` has run successfully, and the 4 skills exist in `skills.data_services`: `de-job-standards`, `uc-documentation`, `data-quality-checks`, `code-review-checklist`.
- An **open merge request** in `dbx-group1/asml-demo` changes `skills/de-job-standards/SKILL.md`. It adds `timeout_seconds: 3600` and `max_concurrent_runs: 1` to the job settings, which are two of the gaps in the baseline. Its CI `validate_skills` check is green.
- A pre-run tab of the Job run that shows `updated: skills.data_services.de-job-standards`.

**Do first (10 s): retire the personal copy.** Delete `/Users/<you>/.assistant/skills/job-standards/`. Keep `table-governance/` and `pii-management/`.
**Say:** "The team standard replaces my personal copy. There's no precedence order between skill sources, and Genie Code picks skills by relevance, so keep **one** source per standard."

**Show (60 s): the governance path.**
1. **GitLab:** the repo layout (`skills/<name>/SKILL.md`, `skills.yaml` maps each folder to a UC name). Then open the MR. The **`validate_skills` pipeline** checks names and frontmatter before anything can merge. **Merge it.**
2. **Databricks:** **Jobs > skills-sync-uc > Run now**. While it runs: "This Job pulls from GitLab: the workspace fetches the repo, so nothing in GitLab needs a Databricks credential or network access into the workspace. It runs as a service principal, so a person's login never publishes the team standard." Switch to the pre-run tab: `updated: …de-job-standards`, and the other three skills `unchanged`.
3. **Catalog Explorer > skills > data_services:** the 4 skills as Unity Catalog securables, with an owner, permissions, and a full audit trail.

**Do live (30 s): access is a GRANT.**
```sql
GRANT USE CATALOG ON CATALOG skills TO `<demo-group>`;
GRANT USE SCHEMA  ON SCHEMA  skills.data_services TO `<demo-group>`;
GRANT READ VOLUME ON SKILL   skills.data_services.`de-job-standards` TO `<demo-group>`;   -- repeat per skill, or use Catalog Explorer > Permissions
```

**New chat, Prompt 2c:**

> Build a daily Job that writes a gold table of guest satisfaction per property from samples.wanderbricks.reviews and properties.

**Point out:**
- `de-job-standards` (and `data-quality-checks` for the `dq_checks` task) load from **Unity Catalog** without being mentioned.
- Same conventions as 2b: `gold_` table prefix, snake_case job name `wanderbricks_guest_satisfaction_daily`, `audit_timestamp` / `source_system` last, a `project: asml_demo` tag.
- **New since the merge:** `timeout_seconds: 3600` and `max_concurrent_runs: 1`, which were **merged in GitLab 2 minutes ago**.

**Say:** "Same SKILL.md format as the folder skill I just wrote. GitLab owns the content and the review process, and Unity Catalog owns who can use it. Your AI marketplace stays in GitLab; Databricks just governs and serves it. The same skills work in Claude Code, Copilot or Cursor through Unity Gateway."

*(handout)* How it's wired: CI validates on every MR. The Job `skills-sync-uc` (Git source = GitLab, run as service principal, every 15 min or Run now) runs the publisher from `databricks/unity-gateway`. It creates, updates or skips each skill, and never deletes one. With ASML's self-hosted GitLab runners on an allowed network, CI can publish directly on merge instead (`publish_to_unity_catalog` job). Setup steps are in the repo README.

**Status to say honestly:** "UC skills in Genie Code are a **Beta preview** today. Workspace skill folders are the generally available option."

---

## 2d. MCP: Genie Agent as a tool (2 min)

**Bridge:** "Skills tell Genie Code *how* to work. MCP servers give it *tools* it can call: live systems and curated knowledge it doesn't hold itself."

**Pre-stage:** the Genie Agent **WanderBricks Reviews** (over `reviews`, `properties`, `bookings`) exists, and the demo group has access to it and its tables.

**Show (20 s):** Genie Code -> Customizations -> **Connectors**: the built-in connectors (Slack, GitHub, Atlassian, ...), then the custom/external MCP servers and the per-tool enable toggles. Admins control which servers are available; users pick from the approved ones.

**Do live: add the server (30 s):** Genie Code pane -> **Settings** -> **MCP Servers** -> **Add Server** -> **Genie Agent** -> select **WanderBricks Reviews** -> **Save**.

**Say while the dialog is open:** "Four kinds of server live here: a **UC MCP Service** for external servers, **Unity Catalog functions** as SQL tools, **AI Search** indexes, and **Genie Agents**. The fifth option, an App-hosted custom MCP server, needs Databricks Apps, which you won't have until next year, so everything today runs without Apps."

**New chat, Prompt 2d:**

> Ask the WanderBricks Reviews agent which property types had the most 1-star reviews last quarter, then use that to propose an alert threshold for the property health job.

**Point out:** the agent call shows up in the reasoning panel as a **tool call**. The business answer comes from a curated Genie space your analysts already maintain, and Genie Code turns it into an engineering decision.

**Say (one line, no demo):** "Need live GitLab access, like code search, open MRs or pipeline status? The same dialog takes GitLab's MCP server as a **UC MCP Service**: an `EXECUTE` grant decides who can use it, and per-user OAuth means each engineer only sees the repos they already have. For *standards*, use the skills from 2c; MCP is for live data and actions."

---

## 2e. Memory + project memory (2 min)

**Prompt (chat A):**

> Remember that WanderBricks reviews with is_deleted = true are soft-deleted and must always be excluded from any metric.

**New chat B:**

> Give me the average rating per property type for the last 90 days.

**Point out:** the `is_deleted = false` filter appears without being told (476 soft-deleted rows in the sample data). Show the memory entry.

**Say:** "Instructions = rules **you** write, applied every time. Memory = context Genie Code **gathers** and recalls when relevant. Both are personal."

**Project memory (team-wide):** open [`project/AGENTS.md`](project/AGENTS.md) + [`project/docs/project_context.md`](project/docs/project_context.md). Open a notebook inside `project/` and ask:

> What's the SLA and owner for the property health job, and which tables does it write?

**Say:** "This lives in Git, so it's reviewed in merge requests, like the team skills in 2c, and shared with all 500 people you'll train. It fits your GitLab-first approach."

---

## 3. Best practices (1 min, one slide)

Tie each tip back to a moment from the demo:

1. **Be specific + `@` reference assets** (format, library, detail; seed schema with `SELECT * FROM ...`), as in Prompt 1a's `@samples.wanderbricks.reviews`.
2. **Document tables and columns in UC** (AI-generated comments). This is the biggest quality lever for machine-data tables, and the reason 1a found the right columns on its own.
3. **One chat per task**, no marathon chats. We started a new chat every segment.
4. **Effort level Low** for repeated simple tasks.
5. **Standards as skills, live systems as MCP tools.** Keep team skills in GitLab, served from UC, with one source per standard (2c); connect tools like the Genie Agent (2d). Our prompts stayed one line.

---

## 4. Cost and usage (2 min)

**Say:** "Since 8 Jul 2026 Genie Code is pay-as-you-go with a per-user free monthly allowance, tracked through Unity Gateway."

**Run:** [`cost/genie_code_usage.sql`](cost/genie_code_usage.sql) (pre-run): billed usage per user/day for `surface = 'GENIE_CODE'`, then free vs paid per user this month.

**Show:** a budget screen: budgets per account, workspace, group or user, with alerts. **An estimate, not a hard cap.**

*(handout)* Genie Code events dashboard; the 4-step "diagnose a cost spike" flow.

---

## 4b. Genie Code CLI (optional, 2 min, only if ahead of time)

Run Prompt 2b-1 in a terminal with the Genie Code CLI. Note that the CLI has its own skills and instructions today. The same UC skills from 2c can be loaded into CLI agents through Unity Gateway.

---

## 5. Handoff (1 min)

"That's the customization stack: instructions, skills (personal and team-governed from GitLab), MCP tools, memory, plus the cost guardrails. Matteo and Fabian will now show where this goes next: the CLI, ZeroOps, App Builder and Omnigent."

---

## Fallbacks

| If... | Then... |
| --- | --- |
| A live run is slow | Switch to the pre-run tab and narrate the reasoning panel |
| A skill doesn't auto-load | `@job-standards` explicitly; check you started a new chat |
| UC skill doesn't load in 2c | New chat? Preview on? `READ VOLUME` granted to the group you're in? Then `@de-job-standards` explicitly |
| `skills-sync-uc` run is slow or fails | Show the pre-run successful run (`updated: …`); usual causes: the GitLab access token on the service principal expired, or the MR isn't merged yet |
| Genie Agent not offered in Add Server, or the call fails | Check the demo user has access to the agent and its tables; otherwise show the pre-run tab and move on |
| Memory not recalled | Show the saved memory entry, then say "recall is relevance-based, unlike instructions" |

## Reset between rehearsals

1. Run the reset section of `setup/00_setup_and_reset.sql`
2. Empty `/Users/<you>/.assistant_instructions.md`
3. Remove demo skill folders from `/Users/<you>/.assistant/skills/`
4. Delete the WanderBricks memory (ask Genie Code to forget it)
5. Delete the demo jobs created by Genie Code (Jobs UI, filter by tag `project:asml_demo`). **Not** `skills-sync-uc`.
6. Remove **WanderBricks Reviews** from Genie Code Settings -> MCP Servers so the live "Add Server" step works again (keep the Genie Agent itself)
7. **Revoke the 2c grants** so the team skills are invisible again: `REVOKE READ VOLUME ON SKILL skills.data_services.<skill> FROM <demo-group>` (per skill), plus the schema/catalog grants
8. **Re-stage the 2c MR:** revert the merged change on `main` (Revert button on the MR), **Run now** on `skills-sync-uc`, then open a fresh MR with the same change

## Pre-run checks (delete this section before sharing)

- [ ] You can GRANT/REVOKE `READ VOLUME` on the skills (they're owned by the service principal `gitlab-skills-publisher`); confirm the exact `GRANT … ON SKILL` syntax, or use Catalog Explorer > Permissions
- [ ] The team skills are really invisible before 2c. If they show up because you own the `skills` catalog, rehearse 2c with a separate demo user or group
- [ ] Time one `skills-sync-uc` run (serverless startup), and keep the pre-run tab ready
- [ ] Your 2b `job-standards` user skill uses the same conventions as the UC `de-job-standards`: `gold_` prefix, snake_case job names, `audit_timestamp` / `source_system` last, `project` tag
