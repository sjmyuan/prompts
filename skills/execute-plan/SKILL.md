---
name: execute-plan
description: Execute structured development plans step-by-step with progress tracking, validation checkpoints, and error recovery. Use when executing / carrying out / resuming / reviewing a plan from plan-development-task, or a delivery cell / rework from orchestrate-feature-delivery.
---

<when-to-use-this-skill>
- You need to execute an outlined plan (implementation plan, refactoring plan, or bug-fix plan)
- A structured plan from plan-development-task needs to be carried out with progress tracking and validation checkpoints
- A previously started plan needs to be resumed after interruption or context reset
- All plan steps are complete and a post-execution review with the review-code skill is needed
- A step has failed or is blocked and needs error recovery before proceeding
- A delivery index from orchestrate-feature-delivery points to planned feature × repo cells ready for execution
- You need to execute a POC plan (a standalone feature proving one ADR option) and stop at an evaluation report for the decision gate
- You need to execute a plan containing an appended `## Rework <date>` section (a rework triggered by orchestrate-feature-delivery) — run only the rework steps, never re-run the completed original steps
- Do NOT load when no plan has been generated yet — if the user describes a problem without referencing an existing plan, let plan-development-task handle it first
</when-to-use-this-skill>

<knowledge>

<step-status-definitions>
Status emojis used to track each step:

| Status | Emoji | Meaning |
|---|---|---|
| Pending | ⏳ | Not yet started |
| In Progress | 🔄 | Currently being worked on |
| Completed | ✅ | Successfully finished |
| Failed | ❌ | Encountered errors (include error details) |
| Blocked | 🚫 | Cannot proceed (include blocker details) |
</step-status-definitions>

<step-tracking-format>
Record each step in the plan file using this format:

```
### Step N: [Step Title] [Status Emoji]
**Objective**: [What this step achieves]
**Files**: [Files created, modified, or deleted]
**Implementation**: [Key changes or actions taken]
**Validation**: [Test results or verification outcomes]
**Status**: [Status emoji] [Status description]
```
</step-tracking-format>

<feature-folder-structure>
Each feature implementation lives in its own folder with two files:

```
{location}/{repo}/{feature-name}/
├── plan.md      # Step-by-step execution plan with live status tracking
└── context.md   # All context, references, requirements, constraints that define the plan
```

- **Location**: For an **orchestrate-feature-delivery** cell use the epic's delivery folder `deliveries/<epic-name>/{repo}/{feature-name}/` (already created by the orchestrator); otherwise ask the user or default to `docs/feature-implementations/`.
- **Repo-first layout**: When a plan belongs to a specific repo (a cell from **orchestrate-feature-delivery**), use `deliveries/<epic-name>/{repo}/{feature-name}/`; fall back to `{location}/{feature-name}/` when no repo applies.
- **Feature name**: Derive a short, descriptive kebab-case name from the plan's objective (e.g., `add-auth-system`, `refactor-validation-handler`, `fix-null-pointer-in-transformer`).
- **Plan file**: Contains the numbered step list with status emojis, updated in real-time as execution progresses. Serves as the live execution dashboard.
- **Context file**: Captures all background material that informed the plan — requirements docs, ADRs, user stories, spike findings, codebase references, constraints, assumptions, and decisions. Written once at plan creation and not modified during execution.
- Both files are kept as a permanent record after execution completes — they are never deleted.
</feature-folder-structure>

<plan-input-schema>
A plan consumed by this skill consists of numbered steps. Each step must have:
- **Step number**: Sequential integer starting from 1
- **Title**: Short descriptive name of the step
- **Objective**: What the step achieves

The plan may be provided as:
- An existing `plan.md` file in a feature folder (created by **export-plan** in plan-development-task, an **orchestrate-feature-delivery** cell folder, or a previous execution)
- A plan summarized in the conversation by plan-development-task
- A plan described ad-hoc by the user

This skill is responsible for materializing the plan into `plan.md` with the **step-tracking-format** if it does not already exist as a file.
</plan-input-schema>

<commit-conventions>
Small-step commit rules applied throughout execution:

| Rule | Detail |
|---|---|
| Commit frequency | One commit per step, after the step is validated and marked ✅ |
| Commit size | A single logical change — the step's objective only |
| Message format | Follow the repo's existing convention (check recent `git log`); default to `type(scope): summary` |
| Message content | Neutral description of the change. NEVER include AI-related words or hints: `AI`, `Copilot`, `assistant`, `agent`, `LLM`, `model`, `generated`, `automated`, or any reference to how the change was produced |
| Staging | Stage only the files belonging to this step (`git add <file>...`); never blind `git add -A` |
| Push gating | Never push to remote without explicit user confirmation (see **request-push-approval**) |
| Pre-commit check | Commit only after the step's validation checkpoint (tests/lint) passes |
</commit-conventions>

<code-comment-conventions>
Generated code must match the repo's existing comment style: detect it first, then follow it. Comment the **why** (non-obvious intent, workarounds, invariants, edge cases), never restate the **what**; never narrate the change (no plan-step references, "added/generated" markers, section banners, or AI mentions); match the repo's density — a sparse repo gets sparse comments, docstrings only where the repo already uses them (public API only); keep line comments ≤ 15 words. Detect the repo's convention during **verify-prerequisites** and enforce it in **commit-step**. Full rubric: **reference/code-comment-style.md**.
</code-comment-conventions>

<rework-plan-execution>
When the plan file contains an appended `## Rework <date>` section (a rework triggered by **orchestrate-feature-delivery**'s **handle-post-implementation-issue**):
- Execute **only** the rework section — the original steps are all ✅ and are never re-run or modified.
- Treat the rework steps as a fresh step sequence with **step-status-definitions** statuses (⏳ → 🔄 → ✅).
- **verify-prerequisites** still applies — the rework runs on its own branch per the repo's branch convention (the original branch/PR may already be merged).
- Commit conventions, **request-push-approval**, and **review-post-execution** apply exactly as for a normal plan.
</rework-plan-execution>
<poc-execution-mode>
A POC plan (from **plan-development-task**'s **plan-poc** / an **orchestrate-feature-delivery** POC cell) executes like a normal feature on a **POC branch** — track, small-step commits, validation — but stops before merging: after the final **evaluation step**, produce the evaluation report (see **produce-poc-report**) and **STOP**. Pushing a POC branch is for review/evidence only (ask the user); merging happens only after the orchestrator's decision gate adopts it. Completion routes to the decision gate — never to plain **done**.
</poc-execution-mode>

<scope-boundary-check>
The plan file's `## Scope Boundary` block (written by **export-plan** in plan-development-task) defines what execution may change. If the plan has no boundary block, treat the plan's listed steps and files as the boundary.
- Within **In scope** or a **Minor exception** → proceed without asking.
- Beyond **In scope** (touching an **Out of scope** file, behavior, or ADR decision) → STOP, refuse, and ask the user with options: (a) extend the boundary, (b) record as a follow-up and stay in scope, (c) proceed anyway with a recorded deviation note.
- Never adapt silently to out-of-scope changes.
</scope-boundary-check>

<context-loading-guide>
Load only the example most relevant to the current execution scenario to minimize context size.

| Load when | Provides | File |
|---|---|---|
| Executing any step that writes or modifies code | Code comment doctrine: why-not-what, banned patterns, density matching, pre-commit self-check | [reference/code-comment-style.md](reference/code-comment-style.md) |
| Generating code that needs to match the repo's comment style before committing | Output model: convention detection + pre-commit comment scan in action | [examples/comment-hygiene.md](examples/comment-hygiene.md) |
| Executing a small, focused plan (single component or focused task) | Output model: detailed progress updates for a simple focused execution | [examples/single-component-refactor.md](examples/single-component-refactor.md) |
| Executing a plan that spans multiple files and architectural layers | Output model: execution tracking across multiple files and layers | [examples/multi-file-implementation.md](examples/multi-file-implementation.md) |
| A step fails with compilation errors or unexpected output | Output model: error recovery, ❌→✅ status transitions, and retry patterns | [examples/handling-failed-steps.md](examples/handling-failed-steps.md) |
| Executing a plan with 10+ steps requiring context preservation | Output model: long plan progress tracking and context continuity | [examples/long-plan-execution.md](examples/long-plan-execution.md) |
| All plan steps are complete and post-execution review is needed | Output model: applying review-code after completion, adding fix steps, keeping plan as permanent record | [examples/post-execution-review.md](examples/post-execution-review.md) |
| A step is ambiguous, requires user input, or cannot proceed due to a missing dependency or external blocker | Output model: pausing execution at a blocked step, informing the user, and resuming after input | [examples/handling-failed-steps.md](examples/handling-failed-steps.md) |
| Executing a plan with prerequisite checks, one commit per step, and push approval at the end | Output model: verify-prerequisites, commit-step, and request-push-approval in action | [examples/small-step-commits.md](examples/small-step-commits.md) |
| Executing a plan with an appended `## Rework` section (run only the rework steps) | Rework execution walkthrough (shared with the orchestrator) | [../orchestrate-feature-delivery/examples/post-implementation-rework.md](../orchestrate-feature-delivery/examples/post-implementation-rework.md) |
| Executing a POC plan (stop at evaluation report, no merge) | POC execution mode + evaluation report walkthrough | [examples/execute-adr-option-poc.md](examples/execute-adr-option-poc.md) |
| POC round from dispatch to decision gate (shared with the orchestrator) | End-to-end POC walkthrough | [../orchestrate-feature-delivery/examples/adr-option-poc.md](../orchestrate-feature-delivery/examples/adr-option-poc.md) |
| A step, recovery fix, or review fix risks exceeding the plan's scope boundary | Output model: refusal + decision options | [examples/refusing-out-of-scope-rework.md](examples/refusing-out-of-scope-rework.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<track-plan>
1. Locate or create the feature folder and its two files (`plan.md` + `context.md`) per **feature-folder-structure**; for an **orchestrate-feature-delivery** cell use the existing `deliveries/<epic-name>/{repo}/{feature-name}/`, otherwise ask the user or default to `docs/feature-implementations/`.
2. Derive a short kebab-case feature name from the plan's objective (e.g., `add-auth-system`, `fix-null-pointer-in-transformer`) per **feature-folder-structure**.
3. Before creating a new plan, check if the feature folder already exists with a plan file. If it contains an appended `## Rework <date>` section, execute only the rework steps (see **rework-plan-execution**) — never re-run or modify the completed original steps. If a plan file has steps with ❌ failed or 🚫 blocked status, ask the user whether to **resume** from the last known state or **start fresh** (create a new folder/overwrite).
4. Materialize the plan into `plan.md` per **plan-input-schema**: list each step with its number, title, objective, and initial status ⏳ pending, using the **step-tracking-format**.
5. Populate `context.md` with all relevant background: requirements docs, ADRs, user stories, spike findings, codebase references, constraints, assumptions, and any other material that informed the plan.
6. Update step status in the plan file immediately after each state change (⏳ → 🔄 → ✅, or ❌/🚫 on failure). Refer to **step-status-definitions** for emoji meanings.
7. Never modify plan structure, objectives, steps, or the **Scope Boundary** block except to update statuses or add clarifying notes.
8. Report progress: at plan start show all steps with ⏳ pending; after each step completion show the full list with current statuses and per-step details (files, implementation, validation); never summarize multiple steps together; at plan end show the final all-✅ list with a summary of accomplishments.
</track-plan>

<execute-step>
1. Before starting a step, mark it as 🔄 in-progress in the plan file and briefly explain your approach. Apply **check-scope-boundary** — if the step's required changes exceed the plan's scope boundary, refuse and ask instead of adapting.
2. Execute the step fully — no partial implementations.
3. After completing the step, validate the outcome meets the step's objectives.
4. Mark the step as ✅ completed; document files changed, implementation details, and validation results in the plan file.
5. Confirm the prerequisite step is fully ✅ completed before starting a step that depends on it.
6. Display the full updated step list with current statuses after each completion.
</execute-step>

<handle-errors>
1. Mark the failed step as ❌ with error details in the plan file.
2. Document the error clearly.
3. Analyze the root cause.
4. Apply **check-scope-boundary** to the recovery fix; if the only viable fix exceeds the plan's scope boundary, refuse and ask the user (with options) instead of silently changing out-of-scope code. Otherwise fix and retry the step.
5. Update step status to ✅ if resolved, or 🚫 blocked if unresolvable.
6. If blocked, consult the user before proceeding.
7. Display the updated full step list with current statuses.
8. Never skip a failed step or failed validation — address issues before proceeding.
</handle-errors>

<check-scope-boundary>
1. Read the plan's **Scope Boundary** block (see **scope-boundary-check**); fall back to the plan's steps/files if absent.
2. Evaluate the required change (a planned step, an error-recovery fix, or a review fix) against **In scope** and **Minor exceptions**.
3. If within scope → proceed normally.
4. If beyond scope → mark the step 🚫 blocked (or hold), refuse, and ask the user with options: extend the boundary, file a follow-up and stay in scope, or proceed anyway with a recorded deviation.
5. Act on the user's decision; if the boundary is extended, update the plan's boundary block and proceed.
</check-scope-boundary>

<run-validation-checkpoints>
1. After code changes, run relevant tests to confirm correctness.
2. After significant changes, run linting, formatting, and type-checking.
3. For build-dependent projects, verify the build succeeds at key milestones.
4. Validate incrementally — do not wait until the end of the plan.
</run-validation-checkpoints>

<review-post-execution>
1. After ALL plan steps are marked ✅ completed, apply the **review-code** skill on all files changed or created during execution.
2. Evaluate correctness, security, performance, maintainability, and test coverage.
3. If 🚫 Blocker or 🔴 Major issues are found:
   1. Apply **check-scope-boundary** to each finding's required fix — if a fix exceeds the plan's scope boundary, refuse and ask the user before adding it. Otherwise record the finding as a new fix step in the plan file with ⏳ pending status.
   2. Apply **execute-step** for each fix step.
   3. Re-run the **review-code** skill on the affected files.
   4. Repeat until no 🚫 Blockers or 🔴 Majors remain.
4. If only 🟡 Minor and 🟢 Nit findings remain, document them in the final summary without blocking completion.
5. Display the final completion summary once the review passes. Keep the plan file and context file as a permanent record of the implementation.
</review-post-execution>



<verify-prerequisites>
1. Before starting the first step, verify the environment is ready: the correct feature branch is checked out (create it if the plan requires one and the user confirms the branch name and base, naming it per the **repo's branch convention** — detect from existing branches / git config / team docs, or ask the user; never assume a prefix), the working tree has no unrelated uncommitted changes, dependencies and toolchain are available, and baseline tests/lint pass. Also detect the repo's comment style per **code-comment-conventions** (sample recently modified files, `.editorconfig`, CONTRIBUTING docs) and record a one-line convention note in the plan file.
2. If anything is missing or failing, STOP and raise it to the user: state exactly what is not ready, what is needed to proceed, and ask how to proceed. Do not start executing steps until it is resolved.
3. Record the outcome (ready or blockers) in the plan file before execution begins.
</verify-prerequisites>

<commit-step>
1. After a step is validated and marked ✅, run `git status` and `git diff` to identify the files changed by this step.
2. Stage only those files — never unrelated or pre-existing changes.
3. Scan the staged diff against **code-comment-conventions**: remove or shorten restating comments, process-narration markers (plan-step references, "added/generated" notes, section banners, AI mentions), and comments that exceed the repo's density; re-stage after trimming.
4. Write a small commit message following **commit-conventions**: repo convention if known, else `type(scope): summary`, describing the change neutrally.
5. Scan the message for AI-related words (see **commit-conventions**) and rewrite until none remain.
6. Commit locally; report the commit hash and message. Never push.
7. If the step produced no code change (e.g., documentation-only), note that no commit is needed.
</commit-step>

<produce-poc-report>
1. After the plan's final evaluation step, collect the measured evidence for each **success criterion** (benchmarks, complexity diff, integration results).
2. Write an **Evaluation Report** into the feature folder (`evaluation-report.md`): per-criterion evidence, a verdict line (meets / misses), and any caveats.
3. Do NOT push or merge — the report feeds the decision gate; ask the user before pushing for review.
</produce-poc-report>

<request-push-approval>
1. When all steps are ✅ complete — or the user asks to sync — summarize the local state: branch name, commits created, and how many commits are ahead of the remote base. For a **POC branch** (see **poc-execution-mode**), pushing is review/evidence only — merging waits for the orchestrator's decision gate.
2. Ask the user explicitly: "Push branch [branch name] to remote?" Wait for a decision.
3. Push only after the user confirms; report success or any errors.
4. If the user declines or defers, leave the branch local and tell them the commits are ready to push whenever they choose.
</request-push-approval>

<manage-user-interaction>
1. Execute the full plan autonomously without asking for permission at each step.
2. If a step is ambiguous or requires user input, pause and ask before proceeding.
3. If blocked on a step due to missing information or external dependencies, inform the user and wait for guidance.
4. When deviating from the plan, apply **check-scope-boundary** and explain the adaptation — never deviate silently.
5. Before any push, apply **request-push-approval** — never push without the user's confirmation.
</manage-user-interaction>

</capabilities>



<rules>

<rule> **At Plan Start**: Apply **track-plan** to create the feature folder with plan and context files before executing any step. </rule>
<rule> **During Each Step**: Apply **execute-step** for every step in the plan. </rule>
<rule> **Throughout Execution**: Apply **track-plan** — keep the step list current and show the full list with statuses after every step. </rule>
<rule> **When a Step Fails**: Apply **handle-errors** immediately. </rule>
<rule> **At Validation Points**: Apply **run-validation-checkpoints** after code changes and at major milestones. Validate incrementally, not just at the end. </rule>
<rule> **When Facing Ambiguity or Blockers**: Apply **manage-user-interaction** — pause and ask rather than assuming. </rule>
<rule> **After All Steps Complete**: Apply **review-post-execution**. </rule>
<rule> **Before Starting the First Step**: Apply **verify-prerequisites** — if the branch or environment is not ready, raise it to the user and wait. </rule>
<rule> **After Each ✅ Step**: Apply **commit-step** to record the change as one small commit. </rule>
<rule> **Before Any Push**: Apply **request-push-approval** — never push to remote without the user's confirmation. </rule>
<rule> **When the Plan Contains a Rework Section**: Apply **rework-plan-execution** — run only the appended `## Rework` steps and never modify the completed original steps. </rule>
<rule> **When the Plan is a POC** (type: poc): Apply **poc-execution-mode** — run like a feature but stop at the evaluation report; never merge before the decision gate. </rule>
<rule> **After the Final Evaluation Step of a POC**: Apply **produce-poc-report** and route to the orchestrator's decision gate. </rule>
<rule> **When a Step, Recovery Fix, or Review Fix Exceeds the Boundary**: Apply **check-scope-boundary** — refuse and ask the user with options, never adapt silently. </rule>
<rule> **When Deviating from the Plan**: Apply **check-scope-boundary** before adapting. </rule>

</rules>