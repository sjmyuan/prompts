# plan-feature-implementation

1. **Prepare Environment (Prerequisites)**: Apply **plan-prerequisites** from the SKILL.md — ensure the feature branch exists, named per the **repo's branch convention** (detect from existing branches / git config / team docs, or ask the user; never assume a prefix), based on the correct base; the working tree is clean, dependencies and toolchain are installed, and baseline tests, linting, and type-checking pass. If any check is not ready, stop and raise it to the user before continuing.
2. Break down high-level software requirements into specific, independently testable functionalities.
3. **Define Scope Boundary**: Apply **define-scope-boundary** — derive the **In scope**/**Out of scope** lists from the requirement scope and the governing ADR (for **orchestrate-feature-delivery** cells); present to the user for ratification.
4. Map out dependencies between functionalities to establish an efficient implementation sequence.
5. **Consolidate Steps**: Group related functionalities together when they share context or can be tested together, reducing the total step count while maintaining clarity. Consolidation strategies: (a) merge test-and-implement steps for simple getters/setters or config properties into a single step, (b) combine Clean Up Unused Code + Clean Up Tests + Verify Cleanup into one cleanup step when changes are small, (c) group Validate Linting, Formatting and Type Checking across multiple functionalities into one final quality gate step.
6. Load **reference/tdd-approach-selection.md** to select the appropriate TDD variant for each functionality. Document the rationale.
7. Create a detailed step-by-step implementation plan (starting with the ratified `## Scope Boundary` block). For each functionality, include the following steps:
   1. **Write Focused Tests**: Create precise unit tests for a single functionality, task or requirement, ensuring coverage of all possible scenarios, edge cases, and invalid inputs.
   2. **Confirm Test Failure**: Execute the tests to verify they fail initially, confirming their validity before implementation begins.
   3. **Implement Minimal Code**: Write the simplest code required to pass the tests, avoiding over-engineering or adding features not directly related to the current test cases.
   4. **Verify Implementation**: Re-run the tests to confirm that the implemented code passes all test cases successfully. Debug and refine as necessary.
   5. **Refactor**: Improve the code's structure, readability, and performance while maintaining functionality, ensuring no tests break during the process.
   6. **Validate Refactoring**: Run the tests again after refactoring to ensure the updated code still passes all test cases without introducing regressions.
   7. **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after implementation.
   8. **Clean Up Tests**: Update or remove tests that are no longer relevant, ensuring the test suite remains accurate and effective.
   9. **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
   10. **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
8. Ensure the total number of steps in the plan is manageable and does not exceed 25 steps. The full TDD cycle can generate up to 10 steps per functionality; use consolidation strategies to reduce this where appropriate.
9. **Validate Plan Quality**: Load **reference/plan-quality-checklist.md** and verify — every functionality has tests defined, dependency ordering is correct, step count ≤ 25, and TDD variants are documented. Revise any failing items before presenting to the user.
10. Summarize the complete plan to the user.
