# Example: Parallel vs Sequential Waves

**Scenario**: A notification-overhaul spike produced a solution doc touching `message-bus`, `subscriber-service`, and `notifier-service`. The user asks: "Which features can run in parallel and which must wait for another feature's code to be merged first?"

**Applies**: **order-feature-delivery**

## Features

- **F1 bus-schema** — `message-bus`: new backward-compatible event envelope.
- **F2 subscriber-consume** — `subscriber-service`: consume the new envelope.
- **F3 notifier-publish** — `notifier-service`: publish the new envelope.

## Edge classification

- **F2 vs F1**: **contract-first (soft)** — the envelope schema is agreed up front; F2 builds against stubs. Develop in parallel, merge after F1.
- **F3 vs F1**: **contract-first (soft)** — same reasoning.
- **F2 vs F3**: **independent** — different repos, different flow direction; no edge.

## Waves

1. Directed graph: F1 → F2, F1 → F3.
2. `Wave(F1) = 0`; `Wave(F2) = Wave(F3) = 1`.
3. Critical path: F1 → (F2 or F3), depth 2.

**Wave 0**: F1 · **Wave 1 (parallel)**: F2, F3

## Develop vs merge outcome

- **Develop now (all three)**: F2 and F3 build in parallel against the agreed envelope — contract-first, so waves don't block development, only merges.
- **Merge**: F1 first; F2 and F3 each merge after F1 merges, in either order.
- **Contrast**: if the envelope could NOT be agreed up front (schema still uncertain), F2/F3 become **merge-blocked** — development itself waits for F1's PR to merge, lengthening the critical path. This contrast is the core "parallel vs wait" decision the capability surfaces, which **orchestrate-delivery** then enforces via develop/merge gating.
