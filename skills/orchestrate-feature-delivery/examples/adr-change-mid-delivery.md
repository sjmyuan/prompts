# Example: ADR Change Mid-Delivery

**Scenario**: The payment-migration epic is mid-delivery — `order-service/F2` is **done**, `api-gateway/F3` is **planned**, `order-service/F4` is **in-progress**. Integration testing of F2 reveals the payment gateway does not reject atomically; the team revises `adr-wallet-01-payment-failure-handling.md` (compensating transactions). The user says: "The payment-failure decision changed — route what's affected."

**Applies**: **handle-adr-change** → **update-delivery-index**

## 1. Confirm the change + list governed cells

- Changed decision: `adr-wallet-01-payment-failure-handling.md` — revised to compensating transactions. Drift is signaled by the **adr-writer** agent's return; the ADR itself stays versionless (rewritten in place, per **adr-drift**).
- Governed cells (index `ADRs:` per feature): F2 (done) · F3 (planned) · F4 (in-progress).

## 2. Route each cell by status

| Cell | Status | Route |
|---|---|---|
| order-service/F2 | done | post-merge rework — new `F2-r1` in a new wave (see **rework-modes**) |
| api-gateway/F3 | planned | re-plan in place — dispatch **plan-development-task** against the revised ADR (nothing implemented; no history to preserve) |
| order-service/F4 | in-progress | pre-merge rework — sibling `rework-<date>.md`, same cell, no new wave (see **rework-modes**) |

## 3. Dispatch

- **Agent A** (coding-assistant) → re-plan `api-gateway/F3` (**plan-development-task**) against the revised decision.
- **Agent B** (coding-assistant) → write + execute the pre-merge rework for `order-service/F4` (**plan-development-task** → **execute-plan**), sibling `rework-2026-08-24.md`, original steps never modified.
- **F2-r1** (post-merge): the ADR + solution doc are already revised — write + execute the rework file.
- No in-flight POC cells here — otherwise surface them to the user (the change may invalidate success criteria).

## 4. Update the index

| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| order-service/F2 | 1234-f2-wallet | #42 (merged) | e5f6a7b | done | — | deliveries/payment-migration/order-service/wallet-service/ |
| order-service/F2-r1 (Rework of F2) | — | — | — | unplanned | — | deliveries/payment-migration/order-service/wallet-service/rework-2026-08-24.md |
| api-gateway/F3 | 1234-f3-gateway | — | — | planned → re-planning | agent-A | deliveries/payment-migration/api-gateway/wallet-api-gateway/ |
| order-service/F4 | 1234-f4 | — | d4e5f6a | in-progress (rework) | agent-B | deliveries/payment-migration/order-service/order-wallet-integration/ |

Recorded per **update-delivery-index**: F3 → re-planning, F4 keeps **in-progress** (sibling rework file is the record), `F2-r1` added in a new wave — then **rewrite-concise**.

## 5. Next actions

No planned cell is dispatched on the stale decision. Re-plan F3, run F4's rework, and plan/execute F2-r1; all status changes land in the index before the next dispatch.
