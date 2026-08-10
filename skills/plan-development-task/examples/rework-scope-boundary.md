# Example: Rework Append That Risks Exceeding the Feature Scope

**Scenario**: A rework append is requested for a delivered feature, but the rework would change code listed in the original plan's **Out of scope**. Demonstrates **define-scope-boundary** and the rework guard — refuse and ask, never append silently.

**Applies**: **define-scope-boundary**, **rework-plan-convention**

## User Request

"We found a defect in the delivered checkout rework: on partial payment failure the compensating rollback retries with wrong credentials. Investigate and fix it."

## Boundary Check

Original boundary (from the existing `plan.md`):

```
## Scope Boundary
**In scope**: wallet-service `application/` + `test/`; ADR-001 payment-failure decision
**Out of scope**: `payment-gateway/` client code; ADR-002 cutover; other modules
```

The rework request requires changing `payment-gateway/` credential retry logic — **Out of scope**.

## Refusal + Decision Options

The rework exceeds the original boundary, so the planner refuses to append silently and presents options:

> "This rework requires changing `payment-gateway/` credential retry logic, which is **Out of scope** (original boundary). Options: (a) extend the boundary to include `payment-gateway/` credential handling, (b) keep it out and file a follow-up feature, (c) treat it as a new feature cell `F2-r2` instead of an append."

**User decision**: (a) extend the boundary for this rework only.

## Appended Plan (Boundary Updated)

The rework section inherits the original boundary, tightened and extended per the user decision:

```markdown
## Rework 2026-08-10
Trigger: compensating rollback uses wrong credentials on partial failure
Boundary: original **In scope** + `payment-gateway/` credential retry (user-approved extension);
original **Out of scope** otherwise unchanged
- [ ] Fix credential retry selection in compensating rollback
- [ ] Update payment-gateway client tests for partial failures
- [ ] Validate linting, formatting, type checking
```

Original steps 1–N remain byte-for-byte unchanged.
