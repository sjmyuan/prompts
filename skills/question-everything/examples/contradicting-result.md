# Example: Verification Contradicts a Sub-Agent's Finding (New Round)

**Scenario**: A code-exploration sub-agent concluded "Service X syncs orders to the warehouse via Kafka topic `orders.warehouse`". The finding feeds an integration-design area, so the spike orchestrator runs the verification loop before embedding it in the findings doc.

Applies **verify-sub-agent-results** (via `question-everything`) — the **question-the-result** → verify → compare → reinvestigate loop, repeated across two rounds.

## Input / Context
- **Original sub-agent result**: "Order sync to the warehouse uses Kafka topic `orders.warehouse`; latency ~2s."
- **Stakes**: integration design; choosing the wrong transport model changes the architecture.

## Round 1
### Questioning (question-the-result)
- **C1 (Correctness, high)** — Is Kafka really the transport, or is there also/only a DB-polling path?
- **C2 (Completeness, high)** — What happens when Kafka is down? Is there a fallback path?
- **C3 (Ambiguity, medium)** — "syncs orders" — full order payloads or just notification events?

### Verification (new same-type sub-agent)
A NEW research agent (same type as the original, not the original instance) is dispatched and instructed to trace the actual sync path from primary sources.

### Comparison (verdicts vs. result)
- **C1** — DISAGREE: primary sync is DB polling (`OrderPoller`); Kafka is used only for notifications.
- **C2** — AGREE: a DB fallback exists.
- **C3** — AGREE: only notification events, not payloads.

A material verdict DISAGREEs → a new research agent (same type, not the original instance) redoes the investigation with the corrected understanding.

## Round 2
### Re-investigation (new same-type agent)
A NEW research agent (same type as the original, never the original instance) receives the divergence — the C1–C3 verdicts, the `OrderPoller` evidence, and the corrected understanding — and redoes the investigation from scratch. It returns a corrected result: "Order sync is DB polling based; Kafka is notification-only."

### Questioning (question-the-result)
Question the corrected result:
- **C4 (Correctness, high)** — Does the poller batch or process one-by-one? Is the poll interval as stated?
- **C5 (Completeness, medium)** — Are there other consumers of the same Kafka topic that would be affected?

### Verification (new same-type sub-agent)
Another NEW research agent (again not the original instance) verifies C4–C5.

### Comparison (verdicts vs. result)
- **C4** — AGREE: batch processing every 30s, matches.
- **C5** — AGREE: only one consumer.

All AGREE → **result accepted**: "Order sync is DB-polling based; Kafka is notification-only." The corrected result, not the original, is used for the integration decision.
