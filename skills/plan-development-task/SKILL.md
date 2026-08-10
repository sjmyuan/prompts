---
name: plan-development-task
description: Classify, clarify, and generate TDD-based step-by-step plans for bug fixes, features, and refactors. Use when planning / investigating / designing changes or appending rework for bugs, regressions, new features, enhancements, refactoring, or technical debt.
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
- User wants to append rework steps to an already-implemented feature plan — a focused rework triggered by orchestrate-feature-delivery's handle-post-implementation-issue flow

**Differentiation rules** (when multiple skills could apply):
- **New behavior being introduced?** → This is a **feature** — apply **plan-feature-implementation**
- **No new behavior, just restructuring?** → This is a **refactor** — apply **plan-refactor**
- **Something is broken?** → This is a **bug fix** — apply **plan-bug-fix**
- **Both restructure AND add new behavior?** → Apply **plan-refactor** first to stabilize, then **plan-feature-implementation** for the new behavior
- **Multi-feature / multi-repo decomposition of spike results?** → Do NOT plan a whole breakdown here — apply **orchestrate-feature-delivery** first to split, sequence, and orchestrate features, then plan each feature × repo cell with this skill
- **Rework append for an already-delivered feature?** → Apply this skill in append mode per **rework-plan-convention** — orchestrate-feature-delivery triggers it; never rewrite the implemented plan
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

<plan-prerequisites>
Every plan starts with a **Prepare Environment** step (Step 1) that covers:

| Check | Not ready → |
|---|---|
| Feature branch exists, based on the correct base branch, named per the **repo's branch convention** (detect from existing branches / git config / team docs, or ask the user — never assume a prefix) | Ask the user for the branch name and base; create the branch as part of Step 1 |
| Working tree is clean (no unrelated uncommitted changes) | Stop and raise to the user before proceeding |
| Dependencies and toolchain installed | Stop and raise to the user (request install or confirmation) |
| Baseline tests / lint / type-check pass | Stop and raise to the user (decide: fix baseline first or proceed) |

If any check is not ready, the agent must **stop and raise it to the user** — never start execution silently. The branch name and base are recorded so **export-plan** can persist them to `context.md`.
</plan-prerequisites>

<scope-boundary>
Every plan carries an explicit **Scope Boundary** that the executor checks during execution:

| Field | Content |
|---|---|
| **In scope** | Files/areas, behaviors, and (for **orchestrate-feature-delivery** cells) ADR decisions the plan may change |
| **Out of scope** | Files/areas, behaviors, and ADR decisions that must NOT change — the plan's non-goals |
| **Rule** | No step, error-recovery fix, or review fix may require changes beyond **In scope**. If one does, the executor refuses and asks the user — never adapts silently |
| **Minor exceptions** | Proceed without asking: doc/comment-only edits; changes confined to files already in **In scope**; test-only changes for this plan's own tests |

Derive the boundary from the classified change type, the confirmed scope, and (for orchestrator cells) the governing ADR decision. Present it to the user for ratification during plan confirmation, then persist it via **export-plan**. Rework sections inherit the original boundary and tighten it to the governing ADR.
</scope-boundary>

<rework-plan-convention>
When the plan is a **rework append** for an already-implemented feature (triggered by **orchestrate-feature-delivery**'s **handle-post-implementation-issue**), the feature folder already exists with an implemented `plan.md`:
- **Append, never rewrite**: write a `## Rework <date>` section at the end of the existing `plan.md`; implemented steps stay byte-for-byte unchanged.
- New steps are numbered within the rework section, reference the triggering issue and the reworked ADR decision, and follow the classified change type (usually a bug-fix/feature plan).
- The rework section carries its own **Scope Boundary** (see **scope-boundary**): it inherits the original **In scope** and tightens it to the governing ADR decision.
- Before appending, check the rework request against the original boundary: if it would change something in the original **Out of scope** or reopen another ADR, refuse and ask the user — this may be a new feature cell rather than a rework append.
- **Prepare Environment** (see **plan-prerequisites**) still applies — the rework runs on its own branch per the repo's branch convention (the original branch/PR may already be merged).
- If the plan is very long, use a sibling `rework-plan.md` and record it in the delivery index.
</rework-plan-convention>

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
| Appending a rework plan to an implemented feature plan | Append-only rework section (shared with the orchestrator) | [../orchestrate-feature-delivery/examples/post-implementation-rework.md](../orchestrate-feature-delivery/examples/post-implementation-rework.md) |
| Rework append that risks exceeding the feature's scope boundary | Boundary definition + refusal with decision options | [examples/rework-scope-boundary.md](examples/rework-scope-boundary.md) |
| Bug: simple logic / timing errors | Full workflow example | [examples/bug-fix-simple-logic.md](examples/bug-fix-simple-logic.md) |
| Bug: slow responses, N+1 queries | Full workflow example | [examples/bug-fix-performance.md](examples/bug-fix-performance.md) |
| Feature: complex algorithms or business rules | Full workflow example | [examples/feature-complex-transformation.md](examples/feature-complex-transformation.md) |
| Feature: simple config properties or flags | Full workflow example | [examples/feature-simple-configuration.md](examples/feature-simple-configuration.md) |
| Refactor: splitting large classes (SRP) | Full workflow example | [examples/refactor-service-splitting.md](examples/refactor-service-splitting.md) |
| Refactor: interface extraction for testability | Full workflow example | [examples/refactor-interface-implementation.md](examples/refactor-interface-implementation.md) |
</context-loading-guide>

<skill-boundary>
This skill produces a **plan** but does not execute changes. After the plan is confirmed, use **export-plan** to persist it to a feature folder, then pair with **execute-plan** for implementation.
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

<define-scope-boundary>
1. Derive the boundary from the classified change type, the confirmed scope, and (for **orchestrate-feature-delivery** cells) the governing ADR decision.
2. List **In scope**: the files/areas, behaviors, and ADR decisions the plan may change.
3. List **Out of scope**: non-goals — other behaviors, other ADRs, other modules, unrelated cleanup.
4. Present both lists to the user and request ratification or adjustment.
5. Hand the ratified boundary to the plan for inclusion as a `## Scope Boundary` block and to **export-plan** for persistence.
</define-scope-boundary>

<export-plan>
1. After the user confirms the plan, ask whether they would like to persist it to a feature folder for later execution by **execute-plan**.
2. If the user agrees, determine the storage location: for an **orchestrate-feature-delivery** cell use the epic's delivery folder `deliveries/<epic-name>/{repo}/{feature-name}/` (created by the orchestrator); otherwise ask the user or default to `docs/feature-implementations/`.
3. Derive a short kebab-case feature name from the plan's objective (e.g., `fix-null-pointer-in-transformer`).
4. Determine the repo name when the plan belongs to a specific repo (an **orchestrate-feature-delivery** cell); use the **repo-first** layout `{location}/{repo}/{feature-name}/` — the delivery folder already exists, write into it; fall back to `{location}/{feature-name}/` when no repo applies so all plans for one repo live together.
5. Write `plan.md` — start with the ratified `## Scope Boundary` block (see **scope-boundary**), then the complete numbered step list with objectives. When appending a rework plan (per **rework-plan-convention**), append a `## Rework <date>` section (with its own boundary) to the existing `plan.md` instead of overwriting it.
6. Write `context.md` — capture all background: the user's original request, the classified change type, root cause or requirement summary, TDD approach rationale, the scope boundary rationale (see **scope-boundary**), the target branch name and base branch (see **plan-prerequisites**), constraints, assumptions, and any codebase references gathered. For an **orchestrate-feature-delivery** cell, also record the spike references from the agent brief (change-summary items, ADR files, solution-doc sections) so execution/resume agents can load full context on demand.
7. Inform the user of the saved location so they can invoke **execute-plan** to carry it out.
</export-plan>

</capabilities>

<rules>

<rule> When the user makes a request about code changes, first apply **classify-change-type** to determine whether it is a bug fix, feature, or refactor. </rule>
<rule> If the classified type is **Bug Fix**: apply **define-bug-scope** to identify the root cause, then apply **plan-bug-fix** to generate the fix plan. </rule>
<rule> If the classified type is **Feature**: apply **define-feature-scope** to clarify the requirement, then apply **plan-feature-implementation** to generate the implementation plan. </rule>
<rule> If the classified type is **Refactor**: apply **define-refactor-scope** to clarify the scope and constraints, then apply **plan-refactor** to generate the refactoring plan. </rule>
<rule> When both restructuring and new behavior are needed: apply **plan-refactor** first to stabilize the structure, then apply **plan-feature-implementation** for the new behavior. </rule>
<rule> After the plan is confirmed by the user: optionally apply **export-plan** to persist the plan to files for later execution by execute-plan. </rule>
<rule> When generating any plan (bug fix, feature, or refactor): always include the **Prepare Environment** prerequisites step first per **plan-prerequisites**; if any check is not ready, raise it to the user instead of starting execution. </rule>
<rule> When generating any plan: apply **define-scope-boundary** and include the ratified boundary as a `## Scope Boundary` block so the executor can check against it. </rule>
<rule> When appending a rework plan to an already-implemented feature (triggered by **orchestrate-feature-delivery**), apply **rework-plan-convention** and **export-plan** in append mode — never overwrite the implemented steps. </rule>
<rule> When appending a rework: check the rework request against the original boundary (see **rework-plan-convention**); if it exceeds it, refuse and ask the user — never append silently. </rule>

</rules>
