---
name: refactor-planner
description: Analyze refactoring needs and generate detailed, step-by-step TDD-based refactoring plans. Handles code cleanup, architecture improvements, technical debt, and code quality enhancements. Use when users request refactoring, code improvements, structural changes, or cleanup tasks. This skill produces a plan but does not execute changes—pair with plan-executor for implementation.
---

<when-to-use-this-skill>
- User submits a refactor request to refactor existing functionalities
- User submits a code issue fix request
- User submits a code improvement request
</when-to-use-this-skill>


<capabilities>

The capabilities section describes additional capabilities that you can refer to.

<defining-refactor-request>
- Gather relevant information from the codebase, knowledge base, and user input to clearly define the refactor request.
- Identify and clarify any ambiguous terms or implicit assumptions to ensure proper understanding.
- Ask questions to the user to refine and narrow down the focus of the refactor request as needed.
- Present a structured summary of the refactor request to the user and request confirmation or refinements.
</defining-refactor-request>

<adapting-tdd-approach>
- Recognize when the full TDD cycle may be adapted or streamlined based on the refactoring type:
  - **Simple cleanups** (removing unused imports, fixing formatting): May skip test creation if existing tests provide adequate coverage
  - **Type improvements** (adding/refining TypeScript types): Focus on type-checking validation rather than test-first approach
  - **Documentation-only changes**: No test cycle needed, validate with linting only
  - **Code organization** (file moves, renames): Existing tests should pass unchanged
  - **Complex logic changes**: Always follow full TDD cycle for safety
- When adapting the approach, always ensure existing tests pass before and after changes
- Document the rationale for adapting the TDD approach in the plan
</adapting-tdd-approach>

<refactor-planning>
- **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before refactoring begins.
- Break down the refactor request into specific, measurable objectives and clearly defined constraints.
- Identify and map dependencies between objectives to establish an efficient and logical refactoring sequence.
- **Consolidate Steps**: Group related objectives together when they share context or can be tested together, reducing the total step count while maintaining clarity.
- Create a detailed step-by-step refactor plan following the TDD approach. For each objective, the steps should include:
  - **Write Focused Tests**: Create precise unit tests targeting the specific refactoring objective, ensuring comprehensive coverage of all scenarios, edge cases, and invalid inputs.
  - **Confirm Test Failure**: Execute the tests to verify they fail initially, validating that the tests correctly identify the current code behavior before refactoring begins.
  - **Refactor Code**: Modify the minimum amount of code necessary to pass the tests while achieving the refactoring objective, avoiding over-engineering or introducing unrelated changes.
  - **Verify Refactor**: Re-run all tests to confirm the refactored code passes successfully. Debug and refine as necessary to ensure correctness.
  - **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after the refactor.
  - **Clean Up Tests**: Update or remove tests that are no longer relevant due to the refactor, ensuring the test suite remains accurate and effective.
  - **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
  - **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
- Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
- Summarize the complete plan to the user. For example:
  """
  To complete the refactoring request of [refactor request summary], the plan is as follows:
  - Step 1: Validate Baseline (run existing tests, lint, type-check)
  - Step 2: Write Focused Tests for refactor objective A
  - Step 3: Confirm Test Failure for refactor objective A
  - Step 4: Refactor Code for refactor objective A
  - Step 5: Verify Refactor for refactor objective A
  - Step 6: Clean Up Unused Code for refactor objective A
  - Step 7: Clean Up Tests for refactor objective A
  - Step 8: Verify Cleanup for refactor objective A
  - Step 9: Validate Linting, Formatting and Type Checking for refactor objective A
  - Step 10: Write Focused Tests for refactor objective B
  - Step 11: Confirm Test Failure for refactor objective B
  - Step 12: Refactor Code for refactor objective B
  - Step 13: Verify Refactor for refactor objective B
  - Step 14: Clean Up Unused Code for refactor objective B
  - Step 15: Clean Up Tests for refactor objective B
  - Step 16: Verify Cleanup for refactor objective B
  - Step 17: Validate Linting, Formatting and Type Checking for refactor objective B
  - ... 
  I will apply **plan-executor** skill to refactor the code step by step as outlined.
  """
</refactor-planning>

<refactor-planning-examples>

When you need specific examples to understand how to apply the refactoring planning approach, load the relevant example file from the examples folder:

- **Service Layer Splitting**: When refactoring involves breaking down large handler or service classes into smaller, focused components following Single Responsibility Principle, read [examples/service-splitting.md](examples/service-splitting.md)
- **Validation Extraction**: When refactoring involves extracting validation logic from handlers or services into dedicated validator classes, read [examples/validation-extraction.md](examples/validation-extraction.md)
- **Interface Implementation**: When refactoring involves improving abstraction by adding interfaces and dependency injection for better testability, read [examples/interface-implementation.md](examples/interface-implementation.md)

Only load example files when they are directly relevant to the current refactoring task to minimize context size.

</refactor-planning-examples>

</capabilities>

<rules>

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> If the user submits a refactoring request, apply the **defining-refactor-request** capability to clarify the scope, objectives, and constraints of the refactor request. </rule>
<rule> After defining the refactor request, apply the **adapting-tdd-approach** capability to evaluate whether to adapt tdd approach based on the refactoring type and complexity. </rule>
<rule> Apply the **refactor-planning** capability to generate a detailed refactor plan, incorporating baseline validation and step consolidation strategies. </rule>
<rule> Always check lint and type check together when fixing lint or type check issue </rule>
</rules>