---
name: plan-development-task
description: Classify, clarify, and generate detailed step-by-step TDD-based plans for bug fixes, feature implementations, and refactors. Use when planning / investigating / designing changes for bugs, regressions, failing tests, new features, enhancements, refactoring, code cleanup, or technical debt.
---

<when-to-use-this-skill>
- User reports a bug, defect, or unexpected behavior in existing code
- User describes a regression or something that worked before but no longer does
- User reports failing tests or incorrect outputs in existing functionality
- User asks to investigate and fix a problem in existing code
- User submits a requirement to add new functionality or features
- User asks to implement a new feature, enhancement, or behavior
- User describes desired functionality that does not currently exist in the codebase
- User asks an exploratory question about whether a feature is possible (e.g., "is it possible to...", "can we add...", "would it be feasible to...")
- User requests refactoring of existing code or functionality
- User asks for code cleanup, restructuring, or quality improvements
- User wants to reduce technical debt or improve code organization
- User requests improvements to maintainability, readability, or performance without changing behavior

**Differentiation rules** (when multiple skills could apply):
- **New behavior being introduced?** → This is a **feature** (plan-feature-implementation)
- **No new behavior, just restructuring?** → This is a **refactor** (plan-refactor)
- **Something is broken?** → This is a **bug fix** (plan-bug-fix)
- **Both restructure AND add new behavior?** → Use plan-refactor first to stabilize, then plan-feature-implementation for the new behavior
</when-to-use-this-skill>

<knowledge>

<change-type-classification>
Classify the user's request into one of three types:

| Signal | Type | Reasoning |
|---|---|---|
| "bug", "broken", "error", "exception", "not working", "incorrect", "wrong output", "failing", "regression" | **Bug Fix** | Something is producing incorrect or unexpected results |
| "new", "add", "implement", "create", "support", "enhance", "extend", "feature", "capability" | **Feature** | New observable behavior is being introduced |
| "refactor", "clean up", "restructure", "extract", "organize", "improve quality", "reduce debt", "split", "consolidate" | **Refactor** | Internal structure changes without behavior change |

When unsure, ask the user: "Is the goal to fix something that's broken (bug), add new behavior (feature), or restructure without changing behavior (refactor)?"
</change-type-classification>

<tdd-approach-selection>
Load **[reference/tdd-approach-selection.md](reference/tdd-approach-selection.md)** and select the appropriate TDD variant based on the change type and sub-type. Document the rationale for the chosen variant in the plan.
</tdd-approach-selection>

<context-loading-guide>
Load only the examples directly relevant to the current change type to minimize context size.

**Bug fix examples** — cover the full workflow: classify → define-bug-scope → plan-bug-fix.

| Load when | Provides | File |
|---|---|---|
| Selecting TDD variant per sub-type | 15-row TDD approach selection table | [reference/tdd-approach-selection.md](reference/tdd-approach-selection.md) |
| Generating bug fix plan | Detailed steps for plan-bug-fix | [reference/plan-bug-fix.md](reference/plan-bug-fix.md) |
| Generating feature implementation plan | Detailed steps for plan-feature-implementation | [reference/plan-feature-implementation.md](reference/plan-feature-implementation.md) |
| Generating refactor plan | Detailed steps for plan-refactor | [reference/plan-refactor.md](reference/plan-refactor.md) |
| Validating plan quality | Checklist: coverage, sequencing, steps, TDD, clarity | [reference/plan-quality-checklist.md](reference/plan-quality-checklist.md) |
| Bug: simple logic / timing errors | Full workflow example | [examples/bug-fix-simple-logic.md](examples/bug-fix-simple-logic.md) |
| Bug: slow responses, N+1 queries | Full workflow example | [examples/bug-fix-performance.md](examples/bug-fix-performance.md) |
| Feature: complex algorithms or business rules | Full workflow example | [examples/feature-complex-transformation.md](examples/feature-complex-transformation.md) |
| Feature: simple config properties or flags | Full workflow example | [examples/feature-simple-configuration.md](examples/feature-simple-configuration.md) |
| Refactor: splitting large classes (SRP) | Full workflow example | [examples/refactor-service-splitting.md](examples/refactor-service-splitting.md) |
| Refactor: interface extraction for testability | Full workflow example | [examples/refactor-interface-implementation.md](examples/refactor-interface-implementation.md) |
</context-loading-guide>

<skill-boundary>
This skill produces a **plan** but does not execute changes. Pair with **execute-plan** for implementation.
</skill-boundary>

</knowledge>

<capabilities>

<classify-change-type>
1. Read the user's request and identify keywords and signals that indicate the type of change.
2. Consult **change-type-classification** knowledge to map signals to a change type (bug fix, feature, or refactor).
3. If the type is ambiguous, ask the user targeted clarifying questions to disambiguate.
4. Present the classified type and reasoning to the user.
5. Route to the appropriate pair of capabilities based on the classified type:
   - **Bug Fix** → apply **define-bug-scope**, then **plan-bug-fix**
   - **Feature** → apply **define-feature-scope**, then **plan-feature-implementation**
   - **Refactor** → apply **define-refactor-scope**, then **plan-refactor**
</classify-change-type>

<define-bug-scope>
1. Gather relevant information from the codebase, knowledge base, test results and user input to clearly identify the bug.
2. Analyze the information to identify patterns, inconsistencies, or anomalies that may indicate the root cause of the bug.
3. Formulate hypotheses about potential causes and systematically test them through code inspection, debugging, or additional logging.
4. Ask questions to the user to narrow down the possibilities until the most likely root cause is identified.
5. Present the identified root cause and the reasoning process to the user and request confirmation or refinements.
</define-bug-scope>

<plan-bug-fix>
Load **[reference/plan-bug-fix.md](reference/plan-bug-fix.md)** and follow its steps.
</plan-bug-fix>

<define-feature-scope>
1. Gather relevant information from the codebase, knowledge base, and user input to clearly define the software requirement.
2. Identify and clarify any ambiguous terms or implicit assumptions to ensure proper understanding.
3. Ask questions to the user to refine and narrow down the focus of the software requirement as needed.
4. Present a structured summary of the requirement to the user and request confirmation or refinements.
</define-feature-scope>

<plan-feature-implementation>
Load **[reference/plan-feature-implementation.md](reference/plan-feature-implementation.md)** and follow its steps.
</plan-feature-implementation>

<define-refactor-scope>
1. Gather relevant information from the codebase, knowledge base, and user input to clearly define the refactor request.
2. Identify and clarify any ambiguous terms or implicit assumptions to ensure proper understanding.
3. Ask questions to the user to refine and narrow down the focus of the refactor request as needed.
4. Present a structured summary of the refactor request to the user and request confirmation or refinements.
</define-refactor-scope>

<plan-refactor>
Load **[reference/plan-refactor.md](reference/plan-refactor.md)** and follow its steps.
</plan-refactor>

</capabilities>

<rules>

<rule> When the user makes a request about code changes, first apply **classify-change-type** to determine whether it is a bug fix, feature, or refactor. </rule>
<rule> If the classified type is **Bug Fix**: apply **define-bug-scope** to identify the root cause, then apply **plan-bug-fix** to generate the fix plan. </rule>
<rule> If the classified type is **Feature**: apply **define-feature-scope** to clarify the requirement, then apply **plan-feature-implementation** to generate the implementation plan. </rule>
<rule> If the classified type is **Refactor**: apply **define-refactor-scope** to clarify the scope and constraints, then apply **plan-refactor** to generate the refactoring plan. </rule>
<rule> When both restructuring and new behavior are needed: apply **plan-refactor** first to stabilize the structure, then apply **plan-feature-implementation** for the new behavior. </rule>

</rules>
