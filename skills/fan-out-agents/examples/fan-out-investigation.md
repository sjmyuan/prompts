# Example: Fanning a Broad Codebase Question Across Three Investigation Clones

**Scenario**: A read-only investigation host (applying `investigate-code`) receives a broad question spanning three separable subsystems. The platform lets the host spawn same-type sub-agents. One serial sweep would be slow and shallow, so the host fans out.

**Applies**: `fan-out-tasks`

## Input

> "How does checkout and payment work end to end, including refunds and payment failures?"

## Step 1–2 — detect and decide to fan out

The question decomposes into three separable, independently answerable slices:

- area 1 — order API + checkout orchestration
- area 2 — payment gateway integration + adapters
- area 3 — refunds + failure/retry handling

Same capability and reporting doctrine across areas, not serial, not trivial → fan out.

## Step 3 — split with a coverage sanity check

| Area | In scope | Out of scope |
|---|---|---|
| 1 — checkout | order-service controllers, `CheckoutOrchestrator` | gateway internals (area 2), refund logic (area 3) |
| 2 — gateway | payments module, gateway adapter, config | checkout flow, refund endpoints |
| 3 — failure | refund endpoints, retry/compensation paths | happy-path capture (area 2) |

Sanity check: every part of the question is claimed (no holes); the shared `PaymentResult` type is read in each area's own scope — flagged as a boundary file for one spot-check (no double-reads).

## Step 4 — briefs authored inline by the host

Each clone gets a brief; area 2 abbreviated:

> Scope in: `payments/`, gateway adapter, config. Out: checkout, refund endpoints.
> Sub-question: how does the gateway integration capture a payment, and what happens on failure?
> Return: findings with file:line + searched-negatives + confidence tags (✅ Verified / 🔶 Inferred / 💭 Assumption / ⚠️ Inconsistency / ❓ Gap) per `investigate-code`.
> Leaf: do not fan out further.

## Steps 5–6 — clone reports, then merge

- area 1 — ✅ Verified: checkout calls `PaymentsClient.capture` at `CheckoutOrchestrator.java:41`.
- area 2 — ✅ Verified: `GatewayAdapter` retries 5× on network error (`GatewayAdapter.java:88`).
- area 3 — 🔶 Inferred: no retry on the refund path (no config found).

Merge: areas 1 and 3 both cite `RefundService` → dedupe to one claim at the canonical call. The `PaymentResult` boundary file is read once to settle the shared status contract. A conflict surfaces: area 2 ✅ Verified "5 retries in the gateway adapter" vs area 3 🔶 Inferred "no retry on refunds" → ⚠️ Inconsistency to verify, not to hide.

## Steps 7–8 — merged answer and validation

Merged answer (BLUF, compact):

> Checkout captures payments through the gateway adapter, which retries 5× on network errors. Refunds are not confirmed to retry. ⚠️ Inconsistency — verify whether refund failures retry (`GatewayAdapter.java:88` vs `RefundService`).

Confidence & Coverage block lists ✅ Verified locations, the 🔶 Inferred refund-retry assumption, and the ❓ Gap (compensation path not traced). Coverage summary confirms all three areas returned and none was dropped; the original question is answered directly.
