# Example: Reworking a Delivered Feature After a Post-Implementation Issue

**Scenario**: `order-service/F2` is **done** (merged). Integration testing reveals a defect: the delivered checkout flow mishandles partial payment failures — the decision in ADR-001 assumed the payment gateway rejects atomically, which is false. The user says: "We found an issue in the delivered checkout rework — investigate and fix it."

**Applies**: **handle-post-implementation-issue** → **update-delivery-index**

## 1. Identify scope + suggest skill routing

- Affected cell: `order-service/F2` (done) · governing decision: ADR-001 (`adr-001-wallet.md` — payment failure handling)
- Focused spike scope: ADR-001 only — the rest of the epic is not re-opened.
- Skill-routing suggestion presented to the user before dispatch:

| Step | Agent | Skill |
|---|---|---|
| Focused spike on ADR-001 | **spike-conductor** | **conduct-spike** |
| ADR revision (decision changes) | **adr-writer** | **draft-adr** |
| Solution-doc refresh (target state changes) | **solution-doc-writer** | **write-solution-doc** |
| Append rework plan | **coding-assistant** | **plan-development-task** |
| Execute rework plan | **coding-assistant** | **execute-plan** |

## 2. Focused spike

- Dispatch **spike-conductor** scoped to ADR-001: validate the payment-gateway assumption and compare compensating-failure options.
- Result: ADR-001 revised (decision changes to compensating transactions), solution doc §Wallet updated, change summary gains items 9–11.

## 3. Update the delivery index

| Cell | Status | Agent | Plan location |
|---|---|---|---|
| order-service/F2 | done · Rework: F2-r1 · ADR-001 spike · appended plan | spike-conductor (rework) | deliveries/payment-migration/order-service/wallet-service/ |
| order-service/F2-r1 | unplanned | — | deliveries/payment-migration/order-service/wallet-service/ (append) |

New **Wave 3**: `F2-r1` (after F2 merged). New change-summary items 9–11 trace to ADR-001.

## 4. Append the plan (never modify implemented steps)

`plan-development-task` appends to the existing `deliveries/payment-migration/order-service/wallet-service/plan.md`:

```markdown
## Rework 2026-08-08
Trigger: partial-payment failure handling (ADR-001 revised)
- [ ] Add compensating-transaction rollback on partial failure
- [ ] Update payment-gateway client error mapping
- [ ] Update checkout integration test for partial failures
```

Original steps 1–N remain byte-for-byte unchanged.

## 5. Execute the appended plan

- Dispatch **execute-plan** to run **only** the `## Rework` steps; completed original steps are never re-run.

## 6. Next actions

- After execution, update the index (`F2-r1` → in-progress → done after PR merge); ask the user before pushing or opening a PR.
- Pre-merge variant: when the cell is implemented but not yet merged/committed/pushed (status **in-progress**), the rework is still **append-only** (implemented steps never modified) but stays on the same cell — see **examples/pre-merge-rework.md**.
