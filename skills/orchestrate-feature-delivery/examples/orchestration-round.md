# Example: One Orchestration Round with Parallel Agents

**Scenario**: The delivery index from **multi-repo-feature-decomposition** exists — 4 features, 3 waves, 5 cells, all **unplanned**. The user says: "Start delivering — dispatch agents."

**Applies**: **orchestrate-delivery** → **update-delivery-index**

## 1. Assess state

- **Wave 0**: `shared-contracts/F1` — ready (no deps, unplanned)
- **Wave 1**: `order-service/F2`, `api-gateway/F3` — wait for F1 (not yet ready)
- **Wave 2**: `order-service/F4`, `api-gateway/F4` — wait for F2 + F3

## 2. Dispatch — Phase 1 (planners only)

- **Planner A** → plan `shared-contracts/F1` (plan-development-task)
  - Brief: scope brief + spike references — `adr-wallet-01-payment-failure-handling.md` (`spikes/payment-migration/adrs/`), solution-doc §Wallet. Agent loads them on demand for full context.

> **Plan-first gate**: no executor may touch `F1` until Planner A's `plan.md` exists on disk. The gate forbids the reverse order — never implement first and back-fill a plan.

## 3. Verify the gate + update index

- Planner A returns: `deliveries/payment-migration/shared-contracts/wallet-contracts/plan.md` exists (verified on disk) → `F1` may advance.

| Cell | Branch | PR | Commit | Status | Agent | Location |
|---|---|---|---|---|---|---|
| shared-contracts/F1 | 1234-f1-contracts | — | — | **planned** | planner-A | deliveries/payment-migration/shared-contracts/wallet-contracts/ |

F2 and F3 become develop-ready (F1 planned; contract-first allows planning in parallel).

## 4. Dispatch — Phase 2 (executors + planners, gated)

- **Executor A** → execute `shared-contracts/F1` (execute-plan) — plan file verified
- **Planner B** → plan `order-service/F2`
- **Planner C** → plan `api-gateway/F3`

> **Delegation rule in action**: when any agent's plan or execution surfaces a solution-doc or ADR change, the orchestrator dispatches a **solution-doc-writer** / **adr-writer** agent for the update — it never edits artifacts itself.

## 5. Push approval + merge

F1's execution completes. Per **branch-and-push-conventions**, the branch is pushed and the PR opened only after user approval — F1 becomes **done** only after the PR merges / the user verifies the code.

## 6. Collect + update index

| Cell | Branch | PR | Commit | Status | Agent | Location |
|---|---|---|---|---|---|---|
| shared-contracts/F1 | 1234-f1-contracts | #1 | a1b2c3d | **done** (PR merged after approval) | executor-A | deliveries/payment-migration/shared-contracts/wallet-contracts/ |
| order-service/F2 | 1234-f2-wallet | — | — | **planned** | planner-B | deliveries/payment-migration/order-service/wallet-service/ |
| api-gateway/F3 | 1234-f3-gateway | — | — | **planned** | planner-C | deliveries/payment-migration/api-gateway/wallet-api-gateway/ |
| order-service/F4 | — | — | — | unplanned | — | — |
| api-gateway/F4 | — | — | — | unplanned | — | — |

## 7. Next actions

Verify F2 + F3 plan files, then execute both in parallel (develop-ready, no conflict); with F1 **done**, F2 and F3 are now merge-ready. F4 cells remain wave-2 until F2 + F3 merge. All status changes landed in the index before the next round was dispatched.
