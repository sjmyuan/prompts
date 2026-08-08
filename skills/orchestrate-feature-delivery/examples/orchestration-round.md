# Example: One Orchestration Round with Parallel Agents

**Scenario**: The delivery index from **multi-repo-feature-decomposition** exists — 4 features, 3 waves, 5 cells, all **unplanned**. The user says: "Start delivering — dispatch agents."

**Applies**: **orchestrate-delivery** → **update-delivery-index**

## 1. Assess state

- **Wave 0**: `shared-contracts/F1` — ready (no deps, unplanned)
- **Wave 1**: `order-service/F2`, `api-gateway/F3` — wait for F1 (not yet ready)
- **Wave 2**: `order-service/F4`, `api-gateway/F4` — wait for F2 + F3

## 2. Dispatch (round 1)

- **Agent A** (coding-assistant) → plan `shared-contracts/F1` (plan-development-task)
  - Brief: scope brief + spike references — change-summary items 1–3, ADR-001 (`spikes/payment-migration/adrs/adr-001-wallet.md`), solution-doc §Wallet. Agent loads them on demand for full context.

> **Delegation rule in action**: when any agent's plan or execution surfaces a solution-doc or ADR change, the orchestrator dispatches a **solution-doc-writer** / **adr-writer** agent for the update — it never edits artifacts itself.

## 3. Collect + update index

| Cell | Status | Agent | Location |
|---|---|---|---|
| shared-contracts/F1 | **planned** | agent-A | deliveries/payment-migration/shared-contracts/wallet-contracts/ |

F2 and F3 become develop-ready (F1 planned; contract-first allows planning in parallel).

## 4. Dispatch (round 2, parallel)

- **Agent A** (coding-assistant) → execute `shared-contracts/F1` (execute-plan)
- **Agent B** (coding-assistant) → plan `order-service/F2`
- **Agent C** (coding-assistant) → plan `api-gateway/F3`

## 5. Collect + update index

| Cell | Status | Agent | Location |
|---|---|---|---|
| shared-contracts/F1 | **done** | agent-A | deliveries/payment-migration/shared-contracts/wallet-contracts/ |
| order-service/F2 | **planned** | agent-B | deliveries/payment-migration/order-service/wallet-service/ |
| api-gateway/F3 | **planned** | agent-C | deliveries/payment-migration/api-gateway/wallet-api-gateway/ |
| order-service/F4 | unplanned | — | — |
| api-gateway/F4 | unplanned | — | — |

## 6. Next actions

Execute F2 + F3 in parallel (both develop-ready, no conflict); F4 cells remain wave-2 until F2 + F3 merge. All status changes landed in the index before the next round was dispatched.
