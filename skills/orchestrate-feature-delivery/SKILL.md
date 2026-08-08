---
name: orchestrate-feature-delivery
description: Orchestrate delivery of a spiked epic: decompose spike output into repo-mapped feature waves, dispatch agents for planning, execution, and solution-doc/ADR updates, and keep the delivery index current. Use when decomposing, sequencing, planning, executing, resuming, or tracking the delivery of spiked work into features, phases, or per-repo pull requests.
---

<when-to-use-this-skill>
- User finished a spike and wants to decompose its change summary / solution doc into features or phases for delivery (creates the delivery index)
- User wants to sequence which features can proceed in parallel and which must wait for another feature's PR to merge first
- User wants to dispatch parallel agents to plan (via plan-development-task) or execute (via execute-plan) feature × repo cells of an epic
- User wants to resume or continue delivery of an existing spiked epic at any time — the delivery index is loaded and next actions are derived from its status
- User wants to review or update the delivery index status (which cells are planned, in progress, done, failed, or blocked)
- Do NOT load before a spike's change summary / solution doc exists — let conduct-spike produce them first
- Do NOT load to plan or execute a single, already-scoped change directly — plan-development-task and execute-plan handle single cells; this skill orchestrates the whole epic
</when-to-use-this-skill>

<knowledge>

<orchestrator-role>
This skill is the persistent orchestrator for **one spiked epic**. Its input is always the **delivery index** plus the spike output (change summary, solution doc, ADRs). It decomposes, sequences, dispatches agents, and keeps the index current — it never plans, codes, or edits artifacts itself. **Planning, execution, solution-doc updates, and ADR updates are ALWAYS delegated** to the corresponding agents (see **agent-dispatch**); the orchestrator only dispatches and tracks. The index is the single source of truth; conversation text is not.
</orchestrator-role>

<feature-definition>
A feature is a coherent, independently valuable deliverable spanning one or more repos. Granularity rules:
- **One PR per repo per feature** is a **soft** guideline — multiple features may merge in a single PR when convenient for development.
- If a repo's slice of a feature would exceed one reviewable PR, split the feature.
- Small shared-library changes stay inside the **first consuming feature**; only large or widely-shared changes become their own leading feature.
- Feature IDs: `F1`, `F2`, … with kebab-case names and one-line descriptions.
</feature-definition>

<dependency-edge-types>
Classify each feature pair into one of:

| Edge | Meaning | Develop | Merge |
|---|---|---|---|
| **merge-blocked** (hard) | B consumes a concrete artifact only existing after A's PR (new endpoint, changed schema, new lib version) | after A's contract is known | only after A's PR merges |
| **contract-first** (soft) | A and B agree on the interface; B builds against stubs | in parallel | B after A |
| **conflict** | both change the same files in the same repo | serialize or split | — |

Wave computation and intra-feature merge order: **reference/dependency-ordering-guide.md**.
</dependency-edge-types>

<delivery-index>
The delivery index is written next to the spike artifacts and is the epic's **source of truth for state**: features, waves, repo mapping, dependency edges, per-cell status, plan locations, and agent assignments. It also **references the spike output** (change summary file, ADR files, solution-doc sections) so agents can load full context on demand. Full format: **reference/delivery-index-format.md**.
</delivery-index>

<delivery-state-machine>
Each cell follows: **unplanned → planned → in-progress → done**, with **failed** and **blocked** as recoverable side states. A cell is **ready to dispatch** when its wave dependencies are done (merged) and its status is unplanned or planned. Full transitions: **reference/orchestration-guide.md**.
</delivery-state-machine>

<agent-dispatch>
Every delivery task is delegated to a dedicated agent — the orchestrator never performs these itself:

| Task | Delegated agent | Agent applies | Result |
|---|---|---|---|
| **Plan** a cell | **coding-assistant** | **plan-development-task** | `plan.md` + `context.md` (spike references persisted into `context.md`) |
| **Execute** a cell | **coding-assistant** | **execute-plan** | code changes + commits (reads `plan.md` + `context.md`) |
| **Update solution doc** | **solution-doc-writer** | **write-solution-doc** | revised solution-doc sections, rewritten in place |
| **Update ADR** | **adr-writer** | **draft-adr** | revised ADR, rewritten in place |

Dispatch one agent per task, in parallel, subject to **wave gating** (only cells whose dependency cells are done) and **no-conflict** rules (never run conflicting cells on the same repo simultaneously). Each agent brief carries the cell's scope brief **plus its spike references** (change-summary items, ADR files, solution-doc section) so the agent can load full context on demand. When planning or execution surfaces changes to the spike's solution doc or ADRs, dispatch a **solution-doc-writer** / **adr-writer** agent for that update instead of editing artifacts directly. Use the platform's agent/sub-agent mechanism — detect what is available. Full rules: **reference/orchestration-guide.md**.
</agent-dispatch>

<plan-layout>
Per-repo plans use a **repo-first** layout so all plans for one repo live in one location:
```
{location}/{repo}/{feature-name}/
├── plan.md
└── context.md
```
Default location: `docs/feature-implementations/`. Plans are produced by **plan-development-task** and executed by **execute-plan**.
</plan-layout>

<branch-and-push-conventions>
Execution agents commit locally and small-step; pushing branches or opening PRs happens only after user confirmation. One branch per repo per cell.

| Concern | Convention |
|---|---|
| Branch naming | One branch per repo per cell, named to match the **repo's branch convention** (detect it from existing branches, git config, or team docs — or ask the user); never assume a prefix like `feat/` |
| Branch creation | Created during the execution agent's **Prepare Environment** step (see **plan-development-task** prerequisites) |
| Committing | Execution agents commit after each ✅ step, with messages that contain no AI-related wording (see **execute-plan** commit-conventions) |
| Pushing / PRs | Never automatic — the orchestrator asks the user for confirmation before pushing any branch or opening a PR |
| Cell done | A cell is **done** only after its PR merges or the user confirms the code is verified; pushing alone is not done |
</branch-and-push-conventions>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Dispatching parallel agents, wave gating, status transitions, or failure handling | Agent dispatch, orchestration loop, resume, failure rules | [reference/orchestration-guide.md](reference/orchestration-guide.md) |
| Classifying dependency edges, computing waves, or intra-feature merge order | Edge types, wave algorithm, develop-vs-merge | [reference/dependency-ordering-guide.md](reference/dependency-ordering-guide.md) |
| Writing or updating the delivery index | Index schema, per-cell briefs, status lifecycle | [reference/delivery-index-format.md](reference/delivery-index-format.md) |
| Running a full end-to-end decomposition from change summary to index | End-to-end multi-repo example | [examples/multi-repo-feature-decomposition.md](examples/multi-repo-feature-decomposition.md) |
| Running one orchestration round with parallel agents | Dispatch + status-update walkthrough | [examples/orchestration-round.md](examples/orchestration-round.md) |
| Continuing an interrupted epic | Resume walkthrough with mixed statuses | [examples/resume-after-interruption.md](examples/resume-after-interruption.md) |
| Distinguishing parallel vs merge-blocked features | Dependency-ordering-focused example | [examples/parallel-vs-sequential-waves.md](examples/parallel-vs-sequential-waves.md) |
</context-loading-guide>

<skill-boundary>
This skill decomposes, sequences, orchestrates, and tracks — it never plans, codes, or edits artifacts itself. Plan and execution go to the **coding-assistant** agent (**plan-development-task** / **execute-plan**), solution-doc updates to the **solution-doc-writer** agent (**write-solution-doc**), and ADR updates to the **adr-writer** agent (**draft-adr**) — always dispatched, never done here. Resuming an existing epic belongs here.
</skill-boundary>

</knowledge>

<capabilities>

<decompose-change-into-features>
1. Load the spike artifacts: change summary (primary), solution doc, and ADRs.
2. Group change items into features — each feature is a coherent, independently valuable deliverable; group by ADR traceability and target-state module boundaries.
3. Apply the granularity rules from **feature-definition**: split repo-slices larger than one reviewable PR; keep small shared-library changes inside the first consuming feature; extract only large or widely-shared changes as leading features.
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
3. For each multi-repo feature, determine the intra-feature PR merge order (contract lib repo first, consumers last).
4. For each feature, state clearly: can develop now (parallel) vs can only merge after which prior PRs — using the edge table.
5. Present the wave plan (parallel features per wave, blocked features) and confirm with the user.
</order-feature-delivery>

<produce-delivery-index>
1. Write the **delivery index** next to the spike artifacts, following **reference/delivery-index-format.md** — include the **Spike References** block (change summary file, ADR files, solution-doc sections).
2. Create the per-repo plan folders using the **plan-layout** (`{location}/{repo}/{feature-name}/`).
3. Mark each cell's initial status **unplanned** and its plan location.
4. Confirm the index location with the user — from here the epic is driven by **orchestrate-delivery**.
</produce-delivery-index>

<update-delivery-index>
1. After every agent result, update the cell's status per the **delivery-state-machine**: unplanned → planned (plan written), planned → in-progress (execution started), in-progress → done (PR merged or code verified), plus failed or blocked with the reason.
2. When a cell's PR merges, re-check its downstream cells — any now wave-ready move to dispatchable.
3. Record the agent assignment, plan location, and branch name for each cell (per **branch-and-push-conventions**).
4. Always keep the index as the single source of truth; never leave status changes only in conversation.
</update-delivery-index>

<orchestrate-delivery>
1. Load the delivery index — or create it first via **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index** if it does not exist.
2. Assess current state from the index: per-cell statuses, completed waves, ready cells, blocked cells.
3. Select ready cells: wave dependencies done and status unplanned (→ dispatch a **plan** agent) or planned (→ dispatch an **execute** agent); skip done cells.
4. Dispatch parallel agents, one per cell, respecting wave gating and no-conflict rules (**reference/orchestration-guide.md**); include each cell's scope brief, its **spike references**, and its **branch name** (per **branch-and-push-conventions**) in the agent brief so the agent has full context and the branch to use.
5. When a plan or execution surfaces changes to the spike's solution doc or ADRs, dispatch **solution-doc-writer** / **adr-writer** agents for those updates — never edit the artifacts yourself.
6. Collect results and apply **update-delivery-index**.
7. When a cell's work is complete and ready to integrate, ask the user for confirmation before pushing its branch or opening a PR (per **branch-and-push-conventions**); do not push or open PRs automatically.
8. Re-assess and report next actions; repeat until all cells are done or the user pauses.
</orchestrate-delivery>

<resume-delivery>
1. Load the existing delivery index plus the spike output.
2. Determine the current state: completed waves (skip), in-progress cells (resume from the last step in `plan.md`), failed cells (ask the user to re-plan or retry), blocked cells (wait for the blocker), unplanned cells (plan next).
3. Apply **orchestrate-delivery** from that state — never redo completed work.
4. Tell the user exactly what is resumed vs skipped before dispatching.
</resume-delivery>

</capabilities>

<rules>

<rule> When spike output exists but no delivery index, apply **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**. </rule>
<rule> When a delivery index exists and the user wants to drive or continue delivery, apply **orchestrate-delivery**; apply **resume-delivery** when continuing an epic interrupted in a previous session. </rule>
<rule> After any agent reports a result, always apply **update-delivery-index** before dispatching further agents. </rule>
<rule> When the work is plan or execute → always dispatch the **coding-assistant** agent (applying **plan-development-task** / **execute-plan**); update-solution-doc → **solution-doc-writer** (applying **write-solution-doc**); update-ADR → **adr-writer** (applying **draft-adr**); never perform these tasks directly. </rule>
<rule> When the user asks about a single cell's plan or status, read the delivery index and route the cell to **plan-development-task** or **execute-plan** — do not re-run the whole orchestration. </rule>

</rules>
