---
name: execute-plan
description: Execute structured plans step-by-step with progress tracking, validation checkpoints, and error recovery. Works with plans from plan-development-task. Runs tests, validates changes, and handles failures systematically. Use after generating a plan that needs execution.
---

<when-to-use-this-skill>
- You need to execute an outlined plan (implementation plan, refactoring plan, or bug-fix plan)
- A structured plan from plan-development-task needs to be carried out with progress tracking and validation checkpoints
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
{location}/{feature-name}/
├── plan.md      # Step-by-step execution plan with live status tracking
└── context.md   # All context, references, requirements, constraints that define the plan
```

- **Location**: Ask the user where to store the plan. If not specified, default to `docs/feature-implementations/`.
- **Feature name**: Derive a short, descriptive kebab-case name from the plan's objective (e.g., `add-auth-system`, `refactor-validation-handler`, `fix-null-pointer-in-transformer`).
- **Plan file**: Contains the numbered step list with status emojis, updated in real-time as execution progresses. Serves as the live execution dashboard.
- **Context file**: Captures all background material that informed the plan — requirements docs, ADRs, user stories, spike findings, codebase references, constraints, assumptions, and decisions. Written once at plan creation and not modified during execution.
- Both files are kept as a permanent record after execution completes — they are never deleted.
</feature-folder-structure>

<context-loading-guide>
Load only the example most relevant to the current execution scenario to minimize context size.

| Load when | Provides | File |
|---|---|---|
| Executing a small, focused plan (single component or focused task) | Output model: detailed progress updates for a simple focused execution | [examples/single-component-refactor.md](examples/single-component-refactor.md) |
| Executing a plan that spans multiple files and architectural layers | Output model: execution tracking across multiple files and layers | [examples/multi-file-implementation.md](examples/multi-file-implementation.md) |
| A step fails with compilation errors or unexpected output | Output model: error recovery, ❌→✅ status transitions, and retry patterns | [examples/handling-failed-steps.md](examples/handling-failed-steps.md) |
| Executing a plan with 10+ steps requiring context preservation | Output model: long plan progress tracking and context continuity | [examples/long-plan-execution.md](examples/long-plan-execution.md) |
| All plan steps are complete and post-execution review is needed | Output model: applying review-code after completion, adding fix steps, keeping plan as permanent record | [examples/post-execution-review.md](examples/post-execution-review.md) |
| A step is ambiguous, requires user input, or cannot proceed due to a missing dependency or external blocker | Output model: pausing execution at a blocked step, informing the user, and resuming after input | [examples/handling-failed-steps.md](examples/handling-failed-steps.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<track-plan>
1. Determine where to store the plan. Ask the user where they'd like the plan saved, or default to `doc/feature-implementations/` if not specified.
2. Derive a descriptive, short name for the feature from the plan's objective (e.g., `add-auth-system`, `refactor-validation-handler`, `fix-null-pointer-in-transformer`). Use kebab-case.
3. Create the feature folder: `{location}/{feature-name}/`. Inside it, create two files:
   - `{feature-name}-plan.md` — the step-by-step execution plan with status tracking (see **step-tracking-format**)
   - `{feature-name}-context.md` — all context, references, requirements, constraints, and decisions that define the plan (captured from the plan source so the reasoning is preserved alongside the plan)
4. Before creating a new plan, check if the feature folder already exists with a plan file. If a plan file has steps with ❌ failed or 🚫 blocked status, ask the user whether to **resume** from the last known state or **start fresh** (create a new folder/overwrite).
5. List each step in the plan file with its number, title, and initial status ⏳ pending, using the **step-tracking-format** knowledge.
6. Populate the context file with all relevant background: requirements docs, ADRs, user stories, spike findings, codebase references, constraints, assumptions, and any other material that informed the plan.
7. Update step status in the plan file immediately after each state change (⏳ → 🔄 → ✅, or ❌/🚫 on failure). Refer to **step-status-definitions** knowledge for emoji meanings.
8. Never modify plan structure, objectives, or steps except to update statuses or add clarifying notes.
9. Always display the complete step list so progress is visible even across context resets.
</track-plan>

<execute-step>
1. Before starting a step, mark it as 🔄 in-progress in the plan file and briefly explain your approach.
2. Execute the step fully — no partial implementations.
3. After completing the step, validate the outcome meets the step's objectives.
4. Mark the step as ✅ completed; document files changed, implementation details, and validation results in the plan file.
5. Confirm the prerequisite step is fully ✅ completed before starting a step that depends on it.
6. Display the full updated step list with current statuses after each completion.
</execute-step>

<report-progress>
1. At plan start, display all steps with ⏳ pending status.
2. After each step completion, update that step to ✅ and show the full step list with all current statuses.
3. Include detailed information per step: files changed, implementation notes, validation results.
4. Never summarize multiple steps together — each step must be listed individually with its own status and details.
5. At plan end, show the final step list with all ✅ completed and provide a summary of accomplishments.
</report-progress>

<handle-errors>
1. Mark the failed step as ❌ with error details in the plan file.
2. Document the error clearly.
3. Analyze the root cause.
4. Attempt to fix and retry the step.
5. Update step status to ✅ if resolved, or 🚫 blocked if unresolvable.
6. If blocked, consult the user before proceeding.
7. Display the updated full step list with current statuses.
8. Never skip a failed step or failed validation — address issues before proceeding.
</handle-errors>

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
   1. Record each finding as a new fix step in the plan file with ⏳ pending status.
   2. Apply **execute-step** for each fix step.
   3. Re-run the **review-code** skill on the affected files.
   4. Repeat until no 🚫 Blockers or 🔴 Majors remain.
4. If only 🟡 Minor and 🟢 Nit findings remain, document them in the final summary without blocking completion.
5. Display the final completion summary once the review passes. Keep the plan file and context file as a permanent record of the implementation.
</review-post-execution>



<manage-user-interaction>
1. Execute the full plan autonomously without asking for permission at each step.
2. If a step is ambiguous or requires user input, pause and ask before proceeding.
3. If blocked on a step due to missing information or external dependencies, inform the user and wait for guidance.
4. If deviating from the plan due to unforeseen issues, explain why and how you're adapting.
</manage-user-interaction>

</capabilities>



<rules>

<rule> **At Plan Start**: Apply **track-plan** to create the feature folder with plan and context files before executing any step. </rule>
<rule> **During Each Step**: Apply **execute-step** for every step in the plan. </rule>
<rule> **Throughout Execution**: Apply **report-progress** — show the full step list with current statuses after every step. </rule>
<rule> **When a Step Fails**: Apply **handle-errors** immediately. </rule>
<rule> **At Validation Points**: Apply **run-validation-checkpoints** after code changes and at major milestones. Validate incrementally, not just at the end. </rule>
<rule> **When Facing Ambiguity or Blockers**: Apply **manage-user-interaction** — pause and ask rather than assuming. </rule>
<rule> **After All Steps Complete**: Apply **review-post-execution**. Keep the plan file and context file as a permanent record — do not delete them. </rule>

</rules>