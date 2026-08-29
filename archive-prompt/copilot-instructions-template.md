<knowledge>

The knowledge section contains information about the software project, including its purpose, architecture, technology stack, etc.

<project-description> 
</project-description>
<tech-stack>
</tech-stack>
<architecture>
</architecture>
<coding-guidelines> 
</coding-guidelines>

</knowledge>

<skills>

The skills section describes additional capabilities that you can refer to, including defining requirements, planning, test-driven development, etc.

<defining-requirement>
- Collect required information from the code base, knowledge section, and user input to define the software requirement.
- Clarify ambiguous terms or assumptions to ensure alignment.
- Summarize the requirement back to the user and ask for confirmation or corrections.
</defining-requirement>

<planning>
- Break down high-level software requirements into specific, independently testable functionalities.
- Map out dependencies between functionalities to establish an efficient implementation sequence.
- Create a detailed step-by-step implementation plan for each functionality.
- Summarize the plan back to the user and ask for confirmation or corrections.
</planning>

<customized-tdd>
Step 1: **Write Focused Tests**, Create precise unit tests for a single functionality or requirement, ensuring coverage of all possible scenarios, edge cases, and invalid inputs.  
Step 2: **Confirm Test Failure**, Execute the tests to verify they fail initially, confirming their validity before implementation begins.  
Step 3: **Implement Minimal Code**, Write the simplest code required to pass the tests, avoiding over-engineering or adding features not directly related to the current test cases.  
Step 4: **Verify Implementation**, Re-run the tests to confirm that the implemented code passes all test cases successfully. Debug and refine as necessary.  
Step 5: **Refactor**, Improve the code’s structure, readability, and performance while maintaining functionality, ensuring no tests break during the process.  
Step 6: **Validate Refactoring**, Run the tests again after refactoring to ensure the updated code still passes all test cases without introducing regressions.
</customized-tdd>

<skills>

<rules>
The rules section outlines decision criteria that determine which skills to apply based on the current context and user inputs.

<rule> When user submit a requirement, apply the **defining-requirement** skill to clarify and structure it. </rule>
<rule> Before implementation, apply the **planning** skill to generate a plan. </rule>
<rule> Use the **customized-tdd** skill to implement the plan, think aloud what you will do before any code changes. </rule>
<rule> After modifying the test code, run the test. </rule>
<rule> After modifying the implementation code, run the test. </rule>
<rule> When run a command in terminal, redirect stdout and stderr to the file output.log, then read the file to get the output</rule>
</rules>