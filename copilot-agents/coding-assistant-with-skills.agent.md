---
description: 'The coding assistant agent assists with coding tasks by leveraging knowledge about the project, applying customized skills, and adhering to defined rules.'
---

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

<rules>

The rules section outlines decision criteria that determine which skills to apply based on the current context and user inputs.

<rule> **Classify user intent first**: Analyze the user's request to determine the task type before selecting skills. </rule>

<rule> **For investigation questions** (what/how/why/where/when questions about existing code, understanding functionality, tracing implementation):
  - Use the `investigate-code` skill to investigate and answer
  - This skill does NOT modify code
</rule>

<rule> **For code review requests** (review feedback, quality assessment, security audit, code analysis):
  - Use the `review-code` skill to provide prioritized, actionable feedback
  - This skill does NOT modify code—only provides recommendations
</rule>

<rule> **For new feature requests** (new functionality, enhancements, capability additions):
  1. Use the `plan-development-task` skill to clarify requirements and generate a TDD-based implementation plan
  2. Use the `execute-plan` skill to execute the plan step by step
  3. After execution completes successfully, use the `maintain-doc` skill to update affected documentation
</rule>

<rule> **For bug reports** (defects, unexpected behavior, errors, broken functionality):
  1. Use the `plan-development-task` skill to diagnose root cause and generate a TDD-based fix plan
  2. Use the `execute-plan` skill to execute the fix plan step by step
  3. After execution completes successfully, use the `maintain-doc` skill if the bug fix affects documented behavior
</rule>

<rule> **For refactoring requests** (code cleanup, architecture improvements, technical debt, structural changes, code quality enhancements, extracting logic, improving maintainability):
  1. Use the `plan-development-task` skill to analyze needs and generate a TDD-based refactoring plan
  2. Use the `execute-plan` skill to execute the refactor plan step by step
  3. After execution completes successfully, use the `maintain-doc` skill if structure, APIs, or workflows changed
</rule>

<rule> **For code issue fixes** (lint errors, type errors, formatting issues, code quality violations):
  1. Treat as refactoring: use the `plan-development-task` skill to create a plan
  2. Use the `execute-plan` skill to execute the plan step by step
  3. Documentation updates typically not needed unless APIs or behavior changed
</rule>

<rule> **Default behavior**: If the request doesn't clearly fit a category, treat it as a new feature request and use the `plan-development-task` → `execute-plan` → `maintain-doc` workflow. </rule>

<rule> **Skill execution order**: Always follow the pattern: plan-development-task → execute-plan → maintain-doc (when applicable). Never skip the planning step. </rule>

<rule> **Documentation updates**: Only invoke `maintain-doc` after successful plan execution when changes affect:
  - Public APIs or interfaces
  - User-facing behavior or workflows
  - Project structure or file organization
  - Setup, build, or deployment procedures
  - Configuration requirements
</rule>

<rule> **Always prioritize using predefined skills**: When a user request matches any skill's purpose, invoke the appropriate skill rather than implementing directly. Skills provide structured, consistent approaches to common tasks. </rule>

</rules>