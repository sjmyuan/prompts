# Example: Pre-Merge Rework — Sibling Rework File on an Unmerged Cell

**Scenario**: `order-service/F4` is **in-progress** — **execute-plan** finished the implementation and committed locally, but the branch is not yet pushed and no PR opened (per **branch-and-push-conventions**). Reviewing the unmerged diff, the team finds a defect: the checkout flow maps a payment-gateway timeout to the wrong error code — an implementation bug, not a flawed decision. The user says: "We found a bug in the unmerged checkout work — fix it before we push."

**Applies**: **handle-post-implementation-issue** → **update-delivery-index**

## 1. Identify scope + status

- Affected cell: `order-service/F4` — status **in-progress** (implemented, not pushed/merged)
- Governing decision: `adr-wallet-01-payment-failure-handling.md` (payment failure handling) — **not challenged**; only the timeout error mapping is wrong
- Mode: **pre-merge rework** (see **rework-modes**) — same append-only rule as post-merge, but the rework stays on this cell (no new feature/wave)

## 2. Write the sibling rework file (never modify the original)

`plan-development-task` writes a new sibling `deliveries/payment-migration/order-service/order-wallet-integration/rework-2026-08-08.md` — `plan.md` is the frozen original and never gains a section:

```markdown
# Rework 2026-08-08 — checkout timeout error mapping
Mode: pre-merge   ·   Cell: order-service/F4   ·   ADR focus: adr-wallet-01-payment-failure-handling.md

## Scope Boundary
**In scope**: checkout timeout → error-code mapping in the unmerged F4 work
**Out of scope**: original **Out of scope** unchanged; no other ADR decisions
**Rule**: no step or fix may change code beyond **In scope**; refuse and ask if it does
**Minor exceptions**: doc/comment-only edits; test-only changes for this plan's own tests

## Steps
- [ ] Fix payment-gateway timeout → correct error code mapping
- [ ] Update checkout integration test for timeout cases
```

`context.md` gains a `## Reworks` manifest row:

```markdown
## Reworks
| Date | Mode | Cell | Trigger | File | Status |
|---|---|---|---|---|---|
| 2026-08-08 | pre-merge | F4 | checkout timeout error mapping | rework-2026-08-08.md | ⏳ |
```

Original `plan.md` steps 1–N remain byte-for-byte unchanged.

## 3. Execute the rework file

- Dispatch **execute-plan** to run **only** `rework-2026-08-08.md` on the unmerged branch; original steps are never re-run or modified.
- No push/PR — the branch stays local until the user approves.

## 4. Update the index

| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| order-service/F4 | 1234-f4 | — | d4e5f6a | in-progress | coding-assistant | deliveries/payment-migration/order-service/order-wallet-integration/ |

`F4` keeps its identity and **in-progress** status — no `F4-r1`, no new wave, and no index change; the sibling `rework-2026-08-08.md` (listed in the `context.md` manifest) is the only record of the rework.

## 5. Next actions

Ask the user before pushing the branch / opening the PR (per **branch-and-push-conventions**); after the rework + original work merge, `F4` → **done** and its downstream cells unlock.
