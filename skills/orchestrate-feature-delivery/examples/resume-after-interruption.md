# Example: Resuming an Interrupted Epic

**Scenario**: Delivery of the payment-migration epic was interrupted (context reset / new session). The delivery index shows mixed statuses. The user says: "Continue where we left off."

**Applies**: **resume-delivery** → **orchestrate-delivery** → **update-delivery-index**

## 1. Load and assess (current index state)

- `shared-contracts/F1` — **done** (merged)
- `order-service/F2` — **in-progress** (plan.md steps 1–3 ✅, step 4 🔄)
- `api-gateway/F3` — **planned** (never executed)
- `api-gateway/F5` — **failed** (compile errors; reason recorded)
- `order-service/F4` — **unplanned** (wave 2, waits F2 + F3)

## 2. Resume decisions

| Cell | Decision | Rationale |
|---|---|---|
| shared-contracts/F1 | **skip** | done |
| order-service/F2 | **resume** | continue execution from step 4 in plan.md |
| api-gateway/F3 | **execute** | wave-ready now that F1 merged |
| api-gateway/F5 | **hold** | failed — ask user: re-plan (plan-development-task) or retry |
| order-service/F4 | **wait** | blocked-by F2 + F3 |

## 3. Dispatch

- **Agent A** → resume `order-service/F2` from step 4 (execute-plan) — works from plan.md + context.md (spike references embedded); reloads ADR-001 / solution-doc from the index's Spike References if a step needs more detail
- **Agent B** → execute `api-gateway/F3`
- F5 pending user decision; F4 waits

## 4. Update index

| Cell | Status | Agent | Location |
|---|---|---|---|
| shared-contracts/F1 | done | agent-A | docs/feature-implementations/shared-contracts/f1/ |
| order-service/F2 | in-progress (step 4 🔄) | agent-A | docs/feature-implementations/order-service/f2/ |
| api-gateway/F3 | in-progress | agent-B | docs/feature-implementations/api-gateway/f3/ |
| api-gateway/F5 | failed (pending) | — | — |
| order-service/F4 | unplanned (blocked-by F2/F3) | — | — |

## 5. Reported to the user

Resumed F2 from step 4 · started F3 · skipped F1 (done) · F5 needs a re-plan/retry decision · F4 waits for F2 + F3. Completed work was never redone.
