---
name: feature-implementation-planner
description: Clarify and structure the requirement first, then generate an implementation plan for the requirement; Use this skill when user submits a requirement to add new functionalities.
---

<when-to-use-this-skill>
- User submits a requirement to add new functionalities.
</when-to-use-this-skill>

<capabilities>

The capabilities section describes additional capabilities that you can refer to.

<defining-requirement>
- Gather relevant information from the codebase, knowledge base, and user input to clearly define the software requirement.
- Identify and clarify any ambiguous terms or implicit assumptions to ensure proper understanding.
- Ask questions to the user to refine and narrow down the focus of the software requirement as needed.
- Present a structured summary of the requirement to the user and request confirmation or refinements.
</defining-requirement>

<implementation-planning>
- Break down high-level software requirements into specific, independently testable functionalities.
- Map out dependencies between functionalities to establish an efficient implementation sequence.
- Create a detailed step-by-step implementation plan for the functionalities following the tdd approach. for each functionality, the steps should include:
  - **Write Focused Tests**, Create precise unit tests for a single functionality, task or requirement, ensuring coverage of all possible scenarios, edge cases, and invalid inputs.  
  - **Confirm Test Failure**, Execute the tests to verify they fail initially, confirming their validity before implementation begins.  
  - **Implement Minimal Code**, Write the simplest code required to pass the tests, avoiding over-engineering or adding features not directly related to the current test cases.  
  - **Verify Implementation**, Re-run the tests to confirm that the implemented code passes all test cases successfully. Debug and refine as necessary.  
  - **Refactor**, Improve the code’s structure, readability, and performance while maintaining functionality, ensuring no tests break during the process.  
  - **Validate Refactoring**, Run the tests again after refactoring to ensure the updated code still passes all test cases without introducing regressions.
  - **Validate Linting, Formatting and Type Checking**, Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
- Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
- Summarize the plan back to the user. for example:
  """
  To implement the requirement of [requirement summary], the plan is as follows:
  - Step 1: Write Focused Tests for functionality A
  - Step 2: Confirm Test Failure for functionality A
  - Step 3: Implement Minimal Code for functionality A
  - Step 4: Verify Implementation for functionality A
  - Step 5: Refactor code related to functionality A
  - Step 6: Validate Refactoring for functionality A
  - Step 7: Validate Linting, Formatting and Type Checking for functionality A
  - Step 8: Write Focused Tests for functionality B
  - Step 9: Confirm Test Failure for functionality B
  - Step 10: Implement Minimal Code for functionality B
  - Step 11: Verify Implementation for functionality B
  - Step 12: Refactor code related to functionality B
  - Step 13: Validate Refactoring for functionality B
  - Step 14: Validate Linting, Formatting and Type Checking for functionality B
  - ...
  """
</implementation-planning>

</capabilities>

<rules>

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> If user submit a requirement, apply the **defining-requirement** capability to clarify and structure it. </rule>
<rule> After defining the requirement, apply the **implementation-planning** capability to generate an implementation plan. </rule>
</rules>