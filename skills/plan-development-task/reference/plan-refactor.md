# plan-refactor

1. **Prepare Environment (Prerequisites)**: Apply **plan-prerequisites** from the SKILL.md — ensure the feature branch exists, named per the **repo's branch convention** (detect from existing branches / git config / team docs, or ask the user; never assume a prefix), based on the correct base; the working tree is clean, dependencies and toolchain are installed, and baseline tests, linting, and type-checking pass. If any check is not ready, stop and raise it to the user before continuing.
2. Break down the refactor request into specific, measurable objectives and clearly defined constraints.
3. **Define Scope Boundary**: Apply **define-scope-boundary** — derive the **In scope**/**Out of scope** lists from the refactor scope and the governing ADR (for **orchestrate-feature-delivery** cells); behavior change stays **Out of scope**; present to the user for ratification.
4. Identify and map dependencies between objectives to establish an efficient and logical refactoring sequence.
5. **Consolidate Steps**: Group related objectives together when they share context or can be tested together, reducing the total step count while maintaining clarity. Consolidation strategies: (a) merge coverage-confirmation and refactor steps for simple extractions or renames into a single step, (b) combine Clean Up Unused Code + Clean Up Tests + Verify Cleanup into one cleanup step when changes are small, (c) group Validate Linting, Formatting and Type Checking across multiple objectives into one final quality gate step.
6. Load **reference/tdd-approach-selection.md** to select the appropriate TDD variant for each objective; existing tests stay green throughout. Document the rationale.
7. Create a detailed step-by-step refactor plan (starting with the ratified `## Scope Boundary` block). For each objective, include the following steps:
   1. **Confirm Existing Coverage**: Verify existing tests cover the behavior being restructured; add characterization tests (which pass immediately) only where coverage is missing.
   2. **Refactor in Small Steps**: Apply one structural change at a time without changing behavior.
   3. **Verify Green**: Re-run all tests after each step; any failure means behavior changed — revert it.
   4. **Clean Up Unused Code**: Remove obsolete or redundant code left by the restructure.
   5. **Clean Up Tests**: Update or remove tests made irrelevant by the restructure.
   6. **Verify Cleanup**: Re-run all tests to confirm the cleanup introduced no regressions.
   7. **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
   A refactor never introduces a failing test; a failing test means new behavior — move it to a feature plan.
8. Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
9. **Validate Plan Quality**: Load **reference/plan-quality-checklist.md** and verify — every objective has existing coverage or characterization tests defined, no step introduces a failing test, dependency ordering is correct, step count ≤ 20, and TDD variants are documented. Revise any failing items before presenting to the user.
10. Summarize the complete plan to the user.
