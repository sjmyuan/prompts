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

<rule> Identify whether the user input is a requirement, refactor request, code review, code issue fix, lint issue fix, type issue fix, code improvement or bug report, then invoke the appropriate skills. </rule>

<rule> By default, first use the `feature-implementation-planner` skill to create a plan, then use the `plan-executor` skill to implement it step by step. </rule>

<rule> For refactor requests,  or code improvement, first use the `refactor-planner` skill to create a plan, then use the `plan-executor` skill to implement it step by step. </rule>

<rule> For code review requests, use the `code-reviewer` skill to review the code and suggest improvements. </rule>

<rule> For bug reports, code issue fix, lint issue fix, or type issue fix, first use the `bug-fix-planner` skill to create a plan, then use the `plan-executor` skill to implement it step by step. </rule>

<rule> For any question, use the `reverse-engineer` skill to answer the question. </rule>

<rule> After completing the plan, use the `doc-maintainer` skill to generate or update documentation based on the code and context. </rule>

<rule> **INVOKE PREDEFINED SKILLS WHENEVER YOU CAN** </rule>
</rules>