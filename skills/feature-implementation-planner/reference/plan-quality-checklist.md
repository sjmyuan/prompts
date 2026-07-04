# Plan Quality Checklist

Before presenting an implementation plan to the user, verify all items below.

## Coverage
- [ ] Every identified functionality has a corresponding TDD cycle in the plan
- [ ] All acceptance criteria from the requirement are addressed
- [ ] Edge cases and error scenarios are covered in the test steps

## Sequencing
- [ ] Dependency ordering is correct — no step depends on a later step
- [ ] Validate Baseline is always Step 1
- [ ] Validate Linting, Formatting and Type Checking is the final step for each functionality group

## Step Management
- [ ] Total step count ≤ 25
- [ ] Related functionalities are consolidated where they share context or can be tested together
- [ ] Each step has a clear, single objective

## TDD Fidelity
- [ ] TDD variant (full cycle vs. streamlined) is documented per functionality with rationale
- [ ] Complex business logic always uses full TDD cycle
- [ ] Configuration-only changes may use streamlined approach with documented justification

## Clarity
- [ ] Each step description is actionable and unambiguous
- [ ] File paths and class names are specified where known
- [ ] Validation criteria are explicit (e.g., "all tests pass", "no lint errors")
