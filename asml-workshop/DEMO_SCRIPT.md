# Demo Script: ASML Genie Code Hackathon (18 min + 2 min buffer)

One storyline: **WanderBricks bookings -> daily booking-revenue Job**, on `samples.wanderbricks`.
Output lands in `genie_code_workshop.asml_demo` (run `setup/00_setup_and_reset.sql` first).

ASML mapping to say out loud once: *property = machine, booking = production run, booking revenue = output KPI, cancelled booking = aborted run.*

To keep to time: every prompt is **pre-run**. Keep a second tab with the finished result for each segment. Show the **job definition**; don't wait for a job run.

| # | Segment | Min | What you show live |
|---|---|---|---|
| 0 | Framing | 1 | "You know Genie Code. Today is about making it yours and keeping it governed." |
| 1 | Built-in skills + baseline | 3 | EDA on `@samples.wanderbricks.bookings`, then "schedule as a daily Databricks Job". Save as the baseline |
| 2a | Instructions | 2 | Same prompt with a workspace instructions file, side by side with the baseline |
| 2b | Skills (workspace + UC) | 4 | `de-job-standards` auto-loads; `@data-quality-checks` explicitly; then GitLab -> Unity Gateway path |
| 2c | Custom MCP | 2 | `mcp-data-standards` App: `get_naming_conventions` + `validate_table_name` |
| 2d | Ontology + memory | 2 | One line on Genie Ontology; memory ("net revenue excludes cancelled bookings"); project memory (`AGENTS.md`) |
| 3 | Best practices | 1 | One slide of 5 tips |
| 4 | Cost and usage | 2 | Billing system-table query + budget screen |
| 5 | Handoff | 1 | To Matteo/Fabian: CLI, ZeroOps, App Builder, Omnigent, roadmap |
| | **Total** | **18** | 2 spare minutes for Q&A or a slow prompt |

---

## 0. Framing (1 min)

**Show:** Catalog Explorer -> `samples.wanderbricks` (`bookings`, `booking_updates`, `properties`, `destinations`) and the empty `genie_code_workshop.asml_demo` schema.

**Say:** "You already know Genie Code. Today is about two things: making it *yours* (your standards, your context) and keeping it *governed* (cost, control). We'll run one prompt, then add one layer at a time and re-run it."

---

## 1. Built-in skills + baseline (3 min)

**Pre-check:**
- `/Workspace/.assistant_workspace_instructions.md` and `/Users/<you>/.assistant_instructions.md` are empty or absent.
- The **UC skills are switched off** in Genie Code > Customizations, and the workspace skills `table-governance` / `pii-management` aren't in `/Workspace/.assistant/skills/` yet (pre-staged copies ready to drop in).
- `mcp-data-standards` is **switched off** in Customizations > Connectors.
- No saved memories about WanderBricks.
- Work from a notebook in `asml-workshop/demo/`.

**Prompt 1a (agent mode, new chat):**

> @samples.wanderbricks.bookings profile this table, show the distribution of booking status, and trend total_amount per month.

**Point out:** it explores UC metadata itself (built-in EDA / Unity Catalog exploration skills), samples the data and builds a chart.

**Prompt 1b:**

> Turn this into a notebook that writes a daily booking revenue table, and schedule it as a Databricks Job that runs daily.

**Point out:** the data engineering + jobs skills, the way ASML actually works.

**Save** the notebook as `demo/baseline_booking_revenue` and screenshot the job settings. **This is the baseline.**

What the baseline usually lacks (check during the pre-run and keep only what you actually saw):

* [ ] Table naming convention (`gold_` prefix, snake_case)
* [ ] Table and column COMMENTs, TBLPROPERTIES
* [ ] Audit columns (`audit_timestamp`, `source_system`)
* [ ] Cancelled bookings (`status = 'cancelled'`) excluded from revenue
* [ ] Job: failure notifications, timeout, retries, tags, max concurrent runs = 1

**One sentence:** "Pipelines/SDP, Lakeflow Designer, dashboards and MLflow also ship as built-in skills. We stay on Jobs because that's how you build."

---

## 2a. Instructions (2 min)

**Show:** the two files side by side:

* Workspace: `/Workspace/.assistant_workspace_instructions.md` (admins only; applies to everyone and takes priority over user instructions)
* User: `/Users/<you>/.assistant_instructions.md` (personal additions)

**Do:** paste [`instructions/workspace_instructions_example.md`](instructions/workspace_instructions_example.md) into the workspace file (pre-staged; just open it). Open [`user_instructions_after.md`](instructions/user_instructions_after.md) as "and this is what each engineer can add on top".

**New chat, re-run Prompt 1b** (or say "Build a notebook from @samples.wanderbricks.bookings that writes a daily booking revenue table and schedule it as a daily Databricks Job").

**Side-by-side with baseline. Point out:** PySpark, `gold_booking_revenue_daily` naming, UC comments, `audit_timestamp` / `source_system` last, Job not SDP, serverless.

**Say:** "Instructions are always on: short global rules your platform team owns. They're not the place for a 3-page standard. That's what skills are for."

*(handout)* `AGENTS.md` / `CLAUDE.md` are also picked up automatically, which is useful for teams already on Claude or Copilot.

---

## 2b. Skills: workspace + Unity Catalog (4 min)

**Pre-stage (before the session):**
- Preview **Unity Gateway skills in Genie** is on.
- Job `skills-sync-uc` has run successfully, and the 4 team skills exist in `uaigw_fe.data_services`: `de-job-standards`, `uc-documentation`, `data-quality-checks`, `code-review-checklist`.
- An **open merge request** in `dbx-group1/asml-demo` changes `skills/de-job-standards/SKILL.md`. It adds `timeout_seconds: 3600` and `max_concurrent_runs: 1` to the job settings, which are two of the gaps in the baseline. Its CI `validate_skills` check is green.
- Pre-run tabs: the Job run that shows `updated: uaigw_fe.data_services.de-job-standards`, and Prompt 2b-1 re-run after the merge.

**1. Anatomy (30 s).** GitLab -> `skills/de-job-standards/SKILL.md`: frontmatter `name` + `description` (the description is what triggers auto-load), steps, an example, edge cases, plus `references/naming-conventions.md`. "Skills are folders of Markdown, and they can ship scripts too."

**2. Turn them on (20 s).**
- Drop `table-governance/` and `pii-management/` into `/Workspace/.assistant/skills/`: "workspace skills, owned by the platform team".
- Genie Code > **Customizations** > **Skills**: enable the Unity Catalog skills.
- **Say:** "UC decides who *may* use a skill (a `READ VOLUME` grant); each engineer opts in. There's no precedence order between skill sources, so keep **one** source per standard."

**3. New chat, Prompt 2b-1 (auto-load):**

> Build a daily Job that writes a gold table of booking revenue per destination and property type from samples.wanderbricks.bookings and properties.

**Point out:** in the reasoning panel, `de-job-standards` (UC) and `table-governance` (workspace) load **without being mentioned**. The output has tasks ingest -> transform -> dq_checks -> publish, retries, a failure notification, tags including `project`, `gold_booking_revenue_daily`, audit columns last.

**4. Prompt 2b-2 (explicit):**

> @data-quality-checks validate gold_booking_revenue_daily and add the checks as the dq_checks task of this job.

**Point out:** one query per check from the skill's check catalog, a PASS/FAIL table, and blocking checks wired into the job.

**5. The GitLab -> Unity Gateway path (90 s).**
```
GitLab repo (source of truth)  ──git fetch──▶  Databricks Job "skills-sync-uc"  ──▶  UC skills  ──▶  Genie Code
merge request + CI validation                  (runs inside the workspace,           uaigw_fe.data_services.*   (Unity Gateway
                                               as a service principal)               GRANT = who can use it     skills preview)
```
1. **GitLab:** open the MR. The **`validate_skills` pipeline** checks names and frontmatter before anything can merge. **Merge it.**
2. **Databricks:** **Jobs > skills-sync-uc > Run now**. While it runs: "This Job pulls from GitLab: the workspace fetches the repo, so nothing in GitLab needs a Databricks credential or network access into the workspace. It runs as a service principal, so a person's login never publishes the team standard." Switch to the pre-run tab: `updated: …de-job-standards`, the other three `unchanged`.
3. **Catalog Explorer > uaigw_fe > data_services:** the skills as Unity Catalog securables, with an owner, permissions, and an audit trail.
4. **Pre-run tab of Prompt 2b-1 after the merge:** the job now has `timeout_seconds: 3600` and `max_concurrent_runs: 1`.

**Say:** "GitLab owns the content and the review process, and Unity Catalog owns who can use it. Your AI marketplace stays in GitLab; Databricks governs and serves it. The same skills work in Claude Code, Copilot or Cursor through Unity Gateway. UC skills in Genie Code are a **Beta preview** today; workspace skills are the GA alternative, fed from the same repo."

*(handout)* With ASML's self-hosted GitLab runners on an allowed network, CI can publish directly on merge instead (`publish_to_unity_catalog` job). Setup steps are in the skills repo README.

---

## 2c. Custom MCP: Data Standards Gateway (2 min)

**Bridge:** "Skills put knowledge into the context. MCP servers give Genie Code **tools** it can call, including ones that compute or check things."

**Pre-stage:** the App [`mcp-data-standards`](mcp-data-standards/README.md) is deployed and added in Customizations > Connectors (switched off until now).

**Show (30 s):** Genie Code -> **Customizations** -> **Connectors**: the standard connectors (Gmail, Slack, GitHub, ...), then the custom `mcp-data-standards` with its 4 tools. Switch it on.

**New chat, Prompt 2c-1:**

> What are the naming conventions for this project?

**Point out:** Genie Code calls `get_naming_conventions` (visible as a tool call in the reasoning panel).

**Prompt 2c-2:**

> Validate the table names booking_revenue_gold and gold_booking_revenue_daily.

**Point out:** `validate_table_name` returns **FAIL** for `booking_revenue_gold` ("the layer is a prefix, not a suffix. Did you mean `gold_booking_revenue`?") and **OK** for `gold_booking_revenue_daily`. A skill can only *describe* the rule; a tool *checks* it deterministically. The workspace instructions tell Genie Code to validate every new table name this way.

**Say:** "In production, this App reads your standards from Unity Catalog. ASML has Apps disabled today; when you re-enable them, this is how you expose your GitLab AI marketplace, internal runbooks or any REST API as tools Genie Code can call. Admins decide which connectors exist; each user switches them on."

---

## 2d. Genie Ontology + memory (2 min)

**Genie Ontology (one line):** "For structured data access, the direction is **Genie Ontology**: an automated layer that replaces Genie Agents. You'll see it in the roadmap section."

**Memory, chat A:**

> Remember that net revenue always excludes cancelled bookings (status = 'cancelled').

**New chat B:**

> Give me net revenue per destination per month.

**Point out:** the `status <> 'cancelled'` filter appears without being told (15,285 cancelled bookings, about 8.4M of `total_amount`, in the sample data). Show the memory entry.

**Say:** "Instructions = rules **you** write, applied every time. Memory = context Genie Code **gathers** and recalls when relevant. Memory is **per user**, not shared."

**Project memory (team-wide):** open [`project/AGENTS.md`](project/AGENTS.md) + [`project/docs/project_context.md`](project/docs/project_context.md). Open a notebook inside `project/` and ask:

> What's the SLA and owner for the booking revenue job, and which tables does it write?

**Say:** "This lives in Git, so it's reviewed in merge requests, like the team skills, and shared with all 500 people you'll train. It's the team-shared alternative to personal memory."

---

## 3. Best practices (1 min, one slide)

Tie each tip back to a moment from the demo:

1. **Be specific + `@` reference assets** (format, library, detail; seed schema with `SELECT * FROM ...`), as in Prompt 1a's `@samples.wanderbricks.bookings`.
2. **Document tables and columns in UC** (AI-generated comments). This is the biggest quality lever for machine-data tables, and the reason 1a found the right columns on its own.
3. **One chat per task**, no marathon chats. We started a new chat every segment.
4. **Effort level Low** for repeated simple tasks.
5. **Standards as skills, checks as tools.** Keep team skills in GitLab, served from UC (2b); expose deterministic checks as MCP tools (2c). Our prompts stayed one line.

---

## 4. Cost and usage (2 min)

**Say:** "Since 8 Jul 2026 Genie Code is pay-as-you-go with a per-user free monthly allowance, tracked through Unity Gateway."

**Run:** [`cost/genie_code_usage.sql`](cost/genie_code_usage.sql) (pre-run): billed usage per user/day for `surface = 'GENIE_CODE'`, then free vs paid per user this month.

**Show:** a budget screen: budgets per account, workspace, group or user, with alerts. **An estimate, not a hard cap.**

*(handout)* Genie Code events dashboard; the 4-step "diagnose a cost spike" flow.

---

## 5. Handoff (1 min)

"That's the customization stack: instructions, skills (team-governed from GitLab via Unity Catalog), MCP tools, memory, plus the cost guardrails. Matteo and Fabian will now show where this goes next: the CLI, ZeroOps, App Builder, Omnigent and the roadmap, including Genie Ontology."

---

## Fallbacks

| If... | Then... |
| --- | --- |
| A live run is slow | Switch to the pre-run tab and narrate the reasoning panel |
| A skill doesn't auto-load | New chat? Switched on in Customizations (UC) or in `/Workspace/.assistant/skills/` (workspace)? Then `@de-job-standards` explicitly |
| `skills-sync-uc` run is slow or fails | Show the pre-run successful run (`updated: …`); usual causes: the GitLab access token on the service principal expired, or the MR isn't merged yet |
| `mcp-data-standards` doesn't respond | Check the App is running (Compute > Apps) and the connector is switched on; otherwise show `server.py` and the pre-run tab |
| Memory not recalled | Show the saved memory entry, then say "recall is relevance-based, unlike instructions" |

## Reset between rehearsals

1. Run the reset section of `setup/00_setup_and_reset.sql`
2. Empty `/Workspace/.assistant_workspace_instructions.md` and `/Users/<you>/.assistant_instructions.md`
3. Remove `table-governance/` and `pii-management/` from `/Workspace/.assistant/skills/`
4. Switch the UC skills off in Genie Code > Customizations > Skills (keep the UC grants)
5. Switch `mcp-data-standards` off in Customizations > Connectors (keep the App running)
6. Delete the WanderBricks memory (ask Genie Code to forget it)
7. Delete the demo jobs created by Genie Code (Jobs UI, filter by tag `project:asml_demo`). **Not** `skills-sync-uc`
8. **Re-stage the 2b MR:** revert the merged change on `main` (Revert button on the MR), **Run now** on `skills-sync-uc`, then open a fresh MR with the same change

## Pre-run checks (delete this section before sharing)

- [ ] `skills-sync-uc` exists in the hackathon workspace (target `uaigw_fe.data_services`) and has run successfully
- [ ] UC skills switched off in Customizations really disappear from "list your skills" in a new chat, and come back when switched on
- [ ] Apps are enabled in the demo workspace; `mcp-data-standards` deployed; the Connectors path (Add MCP server > Custom MCP server) matches the UI
- [ ] Prompt 2b-1 doesn't already exclude cancelled bookings (otherwise the 2d memory moment is weaker); if it does, keep the memory demo but point at the saved entry
- [ ] `de-job-standards` and `mcp-data-standards` give the same naming rules (`gold_` prefix). The skills repo is the source of truth
- [ ] Pre-run outputs saved for every prompt; the old reviews-based notebooks in `demo/` and `dry-run/` replaced by booking-revenue ones
