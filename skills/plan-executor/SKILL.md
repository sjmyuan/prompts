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
- **Initialize Tracking**: At the start of execution, record all plan steps in the tracking system (todo tool or PLAN.md file)
- **Status Updates**: Update step status immediately after completion (not-started → in-progress → completed)
- **Immutable Plan**: Never modify the plan structure, objectives, or steps except to update status or add clarifying notes
- **Preserve Context**: Maintain the original plan's intent, sequence, and dependencies throughout execution
</plan-tracking>

<step-execution>
- **Sequential Execution**: Execute steps in order unless dependencies allow parallelization
- **Think Aloud**: Before implementing each step, briefly explain your approach and what you're about to do
- **Complete Thoroughly**: Fully complete each step before moving to the next—no partial implementations
- **Validate Results**: After each critical step, verify the outcome meets the step's objectives
- **Handle Dependencies**: When a step depends on another, confirm the prerequisite is fully completed first
</step-execution>

<progress-reporting>
- **Milestone Updates**: Provide status summaries at natural breakpoints:
  - After completing major phases (e.g., all tests written, all refactors completed)
  - After every 8-10 steps for long plans
  - When switching contexts (e.g., from one file/component to another)
- **Completion Summary**: After finishing all steps, summarize what was accomplished and any deviations
- **Continuous Visibility**: Update the todo list status promptly so users can track progress in real-time
</progress-reporting>

<error-handling>
- **Anticipate Issues**: Before executing complex steps, identify potential failure points
- **Fail Fast**: If a step fails (e.g., tests don't pass, build errors), immediately investigate and resolve
- **Recovery Strategy**: When encountering errors:
  1. Document the error clearly
  2. Analyze the root cause
  3. Attempt to fix and retry the step
  4. If unresolvable, mark the step as blocked and consult the user
- **Rollback Awareness**: Keep track of changes made, so you can revert if necessary
- **Never Skip**: Don't skip failed steps or validation—address issues before proceeding
</error-handling>

<validation-checkpoints>
- **Test Validation**: After code changes, run relevant tests to confirm correctness
- **Quality Checks**: Periodically run linting, formatting, and type-checking (especially after significant changes)
- **Build Verification**: For build-dependent projects, ensure the build succeeds at key milestones
- **Incremental Validation**: Don't wait until the end—validate incrementally to catch issues early
</validation-checkpoints>

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
- **Single Component Refactor**: Simple 7-step refactor extracting validation logic from DataImportedHandler into a dedicated validator class with progress updates
  - Load: [examples/single-component-refactor.md](examples/single-component-refactor.md)
- **Multi-File Implementation**: Complex 7-step implementation adding data category transformation feature across multiple Java files and layers
  - Load: [examples/multi-file-implementation.md](examples/multi-file-implementation.md)
- **Handling Failed Steps**: Error recovery and debugging during bug fix implementation when encountering compilation errors and missing dependencies
  - Load: [examples/handling-failed-steps.md](examples/handling-failed-steps.md)

**When to load**: Load a specific example when you need concrete guidance for a similar scenario in a Java/Spring Boot context.

</examples>

<rules>

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> **At Plan Start**: Apply the **plan-tracking** capability to initialize the tracking system with all plan steps before beginning execution. </rule>

<rule> **During Execution**: Apply the **step-execution** capability continuously:
  - Before each step: think aloud and explain your approach
  - During each step: execute thoroughly and handle dependencies
  - After each step: validate results and update status to completed immediately
</rule>

<rule> **For Long or Multi-Phase Plans**: Apply the **progress-reporting** capability:
  - After completing major phases (e.g., all tests written, all implementations done)
  - After every 8-10 steps for plans with 15+ steps
  - When switching contexts (moving to different files/components)
  - Always provide a final completion summary at the end
</rule>

<rule> **When Steps Fail or Encounter Errors**: Apply the **error-handling** capability immediately:
  - Document the error clearly
  - Analyze root cause
  - Attempt to fix and retry
  - If unresolvable, consult the user before proceeding
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

</rules>