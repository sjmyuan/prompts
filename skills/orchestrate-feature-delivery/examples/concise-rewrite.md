# Example: Concise Rewrite of Index Prose

**Scenario**: An orchestration round just ran for the payment-migration epic. Agents reported; the index update drifted wordy — it narrates the process and buries facts in prose. The user asks for the updated index.

**Applies**: **rewrite-concise**

## Input (wordy draft)

```markdown
## Summary
It is important to note that we now have 5 features across 3 repos, and the critical path goes from F1 to F2 and F3, and then to F4, in order to complete the epic.

## Cell plan status
I dispatched agent-A to plan shared-contracts/F1, and it was successful, so F1 is now planned. Agent-B reported that order-service/F2 is in-progress and it might possibly finish tomorrow, but in general we cannot merge it until F1's contract merges first. As mentioned above, api-gateway/F3 and order-service/F4 are still unplanned.
```

## Rewritten output

```markdown
## Summary
5 features · 3 repos · 3 waves · critical path: F1 → F2/F3 → F4

## Cell plan status
| Cell | Branch | PR | Status | Agent | Plan location |
|---|---|---|---|---|---|
| shared-contracts/F1 | 1234-f1 | — | planned | agent-A | deliveries/payment-migration/shared-contracts/wallet-contracts/ |
| order-service/F2 | f2-svc | — | in-progress | agent-B | deliveries/payment-migration/order-service/wallet-service/ |
| api-gateway/F3 | — | — | unplanned | — | — |
| order-service/F4 | — | — | unplanned | — | — |
```

## What moved

| Wordy draft | Rewritten | Rule |
|---|---|---|
| "It is important to note that we now have 5 features…" | `5 features · 3 repos · 3 waves · critical path: F1 → F2/F3 → F4` | Delete filler; compress to the one-line Summary |
| "I dispatched agent-A to plan… it was successful, so F1 is now planned" | Row: F1 `planned` · agent-A | Process narration → state; fact moves to the table |
| "Agent-B reported that F2 is in-progress and it might possibly finish tomorrow" | Row: F2 `in-progress` · agent-B | Narration + hedge → state; drop the forecast (no fact) |
| "in general we cannot merge it until F1's contract merges first" | F2's `Dependencies` line: blocked-by F1 (merge-blocked) | Fact belongs in the dependency table, not prose |
| "As mentioned above, F3 and F4 are still unplanned" | Rows: F3, F4 `unplanned` | Banned phrase deleted; fact moves to the table |
