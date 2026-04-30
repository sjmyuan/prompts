---
name: bug-fix-planner
description: Diagnose bug root causes and generate detailed, step-by-step TDD-based bug fix plans. Use this skill when users report bugs, unexpected behavior, or defects. This skill produces a plan but does not execute changes—pair with plan-executor for implementation.
---

<when-to-use-this-skill>
- User reports a bug, defect, or unexpected behavior
- User describes a regression or something that worked before but no longer does
- User reports failing tests or incorrect outputs in existing functionality
- User asks to investigate and fix a problem in existing code
</when-to-use-this-skill>

<knowledge>

<tdd-approach-selection>
Select the appropriate TDD variant based on the bug type:

| Bug type | TDD approach |
|---|---|
| **Simple bugs** (typos, minor logic errors, incorrect constants) | May consolidate test writing and fixing in fewer steps if existing tests provide adequate coverage |
| **Type-related bugs** (missing/incorrect TypeScript types) | Focus on type-checking validation rather than test-first approach |
| **Configuration bugs** (incorrect environment settings, build config) | Validate with build/run rather than unit tests |
| **Performance bugs** | Require performance tests and benchmarks in addition to functional tests |
| **Complex logic bugs** | Always follow full TDD cycle for safety and thorough validation |

Always ensure existing tests pass before and after changes. Document the rationale for the chosen TDD variant in the plan.
</tdd-approach-selection>

<example-selector>
Load only the example directly relevant to the current bug type to minimize context size. Each example covers the full workflow: root cause identification (**identify-bug-root-cause**) and plan generation (**plan-bug-fix**).

- **Simple Logic Bugs**: When fixing bugs related to incorrect logic, timing, or calculation errors, read [examples/simple-logic-bug.md](examples/simple-logic-bug.md)
- **Type-Related Bugs**: When fixing bugs related to TypeScript types, optional fields, or type safety issues, read [examples/type-related-bug.md](examples/type-related-bug.md)
- **Data Persistence Bugs**: When fixing bugs related to database operations, async handling, or data loss issues, read [examples/data-persistence-bug.md](examples/data-persistence-bug.md)
</example-selector>

</knowledge>

<capabilities>

<identify-bug-root-cause>
1. Gather relevant information from the codebase, knowledge base, test results and user input to clearly identify the bug.
2. Analyze the information to identify patterns, inconsistencies, or anomalies that may indicate the root cause of the bug.
3. Formulate hypotheses about potential causes and systematically test them through code inspection, debugging, or additional logging.
4. Ask questions to the user to narrow down the possibilities until the most likely root cause is identified.
5. Present the identified root cause and the reasoning process to the user and request confirmation or refinements.
</identify-bug-root-cause>

<plan-bug-fix>
1. **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before bug fixing begins.
2. Break down the identified bug root cause into specific, independently testable issues.
3. Map out dependencies between issues to establish an efficient bug-fixing sequence.
4. **Consolidate Steps**: Group related issues together when they share context or can be tested together, reducing the total step count while maintaining clarity.
5. Consult **tdd-approach-selection** knowledge to select the appropriate TDD variant for each issue.
6. Create a detailed step-by-step bug-fixing plan. For each issue, include the following steps:
   1. **Write Focused Tests**: Create precise unit tests targeting the specific bug issue, ensuring comprehensive coverage of all scenarios, edge cases, and invalid inputs.
   2. **Confirm Test Failure**: Execute the tests to verify they fail initially, validating that the tests correctly identify the current code behavior before fixing begins.
   3. **Fix Code**: Modify the minimum amount of code necessary to pass the tests while addressing the bug, avoiding over-engineering or introducing unrelated changes.
   4. **Verify Fix**: Re-run all tests to confirm the fix works successfully. Debug and refine as necessary to ensure correctness.
   5. **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after the bug fix.
   6. **Clean Up Tests**: Update or remove tests that are no longer relevant due to the bug fix, ensuring the test suite remains accurate and effective.
   7. **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
   8. **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
7. Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
8. Summarize the complete plan to the user. For example:
  ```
  To fix the bug of [bug summary], the plan is as follows:
  - Step 1: Validate Baseline (run existing tests, lint, type-check)
  - Step 2: Write Focused Tests for issue A
  - Step 3: Confirm Test Failure for issue A
  - Step 4: Fix Code for issue A
  - Step 5: Verify Fix for issue A
  - Step 6: Clean Up Unused Code for issue A
  - Step 7: Clean Up Tests for issue A
  - Step 8: Verify Cleanup for issue A
  - Step 9: Validate Linting, Formatting and Type Checking for issue A
  - Step 10: Write Focused Tests for issue B
  - Step 11: Confirm Test Failure for issue B
  - Step 12: Fix Code for issue B
  - Step 13: Verify Fix for issue B
  - Step 14: Clean Up Unused Code for issue B
  - Step 15: Clean Up Tests for issue B
  - Step 16: Verify Cleanup for issue B
  - Step 17: Validate Linting, Formatting and Type Checking for issue B
  - ...
  I will apply **plan-executor** skill to fix the bug step by step as outlined.
  ```
</plan-bug-fix>

</capabilities>

<rules>

<rule> When the user reports a bug, apply **identify-bug-root-cause**. </rule>
<rule> After identifying the root cause, consult **tdd-approach-selection** knowledge to select the TDD variant, then apply **plan-bug-fix**. </rule>
<rule> After presenting the bug-fix plan to the user, immediately apply the **plan-executor** skill to execute the steps. </rule>

</rules>

