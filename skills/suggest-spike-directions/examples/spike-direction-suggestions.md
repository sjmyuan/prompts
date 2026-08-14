# Example: Spike Direction Suggestions — 3 Deeper, 3 Broader

**Scenario**: The user just completed a spike round investigating "how to reduce order API latency" and asks what to investigate next. The findings revealed the bottleneck is in `order-processing-worker`'s DB queries, not the REST layer. The skill suggests 6 concrete next-step candidates — 3 to go deeper on unresolved details, 3 to broaden to adjacent concerns.

**Applies**: `suggest-spike-directions` — run manually after a spike round completes (e.g., after `conduct-spike`'s investigation phase)

**What makes this distinct**: The suggestions are all grounded in specific findings from the investigation. None are generic ("maybe look at caching?"). Each cites exactly what was found and why going deeper or broader matters.

---

## Context: What the Spike Round Found

**Original spike goal**: Reduce order API p95 latency under peak load.

**Key findings from this round**:
- The "order API" is actually two services: `order-ingestion-service` (REST, 45ms p95 — fast) and `order-processing-worker` (async, 2.3s p95 — the bottleneck)
- 1.8s of the 2.3s is spent in DB queries; 0.3s in ORM hydration; 0.2s in the payment gateway call
- EventBridge already exists and carries `OrderReceived` events — the async pattern is partially in place
- The payment gateway has a 500ms SLA on `/authorize` — the spike didn't investigate retry/timeout behavior
- `order-processing-worker` calls `inventory-svc` and `payment-gateway` — neither was investigated
- Current monitoring assumes synchronous request-response; async processing has no dashboards

---

## Assistant Output: Direction Suggestions

> "Here's what we learned this round. Before we decide what's next, let me suggest some directions — 3 to go deeper on unresolved details, 3 to broaden to concerns we haven't covered yet.

---

## Where to take this spike next?

### Go Deeper (narrow the focus on unresolved details)

| # | Candidate question | Based on (evidence from this round) | Why it matters |
|---|---|---|---|
| **D1** | Which specific DB query in `order-processing-worker` consumes the 1.8s — is it the `SELECT` on `orders` joined with `order_items`, or the `UPDATE` on `inventory`? And is the bottleneck the query itself or a missing index? | We measured 1.8s in DB but didn't identify which query or whether an index would fix it | If it's a single missing index, the fix is trivial. If it's a complex join across 5 tables, we may need schema changes or a read replica — very different effort levels |
| **D2** | What is the payment gateway's actual retry and timeout behavior? The SLA says 500ms, but we didn't trace what happens on timeout — does `order-processing-worker` retry, fail the order, or hang? | We noted the 500ms SLA but didn't investigate the integration's error handling | If the gateway times out and the worker has no retry logic, orders may silently fail. This could be a bigger reliability issue than latency |
| **D3** | The ORM hydration takes 0.3s — is that from loading full object graphs (eager fetching) or N+1 queries during serialization? Can we switch to raw SQL + dataclasses for the hot path? | We measured 0.3s in ORM but didn't profile what the ORM is actually doing | 0.3s is 13% of the latency — if it's fixable with a query hint or by skipping hydration for unused fields, it's low-effort high-impact |

### Go Broader (expand to adjacent concerns we haven't covered)

| # | Candidate question | Based on (evidence from this round) | Why it matters |
|---|---|---|---|
| **B1** | `order-processing-worker` calls `inventory-svc` on every order — can `inventory-svc` handle the throughput if we optimize `order-processing-worker` and order volume increases? | We identified `inventory-svc` as a dependency but didn't investigate its capacity or bottlenecks | If we fix the order worker but `inventory-svc` becomes the new bottleneck, we've just moved the problem. The spike should cover the full hot path |
| **B2** | How will monitoring and alerting work after moving to async processing? Current dashboards assume synchronous request-response — do we need new metrics, traces, or SLAs for the event-driven path? | We found EventBridge already carries `OrderReceived` events, but monitoring is built for the sync REST path | If ops can't see when async orders fail or lag, the team will be blind to production issues. This is a readiness gate for going live |
| **B3** | The mobile client currently polls `GET /api/orders/{id}` every 5 seconds for status updates — if we go fully async, how does the client know when an order is processed? WebSockets? Push notifications? Server-sent events? | We investigated the backend but didn't look at the client contract — the current polling pattern assumes sync processing | Changing the client contract may require mobile team involvement, API gateway changes, and a new real-time infrastructure — this could be the long pole in the schedule |

---

Would you like to pursue any of these directions? Pick one (or more) and I'll start a new spike round. Or if you're satisfied with the current results, we can stop here."

---

### User Response

> "D1 and B1 are both critical — let's start with D1 (which DB query is the bottleneck) since that determines whether the fix is easy or hard. Then we can look at inventory-svc."

### Assistant

> "Got it. Handing back to `conduct-spike` to start a new spike round: 'Identify the specific DB query causing 1.8s latency in order-processing-worker and determine whether an index, query rewrite, or schema change is needed.' Let me define the scope..."

---

## Key Takeaways

1. **Every candidate is anchored to a specific finding**: D1 cites "1.8s in DB but didn't identify which query", B1 cites "identified `inventory-svc` as a dependency but didn't investigate". No vague suggestions.

2. **The "why it matters" column makes each candidate self-selling**: The user can immediately see the impact of pursuing (or ignoring) each direction. D1: "trivial fix vs. schema change — very different effort." B2: "if ops can't see failures, the team is blind."

3. **Both directions are always offered**: The user might default to going deeper (D1-D3), but B2 (monitoring) is something they hadn't considered and is a genuine readiness gate. The suggestions surface what the user would miss.

4. **The user drives the decision**: The skill doesn't push a direction — it presents the menu and lets the user choose. The user combined D1 + B1, showing they value both depth and breadth.

5. **Each candidate is a concrete, answerable question**: Not "investigate the DB" but "which specific query — the SELECT join or the UPDATE — and is it the query or a missing index?" This precision makes the next spike round immediately scoped.
