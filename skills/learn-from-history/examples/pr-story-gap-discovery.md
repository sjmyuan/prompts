# Example: PR Story-Gap Discovery

**Applies**: `analyze-code-change-history` → `detect-learning-signals` → `determine-provision-target` → `generate-provision-plan` → `review-and-apply`

**Scenario**: User provides a user story about adding a "bulk delete" feature and the PR that implemented it. The implementation diverged from the story in several important ways that reveal reusable knowledge about the codebase.

---

## Input

**User story** (provided by user):
> As an admin, I want to bulk-delete up to 500 users at once so I can clean up inactive accounts efficiently.
>
> Acceptance Criteria:
> - Select multiple users via checkboxes and click "Delete Selected"
> - Show a confirmation dialog with count before deleting
> - Display success/error count after operation completes
>
> Notes: Use the existing user deletion API endpoint.

**PR**: `feature/bulk-delete-users` (#342)
User provides the PR link or diff directly.

---

## Step 1: analyze-code-change-history

### Gather inputs
- Story text: confirmed
- PR diff: retrieved (15 files changed, +340 / -12 lines)

### Parse the user story
- **Explicit requirements**: Bulk select, confirm dialog, result summary
- **Implicit assumption**: "Use the existing user deletion API endpoint" — assumes `DELETE /api/users/:id` can handle bulk
- **Acceptance criteria**: Selection UI, confirmation, result display
- **Scope**: Max 500 users, admin only

### Analyze the PR changes
Files changed reveal the story didn't capture:

| File | Change | What it reveals |
|---|---|---|
| `src/api/users.ts` | NEW: `POST /api/users/bulk-delete` with body `{ ids: string[] }` | The existing single-delete endpoint couldn't be used for bulk — would require 500 HTTP calls. Story assumed wrong. |
| `src/api/middleware/rate-limit.ts` | MODIFIED: increased body size limit for bulk-delete route | The rate limiter had a 10KB body limit; 500 user IDs exceed it. Undocumented constraint. |
| `src/db/transactions.ts` | NEW: `deleteUsersInTransaction()` helper | Direct deletes caused partial failures — needed transactional deletion. Story didn't mention data integrity. |
| `src/hooks/useBulkSelection.ts` | NEW: shared hook for bulk selection with shift-click | Team extracted a reusable hook since another story needs bulk-select for exports next sprint. |
| `src/components/BulkActionBar/` | NEW: floating action bar that appears when items selected | A new UI pattern was invented — not in the story, but will be reused by other bulk operations. |

### Compare story vs implementation

| Analysis Lens | Finding | Strength |
|---|---|---|
| **Missing capability** | Story assumed `DELETE /api/users/:id` works for bulk. It doesn't. Required new `POST /api/users/bulk-delete` endpoint. | High |
| **Discovered constraint** | Rate limiter's 10KB body limit blocks bulk operations. Must check body-size config for any bulk API. | High |
| **Architectural decision** | Bulk deletes must use database transactions — partial failures are unacceptable. This applies to ALL bulk mutating operations. | High |
| **Unexpected dependency** | Implementation created shared `useBulkSelection` hook — bulk selection is now a reusable pattern with shift-click support. | Medium |
| **Unexpected dependency** | New `BulkActionBar` component — floating action bar pattern now exists for other bulk operations. | Medium |
| **Story ambiguity resolved** | "Up to 500" — implementation added chunked processing (100 per batch) to avoid DB timeout. | Medium |

### Extract candidate lessons

**Candidate 1**: "When implementing bulk mutating operations, always create a dedicated bulk endpoint (POST, not DELETE) with transactional support. Never loop the single-item endpoint — it fails at scale and cannot guarantee consistency."

**Candidate 2**: "The rate limiter imposes a 10KB body size limit. Any bulk API that sends payloads (e.g., arrays of IDs) must either increase the per-route limit or use paginated batches."

**Candidate 3**: "Bulk selection UI follows the `BulkActionBar` + `useBulkSelection` pattern. When adding bulk operations to any list/page, reuse these components — do not build custom selection UI."

---

## Step 2: detect-learning-signals (quality gate)

### Candidate 1: Transactional bulk endpoints

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Applies to any future bulk operation (archive, export, update, etc.) |
| Non-obviousness | ✅ Pass | Story author (a senior dev) assumed single endpoint works; this is project-specific knowledge |
| Actionability | ✅ Pass | Clear directive: "create dedicated bulk endpoint with transactions" |
| Non-duplication | ✅ Pass | Not in project conventions or any loaded context |
| Specificity | ✅ Pass | Specific: "POST endpoint, transactions, don't loop single-item"; general: applies to all bulk mutations |

**Verdict**: ACCEPT

### Candidate 2: Rate limiter body size

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Any bulk API will hit this until it's documented |
| Non-obviousness | ✅ Pass | Not in rate-limiter docs or inline comments; discovered at runtime |
| Actionability | ✅ Pass | "Check rate-limiter body-size config for any bulk API" |
| Non-duplication | ✅ Pass | Not documented anywhere |
| Specificity | ✅ Pass | Specific: "10KB limit, bulk payloads, per-route override"; general: applies to all bulk APIs |

**Verdict**: ACCEPT

### Candidate 3: BulkActionBar pattern

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Will be reused by bulk export, bulk archive, etc. |
| Non-obviousness | ✅ Pass | New pattern, no existing documentation |
| Actionability | ✅ Pass | "Use BulkActionBar + useBulkSelection for bulk operations" |
| Non-duplication | ✅ Pass | Not in component docs or conventions |
| Specificity | ✅ Pass | Names specific components and the pattern |

**Verdict**: ACCEPT

---

## Step 3: determine-provision-target

**Candidate 1 (bulk endpoints)**: Project-wide architectural rule → project-level persistent notes, "API Design" section.

**Candidate 2 (rate limiter)**: Project-specific constraint → project-level persistent notes, "Known Constraints" or add to "API Design" section alongside candidate 1.

**Candidate 3 (BulkActionBar pattern)**: Component usage convention → project-level persistent notes, "UI Patterns" section.

All three are project-scoped, not skill-specific or personal.

---

## Step 4: generate-provision-plan

| # | Lesson Summary | Signal Type | Target File | Section | Content to Add |
|---|---|---|---|---|---|
| 1 | Bulk mutating operations need dedicated endpoints with transaction support; never loop single-item endpoints | Story-implementation gap (missing capability) | Project conventions | API Design | "Bulk mutating operations (delete, update, archive) must use dedicated POST endpoints with transactional support. Never loop single-item endpoints — it fails at scale and can't guarantee consistency." |
| 2 | Rate limiter has 10KB body size limit; bulk APIs with large payloads need per-route override | Story-implementation gap (discovered constraint) | Project conventions | API Design | "The rate limiter imposes a 10KB body size limit. Bulk APIs sending payloads (arrays of IDs, etc.) must increase the per-route limit or use paginated batches. See `src/api/middleware/rate-limit.ts`." |
| 3 | Bulk selection UI uses BulkActionBar + useBulkSelection pattern; reuse, don't rebuild | Story-implementation gap (unexpected dependency) | Project conventions | UI Patterns | "All bulk operations on lists/tables must reuse the `BulkActionBar` component and `useBulkSelection` hook (supports shift-click). Do not build custom bulk selection UI." |

**Rationale**: All lessons are project-wide conventions or constraints. Project-level notes ensure every developer working in this workspace sees them.

---

## Step 5: review-and-apply

Present to user:

> **3 lessons extracted from PR #342 (bulk-delete-users) vs story:**
>
> 1. **Bulk mutating operations need dedicated transactional endpoints** — story assumed `DELETE /api/users/:id` works for bulk; it doesn't.
>    → Project conventions → API Design
>
> 2. **Rate limiter 10KB body limit blocks bulk payloads** — undocumented constraint discovered at implementation time.
>    → Project conventions → API Design
>
> 3. **BulkActionBar + useBulkSelection is the standard bulk UI pattern** — newly created, will be reused.
>    → Project conventions → UI Patterns
>
> Approve / Modify / Reject each?

User approves all three → write to project conventions.
