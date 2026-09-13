# Example: Verifying a Completed Cell (Independent Gate)

**Scenario**: `order-service/F2` finished execution. The executor reported `DONE_WITH_CONCERNS` with commit range `a1b2c3d..d4e5f6a`. The orchestrator must verify spec compliance and report trust before F2 advances to **verified**.

**Applies**: **verify-cell** → **update-delivery-index**

## 1. Require the executor handoff

- `deliveries/payment-migration/order-service/wallet-service/plan.md` — every step ✅, each with its commit.
- `context.md` `## Execution` — `DONE_WITH_CONCERNS` · range `a1b2c3d..d4e5f6a` · tests `18/18 passing, output pristine` · `review-code` clean (2 Blocker/Major fixed) · concern: "retry cap hard-coded".

## 2. Dispatch a fresh code-reviewer

- **code-reviewer A** (**review-code**) — inputs: `plan.md`, `context.md`, recorded range `a1b2c3d..d4e5f6a`, `adr-wallet-01-payment-failure-handling.md`, solution-doc §Wallet, global constraints.
- code-reviewer A fetches the diff from git over the range — no diff file, and the output never enters the orchestrator's context.
- Not executor-B, the agent that produced the work.

## 3. Verdicts

**Spec compliance** (brief + governing ADR):

- Missing: none.
- Extra: none.
- Misunderstood: none.
- ⚠️ Cannot verify from diff: retry-cap value lives in unchanged config — orchestrator confirmed it matches the ADR.

**Trust check**:

- Executor claimed a Blocker fix ("unbounded retry") — confirmed resolved in the diff (`wallet-service/retry.ts:41`).
- Test evidence `18/18` is consistent with `## Execution`; no re-run needed.

**Verdict**: spec compliant; report trustworthy.

## 4. Handle the open concern

- The hard-coded retry cap is a Minor, outside spec scope and not load-bearing.
- No index record; it stays in the `## Execution` handoff and rolls into the epic integration review.

## 5. Update the index

| Cell | Branch | PR | Commit | Status | Agent | Location |
|---|---|---|---|---|---|---|
| order-service/F2 | 1234-f2-wallet | — | d4e5f6a | **verified** | code-reviewer-A | deliveries/payment-migration/order-service/wallet-service/ |

- F2 awaits merge; with F1 **done**, F2 is now merge-ready.
- Push/PR still waits for user approval per **branch-and-push-conventions**.

## 6. Fix-round variant

Had the code-reviewer found a Missing requirement or a Critical finding, the orchestrator would dispatch the **planner** immediately with the findings to write a sibling `rework-<date>.md`, then the **executor** to run it, then a scoped re-review — capped at 3 rounds, escalating any unresolved finding to the user (see **reference/verification-gate.md**). The cell stays **in-progress**; the rework file is the record. A cell never reaches **verified** with an unresolved spec gap.
