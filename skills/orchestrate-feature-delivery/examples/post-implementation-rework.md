# Example: Reworking a Delivered Feature After a Post-Implementation Issue

**Scenario**: `order-service/F2` is **done** (merged). Integration testing reveals a defect: the delivered checkout flow mishandles partial payment failures — the decision in `adr-wallet-01-payment-failure-handling.md` assumed the payment gateway rejects atomically, which is false. The user says: "We found an issue in the delivered checkout rework — investigate and fix it."

**Applies**: **handle-post-implementation-issue** → **update-delivery-index**

## 1. Identify scope + suggest skill routing

- Affected cell: `order-service/F2` (done) · governing decision: `adr-wallet-01-payment-failure-handling.md` (payment failure handling)
- Focused spike scope: `adr-wallet-01-payment-failure-handling.md` only — the rest of the epic is not re-opened.
- Skill-routing suggestion presented to the user before dispatch:

| Step | Agent | Skill |
|---|---|---|
| Focused spike on `adr-wallet-01-payment-failure-handling.md` | **spike-conductor** | **conduct-spike** |
| ADR revision (decision changes) | **adr-writer** | **draft-adr** |
| Solution-doc refresh (target state changes) | **solution-doc-writer** | **write-solution-doc** |
| Write rework plan | **coding-assistant** | **plan-development-task** |
| Execute rework plan | **coding-assistant** | **execute-plan** |

## 2. Focused spike

- Dispatch **spike-conductor** scoped to `adr-wallet-01-payment-failure-handling.md`: validate the payment-gateway assumption and compare compensating-failure options.
- Result: `adr-wallet-01-payment-failure-handling.md` revised (decision changes to compensating transactions), solution doc §Wallet updated, change summary gains items 9–11.

## 3. Update the delivery index

| Cell | Branch | PR | Status | Agent | Plan location |
|---|---|---|---|---|---|
| order-service/F2 | 1234-f2-wallet | #42 (merged) | done | — | deliveries/payment-migration/order-service/wallet-service/ |
| order-service/F2-r1 (Rework of F2) | — | — | unplanned | — | deliveries/payment-migration/order-service/wallet-service/rework-2026-08-08.md |

The index records state + pointers — F2's status stays **done**, its branch + merged PR stay recorded; the rework's spike focus and steps live in the sibling rework file (see §4).

New **Wave 3**: `F2-r1` (after F2 merged). New change-summary items 9–11 trace to `adr-wallet-01-payment-failure-handling.md`.

## 4. Write the rework plan (never modify the original)

`plan-development-task` writes a new sibling `deliveries/payment-migration/order-service/wallet-service/rework-2026-08-08.md` — the existing `plan.md` is the frozen original and never gains a section:

```markdown
# Rework 2026-08-08 — compensating transactions on partial payment failure
Mode: post-merge   ·   Cell: order-service/F2-r1   ·   ADR focus: adr-wallet-01-payment-failure-handling.md

## Scope Boundary
**In scope**: wallet-service `application/` + `test/`; compensating-transaction rollback per the revised ADR decision
**Out of scope**: other ADRs, other modules — original **Out of scope** unchanged
**Rule**: no step or fix may change code beyond **In scope**; refuse and ask if it does
**Minor exceptions**: doc/comment-only edits; test-only changes for this plan's own tests

## Steps
- [ ] Add compensating-transaction rollback on partial failure
- [ ] Update payment-gateway client error mapping
- [ ] Update checkout integration test for partial failures
```

`context.md` gains a `## Reworks` manifest row:

```markdown
## Reworks
| Date | Mode | Cell | Trigger | File | Status |
|---|---|---|---|---|---|
| 2026-08-08 | post-merge | F2-r1 | partial-payment failure handling (ADR revised) | rework-2026-08-08.md | ⏳ |
```

Original `plan.md` steps 1–N remain byte-for-byte unchanged.

## 5. Execute the rework plan

- Dispatch **execute-plan** to run **only** `rework-2026-08-08.md`; completed original steps are never re-run.

## 6. Next actions

- After execution, update the index (`F2-r1` → in-progress → done after PR merge); ask the user before pushing or opening a PR.
- Pre-merge variant: when the cell is implemented but not yet merged/committed/pushed (status **in-progress**), the rework is still **append-only** (implemented steps never modified) but stays on the same cell — see **examples/pre-merge-rework.md**.
