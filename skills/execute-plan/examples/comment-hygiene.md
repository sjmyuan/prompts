# Example: Comment Hygiene — Zero-Comment Default Before Commit

**Scenario**: A plan adds a retry handler to a repo with sparse, why-only comments. **verify-prerequisites** records the policy + an exemplar; **execute-step** writes comment-minimal from the start (zero default, why-comments on a second pass); **commit-step**'s deterministic pattern scan confirms clean. Demonstrates **verify-prerequisites** (policy detection), **execute-step** (write-time zero-default), and **commit-step** (pattern-scan gate).

---

## User Request

"Execute the plan to add a `RetryHandler` for the payment client, committing after each step."

## Plan to Execute

1. Create RetryHandler class
2. Wire RetryHandler into PaymentClient
3. Add unit tests for retry logic

---

## Prerequisites Check (verify-prerequisites)

Applying **verify-prerequisites** — branch `1234-add-retry-handler` checked out from `main`, working tree clean, baseline green. Comment style sampled from recently modified files:

```
src/client/PaymentClient.java      → no inline comments
src/client/HttpClientFactory.java  → one why-comment ("// keep-alive: pooling beats TLS re-handshake")
```

- Policy + exemplar recorded in plan note: `Policy: sparse, why-only, no docstrings · Exemplar: "// keep-alive: pooling beats TLS re-handshake"`.

---

## Step 1: Create RetryHandler Class ✅

**Files**: `src/client/RetryHandler.java`
**Validation**: compiles; unit tests pass.
**Status**: ✅ Completed

Applying **execute-step** — restated the plan note's policy, then wrote comment-minimal: code first with zero comments; added only one why-comment on the second pass:

```java
// retry only on 429/5xx — 4xx are client errors, retrying is pointless
public Response execute(Request request, int maxRetries) { ... }
```

No restating Javadoc preamble, no `// ===== Step 1` banner, no "added/generated" notes.

Applying **commit-step** — deterministic pattern scan on the staged diff (per **code-comment-conventions**):

```
git add src/client/RetryHandler.java
git diff --cached | grep -iE '// (====|step |added|generated|fixed)|copilot|ai '   → no hits
```

- Scan clean; the single why-comment matches the recorded exemplar's density.
- Committed:

```
git commit -m "feat(client): add retry handler for payment client"
```

Commit `ab12cd3` created locally. Not pushed.

#### Plan Status After Step 1
### Step 1: Create RetryHandler class ✅
### Step 2: Wire RetryHandler into PaymentClient ⏳
### Step 3: Add unit tests for retry logic ⏳
