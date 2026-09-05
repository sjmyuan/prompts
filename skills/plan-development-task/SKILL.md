---
name: plan-development-task
description: Classify, clarify, and generate TDD-based step-by-step plans for bug fixes, features, refactors, or POCs. Use when fixing bugs, adding features, refactoring, exploring feasibility, planning a POC, or reworking.
---

<when-to-use-this-skill>
- User reports a bug, defect, or unexpected behavior in existing code
- User describes a regression or something that worked before but no longer does
- User reports failing tests or incorrect outputs in existing functionality
- User asks to investigate and fix a problem in existing code
- User submits a requirement to add new functionality or features
- User asks to implement a new feature, enhancement, or behavior
- User wants a POC to prove which option of an ADR is better — a standalone feature (not a snippet) that demonstrates one option
- User describes desired functionality that does not currently exist in the codebase
- User asks an exploratory question about whether a feature is possible (e.g., "is it possible to...", "can we add...", "would it be feasible to...")
- User requests refactoring of existing code or functionality
- User asks for code cleanup, restructuring, or quality improvements
- User wants to reduce technical debt or improve code organization
- User requests improvements to maintainability, readability, or performance without changing behavior
- User wants to plan rework for an already-implemented feature — write a sibling `rework-<date>.md`, a focused rework triggered by orchestrate-feature-delivery's handle-post-implementation-issue flow

**Differentiation rules** (when multiple skills could apply):
- **Multi-feature / multi-repo decomposition?** → Do NOT plan the whole breakdown here — apply **orchestrate-feature-delivery** first, then plan each feature × repo cell with this skill
- **Rework for an already-delivered feature?** → Apply this skill per **rework-plan-convention** — write a sibling `rework-<date>.md`; orchestrate-feature-delivery triggers it; never rewrite the implemented plan
</when-to-use-this-skill>

<knowledge>

<change-type-classification>
Classify the user's request into one of three types:

| Signal | Type | Reasoning |
|---|---|---|
| "bug", "broken", "error", "exception", "not working", "incorrect", "wrong output", "failing", "regression" | **Bug Fix** | Something is producing incorrect or unexpected results |
| "new", "add", "implement", "create", "support", "enhance", "extend", "feature", "capability" | **Feature** | New observable behavior is being introduced |
| "refactor", "clean up", "restructure", "extract", "organize", "improve quality", "reduce debt", "split", "consolidate" | **Refactor** | Internal structure changes without behavior change |
| "poc", "proof of concept", "prove which option", "compare approaches", "validate option" | **POC** | An uncertain ADR option needs evidence — build a standalone feature that demonstrates it (see **poc-plan-definition**) |

When unsure, ask the user: "Is the goal to fix something that's broken (bug), add new behavior (feature), or restructure without changing behavior (refactor)?"
</change-type-classification>

<tdd-approach-selection>
TDD variant is selected by change type and sub-type — table in **[reference/tdd-approach-selection.md](reference/tdd-approach-selection.md)**. The plan documents the chosen variant with rationale.
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

The boundary derives from the classified change type, the confirmed scope, and (for orchestrator cells) the governing ADR decision. The user ratifies it before **export-plan** persists it. Rework files inherit the original boundary and tighten it to the governing ADR.
</scope-boundary>
<poc-plan-definition>
A POC plan (from **orchestrate-feature-delivery**'s **poc-definition**) is a **standalone feature** proving one ADR option, never a snippet:

| Property | Content |
|---|---|
| `type` | `poc` |
| **Success criteria** | Measurable evidence for the decision gate |
| **Evaluation step** | Final step that collects that evidence |
| **Scope Boundary** | Option's target area **In scope**; other options and ADRs **Out of scope** |
</poc-plan-definition>

<rework-plan-convention>
A rework (triggered by **orchestrate-feature-delivery**'s **handle-post-implementation-issue**) is written as a new sibling file `rework-<date>.md` in the feature folder — `plan.md` is the frozen original and is never modified:
- Each file opens with `# Rework <date>` + one-line trigger, then its own **Scope Boundary** and numbered steps
- Inherits and tightens the original **Scope Boundary** to the governing ADR decision
- Refuses and asks the user if it would change the original **Out of scope** or reopen another ADR (likely a new feature cell)
- Runs on its own branch (see **plan-prerequisites**)
- Registers a row in the feature's `## Reworks` manifest in `context.md` (date, mode, cell, trigger, file, status) so resume finds the active file

Worked example: [examples/rework-scope-boundary.md](examples/rework-scope-boundary.md).
</rework-plan-convention>

<concise-writing>
All `plan.md` / `context.md` prose follows **reference/writing-style.md** — BLUF takeaways, hard caps (1 sentence per step objective / bullet / ≤20-word sentence), atomic bullets, no banned phrases. Plan files are table-first; context files are takeaway-first.
</concise-writing>

<context-loading-guide>
Load only the examples directly relevant to the current change type to minimize context size.

| Load when | Provides | File |
|---|---|---|
| Selecting TDD variant per sub-type | 15-row TDD approach selection table | [reference/tdd-approach-selection.md](reference/tdd-approach-selection.md) |
| Generating bug fix plan | Detailed steps for plan-bug-fix | [reference/plan-bug-fix.md](reference/plan-bug-fix.md) |
| Generating feature implementation plan | Detailed steps for plan-feature-implementation | [reference/plan-feature-implementation.md](reference/plan-feature-implementation.md) |
| Generating refactor plan | Detailed steps for plan-refactor | [reference/plan-refactor.md](reference/plan-refactor.md) |
| Validating plan quality | Checklist: coverage, sequencing, steps, TDD, clarity | [reference/plan-quality-checklist.md](reference/plan-quality-checklist.md) |
| Writing a rework plan (`rework-<date>.md`) for an implemented feature | Sibling rework file + manifest (shared with the orchestrator) | [../orchestrate-feature-delivery/examples/post-implementation-rework.md](../orchestrate-feature-delivery/examples/post-implementation-rework.md) |
| Rework that risks exceeding the feature's scope boundary | Boundary definition + refusal with decision options | [examples/rework-scope-boundary.md](examples/rework-scope-boundary.md) |
| Bug: simple logic / timing errors | Full workflow example | [examples/bug-fix-simple-logic.md](examples/bug-fix-simple-logic.md) |
| Bug: slow responses, N+1 queries | Full workflow example | [examples/bug-fix-performance.md](examples/bug-fix-performance.md) |
| Feature: complex algorithms or business rules | Full workflow example | [examples/feature-complex-transformation.md](examples/feature-complex-transformation.md) |
| Feature: simple config properties or flags | Full workflow example | [examples/feature-simple-configuration.md](examples/feature-simple-configuration.md) |
| Refactor: splitting large classes (SRP) | Full workflow example | [examples/refactor-service-splitting.md](examples/refactor-service-splitting.md) |
| Refactor: interface extraction for testability | Full workflow example | [examples/refactor-interface-implementation.md](examples/refactor-interface-implementation.md) |
| Planning a POC (standalone feature proving one ADR option) | POC plan steps, success criteria, evaluation step | [reference/plan-poc.md](reference/plan-poc.md) |
| Full POC plan walkthrough | plan-poc end-to-end output | [examples/plan-adr-option-poc.md](examples/plan-adr-option-poc.md) |
| POC round from dispatch to decision gate (shared with the orchestrator) | End-to-end POC walkthrough | [../orchestrate-feature-delivery/examples/adr-option-poc.md](../orchestrate-feature-delivery/examples/adr-option-poc.md) |
| Persisting a confirmed plan to `plan.md` + `context.md` | plan.md + context.md layout for **export-plan** | [examples/export-plan.md](examples/export-plan.md) |
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
   - **Bug Fix** → apply **define-scope**, then **plan-bug-fix**
   - **Feature** → apply **define-scope**, then **plan-feature-implementation**
   - **Refactor** → apply **define-scope**, then **plan-refactor**
   - **POC** → apply **plan-poc**
</classify-change-type>

<define-scope>
1. Gather relevant information from the codebase, knowledge base, test results, and user input to define the scope for the classified change type.
2. **Bug fix**: analyze root-cause patterns and test hypotheses through code inspection, debugging, or logging.
   **Feature / refactor**: identify and clarify ambiguous terms and implicit assumptions.
3. Ask the user targeted questions until the scope is well-defined — root cause confirmed for bugs; requirement or constraints confirmed for features/refactors.
4. Present the result (root cause + reasoning, or a structured scope summary) and request confirmation or refinements.
5. Hand the confirmed scope to the corresponding plan capability and **define-scope-boundary**.
</define-scope>

<plan-bug-fix>
Load **[reference/plan-bug-fix.md](reference/plan-bug-fix.md)** and follow its steps.
</plan-bug-fix>

<plan-feature-implementation>
Load **[reference/plan-feature-implementation.md](reference/plan-feature-implementation.md)** and follow its steps.
</plan-feature-implementation>

<plan-refactor>
Load **[reference/plan-refactor.md](reference/plan-refactor.md)** and follow its steps.
</plan-refactor>
<plan-poc>
Load **[reference/plan-poc.md](reference/plan-poc.md)** and follow its steps.
</plan-poc>

<define-scope-boundary>
1. Derive the boundary from the classified change type, the confirmed scope, and (for **orchestrate-feature-delivery** cells) the governing ADR decision.
2. List **In scope**: the files/areas, behaviors, and ADR decisions the plan may change.
3. List **Out of scope**: non-goals — other behaviors, other ADRs, other modules, unrelated cleanup.
4. Present both lists to the user and request ratification or adjustment.
5. Hand the ratified boundary to the plan for inclusion as a `## Scope Boundary` block and to **export-plan** for persistence.
</define-scope-boundary>

<export-plan>
1. After the user confirms the plan, ask whether they would like to persist it to a feature folder for later execution by **execute-plan**.
2. Determine the storage location: for an **orchestrate-feature-delivery** cell use `deliveries/<epic-name>/{repo}/{feature-name}/`; otherwise resolve the artifact base via `resolve-artifact-location` and use `{base}/feature-implementations/` (no silent default).
3. Derive a short kebab-case feature name from the plan's objective (e.g., `fix-null-pointer-in-transformer`).
4. Use the **repo-first** layout `{location}/{repo}/{feature-name}/` when a repo applies (the delivery folder already exists); else `{location}/{feature-name}/`.
5. Write `plan.md` + `context.md` per **[reference/plan-file-format.md](reference/plan-file-format.md)**.
6. Validate conciseness (see **concise-writing**): one objective per step sentence, one claim per scope-boundary bullet, context.md prose ≤3 sentences per paragraph, no banned phrases.
7. Inform the user of the saved location so they can invoke **execute-plan** to carry it out.
</export-plan>

</capabilities>

<rules>

<rule> When the user makes a request about code changes, first apply **classify-change-type** to determine whether it is a bug fix, feature, refactor, or POC. </rule>
<rule> If the classified type is **Bug Fix**: apply **define-scope**, then **plan-bug-fix**. </rule>
<rule> If the classified type is **Feature**: apply **define-scope**, then **plan-feature-implementation**. </rule>
<rule> If the classified type is **Refactor**: apply **define-scope**, then **plan-refactor**. </rule>
<rule> If the classified type is **POC**: apply **plan-poc**. </rule>
<rule> When both restructuring and new behavior are needed: apply **plan-refactor** first, then **plan-feature-implementation**. </rule>
<rule> After the plan is confirmed: optionally apply **export-plan** to persist it for execution by **execute-plan**. </rule>
<rule> When generating any plan, apply **plan-prerequisites** and **define-scope-boundary**. </rule>
<rule> When planning a rework for an implemented feature, apply **rework-plan-convention** and **export-plan** to write a sibling `rework-<date>.md` — never overwrite implemented steps. </rule>
<rule> When a rework would exceed the original boundary, refuse and ask the user — never write silently. </rule>

</rules>
