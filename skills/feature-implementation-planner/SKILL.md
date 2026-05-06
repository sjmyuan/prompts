---
name: feature-implementation-planner
description: Clarify feature requirements and generate detailed, step-by-step TDD-based implementation plans for new functionality. Breaks down requirements into testable tasks with validation steps. Use when users request new features, enhancements, or functionality additions, or when users ask exploratory questions about whether a feature is possible (e.g., "is it possible to...", "can we add...", "would it be feasible to...") that imply a desire to implement new behavior. This skill produces a plan but does not execute changes—pair with plan-executor for implementation.
---

<when-to-use-this-skill>
- User submits a requirement to add new functionality or features
- User asks to implement a new feature, enhancement, or behavior
- User describes desired functionality that does not currently exist in the codebase
- User requests extending or adding to existing capabilities
- User asks an exploratory question about whether a feature is possible (e.g., "is it possible to...", "can we add...", "would it be feasible to...") where the intent is to introduce new behavior
</when-to-use-this-skill>

<knowledge>

<tdd-approach-selection>
Select the appropriate TDD variant based on the feature type:

| Feature type | TDD approach |
|---|---|
| **Simple features** (small UI additions, basic form fields) | May consolidate test and implementation steps when logic is straightforward |
| **Pure presentational components** | Focus on rendering and prop validation tests with minimal logic testing |
| **Type-only additions** (adding new types/interfaces without behavior) | Focus on type-checking validation rather than test-first approach |
| **Configuration changes** (adding constants, config options) | Minimal testing may suffice if changes don't affect behavior |
| **Complex business logic** | Always follow full TDD cycle for safety and clarity |

Always ensure existing tests pass before and after changes. Document the rationale for the chosen TDD variant in the plan.
</tdd-approach-selection>

<example-selector>
Load only the example directly relevant to the current implementation task to minimize context size. Each example covers the full workflow: requirement definition (**define-requirement**) and plan generation (**plan-implementation**).

- **Adding a New Message Handler**: When implementing a new feature that involves message handling, service logic, and event processing, read [examples/adding-new-message-handler.md](examples/adding-new-message-handler.md)
- **Simple Configuration Addition**: When implementing straightforward configuration properties without complex business logic, read [examples/simple-configuration-addition.md](examples/simple-configuration-addition.md)
- **Complex Transformation Logic**: When implementing sophisticated transformation algorithms or complex business rules requiring rigorous testing, read [examples/complex-transformation-logic.md](examples/complex-transformation-logic.md)
</example-selector>

</knowledge>

<capabilities>

<define-requirement>
1. Gather relevant information from the codebase, knowledge base, and user input to clearly define the software requirement.
2. Identify and clarify any ambiguous terms or implicit assumptions to ensure proper understanding.
3. Ask questions to the user to refine and narrow down the focus of the software requirement as needed.
4. Present a structured summary of the requirement to the user and request confirmation or refinements.
</define-requirement>

<plan-implementation>
1. **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before implementation begins.
2. Break down high-level software requirements into specific, independently testable functionalities.
3. Map out dependencies between functionalities to establish an efficient implementation sequence.
4. **Consolidate Steps**: Group related functionalities together when they share context or can be tested together, reducing the total step count while maintaining clarity.
5. Consult **tdd-approach-selection** knowledge to select the appropriate TDD variant for each functionality.
6. Create a detailed step-by-step implementation plan. For each functionality, include the following steps:
   1. **Write Focused Tests**: Create precise unit tests for a single functionality, task or requirement, ensuring coverage of all possible scenarios, edge cases, and invalid inputs.  
   2. **Confirm Test Failure**: Execute the tests to verify they fail initially, confirming their validity before implementation begins.  
   3. **Implement Minimal Code**: Write the simplest code required to pass the tests, avoiding over-engineering or adding features not directly related to the current test cases.  
   4. **Verify Implementation**: Re-run the tests to confirm that the implemented code passes all test cases successfully. Debug and refine as necessary.  
   5. **Refactor**: Improve the code’s structure, readability, and performance while maintaining functionality, ensuring no tests break during the process.  
   6. **Validate Refactoring**: Run the tests again after refactoring to ensure the updated code still passes all test cases without introducing regressions.
   7. **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after implementation.
   8. **Clean Up Tests**: Update or remove tests that are no longer relevant, ensuring the test suite remains accurate and effective.
   9. **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
   10. **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
7. Ensure the total number of steps in the plan is manageable and does not exceed 25 steps. The full TDD cycle can generate up to 10 steps per functionality; use consolidation strategies to reduce this where appropriate.
8. Summarize the complete plan to the user. For example:
  ```
  To implement the requirement of [requirement summary], the plan is as follows:
  - Step 1: Validate Baseline (run existing tests, lint, type-check)
  - Step 2: Write Focused Tests for functionality A
  - Step 3: Confirm Test Failure for functionality A
  - Step 4: Implement Minimal Code for functionality A
  - Step 5: Verify Implementation for functionality A
  - Step 6: Refactor code related to functionality A
  - Step 7: Validate Refactoring for functionality A
  - Step 8: Clean Up Unused Code for functionality A
  - Step 9: Clean Up Tests for functionality A
  - Step 10: Verify Cleanup for functionality A
  - Step 11: Validate Linting, Formatting and Type Checking for functionality A
  - Step 12: Write Focused Tests for functionality B
  - Step 13: Confirm Test Failure for functionality B
  - Step 14: Implement Minimal Code for functionality B
  - Step 15: Verify Implementation for functionality B
  - Step 16: Refactor code related to functionality B
  - Step 17: Validate Refactoring for functionality B
  - Step 18: Clean Up Unused Code for functionality B
  - Step 19: Clean Up Tests for functionality B
  - Step 20: Verify Cleanup for functionality B
  - Step 21: Validate Linting, Formatting and Type Checking for functionality B
  - ...
  ```
</plan-implementation>

</capabilities>

<rules>

<rule> When the user submits a requirement, apply **define-requirement** to clarify and structure it. </rule>
<rule> After defining the requirement, consult **tdd-approach-selection** knowledge to select the TDD variant, then apply **plan-implementation**. </rule>

</rules>

