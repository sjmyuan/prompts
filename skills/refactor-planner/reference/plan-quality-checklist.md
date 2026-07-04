# Plan Quality Checklist

Before presenting a refactor plan to the user, verify all items below.

## Coverage
- [ ] Every identified refactor objective has a corresponding TDD cycle in the plan
- [ ] All constraints from the refactor request are addressed
- [ ] Existing observable behavior is preserved — no new functionality is introduced

## Sequencing
- [ ] Dependency ordering is correct — no step depends on a later step
- [ ] Validate Baseline is always Step 1
- [ ] Validate Linting, Formatting and Type Checking is the final step for each objective group

## Step Management
- [ ] Total step count ≤ 20
- [ ] Related objectives are consolidated where they share context or can be tested together
- [ ] Each step has a clear, single objective

## TDD Fidelity
- [ ] TDD variant (full cycle vs. streamlined) is documented per objective with rationale
- [ ] Complex logic changes always use full TDD cycle
- [ ] Simple cleanups (formatting, unused imports) may skip test creation with documented justification
- [ ] Code organization moves (file renames, package restructures) verify existing tests pass unchanged

## Clarity
- [ ] Each step description is actionable and unambiguous
- [ ] File paths and class names are specified where known
- [ ] Validation criteria are explicit (e.g., "all existing tests still pass", "no new lint errors")
