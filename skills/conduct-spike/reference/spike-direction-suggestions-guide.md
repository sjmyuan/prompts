# Spike Direction Suggestions Guide

After each spike round completes, suggest 3 go-deeper and 3 go-broader candidate questions grounded in investigation evidence.

## Candidate Generation Procedure

### Step 1: Review What Was Learned

From the investigation summary, findings document, or solution doc (whichever exists at the current point in the workflow), extract:

| Category | What to extract | Example |
|---|---|---|
| **Systems identified** | Every service, database, queue, or component named | `order-ingestion-service`, `orders-pg-01`, `EventBridge` |
| **Constraints measured** | Quantified bottlenecks, SLAs, limits | "p95 latency 2.3s", "500ms payment gateway SLA", "10K req/s peak" |
| **Surprises found** | Things that contradicted assumptions | "EventBridge already exists — user thought there was no message bus" |
| **Open questions** | Things the investigation raised but didn't answer | "Why is the read replica 850ms when the primary is 2ms?" |
| **Boundary touches** | Systems or concerns the spike touched but didn't investigate | "The spike looked at orders, but `inventory-svc` is called on every order" |

### Step 2: Generate 3 Go-Deeper Candidates

For each candidate, ask: **"What specific detail did we uncover but not fully explore?"**

Heuristics for generating go-deeper candidates:

| Heuristic | Trigger | Example candidate |
|---|---|---|
| **Unfinished trace** | You followed a code path but stopped before the end | "We traced `POST /api/orders` to the DB write, but didn't trace what `order-processing-worker` does after picking up the event — what's the full async processing pipeline?" |
| **Unmeasured bottleneck** | You identified something is slow/broken but didn't quantify it | "We know `order-processing-worker` is slow, but haven't profiled which function — is it the DB query, ORM hydration, or the payment gateway call?" |
| **Unexplored edge case** | The happy path works, but failure modes are unknown | "What happens when the payment gateway times out? Is there a retry strategy, dead-letter queue, or does the order silently fail?" |
| **Pending sub-decision** | A high-level decision was made but details remain | "We chose Postgres as the database, but haven't decided: normalized schema vs. denormalized views for the dashboard queries?" |
| **Unclear contract** | An integration point was identified but its API/SLA isn't documented | "The payment gateway's `/authorize` endpoint has a 500ms SLA — but what's the exact retry behavior? Idempotency guarantees? Error code taxonomy?" |
| **Untested assumption in ADR** | An ADR option makes a claim that needs verification | "ADR-002 assumes EventBridge can handle 10K events/sec — has this been load-tested? What's the current throughput?" |

**Format each candidate as**:
- A concrete, answerable question (not "investigate performance" but "profile `order-processing-worker` to identify which function consumes 1.8s of the 2.3s p95 latency")
- Anchored to a specific finding from this round
- With a 1-sentence rationale

### Step 3: Generate 3 Go-Broader Candidates

For each candidate, ask: **"What adjacent concern did this spike exclude that might matter?"**

Heuristics for generating go-broader candidates:

| Heuristic | Trigger | Example candidate |
|---|---|---|
| **Neighboring system** | The spike touched a system but didn't investigate it | "Every order calls `inventory-svc` to reserve stock — should we spike whether `inventory-svc` can handle the increased throughput from our changes?" |
| **Cross-cutting concern** | A concern spans multiple areas but wasn't in scope | "How will the new async processing architecture affect monitoring and alerting? Current dashboards assume synchronous request-response." |
| **Organizational impact** | The solution changes team ownership or process | "After splitting the monolith, which team owns `order-processing-worker`? Currently Team A owns the whole monolith — does Team B take the async worker?" |
| **Alternative approach** | The spike evaluated options within a narrow frame | "We compared Postgres vs. MySQL for the analytics DB — but should we consider a columnar store (ClickHouse) instead? That option was excluded from the original scope." |
| **Longer-term implication** | Today's decision creates tomorrow's constraint | "If we adopt EventBridge for orders now, what's the migration path if we need Kafka-level replay capabilities in 2 years? Is EventBridge a dead-end?" |
| **Upstream/downstream impact** | The spike's solution affects consumers or producers | "The mobile app currently polls `GET /api/orders/{id}` every 5s — if we go async, how does the client get order status updates? WebSockets? Push notifications?" |

**Format each candidate as**:
- A concrete, answerable question that expands scope
- Anchored to something the spike touched but excluded, or a genuine gap
- With a 1-sentence rationale

### Step 4: Present as a Direction Menu

Use this template, grouped into "Go Deeper" and "Go Broader" sections. Each row: candidate question, evidence anchor, rationale.

```markdown
## Where to take this spike next?

### Go Deeper (narrow the focus)
| # | Candidate question | Based on (evidence from this round) | Why it matters |
|---|---|---|---|
| D1 | [concrete question] | [specific finding] | [1-sentence rationale] |
| D2 | [concrete question] | [specific finding] | [1-sentence rationale] |
| D3 | [concrete question] | [specific finding] | [1-sentence rationale] |

### Go Broader (expand the scope)
| # | Candidate question | Based on (evidence from this round) | Why it matters |
|---|---|---|---|
| B1 | [concrete question] | [specific finding or gap] | [1-sentence rationale] |
| B2 | [concrete question] | [specific finding or gap] | [1-sentence rationale] |
| B3 | [concrete question] | [specific finding or gap] | [1-sentence rationale] |
```

### Step 5: Let the User Choose

Ask: "Would you like to pursue any of these directions? Pick one (or more) and I'll start a new spike round. Or if you're satisfied with the current results, we can stop here."

If the user selects a direction, treat it as a new spike scope and restart the workflow from `define-spike-scope`.

---

## Quality Criteria for Candidates

| Criterion | Good | Bad |
|---|---|---|
| **Grounded in evidence** | "We found the read replica has 850ms p95 — should we investigate whether it's replication lag or connection pooling?" | "Maybe we should look at caching?" (no anchor to findings) |
| **Concrete and answerable** | "Profile `calculateTax()` to determine why it consumes 1.2s per call" | "Make it faster" |
| **Not already answered** | Candidate addresses something genuinely unresolved | Candidate re-asks a question the spike already answered |
| **Actionable scope** | Can be investigated in one spike round | Would require a multi-month project |
| **Genuine decision point** | Answering this question changes what the team builds | Answering this question is interesting but has no practical impact |

---

## When to Skip

Skip or lighten direction suggestions when:

- **The user explicitly says they're done**: "That answers my question, no need to go further." Respect this.
- **The spike was a single narrow decision**: "Should we use Postgres or MySQL?" — if answered definitively, there may be no meaningful deeper or broader candidates.
- **The user already has a clear next step**: "Great, now I need to spike the caching layer." — confirm and proceed; don't override their direction.

## Anti-Patterns

| Anti-pattern | Why harmful | Instead |
|---|---|---|
| **Generating candidates without evidence**: "You could also look at X" with no anchor to findings | Feels random, wastes time on tangents | Every candidate must cite a specific finding from this round |
| **Only suggesting deeper, never broader**: Always narrowing | User misses adjacent risks and cross-cutting concerns | Always generate both — the user decides which direction matters |
| **Only suggesting broader, never deeper**: Always expanding scope | Spike never converges; scope creep without resolution | Always generate both — some details need resolution before broadening |
| **Overwhelming with too many candidates**: 7+ in each direction | Decision paralysis | Exactly 3 each — enough variety, not overwhelming |
| **Suggesting the obvious**: Candidates the user already knows about | Insulting, wastes time | Candidates should surface things the investigation revealed that the user may NOT have considered |
