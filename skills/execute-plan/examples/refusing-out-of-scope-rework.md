# Example: Refusing a Recovery Fix That Exceeds the Plan Boundary

**Scenario**: Executing a rework plan; a step fails and the only viable fix requires changing a file listed in **Out of scope**. Demonstrates **check-scope-boundary** inside **handle-errors** — refuse and ask, never silently change out-of-scope code.

**Applies**: **check-scope-boundary**, **handle-errors**

## Plan in Execution

```
## Scope Boundary
**In scope**: `application/` + `test/`
**Out of scope**: `infrastructure/` (DB schema, external client code)
```

### Step 2: Update Compensating Rollback Tests 🔄

**Error**: `infrastructure/PaymentGatewayClient.java` throws on partial failure; the new test cannot compile without handling it.

**Recovery analysis**: the only viable fix is to add retry logic in `infrastructure/PaymentGatewayClient.java` — **Out of scope**.

## Refusal + Decision Options

Applying **check-scope-boundary**: the fix exceeds the boundary, so the executor refuses and asks:

> "Recovering Step 2 requires changing `infrastructure/PaymentGatewayClient.java`, which is **Out of scope**. Options: (a) extend the boundary to include it, (b) stay in scope and record a follow-up, (c) proceed anyway with a recorded deviation."

**User decision**: (a) extend the boundary.

The executor updates the boundary block in `plan.md`, retries the step, and marks it ✅.
