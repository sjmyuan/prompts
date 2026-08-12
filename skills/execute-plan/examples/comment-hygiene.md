# Example: Comment Hygiene — Matching Repo Convention Before Commit

**Scenario**: A plan adds a retry handler to a repo with sparse, why-only comments. The generated code arrives wordy; **commit-step**'s pre-commit scan trims it to the repo's style. Demonstrates **verify-prerequisites** (convention detection) and **commit-step** (comment scan gate).

---

## User Request

"Execute the plan to add a `RetryHandler` for the payment client, committing after each step."

## Plan to Execute

1. Create RetryHandler class
2. Wire RetryHandler into PaymentClient
3. Add unit tests for retry logic

---

## Prerequisites Check (verify-prerequisites)

Applying **verify-prerequisites** — branch `1234-add-retry-handler` checked out from `main`, working tree clean, baseline green. Comment convention sampled from recently modified files:

```
src/client/PaymentClient.java      → no inline comments
src/client/HttpClientFactory.java  → one why-comment ("// keep-alive: pooling beats TLS re-handshake")
```

- Convention note recorded in plan file: `Comment convention: sparse, why-only, no docstrings`.

---

## Step 1: Create RetryHandler Class ✅

**Files**: `src/client/RetryHandler.java`
**Validation**: compiles; unit tests pass.
**Status**: ✅ Completed

The step's first draft carries wordy comments:

```java
// This method is responsible for executing the HTTP request and
// it will automatically retry the request in case of failure up
// to the maximum number of retries that were configured
public Response execute(Request request, int maxRetries) { ... }
// ===== Step 1: retry logic =====
```

Applying **commit-step** — the pre-commit comment scan (per **code-comment-conventions**):

```
git add src/client/RetryHandler.java
git diff --cached   → scan comments
```

- Removed the restating Javadoc preamble — the method name and signature already say this.
- Removed the `// ===== Step 1` banner — process narration.
- Kept one why-comment: `// retry only on 429/5xx — 4xx are client errors, retrying is pointless`.
- Re-staged, then committed:

```
git commit -m "feat(client): add retry handler for payment client"
```

Commit `ab12cd3` created locally. Not pushed.

#### Plan Status After Step 1
### Step 1: Create RetryHandler class ✅
### Step 2: Wire RetryHandler into PaymentClient ⏳
### Step 3: Add unit tests for retry logic ⏳
