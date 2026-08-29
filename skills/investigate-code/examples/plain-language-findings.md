# Example: Plain-Language Findings (Before → After)

## User Request
"How reliable is the fee logic in the billing service?"

## Before — terse, hard to understand

> ⚠️ Inconsistency: 2 different fee patterns. 🔶 Inferred: 3% applies to STANDARD. ❓ Gap: refund branch not traced.

A bare verdict — no plain meaning, no impact, no next step.

### Confidence & Coverage
- ✅ Verified: charging fee formula (ChargingService.java:42)
- 🔶 Inferred: 3% applies to all STANDARD-tier customers
- 💭 Assumptions: "fee" is one concept — FALSE
- ❓ Gaps: refund branch not traced
- ⚠️ Inconsistencies: docs vs code disagree

## After — tag legend + TL;DR + issue cards

Applies `<present-findings-with-confidence>` + **plain-language-presentation**.

> Tag legend: ✅ Verified = I read it in code · 🔶 Inferred = reasoned guess, check my logic · 💭 Assumption = taken for granted · ⚠️ Inconsistency = two sources disagree · ❓ Gap = not investigated

**What I found** — two different "fee" concepts exist: charging (3%) and payout (flat + 1%).
**The issue** — docs describe only the charging fee; the payout fee is undocumented.
**What it means for you** — an engineer reading `docs/billing.md` would miss half the fee logic; payout pricing changes ship unversioned.

### Issue cards

#### ⚠️ Undocumented payout fee
- **Problem**: `docs/billing.md` documents only the charging fee; payouts compute a separate fee nobody documented.
- **Evidence**: `billing/PayoutService.java:58` (flat + 1%) vs `docs/billing.md` (charging only)
- **Why it matters**: payout pricing is a second source of truth with no contract — a change there ships without review intent.
- **What to do**: add the payout formula to `docs/billing.md`, or raise as a docs task.
- **Confidence**: ⚠️ Inconsistency — both sides read directly.

#### 🔶 STANDARD-tier 3% assumption
- **Problem**: the 3% rate was read for one customer tier; others unconfirmed.
- **Evidence**: `ChargingService.java:42` (STANDARD branch)
- **Why it matters**: if other tiers differ, fee estimates are wrong.
- **What to do**: open the tier-branching code or config before quoting rates.
- **Confidence**: 🔶 Inferred — one example read; sibling branches not opened.

### Confidence & Coverage
- ✅ Verified: charging fee formula (`ChargingService.java:42`); payout fee formula (`PayoutService.java:58`)
- 🔶 Inferred: 3% applies to all STANDARD-tier customers (one example read)
- 💭 Assumptions: "fee" is a single concept — FALSE, two distinct `fee` fields exist
- ❓ Gaps: refund branch not traced; pricing config (`application.yml`) not opened
- ⚠️ Inconsistencies: `docs/billing.md` documents only the charging fee; the payout fee is undocumented

## What changed

| Before | After |
|---|---|
| Bare ⚠️ verdict | Issue card: Problem / Evidence / Why it matters / What to do / Confidence |
| Tags unexplained | One-line tag legend at first use |
| No bottom line | Human TL;DR (found / issue / meaning) |
| Routine facts unchanged | ✅ Verified lines stay terse |
