# Example: Executing a POC Plan and Stopping at the Evaluation Report

**Scenario**: The Redis POC plan (`deliveries/payment-migration/order-service/poc-adr-caching-01-redis/plan.md`, `type: poc`) is ready. The user says: "Execute it."

**Applies**: **track-plan** → **execute-step** → **produce-poc-report** → **request-push-approval** (review only)

## 1. Track + execute

- POC branch `poc-adr-caching-01-redis` created per repo convention; steps tracked with statuses, one small-step commit per ✅ step (no AI wording).

## 2. Evaluation step + report

After the final evaluation step, `produce-poc-report` writes `evaluation-report.md`:

```markdown
# Evaluation Report: adr-caching-01-cache-option.md Redis POC
| Criterion | Target | Measured | Verdict |
|---|---|---|---|
| p99 latency @ 2k rps | < 50ms | 34ms | ✅ meets |
| New ops dependencies | ≤ 3 | 1 (redis client) | ✅ meets |
Verdict: option viable — recommend adoption
```

## 3. Stop before merge

- Execution STOPS — the branch is not merged. Push is offered only for review: "Push `poc-adr-caching-01-redis` for review?"
- The report routes to the orchestrator's **evaluate-poc-results** decision gate — the user/team decides adopt (promote/merge) or reject (close + archive).
