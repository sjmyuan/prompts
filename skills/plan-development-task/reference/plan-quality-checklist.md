# Plan Quality Checklist

Before presenting a development plan to the user, verify all items below.

## Prerequisites
- [ ] Plan starts with a **Prepare Environment** step (branch exists or to be created, clean working tree, dependencies installed, baseline tests/lint/type-check pass)
- [ ] Branch name and base branch are captured (for export-plan persistence)
- [ ] If any prerequisite is not ready, the plan raises it to the user rather than starting execution

## Scope Boundary
- [ ] Plan includes a `## Scope Boundary` block with **In scope** and **Out of scope** lists
- [ ] Boundary derived from the change type and governing ADR (for orchestrator cells) and ratified by the user
- [ ] Rework files (`rework-<date>.md`) carry their own boundary — inherits the original **In scope**, tightened to the governing ADR; `plan.md` untouched

## Coverage
- [ ] Every identified issue/functionality/objective has a corresponding TDD cycle in the plan
- [ ] All acceptance criteria from the user request are addressed
- [ ] Edge cases and error scenarios are covered in the test steps
- [ ] For refactors: existing observable behavior is preserved — no new functionality is introduced

## Sequencing
- [ ] Dependency ordering is correct — no step depends on a later step
- [ ] Prepare Environment is always Step 1
- [ ] Validate Linting, Formatting and Type Checking is the final step for each issue/functionality/objective group

## Step Management
- [ ] For bug fix plans: total step count ≤ 20
- [ ] For feature implementation plans: total step count ≤ 25
- [ ] For refactor plans: total step count ≤ 20
- [ ] Related items are consolidated where they share context or can be tested together
- [ ] Each step has a clear, single objective

## TDD Fidelity
- [ ] TDD variant (full cycle vs. streamlined) is documented per item with rationale
- [ ] Complex logic changes (bug fix, feature, or refactor) always use full TDD cycle
- [ ] Configuration-only changes may use streamlined approach with documented justification
- [ ] Documentation-only changes have no test cycle needed; validate with linting only
- [ ] Performance bugs include benchmarks and query-count assertions
- [ ] Code organization moves (file renames, package restructures) verify existing tests pass unchanged

## Clarity
- [ ] Each step description is actionable and unambiguous
- [ ] File paths and class names are specified where known
- [ ] Validation criteria are explicit (e.g., "all tests pass", "no lint errors", "p99 latency < 500 ms")
- [ ] Prose follows concise writing (see **concise-writing**): one objective per step sentence, one claim per scope-boundary bullet, no banned phrases
