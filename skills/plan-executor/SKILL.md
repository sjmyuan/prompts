---
name: plan-executor
description: Execute structured plans step-by-step with progress tracking, validation checkpoints, and error recovery. Works with plans from bug-fix-planner, feature-implementation-planner, or refactor-planner. Runs tests, validates changes, and handles failures systematically. Use after generating an implementation, refactor, or bug-fix plan that needs execution.
---

<when-to-use-this-skill>
- You need to execute an outlined plan (implementation plan, refactoring plan, or bug-fix plan)
- A structured, multi-step task requires systematic execution and progress tracking
</when-to-use-this-skill>

<capabilities>

The capabilities section describes the key capabilities for executing plans effectively.

<plan-tracking>
- **Initialize Tracking**: At the start of execution, record all plan steps in a `PLAN.md` file in the workspace root with detailed structure:
  - If `PLAN.md` already exists, check whether it contains an incomplete plan (steps with ❌ failed or 🚫 blocked status). If so, ask the user whether to **resume** from the last known state or **start fresh** (overwriting with the new plan). If starting fresh, overwrite entirely.
  - List each step with its number, title, and initial status (⏳ pending)
  - Include step descriptions or objectives if provided in the original plan
  - Preserve the complete step list for continuous reference
- **Detailed Step Format**: Track each step with comprehensive information:
  ```
  ### Step N: [Step Title] [Status Emoji]
  **Objective**: [What this step achieves]
  **Files**: [Files created, modified, or deleted]
  **Implementation**: [Key changes or actions taken]
  **Validation**: [Test results or verification outcomes]
  **Status**: [Status emoji] [Status description]
  ```
- **Status Updates**: Update step status immediately after completion (⏳ pending → 🔄 in-progress → ✅ completed):
  - ⏳ **Pending**: Not yet started
  - 🔄 **In Progress**: Currently working on this step
  - ✅ **Completed**: Successfully finished
  - ❌ **Failed**: Encountered errors (include error details)
  - 🚫 **Blocked**: Cannot proceed (include blocker details)
- **Immutable Plan**: Never modify the plan structure, objectives, or steps except to update status or add clarifying notes
- **Preserve Context**: Maintain the original plan's intent, sequence, and dependencies throughout execution
- **Always Display Full List**: Show the complete step list with all statuses so progress is always visible, even across context resets
</plan-tracking>

<step-execution>
- **Sequential Execution**: Execute steps in order unless dependencies allow parallelization
- **Update Status Before**: Mark step as 🔄 in-progress when starting work on it
- **Think Aloud**: Before implementing each step, briefly explain your approach and what you're about to do
- **Complete Thoroughly**: Fully complete each step before moving to the next—no partial implementations
- **Validate Results**: After each critical step, verify the outcome meets the step's objectives
- **Update Status After**: Immediately after completing a step:
  - Mark step as ✅ completed
  - Document files changed, implementation details, and validation results
  - Display the full updated step list showing all current statuses
- **Handle Dependencies**: When a step depends on another, confirm the prerequisite is fully completed first
</step-execution>

<progress-reporting>
- **Detailed Step Tracking**: List each step explicitly with full details, not summaries:
  - Step number and title
  - Current status (✅ completed, 🔄 in-progress, ⏳ pending, ❌ failed, 🚫 blocked)
  - Files modified or created
  - Key implementation details or code changes
  - Validation results or test outcomes
- **Always Show Full Plan**: Display all steps with their current status so the AI can:
  - See exactly which steps are completed and which remain
  - Maintain context even if conversation grows long
  - Resume work accurately after context resets
  - Avoid losing track of progress
- **Update After Each Step**: Immediately after completing a step:
  - Update the step's status to ✅ completed
  - Add implementation details and outcomes
  - Show the updated full step list with current statuses
- **Never Summarize Multiple Steps**: Each step must be tracked individually with its own details—never group or summarize several steps together
- **Continuous Visibility**: Maintain the complete step-by-step progress list throughout execution so it's always visible
</progress-reporting>

<error-handling>
- **Anticipate Issues**: Before executing complex steps, identify potential failure points
- **Fail Fast**: If a step fails (e.g., tests don't pass, build errors), immediately investigate and resolve
- **Recovery Strategy**: When encountering errors:
  1. Mark the step as ❌ failed with error details in the progress list
  2. Document the error clearly
  3. Analyze the root cause
  4. Attempt to fix and retry the step
  5. Update step status to ✅ if resolved, or 🚫 blocked if unresolvable
  6. If blocked, consult the user before proceeding
  7. Display the updated full step list with current statuses
- **Rollback Awareness**: Keep track of changes made, so you can revert if necessary
- **Never Skip**: Don't skip failed steps or validation—address issues before proceeding
</error-handling>

<validation-checkpoints>
- **Test Validation**: After code changes, run relevant tests to confirm correctness
- **Quality Checks**: Periodically run linting, formatting, and type-checking (especially after significant changes)
- **Build Verification**: For build-dependent projects, ensure the build succeeds at key milestones
- **Incremental Validation**: Don't wait until the end—validate incrementally to catch issues early
</validation-checkpoints>

<post-execution-review>
- **Trigger**: After ALL plan steps are marked ✅ completed, before performing plan-cleanup.
- **Scope**: Apply the **code-reviewer** skill on all files changed or created during plan execution.
- **Review Focus**: Evaluate correctness, security, performance, maintainability, and test coverage of the changed files.
- **Handle Findings**:
  - If no 🚫 Blocker or 🔴 Major issues are found: proceed directly to **plan-cleanup**.
  - If 🚫 Blocker or 🔴 Major issues are found:
    1. Record each finding as a new fix step in PLAN.md (e.g., "Fix: [issue title]") with ⏳ pending status
    2. Execute each fix step using the **step-execution** capability
    3. After all fixes are applied, re-run the **code-reviewer** skill on the affected files
    4. Repeat until no 🚫 Blockers or 🔴 Majors remain
  - 🟡 Minor and 🟢 Nit findings: Document in the final summary but do not block completion
- **Goal**: Catch issues that TDD validation may have missed and ensure code quality before declaring the plan complete
</post-execution-review>

<plan-cleanup>
- **After Completion**: Once ALL steps (including any post-execution review fix steps) are marked ✅ completed and the final summary is provided:
  - Delete the PLAN.md file from the workspace
  - Confirm the deletion to the user ("Cleaned up PLAN.md")
  - This keeps the workspace clean and signals clear plan completion
- **Only After Success**: Only delete PLAN.md if the entire plan executed successfully—don't delete if there are ❌ failed or 🚫 blocked steps
- **Final Action**: Deleting PLAN.md should be the very last action after displaying the completion summary
</plan-cleanup>

<user-interaction>
- **Autonomous by Default**: Execute the full plan without asking for permission at each step
- **Pause for Clarity**: If a step is ambiguous or requires user input, pause and ask before proceeding
- **Blocking Issues**: If stuck on a step due to missing information or external dependencies, inform the user and wait for guidance
- **Deviations**: If you must deviate from the plan due to unforeseen issues, explain why and how you're adapting
</user-interaction>

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

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> **At Plan Start**: Apply the **plan-tracking** capability to initialize the tracking system with all plan steps before beginning execution. </rule>

<rule> **During Execution**: Apply the **step-execution** capability continuously:
  - Before each step: mark as 🔄 in-progress and explain your approach
  - During each step: execute thoroughly and handle dependencies
  - After each step: 
    - Validate results and mark as ✅ completed
    - Document files changed, implementation details, and validation results
    - Display the full updated step list with all current statuses
</rule>

<rule> **For All Plans**: Apply the **progress-reporting** capability continuously:
  - At plan start: display all steps with ⏳ pending status
  - After each step completion: update that step to ✅ and show the full step list with updated statuses
  - Display detailed information for each step (files changed, implementation notes, validation results)
  - Never summarize multiple steps—each step must be listed individually with its own details
  - Maintain the complete detailed step list throughout execution for continuous visibility
  - At plan end: show final step list with all ✅ completed and provide a summary of accomplishments
</rule>

<rule> **When Steps Fail or Encounter Errors**: Apply the **error-handling** capability immediately:
  - Mark step as ❌ failed with error details
  - Document the error clearly
  - Analyze root cause
  - Attempt to fix and retry
  - Update status to ✅ if resolved or 🚫 blocked if unresolvable
  - Display the updated full step list with current statuses
  - If blocked, consult the user before proceeding
  - Never skip failed validation steps
</rule>

<rule> **At Validation Points**: Apply the **validation-checkpoints** capability:
  - After code changes: run relevant tests
  - After significant changes: run linting, formatting, type-checking
  - At major milestones: verify builds succeed
  - Don't wait until the end—validate incrementally throughout execution
</rule>

<rule> **When Facing Ambiguity or Blockers**: Apply the **user-interaction** capability:
  - If a step is unclear: pause and ask for clarification
  - If external dependencies are missing: document the blocker and consult the user
  - If deviations from the plan are necessary: explain why and how you're adapting
  - Otherwise, execute autonomously without asking for permission at each step
</rule>

<rule> **Plan Immutability**: Throughout execution, apply the **plan-tracking** immutability principle—never modify the plan structure, objectives, or steps except to update statuses or add brief clarifying notes. Never skip, reorder, or remove steps without explicit user approval. </rule>

<rule> **Complete All Steps**: Execute ALL steps in the plan thoroughly, regardless of the number of steps or files affected. Do not stop early or leave steps partially completed. </rule>

<rule> **After All Plan Steps Complete**: Before cleanup, apply the **post-execution-review** capability:
  - Run the **code-reviewer** skill on all files changed or created during execution
  - If 🚫 Blocker or 🔴 Major issues are found: add fix steps to PLAN.md and execute them, then re-review
  - Only proceed to **plan-cleanup** when the review finds no 🚫 Blockers or 🔴 Majors
  - Document any 🟡 Minor or 🟢 Nit findings in the final summary without blocking completion
</rule>

<rule> **After Plan Completion**: Apply the **plan-cleanup** capability when ALL steps (including post-execution review fix steps) are marked ✅ completed:
  - Display the final completion summary with all steps showing ✅ status
  - Delete the PLAN.md file from the workspace
  - Confirm the deletion ("Cleaned up PLAN.md")
  - Only perform cleanup if the entire plan succeeded—keep PLAN.md if any steps are ❌ failed or 🚫 blocked
</rule>

</rules>