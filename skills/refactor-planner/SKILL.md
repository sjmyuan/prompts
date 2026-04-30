---
name: refactor-planner
description: Analyze refactoring needs and generate detailed, step-by-step TDD-based refactoring plans. Handles code cleanup, architecture improvements, technical debt, and code quality enhancements. Use when users request refactoring, code improvements, structural changes, or cleanup tasks. This skill produces a plan but does not execute changes—pair with plan-executor for implementation.
---

<when-to-use-this-skill>
- User requests refactoring of existing code or functionality
- User asks for code cleanup, restructuring, or quality improvements
- User wants to reduce technical debt or improve code organization
- User requests improvements to maintainability, readability, or performance without changing behavior
</when-to-use-this-skill>

<knowledge>

<tdd-approach-selection>
Select the appropriate TDD variant based on the refactor type:

| Refactor type | TDD approach |
|---|---|
| **Simple cleanups** (removing unused imports, fixing formatting) | May skip test creation if existing tests provide adequate coverage |
| **Type improvements** (adding/refining TypeScript types) | Focus on type-checking validation rather than test-first approach |
| **Documentation-only changes** | No test cycle needed; validate with linting only |
| **Code organization** (file moves, renames) | Existing tests should pass unchanged |
| **Complex logic changes** | Always follow full TDD cycle for safety |

Always ensure existing tests pass before and after changes. Document the rationale for the chosen TDD variant in the plan.
</tdd-approach-selection>

<example-selector>
Load only the example directly relevant to the current refactoring task to minimize context size. Each example covers the full workflow: refactor request definition (**define-refactor-request**) and plan generation (**plan-refactor**).

- **Service Layer Splitting**: When refactoring involves breaking down large handler or service classes into smaller, focused components following Single Responsibility Principle, read [examples/service-splitting.md](examples/service-splitting.md)
- **Validation Extraction**: When refactoring involves extracting validation logic from handlers or services into dedicated validator classes, read [examples/validation-extraction.md](examples/validation-extraction.md)
- **Interface Implementation**: When refactoring involves improving abstraction by adding interfaces and dependency injection for better testability, read [examples/interface-implementation.md](examples/interface-implementation.md)
</example-selector>

</knowledge>

<capabilities>

<define-refactor-request>
1. Gather relevant information from the codebase, knowledge base, and user input to clearly define the refactor request.
2. Identify and clarify any ambiguous terms or implicit assumptions to ensure proper understanding.
3. Ask questions to the user to refine and narrow down the focus of the refactor request as needed.
4. Present a structured summary of the refactor request to the user and request confirmation or refinements.
</define-refactor-request>

<plan-refactor>
1. **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before refactoring begins.
2. Break down the refactor request into specific, measurable objectives and clearly defined constraints.
3. Identify and map dependencies between objectives to establish an efficient and logical refactoring sequence.
4. **Consolidate Steps**: Group related objectives together when they share context or can be tested together, reducing the total step count while maintaining clarity.
5. Consult **tdd-approach-selection** knowledge to select the appropriate TDD variant for each objective.
6. Create a detailed step-by-step refactor plan. For each objective, include the following steps:
   1. **Write Focused Tests**: Create precise unit tests targeting the specific refactoring objective, ensuring comprehensive coverage of all scenarios, edge cases, and invalid inputs.
   2. **Confirm Test Failure**: Execute the tests to verify they fail initially, validating that the tests correctly identify the current code behavior before refactoring begins.
   3. **Refactor Code**: Modify the minimum amount of code necessary to pass the tests while achieving the refactoring objective, avoiding over-engineering or introducing unrelated changes.
   4. **Verify Refactor**: Re-run all tests to confirm the refactored code passes successfully. Debug and refine as necessary to ensure correctness.
   5. **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after the refactor.
   6. **Clean Up Tests**: Update or remove tests that are no longer relevant due to the refactor, ensuring the test suite remains accurate and effective.
   7. **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
   8. **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
7. Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
8. Summarize the complete plan to the user. For example:
  ```
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
  ```
</plan-refactor>

</capabilities>

<rules>

<rule> When the user submits a refactoring request, apply **define-refactor-request** to clarify the scope, objectives, and constraints. </rule>
<rule> After defining the refactor request, consult **tdd-approach-selection** knowledge to select the TDD variant, then apply **plan-refactor**. </rule>
<rule> After presenting the refactor plan to the user, immediately apply the **plan-executor** skill to execute the steps. </rule>

</rules>

