# Example: Git History Pattern Discovery

**Applies**: `analyze-code-change-history` → `detect-learning-signals` → `determine-provision-target` → `generate-provision-plan` → `review-and-apply`

**Scenario**: User asks to mine the last 3 months of git history on the `main` branch to find recurring patterns worth preserving as conventions or knowledge.

---

## Input

```
User: Look at the git history on main for the last 3 months and see if there are
      any patterns worth learning from. I want to capture conventions that evolved
      but were never written down.
```

---

## Step 1: analyze-code-change-history (git history path)

### Gather inputs
- Commit range: `main` branch, last 3 months (~400 commits)
- Retrieved via: `git log --oneline --since="2026-04-23" main`

### Scan commit messages for themes

Initial scan of 400 commit messages reveals clusters:

| Theme | Count | Example messages |
|---|---|---|
| `fix: null check on...` / `fix: handle undefined...` | 23 commits | "fix: null check on user profile response", "fix: handle undefined in payment status" |
| `refactor: extract...to shared` | 14 commits | "refactor: extract date formatting to shared/utils", "refactor: extract validation to shared/validators" |
| `migrate: ...from class to hooks` | 9 commits | "migrate: UserList from class to hooks", "migrate: Dashboard from class to hooks" |
| `fix: timezone...` | 7 commits | "fix: timezone offset in report generation", "fix: timezone conversion in email scheduler" |
| `perf: add memo...` / `perf: add useMemo...` | 6 commits | "perf: add memo to UserTable", "perf: add useMemo to filter calculations" |

### Analyze representative diffs

**Cluster 1 — Null checks (23 commits)**:
Reading 5 representative diffs reveals a pattern: the backend API occasionally returns partial objects (missing optional fields) even when they're documented as always-present. The fix is always the same: add `?.` optional chaining or a `??` default.

**Cluster 2 — Extract to shared (14 commits)**:
Functions that were duplicated in 3+ places get extracted to `src/shared/`. The commit messages often note "used in X, Y, Z" — indicating the extraction happened after duplication was noticed.

**Cluster 3 — Class to hooks migration (9 commits)**:
An ongoing, incremental migration from React class components to hooks. No single PR did it all — it's happening component by component over months.

**Cluster 4 — Timezone fixes (7 commits)**:
All related to the same root cause: the system stores UTC but some report-generation code assumed local time. The fix pattern is consistent: use `date-fns-tz` utilities instead of native `Date` methods.

**Cluster 5 — Performance memoization (6 commits)**:
Components handling large lists get `useMemo`/`React.memo` added after performance complaints. Pattern: any list component with >100 items should be memoized from the start.

### Identify evolutionary patterns

**Pattern A — Backend API partial responses**: The backend API (managed by another team) is not fully reliable about returning all documented fields. Null-safety is mandatory on ALL API response handling — this was discovered through 23 separate bug fixes, each a painful rediscovery.

**Pattern B — Shared utility extraction threshold**: When a function is used in 3+ places, extract to `src/shared/`. This threshold is being applied consistently but was never written down.

**Pattern C — Timezone handling**: All date manipulation must use `date-fns-tz`. Native `Date` methods cause timezone bugs. This was learned 7 times.

**Pattern D — List component memoization**: Any list component rendering >100 items should use `React.memo` + `useMemo` from the start, not as a later optimization.

### Extract candidate lessons

**Candidate 1**: "Always null-check all fields on API responses, even those documented as required. The backend API occasionally omits optional fields. Use optional chaining (`?.`) and nullish coalescing (`??`) on every API response field access."

**Candidate 2**: "When a utility function is used in 3 or more places, extract it to `src/shared/`. This is the project's deduplication threshold."

**Candidate 3**: "All date manipulation must use `date-fns-tz` (specifically `utcToZonedTime` and `zonedTimeToUtc`). Never use native `Date` methods for timezone-sensitive operations. This has caused 7 separate production bugs."

**Candidate 4**: "Any list/table component rendering >100 items must use `React.memo` on the component and `useMemo` on expensive calculations from the start. Don't wait for performance complaints."

---

## Step 2: detect-learning-signals (quality gate)

### Candidate 1: API null-safety

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Applies to every API integration in this project |
| Non-obviousness | ✅ Pass | The API docs say fields are required; the reality is different — this is tribal knowledge |
| Actionability | ✅ Pass | Clear directive with specific syntax |
| Non-duplication | ✅ Pass | Not in any project documentation |
| Specificity | ✅ Pass | Specific: "use ?. and ?? on all response fields"; general: applies to all API calls |

**Verdict**: ACCEPT

### Candidate 2: Extraction threshold

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Applies to all future utility creation |
| Non-obviousness | ✅ Pass | Different teams use different thresholds (2, 3, 5); this project's threshold is unwritten |
| Actionability | ✅ Pass | Clear: "3+ uses → extract to shared/" |
| Non-duplication | ✅ Pass | Not documented |
| Specificity | ✅ Pass | Specific threshold and target directory |

**Verdict**: ACCEPT

### Candidate 3: Timezone handling

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Applies to all date/time code |
| Non-obviousness | ✅ Pass | "Use date-fns-tz" is project-specific; many projects use native Date fine |
| Actionability | ✅ Pass | Specific library and functions to use |
| Non-duplication | ✅ Pass | Not documented |
| Specificity | ✅ Pass | Names the library, functions, and anti-pattern |

**Verdict**: ACCEPT

### Candidate 4: List memoization

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Applies to all list/table components |
| Non-obviousness | ✅ Pass | 100-item threshold is project-specific; community thresholds vary |
| Actionability | ✅ Pass | Clear: ">100 items → React.memo + useMemo" |
| Non-duplication | ✅ Pass | Not in coding standards |
| Specificity | ✅ Pass | Specific threshold and techniques |

**Verdict**: ACCEPT

---

## Step 3: determine-provision-target

All four candidates are project-wide conventions discovered through git history → project-level persistent notes.

| # | Target file | Section |
|---|---|---|
| 1 | Project conventions | API Integration |
| 2 | Project conventions | Code Organization |
| 3 | Project conventions | Date/Time Handling |
| 4 | Project conventions | Performance |

---

## Step 4: generate-provision-plan

| # | Lesson Summary | Signal Type | Target File | Section | Content to Add |
|---|---|---|---|---|---|
| 1 | Always null-check all API response fields with `?.` and `??` — backend occasionally omits documented fields | Evolutionary pattern (23 fix commits) | Project conventions | API Integration | "Always use optional chaining (`?.`) and nullish coalescing (`??`) on every field accessed from API responses. The backend API may omit optional fields despite documentation. Do not assume any field is present." |
| 2 | Extract utilities to `src/shared/` when used in 3+ places | Evolutionary pattern (14 refactor commits) | Project conventions | Code Organization | "When a utility function, hook, or helper is used in 3 or more files, extract it to `src/shared/`. This is the project's deduplication threshold." |
| 3 | All date manipulation must use `date-fns-tz`; never native `Date` for timezone ops | Evolutionary pattern (7 fix commits) | Project conventions | Date/Time Handling | "Use `date-fns-tz` (`utcToZonedTime`, `zonedTimeToUtc`) for all date manipulation. Never use native `Date` methods for timezone-sensitive operations — this has caused 7 production bugs." |
| 4 | List components with >100 items must use `React.memo` + `useMemo` from the start | Evolutionary pattern (6 perf commits) | Project conventions | Performance | "Any list or table component rendering more than 100 items must use `React.memo` on the component and `useMemo` for expensive calculations. Apply this proactively, not as a later optimization." |

**Rationale**: All four are project-wide conventions that became apparent through recurring commits. Project-level notes ensure they are loaded in every session within this workspace.

---

## Step 5: review-and-apply

Present to user:

> **4 lessons extracted from 3 months of git history (400 commits):**
>
> 1. **API responses need defensive null-checking** — 23 fix commits show backend omits fields.
>    → Project conventions → API Integration
>
> 2. **3-use threshold for shared/ extraction** — 14 refactor commits follow this unwritten rule.
>    → Project conventions → Code Organization
>
> 3. **Use date-fns-tz, never native Date** — 7 timezone bug fixes from the same root cause.
>    → Project conventions → Date/Time Handling
>
> 4. **Memoize list components over 100 items** — 6 perf commits pattern.
>    → Project conventions → Performance
>
> Approve / Modify / Reject each?

User approves all four → write to project conventions.
