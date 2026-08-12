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
- User wants a POC to prove which option of an ADR is better — a standalone feature (not a snippet) that demonstrates one option
- User describes desired functionality that does not currently exist in the codebase
- User asks an exploratory question about whether a feature is possible (e.g., "is it possible to...", "can we add...", "would it be feasible to...")
- User requests refactoring of existing code or functionality
- User asks for code cleanup, restructuring, or quality improvements
- User wants to reduce technical debt or improve code organization
- User requests improvements to maintainability, readability, or performance without changing behavior
- User wants to append rework steps to an already-implemented feature plan — a focused rework triggered by orchestrate-feature-delivery's handle-post-implementation-issue flow

**Differentiation rules** (when multiple skills could apply):
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
| "poc", "proof of concept", "prove which option", "compare approaches", "validate option" | **POC** | An uncertain ADR option needs evidence — build a standalone feature that demonstrates it (see **poc-plan**) |

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
<poc-plan>
A POC plan (from **orchestrate-feature-delivery**'s **poc-definition**) builds a **standalone feature** — a full, coherent slice demonstrating one ADR option, never a snippet. It carries `type: poc`, the option's **success criteria** (measurable evidence for the decision gate), and a final **evaluation step** that collects that evidence. The **Scope Boundary** covers the option's target area; other options and ADRs stay **Out of scope**.
</poc-plan>

<rework-plan-convention>
When the plan is a **rework append** for an already-implemented feature (triggered by **orchestrate-feature-delivery**'s **handle-post-implementation-issue**), the feature folder already exists with an implemented `plan.md`:
- **Append, never rewrite**: write a `## Rework <date>` section at the end of the existing `plan.md`; implemented steps stay byte-for-byte unchanged.
- New steps are numbered within the rework section, reference the triggering issue and the reworked ADR decision, and follow the classified change type (usually a bug-fix/feature plan).
- The rework section carries its own **Scope Boundary** (see **scope-boundary**): it inherits the original **In scope** and tightens it to the governing ADR decision.
- Before appending, check the rework request against the original boundary: if it would change something in the original **Out of scope** or reopen another ADR, refuse and ask the user — this may be a new feature cell rather than a rework append.
- **Prepare Environment** (see **plan-prerequisites**) still applies — the rework runs on its own branch per the repo's branch convention (the original branch/PR may already be merged).
- If the plan is very long, use a sibling `rework-plan.md` and record it in the delivery index.
</rework-plan-convention>

<concise-writing>
All prose in plans and context files follows **reference/writing-style.md** — BLUF takeaways, hard caps (step objective 1 sentence, bullet 1 claim, paragraph ≤ 3 sentences, sentence ≤ 20 words), atomic bullets, no banned phrases, So-what test.
</concise-writing>

<context-loading-guide>
Load only the examples directly relevant to the current change type to minimize context size.

**Bug fix examples** — cover the full workflow: classify → define-scope → plan-bug-fix.

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
| Planning a POC (standalone feature proving one ADR option) | POC plan steps, success criteria, evaluation step | [reference/plan-poc.md](reference/plan-poc.md) |
| Full POC plan walkthrough | plan-poc end-to-end output | [examples/plan-adr-option-poc.md](examples/plan-adr-option-poc.md) |
| POC round from dispatch to decision gate (shared with the orchestrator) | End-to-end POC walkthrough | [../orchestrate-feature-delivery/examples/adr-option-poc.md](../orchestrate-feature-delivery/examples/adr-option-poc.md) |
| Writing or reviewing plan.md / context.md prose | BLUF rules, sentence/paragraph caps, banned-phrase list, atomic bullets | [reference/writing-style.md](reference/writing-style.md) |
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
2. **Bug fix**: analyze for root-cause patterns and test hypotheses through code inspection, debugging, or logging. **Feature / refactor**: identify and clarify ambiguous terms and implicit assumptions.
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
1. Load the ADR and the option's **tech details** (from **draft-adr**'s **detail-options-tech** — target-state diagrams + code change profile); for an **orchestrate-feature-delivery** cell use the agent brief's spike references.
2. Clarify with the user: which option, the **success criteria** (measurable — latency, complexity, migration cost), and the standalone feature slice that demonstrates it end-to-end.
3. Apply **define-scope-boundary** — the option's target area is **In scope**; other options and ADRs are **Out of scope**.
4. Produce a feature plan per **reference/plan-poc.md** — build the full slice TDD-style, then a final **evaluation step** that measures/collects evidence against each success criterion.
5. Mark the plan `type: poc`; record success criteria + evaluation method in `context.md` via **export-plan**.
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
2. If the user agrees, determine the storage location: for an **orchestrate-feature-delivery** cell use the epic's delivery folder `deliveries/<epic-name>/{repo}/{feature-name}/` (created by the orchestrator); otherwise ask the user or default to `docs/feature-implementations/`.
3. Derive a short kebab-case feature name from the plan's objective (e.g., `fix-null-pointer-in-transformer`).
4. Determine the repo name when the plan belongs to a specific repo (an **orchestrate-feature-delivery** cell); use the **repo-first** layout `{location}/{repo}/{feature-name}/` — the delivery folder already exists, write into it; fall back to `{location}/{feature-name}/` when no repo applies so all plans for one repo live together.
5. Write `plan.md` — start with the ratified `## Scope Boundary` block (see **scope-boundary**), then the complete numbered step list with objectives. When appending a rework plan (per **rework-plan-convention**), append a `## Rework <date>` section (with its own boundary) to the existing `plan.md` instead of overwriting it.
6. Write `context.md` — capture all background: the user's original request, the classified change type, root cause or requirement summary, TDD approach rationale, the scope boundary rationale (see **scope-boundary**), the target branch name and base branch (see **plan-prerequisites**), constraints, assumptions, and any codebase references gathered. For an **orchestrate-feature-delivery** cell, also record the spike references from the agent brief (change-summary items, ADR files, solution-doc sections) so execution/resume agents can load full context on demand.
7. Validate conciseness (see **concise-writing**): each step states one objective in one sentence, scope-boundary bullets are one claim each, context.md prose ≤3 sentences per paragraph, no banned phrases.
8. Inform the user of the saved location so they can invoke **execute-plan** to carry it out.
</export-plan>

</capabilities>

<rules>

<rule> When the user makes a request about code changes, first apply **classify-change-type** to determine whether it is a bug fix, feature, or refactor. </rule>
<rule> If the classified type is **Bug Fix**: apply **define-scope** to identify the root cause, then apply **plan-bug-fix** to generate the fix plan. </rule>
<rule> If the classified type is **Feature**: apply **define-scope** to clarify the requirement, then apply **plan-feature-implementation** to generate the implementation plan. </rule>
<rule> If the classified type is **Refactor**: apply **define-scope** to clarify the scope and constraints, then apply **plan-refactor** to generate the refactoring plan. </rule>
<rule> If the classified type is **POC**: apply **plan-poc** to generate the proof-of-concept plan. </rule>
<rule> When both restructuring and new behavior are needed: apply **plan-refactor** first to stabilize the structure, then apply **plan-feature-implementation** for the new behavior. </rule>
<rule> After the plan is confirmed by the user: optionally apply **export-plan** to persist the plan to files for later execution by execute-plan. </rule>
<rule> When generating any plan (bug fix, feature, or refactor): always include the **Prepare Environment** prerequisites step first per **plan-prerequisites**; if any check is not ready, raise it to the user instead of starting execution. </rule>
<rule> When generating any plan: apply **define-scope-boundary** and include the ratified boundary as a `## Scope Boundary` block so the executor can check against it. </rule>
<rule> When appending a rework plan to an already-implemented feature (triggered by **orchestrate-feature-delivery**), apply **rework-plan-convention** and **export-plan** in append mode — never overwrite the implemented steps. </rule>
<rule> When appending a rework: check the rework request against the original boundary (see **rework-plan-convention**); if it exceeds it, refuse and ask the user — never append silently. </rule>

</rules>
