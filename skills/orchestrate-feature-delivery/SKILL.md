---
name: orchestrate-feature-delivery
description: Orchestrate spiked-epic delivery via dispatched agents and a tracking index. Use when decomposing, sequencing, planning, executing, resuming, tracking, or reworking a spiked epic into features or per-repo PRs.
---

<when-to-use-this-skill>
- User finished a spike and wants to decompose its change summary / solution doc into features or phases (creates the delivery index)
- User wants to sequence which features run in parallel and which wait for another feature's PR to merge
- User wants to dispatch parallel agents to plan (plan-development-task) or execute (execute-plan) feature × repo cells of an epic
- User wants to resume or continue delivery of an existing spiked epic — load the index and derive next actions from its status
- User wants to review or update the delivery index status (cells planned / in-progress / done / failed / blocked)
- User found an issue after a feature was implemented (a cell is done/merged) and wants a focused re-investigation spike on the governing ADR, an appended plan, and its execution
- User wants suggestions for which skill handles each part of a post-implementation rework (spike, ADR update, plan append, execution)
- Do NOT load before a spike's change summary / solution doc exists — let conduct-spike produce them first
- Do NOT load to plan or execute a single, already-scoped change — plan-development-task and execute-plan handle single cells
- Do NOT load to run a standalone spike — conduct-spike runs spikes; this skill only triggers a focused spike to rework a delivered feature
</when-to-use-this-skill>

<knowledge>
<orchestrator-role>
Persistent orchestrator for **one spiked epic**; input is always the **delivery index** plus the spike output (change summary, solution doc, ADRs). It decomposes, sequences, dispatches, and tracks — it never plans, codes, or edits artifacts itself (delegation map in **agent-dispatch**). The index is the single source of truth.
</orchestrator-role>
<feature-definition>
A feature is a coherent, independently valuable deliverable spanning one or more repos.
- **One PR per repo per feature** is a **soft** guideline; split a feature if its repo slice would exceed one reviewable PR.
- Small shared-library changes stay inside the **first consuming feature**; only large or widely-shared changes become leading features.
- IDs: `F1`, `F2`, … with kebab-case names and one-line descriptions.
</feature-definition>
<delivery-layout>
All delivery artifacts for an epic live under one top-level folder — one folder per epic (no `docs/` prefix), named after the spiked epic:
```
deliveries/<epic-name>/               # one folder per epic (epic-name = spike name)
├── <repo-name>/<feature-name>/       # one folder per repo per feature
│   ├── context.md                    # distilled spike context + spike references
│   └── plan.md                       # TDD plan from plan-development-task
└── index.md                          # delivery index (single source of truth)
```
- **index.md** is the delivery index — it lives at the epic folder root (see **reference/delivery-index-format.md**).
- **Feature folders are named by the feature's kebab-case name** (e.g. `wallet-contracts`), never its ID (`F1`) — IDs are reference shorthand only (waves, dependencies).
- **context.md** carries the distilled spike context; **plan.md** is written by **plan-development-task** and executed by **execute-plan** (rework appends `## Rework <date>` — see **post-implementation-rework**).
</delivery-layout>
<dependency-edge-types>
Classify each feature pair: **merge-blocked** (hard — develop after A's contract is known, merge only after A merges) · **contract-first** (soft — develop in parallel, merge after A) · **conflict** (same files/repo — serialize or split) · **independent** (parallel, any order).
Wave computation and intra-feature merge order: **reference/dependency-ordering-guide.md**.
</dependency-edge-types>
<delivery-state-machine>
Each cell follows: **unplanned → planned → in-progress → done**, with **failed** and **blocked** as recoverable side states. Gating splits development from merging: a cell is **develop-ready** when its dependency cells are **planned** (contracts agreed — contract-first and independent cells develop in parallel); a cell is **merge-ready** only when its dependencies are **done** (merged). Full transitions: **reference/orchestration-guide.md**.
</delivery-state-machine>
<agent-dispatch>
Every delivery task is delegated — the orchestrator never performs it (task → agent → skill): spike → **spike-conductor** (**conduct-spike**); plan / execute → **coding-assistant** (**plan-development-task** / **execute-plan**); solution-doc → **solution-doc-writer** (**write-solution-doc**); ADR → **adr-writer** (**draft-adr**).
Dispatch one agent per task, in parallel, subject to **develop-gating** (see **delivery-state-machine**) and **no-conflict** (never run conflicting cells on the same repo simultaneously). Each brief carries the cell's scope brief **plus its spike references** (change-summary items, ADR files, solution-doc section) so the agent loads full context on demand. When planning or execution surfaces solution-doc / ADR changes, dispatch the owning agent for that update — never edit artifacts directly. Use the platform's agent mechanism — detect what is available. Full rules: **reference/orchestration-guide.md**.
</agent-dispatch>
<branch-and-push-conventions>
Execution agents commit locally and small-step; pushing or opening PRs happens only after user confirmation.
- One branch per repo per cell, named per the **repo's branch convention** (detect from existing branches / git config / team docs — or ask; never assume a prefix like `feat/`); created during the execution agent's **Prepare Environment** step.
- Commit after each ✅ step, with no AI-related wording (see **execute-plan** commit-conventions).
- A cell is **done** only after its PR merges or the user confirms the code is verified; pushing alone is not done.
</branch-and-push-conventions>
<post-implementation-rework>
When an issue surfaces after a cell is **done**, re-enter investigation for **that cell only** — scope the focused spike to the affected decision (usually the governing ADR), never the whole epic; run by **spike-conductor** (**conduct-spike**), artifact updates delegated to the owning skills. Rework plans are appended, never merged into implemented steps: append a `## Rework <date>` section at the end of the feature's existing `plan.md` (sibling `rework-plan.md` only if very long); implemented steps stay byte-for-byte unchanged; new steps reference the triggering issue and the reworked ADR decision; execution runs **only** the appended steps; the index records the appended plan location and ADR focus.
</post-implementation-rework>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Dispatching parallel agents, gating, status transitions, or failure handling | Agent dispatch, orchestration loop, resume, failure rules | [reference/orchestration-guide.md](reference/orchestration-guide.md) |
| Classifying dependency edges, computing waves, or intra-feature merge order | Edge types, wave algorithm, develop-vs-merge | [reference/dependency-ordering-guide.md](reference/dependency-ordering-guide.md) |
| Writing or updating the delivery index | Index schema, per-cell briefs, status lifecycle | [reference/delivery-index-format.md](reference/delivery-index-format.md) |
| Handling an issue discovered after a cell is implemented | Focused rework spike, append-only plan, execution | [examples/post-implementation-rework.md](examples/post-implementation-rework.md) |
| Running a full end-to-end decomposition from change summary to index | End-to-end multi-repo example | [examples/multi-repo-feature-decomposition.md](examples/multi-repo-feature-decomposition.md) |
| Running one orchestration round with parallel agents | Dispatch + status-update walkthrough | [examples/orchestration-round.md](examples/orchestration-round.md) |
| Continuing an interrupted epic | Resume walkthrough with mixed statuses | [examples/resume-after-interruption.md](examples/resume-after-interruption.md) |
| Distinguishing parallel vs merge-blocked features | Dependency-ordering-focused example | [examples/parallel-vs-sequential-waves.md](examples/parallel-vs-sequential-waves.md) |
</context-loading-guide>

</knowledge>

<capabilities>
<decompose-change-into-features>
1. Load the spike artifacts: change summary (primary), solution doc, and ADRs.
2. Group change items into coherent, independently valuable features by ADR traceability and target-state module boundaries.
3. Apply the **feature-definition** granularity rules.
4. Assign each feature an ID (`F1`, `F2`, …) and a kebab-case name with a one-line description.
5. Present the feature list to the user and confirm before proceeding.
</decompose-change-into-features>
<map-features-to-repos>
1. For each feature, inventory the repos touched by its change items.
2. Build the feature × repo matrix; each cell represents one pull request (soft guideline — see **feature-definition**).
3. Mark config / data / infra-only cells so their plans expect no code PR.
4. Present the matrix and confirm the repo inventory with the user.
</map-features-to-repos>
<order-feature-delivery>
1. For each pair of features, classify the edge using **dependency-edge-types** (merge-blocked / contract-first / conflict / independent).
2. Build the dependency graph and compute waves via topological order — see **reference/dependency-ordering-guide.md**.
3. For each multi-repo feature, determine the intra-feature PR merge order (contract lib first, consumers last).
4. State per feature: develop now (parallel) vs merge only after which prior PRs.
5. Present the wave plan and confirm with the user.
</order-feature-delivery>
<produce-delivery-index>
1. Write the **delivery index** at `deliveries/<epic-name>/index.md` (one folder per epic, no `docs/` prefix — see **delivery-layout**; `<epic-name>` is the spiked epic's name) per **reference/delivery-index-format.md** — include the **Spike References** block (change summary file, ADR files, solution-doc sections).
2. Create per-repo plan folders in the **repo-first** layout: `deliveries/<epic-name>/{repo}/{feature-name}/plan.md` + `context.md` (see **delivery-layout**).
3. Mark each cell's initial status **unplanned** and its plan location.
4. Verify the index against **reference/delivery-index-format.md** — structure, status values, develop/merge readiness — before confirming.
5. Confirm the index location with the user — from here the epic is driven by **orchestrate-delivery**.
</produce-delivery-index>
<update-delivery-index>
1. After every agent result, update the cell's status per the **delivery-state-machine**: unplanned → planned (plan written), planned → in-progress (execution started), in-progress → done (PR merged or code verified), plus failed or blocked with the reason.
2. When a cell's PR merges, re-check downstream cells — any now develop-ready (dependencies planned) or merge-ready (dependencies done) become dispatchable.
3. Record the agent assignment, plan location, and branch name for each cell (per **branch-and-push-conventions**).
4. Keep the index as the single source of truth; never leave status changes only in conversation.
5. Verify the updated index against **reference/delivery-index-format.md** — status values, readiness, recorded branches — before the next dispatch round.
</update-delivery-index>
<orchestrate-delivery>
1. Load the delivery index — or create it first via **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index** if it does not exist.
2. Assess current state from the index: per-cell statuses, completed waves, ready cells, blocked cells.
3. Select develop-ready cells (dependencies **planned** — see **delivery-state-machine**): status unplanned (→ **plan** agent) or planned (→ **execute** agent); skip done cells; gate merges on dependencies **done**.
4. Dispatch parallel agents, one per cell, respecting develop-gating and no-conflict rules (**reference/orchestration-guide.md**); brief each with its scope, **spike references**, and **branch name**.
5. When plan or execution surfaces solution-doc / ADR changes, dispatch **solution-doc-writer** / **adr-writer** for those updates — never edit artifacts yourself.
6. Collect results and apply **update-delivery-index**.
7. When a cell is ready to integrate, ask the user before pushing its branch or opening a PR (per **branch-and-push-conventions**); never push automatically.
8. Re-assess and report next actions; repeat until all cells are done or the user pauses.
</orchestrate-delivery>
<resume-delivery>
1. Load the existing delivery index plus the spike output.
2. Determine the current state: completed waves (skip), in-progress cells (resume from the last step in `plan.md`), failed cells (ask the user to re-plan or retry), blocked cells (wait for the blocker), unplanned cells (plan next).
3. Apply **orchestrate-delivery** from that state — never redo completed work.
4. Tell the user exactly what is resumed vs skipped before dispatching.
</resume-delivery>
<handle-post-implementation-issue>
1. Identify the affected cell (status **done**) and its governing ADR; scope the re-investigation narrowly to that decision — never the whole epic.
2. Present the skill-routing suggestion — focused spike → **spike-conductor** (conduct-spike); ADR decision → **adr-writer** (draft-adr); target state → **solution-doc-writer** (write-solution-doc); append plan → **coding-assistant** (plan-development-task); run appended plan → **coding-assistant** (execute-plan). Confirm the routing with the user.
3. Dispatch **spike-conductor** for the focused spike, scoped to the governing ADR per **post-implementation-rework**; delegate artifact updates to **adr-writer** / **solution-doc-writer**.
4. Apply **update-delivery-index**: record the rework — ADR focus, new change-summary items, rework wave/feature, appended plan location.
5. Dispatch **plan-development-task** (coding-assistant) to append the rework plan per **post-implementation-rework** — implemented steps never modified.
6. Dispatch **execute-plan** (coding-assistant) to run only the appended rework steps.
7. Apply **update-delivery-index**; ask the user before pushing or opening a PR (per **branch-and-push-conventions**).
</handle-post-implementation-issue>

</capabilities>

<rules>
<rule> When spike output exists but no delivery index, apply **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**. </rule>
<rule> When a delivery index exists and the user wants to drive or continue delivery, apply **orchestrate-delivery**; apply **resume-delivery** when continuing an epic interrupted in a previous session. </rule>
<rule> After any agent reports a result, always apply **update-delivery-index** before dispatching further agents. </rule>
<rule> When dispatching any delivery task (plan, execute, solution-doc update, or ADR update), always dispatch the owning agent per **agent-dispatch** — never perform the task directly. </rule>
<rule> When the user asks about a single cell's plan or status, read the delivery index and route the cell to **plan-development-task** or **execute-plan** — do not re-run the whole orchestration. </rule>
<rule> When an issue surfaces after a feature was implemented (a cell is **done**), apply **handle-post-implementation-issue** — never re-run **decompose-change-into-features** on the whole epic, and never modify the implemented plan. </rule>

</rules>
