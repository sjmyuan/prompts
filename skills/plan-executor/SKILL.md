---
name: plan-executor
description: Execute structured plans step-by-step with progress tracking, validation checkpoints, and error recovery. Works with plans from bug-fix-planner, feature-implementation-planner, or refactor-planner. Runs tests, validates changes, and handles failures systematically. Use after generating an implementation, refactor, or bug-fix plan that needs execution.
---

<when-to-use-this-skill>
- You need to execute an outlined plan (implementation plan, refactoring plan, or bug-fix plan)
- A structured, multi-step task requires systematic execution and progress tracking
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
Record each step in PLAN.md using this format:

```
### Step N: [Step Title] [Status Emoji]
**Objective**: [What this step achieves]
**Files**: [Files created, modified, or deleted]
**Implementation**: [Key changes or actions taken]
**Validation**: [Test results or verification outcomes]
**Status**: [Status emoji] [Status description]
```
</step-tracking-format>

</knowledge>

<capabilities>

<track-plan>
1. At the start of execution, create `PLAN.md` in the workspace root.
2. If `PLAN.md` already exists, check for steps with ❌ failed or 🚫 blocked status. If found, ask the user whether to **resume** from the last known state or **start fresh** (overwriting with the new plan).
3. List each step with its number, title, and initial status ⏳ pending, using the **step-tracking-format** knowledge.
4. Update step status immediately after each state change (⏳ → 🔄 → ✅, or ❌/🚫 on failure). Refer to **step-status-definitions** knowledge for emoji meanings.
5. Never modify plan structure, objectives, or steps except to update statuses or add clarifying notes.
6. Always display the complete step list so progress is visible even across context resets.
</track-plan>

<execute-step>
1. Before starting a step, mark it as 🔄 in-progress in PLAN.md and briefly explain your approach.
2. Execute the step fully — no partial implementations.
3. After completing the step, validate the outcome meets the step's objectives.
4. Mark the step as ✅ completed; document files changed, implementation details, and validation results in PLAN.md.
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
1. Mark the failed step as ❌ with error details in PLAN.md.
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
1. After ALL plan steps are marked ✅ completed, apply the **code-reviewer** skill on all files changed or created during execution.
2. Evaluate correctness, security, performance, maintainability, and test coverage.
3. If 🚫 Blocker or 🔴 Major issues are found:
   1. Record each finding as a new fix step in PLAN.md with ⏳ pending status.
   2. Apply **execute-step** for each fix step.
   3. Re-run the **code-reviewer** skill on the affected files.
   4. Repeat until no 🚫 Blockers or 🔴 Majors remain.
4. If only 🟡 Minor and 🟢 Nit findings remain, document them in the final summary without blocking completion.
5. Proceed to **clean-up-plan** only when the review passes.
</review-post-execution>

<clean-up-plan>
1. Once ALL steps (including any post-execution review fix steps) are marked ✅ completed, display the final completion summary.
2. Delete the PLAN.md file from the workspace.
3. Confirm the deletion to the user ("Cleaned up PLAN.md").
4. Only delete PLAN.md if the entire plan succeeded — keep it if any steps are ❌ failed or 🚫 blocked.
</clean-up-plan>

<manage-user-interaction>
1. Execute the full plan autonomously without asking for permission at each step.
2. If a step is ambiguous or requires user input, pause and ask before proceeding.
3. If blocked on a step due to missing information or external dependencies, inform the user and wait for guidance.
4. If deviating from the plan due to unforeseen issues, explain why and how you're adapting.
</manage-user-interaction>

</capabilities>

<examples>

**Note**: Detailed execution examples are available in separate files to reduce context size. Load only the specific example you need.

**Available Examples**:
- **Single Component Refactor**: Simple 7-step refactor extracting validation logic from DataImportedHandler into a dedicated validator class with detailed progress updates
  - Load: [examples/single-component-refactor.md](examples/single-component-refactor.md)
- **Multi-File Implementation**: Complex 7-step implementation adding data category transformation feature across multiple Java files and layers with full step tracking
  - Load: [examples/multi-file-implementation.md](examples/multi-file-implementation.md)
- **Handling Failed Steps**: Error recovery and debugging during bug fix implementation when encountering compilation errors and missing dependencies, showing ❌→✅ status transitions
  - Load: [examples/handling-failed-steps.md](examples/handling-failed-steps.md)
- **Long Plan Execution**: Comprehensive 15-step authentication system implementation demonstrating continuous visibility and context preservation for long plans
  - Load: [examples/long-plan-execution.md](examples/long-plan-execution.md)

**When to load**: Load a specific example when you need concrete guidance for a similar scenario. Choose based on:
- **Single Component Refactor** - for simple, focused refactoring tasks
- **Multi-File Implementation** - for complex features spanning multiple files
- **Handling Failed Steps** - for understanding error recovery patterns
- **Long Plan Execution** - for managing plans with 10+ steps without losing context

</examples>

<rules>

<rule> **At Plan Start**: Apply **track-plan** to initialize PLAN.md with all plan steps before executing any step. </rule>
<rule> **During Each Step**: Apply **execute-step** — mark 🔄 before starting, execute fully, validate and mark ✅ after completing, update PLAN.md. </rule>
<rule> **Throughout Execution**: Apply **report-progress** — show the full step list with current statuses after every step. Never summarize multiple steps together. </rule>
<rule> **When a Step Fails**: Apply **handle-errors** immediately — mark ❌, diagnose, fix and retry, escalate to 🚫 if unresolvable, consult the user before proceeding. </rule>
<rule> **At Validation Points**: Apply **run-validation-checkpoints** after code changes and at major milestones. Validate incrementally, not just at the end. </rule>
<rule> **When Facing Ambiguity or Blockers**: Apply **manage-user-interaction** — pause and ask rather than assuming. </rule>
<rule> **After All Steps Complete**: Apply **review-post-execution**, then **clean-up-plan** once the review passes. </rule>
<rule> **Plan Immutability**: Never modify plan structure, objectives, or step sequence except to update statuses or add brief clarifying notes. Never skip, reorder, or remove steps without explicit user approval. </rule>

</rules>