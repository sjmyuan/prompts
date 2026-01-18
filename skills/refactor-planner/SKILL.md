---
name: refactor-planner
description: Clarify the scope, objectives, and constraints of the refactor request first, then generate a refactoring plan for the refactor request. Use this skill when the user submits a refactor request to refactor existing functionality.
---

<when-to-use-this-skill>
- User submits a refactor request to refactor existing functionalities
</when-to-use-this-skill>


<capabilities>

The capabilities section describes additional capabilities that you can refer to.

<defining-refactor-request>
- Gather relevant information from the codebase, knowledge base, and user input to clearly define the refactor request.
- Identify and clarify any ambiguous terms or implicit assumptions to ensure proper understanding.
- Ask questions to the user to refine and narrow down the focus of the refactor request as needed.
- Present a structured summary of the refactor request to the user and request confirmation or refinements.
</defining-refactor-request>

<refactor-planning>
- Break down the refactor request into specific, measurable objectives and clearly defined constraints.
- Identify and map dependencies between objectives to establish an efficient and logical refactoring sequence.
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
  - Step 1: Write Focused Tests for refactor objective A
  - Step 2: Confirm Test Failure for refactor objective A
  - Step 3: Refactor Code for refactor objective A
  - Step 4: Verify Refactor for refactor objective A
  - Step 5: Clean Up Unused Code for refactor objective A
  - Step 6: Clean Up Tests for refactor objective A
  - Step 7: Verify Cleanup for refactor objective A
  - Step 8: Validate Linting, Formatting and Type Checking for refactor objective A
  - Step 9: Write Focused Tests for refactor objective B
  - Step 10: Confirm Test Failure for refactor objective B
  - Step 11: Refactor Code for refactor objective B
  - Step 12: Verify Refactor for refactor objective B
  - Step 13: Clean Up Unused Code for refactor objective B
  - Step 14: Clean Up Tests for refactor objective B
  - Step 15: Verify Cleanup for refactor objective B
  - Step 16: Validate Linting, Formatting and Type Checking for refactor objective B
  - ... 
  """
</refactor-planning>
<capabilities>

<rules>

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> If the user submits a refactoring request, apply the **defining-refactor-request** capability to clarify the scope, objectives, and constraints of the refactor request. </rule>
<rule> After clarifying the scope, objectives and constraints of the refactor request, apply the **refactor-planning** capability to generate a refactor plan. </rule>
</rules>