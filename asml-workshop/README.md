# ASML Genie Code Hackathon: Demo Kit (30 Nov 2026)

> **Event:** Mon 30 Nov 2026, 13:00-16:00, Veldhoven  
> **Demo owner:** Heena Refai. Slides, CLI and nice-to-haves: Matteo and Fabian  
> **Audience:** about 40 senior data engineers from Data Services (machine data, pipelines, SAP). Power users who will train 500+ people  
> **Slot:** 18-20 min live demo inside the first hour  
> **Branch:** `asml-workshop` of genieCodeWorkshop

## What this kit is

A cut-down version of the genieCodeWorkshop flow covering only the must-have customization layers:

**baseline -> instructions -> skills (workspace + team skills from GitLab via UC) -> custom MCP App -> Genie Ontology + memory/project memory -> best practices -> cost**

We run **one prompt** at the start, save the output as the baseline, then add one layer at a time and re-run the same prompt so the difference is visible.

### Use case: no new dataset

We don't build a new machine-data use case. The demo reuses what already exists:

| Source | What we reuse |
| --- | --- |
| genieCodeWorkshop (this repo) | WanderBricks data on `samples.wanderbricks`, which every workspace has, so there's no data setup and it also works as the lab fallback track |
| [genie-code-skills-demo](https://github.com/databricks-solutions/genie-code-skills-demo) | `table-governance` and `pii-management` skills, the `AGENTS.md` pattern and the instruction templates |

ASML adaptations, taken from the 13 Nov agreement:

* **Jobs, not SDP.** Team job standards come from the GitLab skills registry as the UC skill `de-job-standards`. `job-standards` (reworked from `sdp-basics`) stays in `skills/` as a personal-skill starter for the lab; it's no longer built live.
* **No pre-built skill library.** We show how to build a skill and where it lives, then how team skills flow from GitLab into Unity Catalog and Genie Code. The GitLab registry is `dbx-group1/asml-demo` (mirror: `Heenanl/geniecode_skills`); its README has the full setup.
* **Apps are disabled at ASML today.** The demo still shows a custom App MCP server (`mcp-data-standards`) in our workspace, framed as "when you re-enable Apps". Genie Agents are no longer shown (being phased out in favour of Genie Ontology; Matteo, 24 Nov).

The storyline is **WanderBricks bookings -> daily booking-revenue Job**. Map it to ASML out loud: property = machine, booking = production run, booking revenue = output KPI, cancelled booking = aborted run.

## Timing (18 min + 2 min buffer, CLI stays with Matteo)

| # | Segment | Time | What you show live | Files |
| --- | --- | --- | --- | --- |
| 0 | Framing | 1 min | "You know Genie Code. Today is about making it yours and keeping it governed." | - |
| 1 | Built-in skills + baseline | 3 min | EDA on `@samples.wanderbricks.bookings`, then "schedule as a daily Databricks Job". Save this output as the baseline | `demo/` (created live) |
| 2a | Instructions | 2 min | Same prompt with a workspace instructions file, compared side by side with the baseline | `instructions/` |
| 2b | Skills (workspace + UC) | 4 min | `de-job-standards` auto-loads; `@data-quality-checks` invoked explicitly; then the GitLab -> Unity Gateway path | GitLab `dbx-group1/asml-demo` |
| 2c | Custom MCP | 2 min | `mcp-data-standards` App: `get_naming_conventions` + `validate_table_name` | `mcp-data-standards/` |
| 2d | Ontology + memory | 2 min | One line on Genie Ontology; memory ("net revenue excludes cancelled bookings"); project memory (`AGENTS.md`) | `project/` |
| 3 | Best practices | 1 min | One slide of 5 tips | `HANDOUT.md` |
| 4 | Cost and usage | 2 min | Billing system-table query + budget screen | `cost/` |
| 5 | Handoff | 1 min | To Matteo/Fabian: CLI, ZeroOps, App Builder, Omnigent, roadmap | - |
| | **Total** | **18 min** | The 2 spare minutes are buffer for Q&A or a slow prompt | |

The full run-of-show with prompts, talk track and fallbacks is in [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

## Folder layout

```
asml-workshop/
├── README.md                      # This file
├── DEMO_SCRIPT.md                 # Minute-by-minute run-of-show, prompts, talk track
├── HANDOUT.md                     # One-page lab starter (handout items)
├── setup/00_setup_and_reset.sql   # Demo schema + reset between rehearsals
├── instructions/
│   ├── user_instructions_after.md         # Paste into /Users/<you>/.assistant_instructions.md in 2a
│   └── workspace_instructions_example.md  # Admin-level version (show only)
├── mcp-data-standards/            # Custom MCP App for 2c (app.yaml, server.py, requirements.txt, README.md)
├── skills/                        # table-governance + pii-management -> /Workspace/.assistant/skills/ in 2b
│   ├── job-standards/             # Personal-skill starter for the lab (team version is the UC skill de-job-standards)
│   │   ├── SKILL.md
│   │   └── scripts/check_table_standards.py
│   ├── table-governance/SKILL.md  # From genie-code-skills-demo, adapted for Jobs
│   └── pii-management/SKILL.md    # From genie-code-skills-demo, adapted for Jobs
├── project/                       # Project memory demo (2d); the AGENTS.md here is auto-discovered
│   ├── AGENTS.md
│   └── docs/project_context.md
└── cost/genie_code_usage.sql      # Billing query for segment 4
```

> **Keep the baseline clean.** `AGENTS.md` files are picked up from the folder you work in and its parents. Run segments 1-2d from a notebook in `asml-workshop/demo/`, which is a sibling of `project/`, so `project/AGENTS.md` doesn't leak into the baseline. Before segment 1, check that no demo skills are in `/Users/<you>/.assistant/skills/` or `/Workspace/.assistant/skills/`, that both instruction files are empty or absent, and that the UC skills and `mcp-data-standards` are switched off in Genie Code > Customizations.

## Custom MCP: Data Standards Gateway
The `mcp-data-standards/` folder contains a Databricks App that serves team standards as MCP tools
(naming rules, DQ check catalog, a table-name validator, project context). Its rules mirror the
UC skills from GitLab, which stay the source of truth. Deploy it to your workspace and connect it in
Genie Code > Customizations > Connectors. See `mcp-data-standards/README.md` for details.

## Genie Ontology
Matteo confirmed (24 Nov): Genie Agents will be phased out in favour of the automated Genie Ontology layer.
For structured data access, use ontology-based prompting directly in Genie Code.
The demo mentions this in segment 2d and the roadmap section covers it in detail.

## Prep checklist (Tue 24 Nov prep block)

* [ ] Run `setup/00_setup_and_reset.sql` (creates `genie_code_workshop.asml_demo`)
* [ ] Pre-run every prompt in `DEMO_SCRIPT.md` and keep the finished outputs in a second tab
* [ ] Baseline notebook + job definition saved as `demo/baseline_*` (don't delete it; it's the comparison)
* [ ] `table-governance` + `pii-management` tested as workspace skills (auto-load and `@` mention), then removed again before the run
* [ ] `mcp-data-standards` App deployed and added under Customizations > Connectors; both 2c prompts return tool calls (then switched off)
* [ ] UC skills: `skills-sync-uc` Job ran successfully, 4 skills in `uaigw_fe.data_services`, visible in Genie Code after enabling them in Customizations (then switched off again)
* [ ] 2c merge request staged in `dbx-group1/asml-demo` (adds `timeout_seconds` + `max_concurrent_runs` to `de-job-standards`), CI green, pre-run tab of the `updated` Job run
* [ ] Memory scenario rehearsed across two chats; delete the memory afterwards so the live run starts clean
* [ ] `cost/genie_code_usage.sql` runs, Genie Code events dashboard imported (handout), budget screen screenshot
* [ ] Timed solo run (hard stop at 20 min) + backup video

## Open questions for the Mon 23 Nov alignment

1. Do participants have workspace-admin rights? If not, workspace instructions and workspace skills are show-only.
2. Are UC skills (Beta preview) and Databricks Apps allowed in ASML's workspace? Does ASML's workspace restrict IP access or outbound access to their GitLab (affects whether CI pushes or the workspace pulls)?
3. CLI: does it stay with Matteo? Is the CLI GA live for ASML?
4. Is the WanderBricks fallback track for the lab OK with Prashant?
5. Who hosts cost: Heena, or Fabian with the admin angle?

## References

* Genie Code docs: [skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills/) · [instructions](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions/) · [MCP](https://learn.microsoft.com/en-us/azure/databricks/genie-code/mcp/) · [memory](https://learn.microsoft.com/en-us/azure/databricks/genie-code/memory/) · [tips](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips/) · [monitor cost](https://learn.microsoft.com/en-us/azure/databricks/genie/monitor-cost/) · [budgets](https://learn.microsoft.com/en-us/azure/databricks/genie/budgets/)
* UC skills: [create and share UC skills](https://learn.microsoft.com/en-us/azure/databricks/agents/uc-skills/create-share-uc-skills/)
* [genie-code-skills-demo](https://github.com/databricks-solutions/genie-code-skills-demo) · [Blog: Personalizing Genie Code](https://www.databricks.com/blog/personalizing-genie-code-instructions-skills-memory-and-mcp)
