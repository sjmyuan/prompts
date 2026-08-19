# Example: Rework That Risks Exceeding the Feature Scope

**Scenario**: A rework is requested for a delivered feature, but the rework would change code listed in the original plan's **Out of scope**. Demonstrates **define-scope-boundary** and the rework guard — refuse and ask, never write silently.

**Applies**: **define-scope-boundary**, **rework-plan-convention**

## User Request

"We found a defect in the delivered checkout rework: on partial payment failure the compensating rollback retries with wrong credentials. Investigate and fix it."

## Boundary Check

Original boundary (from the existing `plan.md`):

```
## Scope Boundary
**In scope**: wallet-service `application/` + `test/`; `adr-wallet-01-payment-failure-handling.md` payment-failure decision
**Out of scope**: `payment-gateway/` client code; `adr-cutover-01-service-cutover.md` cutover; other modules
```

The rework request requires changing `payment-gateway/` credential retry logic — **Out of scope**.

## Refusal + Decision Options

The rework exceeds the original boundary, so the planner refuses to write silently and presents options:

> "This rework requires changing `payment-gateway/` credential retry logic, which is **Out of scope** (original boundary). Options: (a) extend the boundary to include `payment-gateway/` credential handling, (b) keep it out and file a follow-up feature, (c) treat it as a new feature cell `F2-r2` instead of a rework."

**User decision**: (a) extend the boundary for this rework only.

## Rework File (Boundary Updated)

The rework is written as a new sibling `rework-2026-08-10.md`; the original `plan.md` is never modified. It inherits the original boundary, tightened and extended per the user decision:

```markdown
# Rework 2026-08-10 — compensating rollback credential retry
Mode: post-merge   ·   Cell: order-service/F2-r1   ·   ADR focus: adr-wallet-01-payment-failure-handling.md

## Scope Boundary
**In scope**: original **In scope** + `payment-gateway/` credential retry (user-approved extension)
**Out of scope**: original **Out of scope** otherwise unchanged
**Rule**: no step or fix may change code beyond **In scope**; refuse and ask if it does
**Minor exceptions**: doc/comment-only edits; test-only changes for this plan's own tests

## Steps
- [ ] Fix credential retry selection in compensating rollback
- [ ] Update payment-gateway client tests for partial failures
- [ ] Validate linting, formatting, type checking
```

`context.md` gains a `## Reworks` manifest row for this file. Original `plan.md` steps 1–N remain byte-for-byte unchanged.
