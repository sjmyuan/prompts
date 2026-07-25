# Example: Implementation Recipe — Single Task to Abstraction

**Applies**: `detect-learning-signals` → `analyze-code-changes` → `extract-and-refine-capability` → `provision-lessons`

Then later: `detect-learning-signals` → `analyze-code-changes` → `extract-and-refine-capability` (confidence upgrade) → `provision-lessons`

Then later: `detect-learning-signals` → `analyze-code-changes` → `extract-and-refine-capability` (refine phase) → `provision-lessons`

**Scenario**: This example shows the full learning loop — a single PR yields a **tentative** recipe, more PRs **confirm** it, and later PRs for a related task type trigger **abstraction** into a general capability.

---

## Session 1 — Single PR, Tentative Recipe

```
User: Here's a PR that added bulk-delete for users. I want to capture how
      this kind of task is implemented so newcomers know the pattern.

PR #342: Bulk delete users (2026-04-12)
```

---

### Step 1: analyze-code-change-history

**Single PR analysis** — extract the change pattern:

**Repo map**: Single monorepo.

**Component map** — files touched in #342:

| File | Change | Role |
|---|---|---|
| `src/api/users/bulk-delete.ts` | NEW | API endpoint |
| `src/api/middleware/rate-limit.ts` | MODIFY | Increased body limit |
| `src/db/users/bulk.ts` | NEW | Transactional DB helper |
| `src/hooks/useBulkSelection.ts` | MODIFY | Added bulk selection |
| `src/components/BulkActionBar.tsx` | NEW | Floating action bar |
| `src/components/UserList.tsx` | MODIFY | Wired up checkboxes |
| `tests/api/users/bulk-delete.test.ts` | NEW | API tests |
| `tests/db/users/bulk.test.ts` | NEW | DB tests |

**Change sequence**: 8 files touched in a clear logical order (API → middleware → DB → hooks → UI → tests).

**Generalizability check**: "If someone adds bulk-archive for posts next sprint, would they touch these same files in this same order?" → Yes — `src/api/posts/bulk-archive.ts`, `src/db/posts/bulk.ts`, etc. This looks like a reusable recipe.

**Confidence**: Tentative (1 PR).

---

### Step 2: detect-learning-signals

**Signal detected**: Implementation recipe (signal #13) — single PR shows a structured 8-step change pattern that looks generalizable.

**Quality gate**:

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Any bulk operation (archive, tag, assign) would follow this |
| Non-obviousness | ✅ Pass | A newcomer wouldn't know to touch rate-limit.ts or register in BulkActionBar |
| Actionability | ✅ Pass | 8 concrete, ordered steps |
| Non-duplication | ✅ Pass | Not documented anywhere |
| Specificity | ✅ Pass | Specific file paths; generalizes via `<entity>` and `<action>` parameters |

**Verdict**: ACCEPT. Tentative confidence does not block acceptance — it just means the recipe will be refined as more data arrives.

---

### Step 3: extract-capability

```markdown
<add-bulk-operation>
**Confidence**: Tentative (1 PR: #342)

**Objective**: Add a new bulk operation to an entity, following the team's implementation pattern.

**Trigger**: A story requires adding a bulk action (delete, archive, tag, assign, etc.) to an entity list.

**Steps**:
1. Add API endpoint: create `src/api/<entity>/bulk-<action>.ts` with POST handler accepting `{ ids: string[] }`
2. Update rate limiter: modify `src/api/middleware/rate-limit.ts` to increase body size limit for the new route
3. Add DB helper: create `src/db/<entity>/bulk.ts` with transactional bulk operation
4. Add bulk selection hook: modify `src/hooks/useBulkSelection.ts` if the entity doesn't already support it
5. Register in BulkActionBar: modify `src/components/BulkActionBar.tsx` to add the new action
6. Wire up entity list: modify `src/components/<Entity>List.tsx` to connect checkboxes to the new action
7. Add API tests: create `tests/api/<entity>/bulk-<action>.test.ts`
8. Add DB tests: create `tests/db/<entity>/bulk.test.ts`

**Parameters**:
| Parameter | Description | Example |
|---|---|---|
| `<entity>` | Entity name (plural, kebab-case) | `users` |
| `<action>` | Bulk action name (kebab-case) | `delete` |

**Source**: PR #342 (bulk delete users, 2026-04-12).
**Note**: Tentative — pattern inferred from a single instance. Will be refined as more bulk operation PRs confirm or adjust the recipe.
```

---

### Step 4: determine-provision-target → review-and-apply

Target: Project conventions, "Implementation Recipes" section. Tagged as tentative. **Provisioned.**

---

## Session 2 — Four More PRs, Confidence Upgrade

```
User: Here are 4 more bulk operation PRs from the last two months.
      Does the recipe from #342 hold up?

PRs:
- #367: Bulk archive posts (2026-05-03)
- #389: Bulk tag items (2026-05-21)
- #412: Bulk assign tasks (2026-06-08)
- #435: Bulk export preparation (2026-06-28)
```

---

### Step 5: analyze-code-change-history

**Cross-PR comparison against the tentative recipe**:

| File/Dir | #342 | #367 | #389 | #412 | #435 | Hit rate |
|---|---|---|---|---|---|---|
| `src/api/<entity>/bulk-<action>.ts` | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| `src/api/middleware/rate-limit.ts` | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| `src/db/<entity>/bulk.ts` | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| `src/hooks/useBulkSelection.ts` | ✅ | — | ✅ | ✅ | — | 3/5 |
| `src/components/BulkActionBar.tsx` | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| `src/components/<Entity>List.tsx` | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| `tests/api/<entity>/bulk-<action>.test.ts` | ✅ | ✅ | ✅ | ✅ | ✅ | 5/5 |
| `tests/db/<entity>/bulk.test.ts` | ✅ | ✅ | ✅ | ✅ | — | 4/5 |

**Verdict**: The tentative recipe holds. All 8 steps confirmed across 5 PRs. Refinements discovered:
- Step 4 (`useBulkSelection`) is **conditional** — only 3/5 PRs needed it; entities that already had bulk selection skipped it
- Step 8 (DB tests) may be skipped for operations without DB writes (e.g., #435 export-prep)

**Confidence upgrade**: Tentative → **Confirmed** (5 PRs).

---

### Step 6: extract-capability (refined)

Same steps, updated metadata:

```markdown
<add-bulk-operation>
**Confidence**: Confirmed (5 PRs: #342, #367, #389, #412, #435)

... (same 8 steps) ...

**Refinements from multi-PR analysis**:
- Step 4 is conditional — only needed if entity lacks bulk selection
- Step 8 may be skipped for non-DB operations

**Source**: 5 PRs across Q2 2026. Recipe confirmed by repetition across different entities and actions.
```

**Provisioned** — existing tentative capability updated to confirmed.

---

## Session 3 — Related Task Type, Abstraction

```
User: Here are 3 PRs for export operations. They share a lot with the
      bulk operation recipe. Can you merge them into something general?

PRs:
- #478: Export users to CSV (2026-07-10)
- #492: Export posts to PDF (2026-07-18)
- #511: Export analytics to JSON (2026-07-24)
```

---

### Step 7: analyze-code-change-history

**Cross-PR comparison for export pattern**:

| File/Dir | #478 | #492 | #511 | Hit rate |
|---|---|---|---|---|
| `src/api/<entity>/export-<format>.ts` | ✅ | ✅ | ✅ | 3/3 |
| `src/api/middleware/rate-limit.ts` | ✅ | ✅ | — | 2/3 |
| `src/export/<format>/generator.ts` | ✅ | ✅ | ✅ | 3/3 |
| `src/components/BulkActionBar.tsx` | ✅ | ✅ | ✅ | 3/3 |
| `src/components/<Entity>List.tsx` | ✅ | ✅ | ✅ | 3/3 |
| `tests/api/<entity>/export-<format>.test.ts` | ✅ | ✅ | ✅ | 3/3 |
| `tests/export/<format>/generator.test.ts` | ✅ | ✅ | — | 2/3 |

**Signal**: Implementation recipe (confirmed, 3 PRs). Also — clear overlap with existing `<add-bulk-operation>`.

---

### Step 8: extract-capability (export recipe)

Export capability extracted. Rule triggers: overlaps with existing `<add-bulk-operation>` → route to **abstract-capability**.

---

### Step 9: abstract-capability

**Load existing**: `<add-bulk-operation>` (confirmed, 5 PRs) from project conventions.

**Compare existing vs. new**:

| Step | Bulk operation | Export operation | Shared? |
|---|---|---|---|
| Add API endpoint | `src/api/<entity>/bulk-<action>.ts` | `src/api/<entity>/export-<format>.ts` | ✅ Same pattern |
| Update rate limiter | Always | Sometimes (depends on format) | ⚠️ Conditional |
| Add processing logic | `src/db/<entity>/bulk.ts` | `src/export/<format>/generator.ts` | ✅ Same structure, different domain |
| Add UI hook | `useBulkSelection` (conditional) | N/A | ❌ Bulk-specific |
| Register in action bar | Always | Always | ✅ |
| Wire up entity list | Always | Always | ✅ |
| Add API tests | Always | Always | ✅ |
| Add domain tests | `tests/db/` | `tests/export/` | ✅ Same structure |

**Abstraction**: The core is "add an entity-list operation" — API endpoint → processing logic → action bar registration → entity list wiring → tests. The domain of processing logic (DB vs. export) and some conditional steps vary.

### Refined capability

```markdown
<add-entity-list-operation>
**Confidence**: Confirmed (5 bulk PRs + 3 export PRs = 8 total)

**Objective**: Add a new operation to an entity list that users trigger by selecting items — following the team's established UI-to-backend implementation pattern.

**Trigger**: A story requires an operation (bulk action, export, batch process, etc.) triggered from an entity list.

**Steps**:
1. Add the API endpoint: create `src/api/<entity>/<operation-name>.ts` with the appropriate handler
2. Update rate limiter if the operation sends large payloads: modify `src/api/middleware/rate-limit.ts`
3. Add the processing logic: create `<logic-path>` implementing the operation's core logic
4. Register in the action bar: modify `src/components/BulkActionBar.tsx` to add the new operation
5. Wire up the entity list: modify `src/components/<Entity>List.tsx` to connect checkboxes to the new operation
6. Add API tests: create `tests/api/<entity>/<operation-name>.test.ts`
7. Add logic tests: create `<logic-test-path>`

**Parameters**:
| Parameter | Bulk value | Export value | Description |
|---|---|---|---|
| `<entity>` | `users`, `posts`, etc. | `users`, `posts`, `analytics` | Entity name (plural, kebab-case) |
| `<operation-name>` | `bulk-<action>` | `export-<format>` | API endpoint and file naming convention |
| `<logic-path>` | `src/db/<entity>/bulk.ts` | `src/export/<format>/generator.ts` | Where the core processing logic lives |
| `<logic-test-path>` | `tests/db/<entity>/bulk.test.ts` | `tests/export/<format>/generator.test.ts` | Where logic tests live |
| Rate limiter update | Always required | Conditional (payload size) | Whether step 2 is needed |

**Evolution note**: Started as a tentative recipe from a single PR (#342, bulk delete users, Apr 2026). Confirmed by 4 more bulk PRs (#367, #389, #412, #435). Generalized by merging with export pattern from 3 PRs (#478, #492, #511, Jul 2026). Parameterized 4 points of variance across operation types. The 7-step core pattern covers bulk operations, export operations, and anticipated future entity-list operations.

**Source**: 8 PRs across Q2–Q3 2026.
```

### Validate the abstraction
- Can a newcomer derive the bulk operation recipe? ✅ — fill in bulk column
- Can they derive the export operation recipe? ✅ — fill in export column
- Is anything lost? No — the parameter table preserves all concrete values

---

### Step 10: generate-provision-plan

| # | Lesson Summary | Signal Type | Target File | Section | Content |
|---|---|---|---|---|---|
| 1 | Abstract `add-bulk-operation` + export pattern into unified `add-entity-list-operation` | Implementation recipe (abstracted) | Project conventions | Implementation Recipes (replace existing) | [Refined capability from Step 9] |

**Plan approved. The learning loop is complete: single-PR tentative recipe → confirmed by repetition → abstracted with related task types into a general capability.**

---

## Bonus: Multi-Repo Scenario — Two-Level Extraction

The scenarios above used a monorepo. Here's how the same task type looks when it spans **multiple repos**.

### Input — Single Task, Two Repos

```
User: Here are the PRs for adding "bulk-delete users" — it touches two repos.
      Extract the pattern.

Repos and PRs:
- api-repo: PR #342 — adds the bulk-delete endpoint and DB logic
- web-repo: PR #187 — adds the bulk-delete UI and wiring
```

---

### Step 1: analyze-code-change-history

**Repo map**: Two repos — `api-repo` (backend) and `web-repo` (frontend).

**Per-repo analysis**:

| Repo | PR | Files touched | Change sequence |
|---|---|---|---|
| `api-repo` | #342 | `src/api/users/bulk-delete.ts`, `src/db/users/bulk.ts`, `tests/api/...`, `tests/db/...` | API endpoint → DB helper → tests |
| `web-repo` | #187 | `src/components/BulkActionBar.tsx`, `src/components/UserList.tsx`, `src/hooks/useBulkSelection.ts`, `tests/components/...` | Action bar → entity list → hook → tests |

**Cross-repo orchestration**: `api-repo` must be deployed first (the endpoint must exist before the UI calls it). The dependency order is: 1) api-repo, 2) web-repo.

---

### Step 2: extract-capability (two levels)

**Level 1 — Repo-level capabilities**:

```markdown
<!-- api-repo capability -->
<add-bulk-api-endpoint>
**Level**: Repo-level (api-repo)
**Confidence**: Tentative (1 PR: api-repo #342)

**Objective**: Add a bulk operation API endpoint and database logic in the API repo.

**Steps**:
1. Create `src/api/<entity>/bulk-<action>.ts` with POST handler
2. Create `src/db/<entity>/bulk.ts` with transactional operation
3. Add API tests: `tests/api/<entity>/bulk-<action>.test.ts`
4. Add DB tests: `tests/db/<entity>/bulk.test.ts`

**Parameters**: `<entity>`, `<action>`
```

```markdown
<!-- web-repo capability -->
<add-bulk-ui>
**Level**: Repo-level (web-repo)
**Confidence**: Tentative (1 PR: web-repo #187)

**Objective**: Add bulk operation UI components in the frontend repo.

**Steps**:
1. Register in BulkActionBar: modify `src/components/BulkActionBar.tsx`
2. Wire up entity list: modify `src/components/<Entity>List.tsx`
3. Add selection hook: modify `src/hooks/useBulkSelection.ts` if needed
4. Add component tests: `tests/components/BulkActionBar.test.tsx`

**Parameters**: `<entity>`, `<action>`
```

**Level 2 — Cross-repo capability**:

```markdown
<add-bulk-operation-end-to-end>
**Level**: Cross-repo (api-repo → web-repo)
**Confidence**: Tentative (1 task: api-repo #342 + web-repo #187)

**Objective**: Add a bulk operation end-to-end across the API and frontend repos.

**Trigger**: A story requires a new bulk action on an entity list.

**Steps**:
1. **In api-repo**: Apply `<add-bulk-api-endpoint>` to create the endpoint and DB logic
2. Deploy api-repo (the endpoint must be live before the UI can call it)
3. **In web-repo**: Apply `<add-bulk-ui>` to create the UI components
4. Deploy web-repo
5. End-to-end test: verify the UI can trigger the bulk action and display results

**Parameters**:
| Parameter | Used in | Description |
|---|---|---|
| `<entity>` | Both repos | Entity name (e.g., `users`) |
| `<action>` | Both repos | Bulk action name (e.g., `delete`) |

**Dependencies**: api-repo must be deployed before web-repo. Step 1 must complete before step 3.
```

---

### How this evolves

When a second task (e.g., "bulk-archive posts") follows the same multi-repo pattern:
- Each repo-level capability gets **confirmed** independently
- The cross-repo orchestration gets **confirmed**
- If a third task type (e.g., "export") is added that also spans the same two repos, `abstract-capability` merges the cross-repo capability into a general `<add-entity-list-operation-end-to-end>` — the same abstraction shown in Session 3, but now operating at the cross-repo level with repo-level sub-capabilities

