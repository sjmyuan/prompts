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
| api-gateway/F3 | **execute** | develop-ready now that F1 merged |
| api-gateway/F5 | **hold** | failed — ask user: re-plan (plan-development-task) or retry |
| order-service/F4 | **wait** | blocked-by F2 + F3 |

## 3. Dispatch

- **Agent A** (coding-assistant) → resume `order-service/F2` from step 4 (execute-plan) — works from plan.md + context.md (spike references embedded); reloads ADR-001 / solution-doc from the index's Spike References if a step needs more detail
- **Agent B** (coding-assistant) → execute `api-gateway/F3`
- **Agent C** (solution-doc-writer / adr-writer) → update solution-doc §Wallet and ADR-002 if F2's or F3's execution surfaces artifact changes — the orchestrator never edits them itself
- F5 pending user decision; F4 waits

## 4. Update index

| Cell | Status | Agent | Location |
|---|---|---|---|
| shared-contracts/F1 | done | agent-A | deliveries/payment-migration/shared-contracts/wallet-contracts/ |
| order-service/F2 | in-progress (step 4 🔄) | agent-A | deliveries/payment-migration/order-service/wallet-service/ |
| api-gateway/F3 | in-progress | agent-B | deliveries/payment-migration/api-gateway/wallet-api-gateway/ |
| api-gateway/F5 | failed (pending) | — | — |
| order-service/F4 | unplanned (blocked-by F2/F3) | — | — |

## 5. Reported to the user

Resumed F2 from step 4 · started F3 · skipped F1 (done) · F5 needs a re-plan/retry decision · F4 waits for F2 + F3. Completed work was never redone.
