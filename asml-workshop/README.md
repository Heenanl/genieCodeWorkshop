# ASML Genie Code Hackathon: Demo Kit (30 Nov 2026)

> **Event:** Mon 30 Nov 2026, 13:00-16:00, Veldhoven  
> **Demo owner:** Heena Refai. Slides, CLI and nice-to-haves: Matteo and Fabian  
> **Audience:** about 40 senior data engineers from Data Services (machine data, pipelines, SAP). Power users who will train 500+ people  
> **Slot:** 18-20 min live demo inside the first hour  
> **Branch:** `asml-workshop` of genieCodeWorkshop

## What this kit is

A cut-down version of the genieCodeWorkshop flow covering only the must-have customization layers:

**baseline -> instructions -> skills (personal, then team skills from GitLab via UC) -> MCP -> memory/project memory -> best practices -> cost**

We run **one prompt** at the start, save the output as the baseline, then add one layer at a time and re-run the same prompt so the difference is visible.

### Use case: no new dataset

We don't build a new machine-data use case. The demo reuses what already exists:

| Source | What we reuse |
| --- | --- |
| genieCodeWorkshop (this repo) | WanderBricks data on `samples.wanderbricks`, which every workspace has, so there's no data setup and it also works as the lab fallback track |
| [genie-code-skills-demo](https://github.com/databricks-solutions/genie-code-skills-demo) | `table-governance` and `pii-management` skills, the `AGENTS.md` pattern, the instruction templates and the GitHub/UC HTTP MCP pattern for skills from Git |

ASML adaptations, taken from the 13 Nov agreement:

* **Jobs, not SDP.** `sdp-basics` from the skills-demo repo is reworked into `job-standards`, which covers PySpark notebooks, Delta writes and Lakeflow Jobs. This is the skill we build live.
* **No pre-built skill library.** We show how to build a skill and where it lives, then how team skills flow from GitLab into Unity Catalog and Genie Code. The GitLab registry is `dbx-group1/asml-demo` (mirror: `Heenanl/geniecode_skills`); its README has the full setup.
* **Apps are disabled.** We don't use Apps-hosted MCP. The MCP part uses a Genie Agent; external (GitLab) MCP is mentioned, not demoed, because skills come from the UC sync.

The storyline is **WanderBricks guest reviews -> daily property-health Job**. Map it to ASML out loud: properties = machines, reviews = sensor readings, ratings = health KPI, `is_deleted` = test rigs.

## Timing (20 min, CLI stays with Matteo)

| # | Segment | Time | Live | Files |
| --- | --- | --- | --- | --- |
| 0 | Framing | 1 min | "You know Genie Code. Today is about making it yours and keeping it governed." | - |
| 1 | Built-in skills + baseline | 3 min | EDA on `@reviews`, then "schedule as a daily Job". Save the output as the baseline | `demo/` (created live) |
| 2a | Instructions | 2 min | Same prompt with instructions, side by side with the baseline | `instructions/` |
| 2b | Skills (personal) | 3 min | Build `job-standards`, watch it auto-load, `@job-standards` | `skills/` |
| 2c | Team skills: GitLab -> UC | 3 min | Merge an MR in GitLab, Run now on `skills-sync-uc`, enable UC skills in Customizations, same prompt picks up the change | GitLab `dbx-group1/asml-demo` |
| 2d | MCP: Genie Agent | 2 min | Connectors tab, add the WanderBricks Reviews Genie Agent, it answers inside Genie Code | - |
| 2e | Memory + project memory | 2 min | "Remember: is_deleted reviews are excluded", new chat applies it, then `AGENTS.md` | `project/` |
| 3 | Best practices | 1 min | 5 tips, each tied to a moment they just saw | `HANDOUT.md` |
| 4 | Cost and usage | 2 min | Billing system-table query plus the budget screen | `cost/` |
| 5 | Handoff | 1 min | To Matteo/Fabian: CLI, ZeroOps, App Builder, Omnigent | - |

4b (CLI, 2 min) only fits if you're ahead of time.

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
├── skills/                        # Copy to /Users/<you>/.assistant/skills/ (or Workspace/.assistant/skills/)
│   ├── job-standards/             # Built live in 2b (adapted from sdp-basics)
│   │   ├── SKILL.md
│   │   └── scripts/check_table_standards.py
│   ├── table-governance/SKILL.md  # From genie-code-skills-demo, adapted for Jobs
│   └── pii-management/SKILL.md    # From genie-code-skills-demo, adapted for Jobs
├── project/                       # Project memory demo (2d); the AGENTS.md here is auto-discovered
│   ├── AGENTS.md
│   └── docs/project_context.md
└── cost/genie_code_usage.sql      # Billing query for segment 4
```

> **Keep the baseline clean.** `AGENTS.md` files are picked up from the folder you work in and its parents. Run segments 1-2d from a notebook in `asml-workshop/demo/`, which is a sibling of `project/`, so `project/AGENTS.md` doesn't leak into the baseline. Before segment 1, check that `/Users/<you>/.assistant/skills/` contains no demo skills, that `/Users/<you>/.assistant_instructions.md` is empty or absent, and that the UC skills are switched off in Genie Code > Customizations.

## Prep checklist (Tue 24 Nov prep block)

* [ ] Run `setup/00_setup_and_reset.sql` (creates `genie_code_workshop.asml_demo`)
* [ ] Pre-run every prompt in `DEMO_SCRIPT.md` and keep the finished outputs in a second tab
* [ ] Baseline notebook + job definition saved as `demo/baseline_*` (don't delete it; it's the comparison)
* [ ] Skills copied into `/Users/<you>/.assistant/skills/`, tested for auto-load and `@` mention (then removed again before the run)
* [ ] Genie Agent "WanderBricks Reviews" created over `samples.wanderbricks.reviews`, `properties`, `bookings` and enabled under Customizations > Connectors
* [ ] UC skills: `skills-sync-uc` Job ran successfully, 4 skills in `skills.data_services`, visible in Genie Code after enabling them in Customizations (then switched off again)
* [ ] 2c merge request staged in `dbx-group1/asml-demo` (adds `timeout_seconds` + `max_concurrent_runs` to `de-job-standards`), CI green, pre-run tab of the `updated` Job run
* [ ] Memory scenario rehearsed across two chats; delete the memory afterwards so the live run starts clean
* [ ] `cost/genie_code_usage.sql` runs, Genie Code events dashboard imported (handout), budget screen screenshot
* [ ] Timed solo run (hard stop at 20 min) + backup video

## Open questions for the Mon 23 Nov alignment

1. Do participants have workspace-admin rights? If not, workspace instructions and workspace skills are show-only.
2. Are UC skills (Beta preview) allowed in ASML's workspace? Does ASML's workspace restrict IP access or outbound access to their GitLab (affects whether CI pushes or the workspace pulls)?
3. CLI: does it stay with Matteo? Is the CLI GA live for ASML?
4. Is the WanderBricks fallback track for the lab OK with Prashant?
5. Who hosts cost: Heena, or Fabian with the admin angle?

## References

* Genie Code docs: [skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills/) · [instructions](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions/) · [MCP](https://learn.microsoft.com/en-us/azure/databricks/genie-code/mcp/) · [memory](https://learn.microsoft.com/en-us/azure/databricks/genie-code/memory/) · [tips](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips/) · [monitor cost](https://learn.microsoft.com/en-us/azure/databricks/genie/monitor-cost/) · [budgets](https://learn.microsoft.com/en-us/azure/databricks/genie/budgets/)
* UC skills: [create and share UC skills](https://learn.microsoft.com/en-us/azure/databricks/agents/uc-skills/create-share-uc-skills/)
* [genie-code-skills-demo](https://github.com/databricks-solutions/genie-code-skills-demo) · [Blog: Personalizing Genie Code](https://www.databricks.com/blog/personalizing-genie-code-instructions-skills-memory-and-mcp)
