---
name: orchestrate-feature-delivery
description: Orchestrate spiked-epic delivery via dispatched agents and a tracking index. Use when decomposing, sequencing, planning, executing, resuming, tracking, or reworking a spiked epic into features or per-repo PRs.
---

<when-to-use-this-skill>
- User finished a spike and wants to decompose its change summary / solution doc into features or phases (creates the delivery index)
- User wants to prove an ADR option with a POC before deciding — define and gate POC cells (see **define-poc-scope**)
- User wants to sequence which features run in parallel and which wait for another feature's PR to merge
- User wants to dispatch parallel agents to plan (plan-development-task) or execute (execute-plan) feature × repo cells of an epic
- User wants to resume or continue delivery of an existing spiked epic — load the index and derive next actions from its status
- User wants to review or update the delivery index status (cells planned / in-progress / done / failed / blocked)
- User found an issue after a feature was implemented (a cell is done, or implemented but not yet pushed/merged) and wants rework — focused spike on the governing ADR, a sibling rework file, and its execution
- User reports an ADR decision changed mid-delivery — re-route the cells governed by it (see **handle-adr-change**)
- User wants suggestions for which skill handles each part of a rework (spike, ADR update, rework plan, execution)
- Do NOT load before a spike's change summary / solution doc exists — let conduct-spike produce them first
- Do NOT load to plan or execute a single, already-scoped change — plan-development-task and execute-plan handle single cells
- Do NOT load to run a standalone spike — conduct-spike runs spikes; this skill only triggers focused rework spikes
</when-to-use-this-skill>

<knowledge>
<orchestrator-role>
Persistent orchestrator for **one spiked epic**; input is always the **delivery index** plus the spike output (change summary, solution doc, ADRs). Change summaries come from `summarize-change-scope`; solution doc and ADRs from `write-solution-doc` and `draft-adr`. It decomposes, sequences, dispatches, and tracks — it never plans, codes, or edits artifacts itself (delegation map in **agent-dispatch**). The index is the single source of truth.

**Non-negotiable mandate** — never perform any delivery task yourself; every investigate / plan / execute / artifact update is a separate dispatched agent. **Plan-first gate** — never dispatch an executor until the cell's plan file exists on disk (verified). **Never back-fill** — a plan is always written before execution, never appended after it.
</orchestrator-role>
<feature-definition>
A feature is a coherent, independently valuable deliverable spanning one or more repos.
- **One PR per repo per feature** is a **soft** guideline; split a feature if its repo slice would exceed one reviewable PR.
- Small shared-library changes stay inside the **first consuming feature**; only large or widely-shared changes become leading features.
- IDs: `F1`, `F2`, … with kebab-case names and one-line descriptions.
</feature-definition>
<poc-definition>
A POC proves one option of one ADR as a **standalone feature** — a full, coherent slice, never a snippet. Cells carry `adr` · `option` · `success-criteria` · `replaces` (optional) · `compare` (optional — sibling POCs run in parallel). Two adoption models: **POC-as-implementation** (the branch merges and ships on adopt) and **POC-as-decision-input** (a `poc-gated` feature implements the decided option afterwards). Lifecycle + metadata: **reference/poc-lifecycle.md**.
</poc-definition>
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
- **context.md** carries the distilled spike context and the `## Reworks` manifest; **plan.md** is the original plan from **plan-development-task** — each rework is a sibling `rework-<date>.md` (per **rework-modes**), implemented steps never modified.
</delivery-layout>
<dependency-edge-types>
Classify each feature pair (A → B) by edge type:

| Edge | Develop | Merge |
|---|---|---|
| **merge-blocked** | after A's contract is known | only after A merges |
| **contract-first** | in parallel (against agreed stubs) | after A |
| **poc-gated** | only after the POC decision (see **poc-definition**) | after the decision |
| **conflict** | serialize or split (same files/repo) | — |
| **independent** | parallel | any order |

Wave computation + intra-feature merge order: **reference/dependency-ordering-guide.md**.
</dependency-edge-types>
<delivery-state-machine>
Each cell follows **unplanned → planned → in-progress → done**, plus recoverable **failed** / **blocked**; **in-progress** covers implemented-but-not-yet-merged cells awaiting push approval. POC cells fork: **poc-ready** (evaluation report written) → **adopted** (promote → merge → **done**) or **rejected** (closed); a replaced cell is **superseded**. A cell is **develop-ready** when its dependencies are **planned**; **merge-ready** only when dependencies are **done**. The user records POC **adopted**/**rejected** in the index — the orchestrator never decides. Transitions: **reference/orchestration-guide.md**; rework: **rework-modes**.
</delivery-state-machine>
<agent-dispatch>
Every delivery task is delegated — the orchestrator never performs it. Map task → agent → skill: investigate → **spike-conductor** (**conduct-spike**) · plan → **planner** (**plan-development-task**) · execute → **executor** (**execute-plan**) · solution-doc → **solution-doc-writer** (**write-solution-doc**) · ADR → **adr-writer** (**draft-adr**). Plan and execute are always separate agent sessions — never one agent doing both for the same cell, never execute before a verified plan file (see **plan-first gate** in **orchestrator-role**).
Dispatch one agent per task in parallel, subject to **develop-gating** (see **delivery-state-machine**) and **no-conflict** (never run conflicting cells on the same repo simultaneously). Each brief carries the cell's scope brief **plus spike references** (change-summary items, ADR files, solution-doc section). When plan/execution surfaces solution-doc / ADR changes, dispatch the owning agent — never edit artifacts directly. Detect the platform's agent mechanism (planner / executor / spike-conductor / adr-writer / solution-doc-writer). Full rules: **reference/orchestration-guide.md**.
</agent-dispatch>
<branch-and-push-conventions>
Execution agents commit locally and small-step; pushing or opening PRs happens only after user confirmation.
- One branch per repo per cell, named per the **repo's branch convention** (detect from existing branches / git config / team docs — or ask; never assume a prefix like `feat/`); created during the execution agent's **Prepare Environment** step.
- The index records the branch up front and the PR reference (number/URL) once a PR is opened — pointers only, easy to track; work history stays in `plan.md` (see **delivery-index-format.md**).
- The index records the **head commit** from the execution handoff — a pointer like Branch/PR.
- Commit after each ✅ step, with no AI-related wording (see **execute-plan** commit-conventions).
- A cell is **done** only after its PR merges with the recorded head commit included, or the user confirms the code is verified; pushing alone is not done.
</branch-and-push-conventions>
<rework-modes>
Rework is **always append-only** — implemented steps never change; scoped to the cell (usually its governing ADR), never the whole epic. Each rework is a sibling `rework-<date>.md` — `plan.md` stays the frozen original. Execution runs **only** the rework file's steps. `context.md` holds a `## Reworks` manifest (date, mode, cell, file, status) so resume finds the active file. The index records **state only** — the rework cell + plan pointer; details live in the rework file (see **delivery-index-format.md**).

| Mode | When | Handling |
|---|---|---|
| **Post-merge** | cell **done** (merged/verified) | focused spike (**conduct-spike**) + ADR / solution-doc updates; new rework feature (e.g. `F2-r1`) in a new wave |
| **Pre-merge** | cell **in-progress** (implemented, not pushed/merged) | spike + ADR / solution-doc updates only if the issue challenges the ADR decision; rework stays on the same cell — rework steps merge with the original work |

- **Rework lineage**: `F2-r1` reworks `F2`; `F2-r2` reworks `F2-r1` (latest delivered state); `Rework of:` names it. Rework files key by date — same-day collision suffix `-2`, `-3`. The `## Reworks` manifest is the canonical chain.
</rework-modes>
<adr-drift>
ADRs are **versionless** — drift is signaled by the **adr-writer** agent's return or the user's report, never by diffing the ADR file. Route governed cells by status per the **ADR changes** section in **reference/orchestration-guide.md**.
</adr-drift>
<concise-writing>
All prose in the delivery index follows **reference/writing-style.md** — table-first, one-line Summary, atomic bullets, one-sentence feature descriptions, no process narration, So-what test. **rewrite-concise** is the mandatory final gate: move facts to tables, then shorten to the shortest faithful form — never present prose that fails a cap.
</concise-writing>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| Dispatching parallel agents, gating, status transitions, or failure handling | Agent dispatch, orchestration loop, resume, failure rules | [reference/orchestration-guide.md](reference/orchestration-guide.md) |
| Classifying dependency edges, computing waves, or intra-feature merge order | Edge types, wave algorithm, develop-vs-merge | [reference/dependency-ordering-guide.md](reference/dependency-ordering-guide.md) |
| Writing or updating the delivery index | Index schema, per-cell briefs, status lifecycle | [reference/delivery-index-format.md](reference/delivery-index-format.md) |
| Handling a post-merge rework (cell **done**) | Focused spike, sibling rework file, execution | [examples/post-implementation-rework.md](examples/post-implementation-rework.md) |
| Handling a pre-merge rework (cell **in-progress** — implemented but not pushed/merged) | Sibling rework file on an unmerged cell | [examples/pre-merge-rework.md](examples/pre-merge-rework.md) |
| Running a full end-to-end decomposition from change summary to index | End-to-end multi-repo example | [examples/multi-repo-feature-decomposition.md](examples/multi-repo-feature-decomposition.md) |
| Running one orchestration round with parallel agents | Dispatch + status-update walkthrough | [examples/orchestration-round.md](examples/orchestration-round.md) |
| Continuing an interrupted epic | Resume walkthrough with mixed statuses | [examples/resume-after-interruption.md](examples/resume-after-interruption.md) |
| Distinguishing parallel vs merge-blocked features | Dependency-ordering-focused example | [examples/parallel-vs-sequential-waves.md](examples/parallel-vs-sequential-waves.md) |
| Marking, sequencing, or gating POC cells, or handling a user-recorded POC decision | POC definition, lifecycle, adoption models | [reference/poc-lifecycle.md](reference/poc-lifecycle.md) |
| Running a full POC round (compare POCs → user-recorded decision → adopt/reject) | End-to-end POC walkthrough | [examples/adr-option-poc.md](examples/adr-option-poc.md) |
| Writing or updating the delivery index prose | BLUF rules, rewrite transforms, banned-phrase list | [reference/writing-style.md](reference/writing-style.md) |
| Rewriting wordy index prose to its shortest faithful form | Move-then-shorten walkthrough, before/after model | [examples/concise-rewrite.md](examples/concise-rewrite.md) |
| Handling an ADR change mid-delivery (cells at any status) | ADR-change routing + resume currency check | [reference/orchestration-guide.md](reference/orchestration-guide.md) |
| ADR change mid-delivery with mixed statuses | done / planned / in-progress walkthrough | [examples/adr-change-mid-delivery.md](examples/adr-change-mid-delivery.md) |
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
1. Write the **delivery index** at `deliveries/<epic-name>/index.md` per **reference/delivery-index-format.md** — `<epic-name>` is the spiked epic's name (see **delivery-layout**).
2. Include the **Spike References** block: change summary file, ADR files, solution-doc sections.
3. Create per-repo plan folders in the **repo-first** layout: `deliveries/<epic-name>/{repo}/{feature-name}/plan.md` + `context.md` (see **delivery-layout**).
4. Mark each cell's initial status **unplanned** and its plan location.
5. Verify the index against **reference/delivery-index-format.md** — structure, status values, develop/merge readiness — then apply **rewrite-concise** as the final prose gate (see **concise-writing**).
6. Confirm the index location with the user — from here the epic is driven by **orchestrate-delivery**.
</produce-delivery-index>
<update-delivery-index>
1. After every agent result, update the cell's status per the **delivery-state-machine**: unplanned → planned, planned → in-progress, in-progress → done, plus failed or blocked with the reason.
2. When an agent result looks inconsistent (status vs plan files, claimed merge vs branch state), verify it.
3. Re-read the artifacts or dispatch a fresh check before recording.
4. Apply the **plan-first gate**: mark **planned** only when the planner's plan file exists on disk at the recorded Plan location; never set a cell to **in-progress** without a verified plan file — a missing file is **failed** (reason: no plan file).
5. When the user records a POC decision (**poc-ready → adopted/rejected**), record it in the index.
6. Dispatch the POC follow-ups per **reference/poc-lifecycle.md**: the ADR agent (**adr-writer**) records the outcome in the ADR.
7. On **adopted** — **POC-as-implementation**: ask before promoting/merging the branch, then mark the `replaces` cell **superseded**.
8. On **adopted** — **POC-as-decision-input**: dispatch the **poc-gated** feature with the decided option.
9. On **rejected**: close the cell — archive or discard the branch (ask the user).
10. When a cell's PR merges, confirm the recorded head commit is in the merged PR before marking **done** (see **branch-and-push-conventions**); then re-check downstream cells — any now develop-ready (dependencies planned) or merge-ready (dependencies done) become dispatchable.
11. Record the agent assignment, plan location, branch name, and the **head commit** from the execution handoff for each cell; record the PR reference (number/URL) once a PR is opened (per **branch-and-push-conventions**).
12. Keep the index as the single source of truth; never leave status changes only in conversation.
13. Verify the updated index against **reference/delivery-index-format.md** — status values, readiness, recorded branches — then apply **rewrite-concise**.
</update-delivery-index>
<orchestrate-delivery>
1. Load the delivery index — or create it first via **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index** if it does not exist.
2. Assess current state from the index: per-cell statuses, completed waves, ready cells, blocked cells.
3. **Phase 1 — plan**: select unplanned, develop-ready cells and dispatch the **planner** agent to each, one per cell — no executor is dispatched in this phase (see **agent-dispatch**).
4. **Verify the plan-first gate**: after each planner returns, confirm its plan file (`plan.md` or `rework-<date>.md`) exists on disk at the recorded Plan location before the cell may advance.
5. **Phase 2 — execute**: select **planned** cells whose plan file is verified and dispatch the **executor** agent to each, respecting develop-gating and no-conflict rules (**reference/orchestration-guide.md**).
6. Gate merges on dependencies **done**.
7. Brief each agent with its scope, **spike references**, and **branch name**.
8. When plan or execution surfaces solution-doc / ADR changes, dispatch the owning agent (see **agent-dispatch**) — never edit artifacts yourself.
9. Collect results and apply **update-delivery-index**.
10. When a cell is ready to integrate, ask the user before pushing its branch or opening a PR (per **branch-and-push-conventions**); never push automatically.
11. Re-assess and report next actions; repeat until all cells are done or the user pauses.
</orchestrate-delivery>
<resume-delivery>
1. Load the existing delivery index plus the spike output.
2. Confirm ADR currency with the user — if any governing ADR changed since the last run, apply **handle-adr-change** first.
3. Determine the current state: completed waves (skip), in-progress cells (resume from the last step in `plan.md`), failed cells (ask the user to re-plan or retry), blocked cells (wait for the blocker), unplanned cells (plan next).
4. Apply **orchestrate-delivery** from that state — never redo completed work.
5. Tell the user exactly what is resumed vs skipped before dispatching.
</resume-delivery>
<handle-post-implementation-issue>
1. Identify the affected cell, its governing ADR, and its status — **done** (merged/verified) or **in-progress** (implemented, not pushed/merged).
2. Scope investigation narrowly to that decision — never the whole epic.
3. Present the routing for user confirmation — **append-only in both modes** (per **rework-modes**):
   - **Plan**: dispatch the **planner** agent (plan-development-task) to write a sibling `rework-<date>.md` — implemented steps never modified.
   - **Execute**: dispatch the **executor** agent (execute-plan) to run only the rework file's steps.
   - **Investigate**: dispatch **spike-conductor** (conduct-spike) + **adr-writer** (draft-adr) / **solution-doc-writer** (write-solution-doc) updates for post-merge; pre-merge only if the issue challenges the governing ADR decision.
4. Apply **update-delivery-index** — post-merge adds a new rework feature (e.g. `F2-r1`, `Rework of: F2`) in a new wave; the original cell's status stays **done**.
5. For pre-merge, keep the rework on the same cell (no new feature/wave) — no index change; the sibling `rework-<date>.md` is the record.
6. Ask the user before pushing or opening a PR (per **branch-and-push-conventions**).
</handle-post-implementation-issue>
<handle-adr-change>
1. Confirm the changed ADR and its new decision — from the user or the **adr-writer** agent's return (see **adr-drift**).
2. List the cells governed by that ADR from the index's per-feature `ADRs:` entries.
3. Route each by status per **reference/orchestration-guide.md** (ADR changes) — planned → re-plan (**plan-development-task**); in-progress → pre-merge rework; done → post-merge rework; surface in-flight POCs.
4. Apply **update-delivery-index** and **rewrite-concise**; present routing and confirm before dispatching.
</handle-adr-change>
<define-poc-scope>
1. During **decompose-change-into-features**, when an ADR option needs proof before a decision, flag the mapped cell `type: poc`.
2. Fill the POC metadata per **poc-definition**: `adr`, `option`, `success-criteria`, `replaces` (if it may supersede an existing implementation), `compare` (sibling POC cells for other options).
3. Sequence POC cells **early** (Wave 0) — run `compare` siblings in parallel; add a **poc-gated** edge from the implementing feature to its POC cell.
4. Present the POC cells and success criteria to the user and confirm before recording them in the index.
</define-poc-scope>
<rewrite-concise>
**Objective**: Rewrite any target doc's prose to the shortest form that preserves all facts — the mandatory final gate before presenting or confirming the delivery index.

**Note**: An internal pass — show only the rewritten result, never the process or a before/after unless the user asks. Facts outrank brevity: never drop a fact to hit a cap.

**Steps**:
1. Draft freely — do not self-edit while writing.
2. Treat every sentence as suspicious; scan and label each violation class per **reference/writing-style.md** (filler, redundancy, hedge, narration, multi-claim, over-cap).
3. **Move-then-shorten**: if a fact belongs in a table (status, wave, dependency, PR), move it there first, then shorten what remains.
4. Apply the class-specific transforms per **reference/writing-style.md**.
5. Apply the **So-what test** — delete any sentence that adds no fact; do not reword it.
6. Re-scan against the hard caps; loop until zero violations (max 2 passes).
</rewrite-concise>

</capabilities>

<rules>
<rule> When spike output exists but no delivery index, apply **decompose-change-into-features** → **map-features-to-repos** → **order-feature-delivery** → **produce-delivery-index**. </rule>
<rule> When a delivery index exists and the user wants to drive or continue delivery, apply **orchestrate-delivery**; apply **resume-delivery** when continuing an epic interrupted in a previous session. </rule>
<rule> After any agent reports a result, always apply **update-delivery-index** before dispatching further agents. </rule>
<rule> When dispatching any delivery task (investigate, plan, execute, solution-doc update, or ADR update), always dispatch the owning agent per **agent-dispatch** — never perform the task directly. </rule>
<rule> Never dispatch an executor for a cell until its plan file is verified on disk (the **plan-first gate**); never write or append a plan after execution — a plan is always written before its steps run. </rule>
<rule> Never let a single agent plan and execute the same cell in one session — plan and execute are separate agent dispatches, always in that order. </rule>
<rule> When the user asks about a single cell's plan or status, read the delivery index and route the cell to **plan-development-task** or **execute-plan** — do not re-run the whole orchestration. </rule>
<rule> When an issue surfaces after a feature was implemented (a cell is **done** or **in-progress** — implemented but not pushed/merged), apply **handle-post-implementation-issue** — never re-run **decompose-change-into-features** on the whole epic. </rule>
<rule> When the user reports an ADR change or an **adr-writer** agent returns a revision, apply **handle-adr-change** — never dispatch a planned cell on a stale decision. </rule>
<rule> When decomposing change items and an ADR option needs proof before a decision, apply **define-poc-scope** to flag and sequence POC cells. </rule>
<rule> When a POC cell reaches **poc-ready**, do not evaluate or decide — wait for the user to record **adopted**/**rejected** directly in the index. </rule>
<rule> When the user records a POC decision (**adopted**/**rejected**) in the index, apply **update-delivery-index** to record it and dispatch the follow-ups (ADR update, branch promotion, **poc-gated** feature). </rule>
<rule> When presenting or confirming any delivery index (new or updated), apply **rewrite-concise** as the final gate — never present a draft that fails a **writing-style.md** cap. </rule>

</rules>
