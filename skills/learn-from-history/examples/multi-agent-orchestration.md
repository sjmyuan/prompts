# Example: Multi-Agent Orchestration for Complex Learning

**Applies**: `detect-learning-signals` (agent orchestration path) → `provision-lessons`

**Scenario**: A team lead wants to extract reusable lessons from three sources simultaneously: a recent PR implementing a payment feature (with its user story), the last month of git history for the payment module, and Slack transcripts from the #backend channel where payment-related discussions happened. The platform has a `code-investigator` agent and an `Explore` agent available.

---

## Input

```
User: I want to learn from our recent payment work. Here are the sources:
1. PR #342: "Add recurring billing support" — story + diff
2. Git history for src/payment/ over the last 30 days
3. Slack #backend channel transcripts from July 1-25

Extract anything reusable — patterns, constraints, decisions, procedures.
```

---

## Step 1: Agent Detection

**Platform scan**: Two suitable agents detected:
- `Explore` — description: "Fast read-only codebase exploration and Q&A subagent"
- `code-investigator` — description: "Read-only code investigator that explores codebases, answers questions, traces flows, diagrams architecture, and discovers patterns"

**Suitability assessment**: Both match the code analysis keywords ("explore codebase", "investigate", "discover patterns"). The `code-investigator` is a stronger match for PR analysis (it explicitly discovers patterns). No communication-mining agent found.

**Decision**:
- PR #342 + story → dispatch to `code-investigator` (best fit for pattern discovery)
- Git history → dispatch to `Explore` (good fit for codebase exploration)
- Slack transcripts → no suitable agent; fall back to internal `analyze-communication-history`

---

## Step 2-3: Dispatch

### Agent 1: code-investigator (PR analysis)

**Prompt constructed** following the code analysis agent prompt template from `reference/agent-orchestration-pattern.md`, populated with the PR #342 source material (story text, diff, review comments) and instructed to scan for story-implementation gaps, PR discussion insights, and implementation recipes.

### Agent 2: Explore (git history analysis)

**Prompt constructed** following the code analysis agent prompt template from `reference/agent-orchestration-pattern.md`, populated with the git log (47 commits, file paths, representative diffs) and instructed to scan for evolutionary patterns, bug-fix clusters, and convention evolution.

### Internal: analyze-communication-history (Slack transcripts)

Runs internally since no communication-mining agent is available.

**Dispatch**: Both agents are invoked in parallel. Internal analysis runs concurrently.

---

## Step 3 (continued): Collect and Merge Results

### Agent 1 (code-investigator) returns:

```
CANDIDATE LESSONS FROM PR #342:

1. Summary: All payment API calls must use idempotency keys to prevent duplicate charges
   Evidence: PR review comment — "we got burned by double-charging in the last billing cycle,
   make sure every /charge call includes an X-Idempotency-Key header"
   Signal type: PR discussion insight
   Quality: Reusable ✓, Non-obvious ✓ (not in Stripe docs for this integration pattern),
   Actionable ✓, Undocumented ✓

2. Summary: The billing module has a hard dependency on the notifications service being up —
   if notifications are down, billing operations fail rather than degrading gracefully
   Evidence: src/billing/recurring.ts line 142 — await notifications.send() is not wrapped in try/catch
   Signal type: Story-implementation gap (story didn't mention notification dependency)
   Quality: Reusable ✓, Non-obvious ✓, Actionable ✓, Undocumented ✓

3. Summary: Adding a new billing plan type requires changes in 4 repos: API, worker, admin-panel, notifications
   Evidence: PR touches src/payment/ (API), src/billing/ (worker), admin-panel/ (UI), src/notifications/ (templates)
   Signal type: Implementation recipe (cross-repo)
   Quality: Reusable ✓, Non-obvious ✓, Actionable ✓, Undocumented ✓
```

### Agent 2 (Explore) returns:

```
CANDIDATE LESSONS FROM GIT HISTORY (src/payment/):

1. Summary: All new payment methods require a rollback test in addition to the happy-path test
   Evidence: 6 commits in the last 30 days added rollback tests after initial PRs were merged —
   pattern: commit messages "add rollback test for [payment method]" appeared for card, bank, wallet
   Signal type: Evolutionary pattern
   Quality: Reusable ✓, Non-obvious ✓, Actionable ✓, Undocumented ✓

2. Summary: The payment webhook handler has been patched 4 times for the same class of bug —
   missing signature verification on specific event types
   Evidence: Commits a1b2c3d, e4f5g6h, i7j8k9l, m0n1o2p all add signature checks to different webhook event handlers
   Signal type: Bug-fix cluster
   Quality: Reusable ✓, Non-obvious ✓, Actionable ✓, Undocumented ✓
```

### Internal (analyze-communication-history) returns:

```
CANDIDATE LESSONS FROM SLACK #backend (July 1-25):

1. Summary: New team members consistently struggle with local payment webhook testing —
   they don't know about the stripe-cli --forward-to flag
   Evidence: 3 separate threads (Jul 5, Jul 12, Jul 19) where different engineers asked
   "how do I test webhooks locally?" — same answer each time
   Signal type: Recurring question / Onboarding gap
   Quality: Reusable ✓, Non-obvious ✓, Actionable ✓, Undocumented ✓

2. Summary: Decision made to use Stripe's automatic retry instead of building custom retry logic
   Evidence: Thread on Jul 8 — "let's go with Stripe's built-in retry, don't reinvent the wheel" —
   decision made by tech lead, no ADR written
   Signal type: Decision record
   Quality: Reusable ✓, Non-obvious ✓ (custom retry was the default assumption),
   Actionable ✓, Undocumented ✓
```

### Merge and De-duplication:

Checking for overlaps:
- Agent 1's "idempotency keys" and Agent 2's "webhook signature verification" are different lessons (different concerns) — keep both
- Agent 1's "billing → notifications dependency" and Agent 2's "rollback tests" are different — keep both
- Internal's "webhook testing" and Agent 2's "webhook bugs" are complementary: one is about testing setup, the other about production bugs — merge as related but distinct entries

**No duplicates found. Two complementary pairs identified:**
- Webhook testing (Slack) + webhook bugs (git) → related, keep separate but cross-reference
- Idempotency keys (PR) + Stripe retry decision (Slack) → both about payment reliability, merge into a richer entry

**Merged candidate #1 (from Agent 1 + Internal):**
> Payment reliability: Use idempotency keys on all /charge calls AND rely on Stripe's built-in retry (not custom retry logic). Decision made Jul 8, reinforced by PR #342 review.

---

## Step 5-6: Quality Gate

All 7 candidates (5 original + 2 merged from complementary pairs) pass the quality gate.

---

## Step 7-8: Provisioning

| # | Lesson | Target | Rationale |
|---|---|---|---|
| 1 | Idempotency keys + Stripe retry for payment reliability | Project notes (`conventions.md`) | Project-wide payment convention |
| 2 | Billing module depends on notifications service being up | Project notes (`architecture.md`) | Architectural constraint |
| 3 | New billing plan type touches 4 repos (cross-repo recipe) | Skill file (`develop-payment-feature`) or project notes | Cross-repo procedure — skill if domain-specific, else project notes |
| 4 | All new payment methods require rollback tests | Project notes (`conventions.md`) | Project-wide testing convention |
| 5 | Webhook handler signature verification — recurring bug class | Project notes (`conventions.md`) + linter rule candidate | Preventive — consider adding a lint rule |
| 6 | Local webhook testing setup with stripe-cli | Project notes (`onboarding.md`) | Onboarding gap |
| 7 | Stripe retry decision (informal ADR) | Project notes (`decisions.md` or ADR) | Unformalized decision |

**User reviews and approves all 7.**

---

## Outcome

Seven reusable lessons extracted from 3 heterogeneous sources in parallel. Two agents handled the code-heavy analysis concurrently while internal capability processed Slack transcripts. The parent merged complementary findings (payment reliability from PR + Slack discussion) and de-duplicated across agents. All lessons provisioned to appropriate project documentation.

Without agent orchestration, this would have been a sequential 3-step analysis taking roughly 3× the time.
