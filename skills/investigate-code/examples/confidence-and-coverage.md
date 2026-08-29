# Example: Confidence & Coverage Report — Billing Fee Investigation

## User Request
"How is the fee calculated in the billing service?"

## Response

Applies `<investigate-codebase>` → `<present-findings-with-confidence>`.

The agent traced the charging branch, then re-checked for other `fee` usages and reported the full epistemic profile instead of a partial answer.

### Findings

> Tag legend: ✅ Verified = I read it in code · 🔶 Inferred = reasoned guess, check my logic · 💭 Assumption = taken for granted · ⚠️ Inconsistency = two sources disagree · ❓ Gap = not investigated

**What I found** — two different "fee" concepts exist: charging (3%) and payout (flat + 1%).
**The issue** — docs describe only the charging fee; the payout fee is undocumented.
**What it means for you** — an engineer reading `docs/billing.md` would miss half the fee logic.

**Charging branch** — ✅ Verified, `billing/ChargingService.java:42`:
`fee = grossAmount * 0.03` when `customer.tier == STANDARD`.

**Payout branch** — discovered on re-check, ✅ Verified, `billing/PayoutService.java:58`:
a separate `fee` (`flat + 1%`) computed for payouts — a different `fee` than the charging one.

#### ⚠️ Undocumented payout fee
- **Problem**: `docs/billing.md` documents only the charging fee; the payout fee is undocumented.
- **Evidence**: `billing/PayoutService.java:58` (flat + 1%) vs `docs/billing.md` (charging only)
- **Why it matters**: payout pricing is a second source of truth with no contract.
- **What to do**: add the payout formula to `docs/billing.md`.
- **Confidence**: ⚠️ Inconsistency — both sides read directly.

### Confidence & Coverage

```
### Confidence & Coverage
- ✅ Verified: charging fee formula (`ChargingService.java:42`); payout fee formula (`PayoutService.java:58`)
- 🔶 Inferred: the 3% rate applies to all STANDARD-tier customers (only one example read)
- 💭 Assumptions: "fee" is a single concept in the codebase — FALSE, two distinct `fee` fields exist
- ❓ Gaps: refund branch not traced; pricing config (`application.yml`) not opened
- ⚠️ Inconsistencies: `docs/billing.md` documents only the charging fee; the payout fee is undocumented
```

**Note**: The first pass answered only the charging branch — every claim was verifiable, yet the answer was incomplete (a partial truth). The gap only became visible after re-checking for other `fee` usages.
