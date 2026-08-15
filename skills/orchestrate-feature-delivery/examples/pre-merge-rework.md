# Example: Pre-Merge Rework — Appended Plan on an Unmerged Cell

**Scenario**: `order-service/F4` is **in-progress** — **execute-plan** finished the implementation and committed locally, but the branch is not yet pushed and no PR opened (per **branch-and-push-conventions**). Reviewing the unmerged diff, the team finds a defect: the checkout flow maps a payment-gateway timeout to the wrong error code — an implementation bug, not a flawed decision. The user says: "We found a bug in the unmerged checkout work — fix it before we push."

**Applies**: **handle-post-implementation-issue** → **update-delivery-index**

## 1. Identify scope + status

- Affected cell: `order-service/F4` — status **in-progress** (implemented, not merged/committed/pushed)
- Governing decision: `adr-wallet-01-payment-failure-handling.md` (payment failure handling) — **not challenged**; only the timeout error mapping is wrong
- Mode: **pre-merge rework** (see **rework-modes**) — same append-only rule as post-merge, but the rework stays on this cell (no new feature/wave)

## 2. Append the plan (never modify implemented steps)

`plan-development-task` appends a `## Rework 2026-08-08` section to the existing `deliveries/payment-migration/order-service/order-wallet-integration/plan.md`:

```markdown
## Rework 2026-08-08
Trigger: checkout timeout error mapping (review of unmerged diff)
- [ ] Fix payment-gateway timeout → correct error code mapping
- [ ] Update checkout integration test for timeout cases
```

Original steps 1–N remain byte-for-byte unchanged.

## 3. Execute the appended plan

- Dispatch **execute-plan** to run **only** the `## Rework` steps on the unmerged branch; original steps are never re-run or modified.
- No push/PR — the branch stays local until the user approves.

## 4. Update the index

| Cell | Status | Agent | Plan location |
|---|---|---|---|
| order-service/F4 | in-progress · Rework: appended plan (## Rework 2026-08-08) | coding-assistant | deliveries/payment-migration/order-service/order-wallet-integration/ |

`F4` keeps its identity and **in-progress** status — no `F4-r1`, no new wave.

## 5. Next actions

Ask the user before pushing the branch / opening the PR (per **branch-and-push-conventions**); after the rework + original work merge, `F4` → **done** and its downstream cells unlock.
