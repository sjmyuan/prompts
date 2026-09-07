# Example: Fanning a Large Multi-Module PR Review Across Review Clones

**Scenario**: A review host (applying `review-code`) receives a large PR touching three independent modules. The diff is big and the modules share only a contract file, so the host fans out per module and merges the findings.

**Applies**: `fan-out-tasks`

## Input

A PR changes `payment-service/`, `inventory-service/`, and a shared `webhooks/` handler; 40 files, ~1,900 changed lines.

## Step 1–3 — detect, split, sanity-check

Three separable changed modules with independent review dimensions → fan out per module.

| Area | Files in scope |
|---|---|
| 1 — payments | `payment-service/**` (capture, ledger) |
| 2 — inventory | `inventory-service/**` (reservation, stock) |
| 3 — webhooks | `webhooks/**` handler + shared event schema |

Sanity check: no holes (all changed files claimed), no double-reads — the shared `event-schema` file is the only boundary, flagged for one spot-check.

## Step 4 — briefs authored inline by the host

Each clone brief carries the review return contract per `review-code`: every finding has a severity label (🚫 🔴 🟡 🟢 ⚠️) plus plain-language Issue / Impact / Recommendation, one-line severity legend at first use, non-expert test passed.

## Steps 5–6 — clone reports, then merge

- area 1 — 🔴 Major: ledger entry written before the capture transaction commits (`LedgerService.java:112`).
- area 2 — 🟡 Minor: stock check races the reservation update (`ReservationService.java:54`).
- area 3 — 🔴 Major + 🟡 Minor: webhook retries on non-idempotent events; null `event.id` unhandled.

Merge: two clones independently flag the same null-handling gap on the shared schema → dedupe into one pattern finding with both instances, per `review-code`'s "distinguish patterns from instances". The shared `event-schema` file is read once to settle ownership of the fix. All findings keep their severity and Issue/Impact/Recommendation shape.

## Steps 7–8 — merged review output and validation

Merged review opens with a Summary (one takeaway), groups findings by severity, keeps Positive Highlights, and ends with Next Steps. Every finding still passes the non-expert test, nothing was dropped, and the merged output answers the original "review this PR" task directly.
