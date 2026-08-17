# Plan Executor: Small-Step Commits with Push Approval Example

**Scenario**: A 4-step feature plan executes with one small commit per step, and the branch is pushed only after explicit user confirmation. Demonstrates **verify-prerequisites**, **commit-step**, **request-push-approval**, and **manage-user-interaction** (branch-creation ask, push approval).

---

## User Request

"Execute the plan to add a `CustomerValidator`, commit after each step, and don't push anything until I confirm."

## Plan to Execute

1. Create CustomerValidator class
2. Wire validator into CustomerService
3. Add unit tests for validator
4. Run lint, formatting and type checks

---

## Prerequisites Check (verify-prerequisites)

Applying **verify-prerequisites**:

```
git status        → working tree clean
git branch        → on main; feature branch missing
```

- Branch convention detected from existing branches (`1234-*` ticket style): new branch `1234-add-customer-validator` from `main`.
- Missing: that feature branch. Raise to user: "Create branch `1234-add-customer-validator` from `main` before starting?" User confirms. Branch created.
- Dependencies present, baseline tests pass → **ready**.

Recorded in plan file: `Prerequisites: ready (branch created, baseline green)`.

---

## Step 1: Create CustomerValidator Class ✅

**Files**: `src/validation/CustomerValidator.java`
**Validation**: class compiles; no tests changed.
**Status**: ✅ Completed

Applying **commit-step**:
```
git add src/validation/CustomerValidator.java
git commit -m "feat(validation): add CustomerValidator class"
```
Commit `a1b2c3d` created locally. Not pushed.

#### Plan Status After Step 1
### Step 1: Create CustomerValidator class ✅
### Step 2: Wire validator into CustomerService ⏳
### Step 3: Add unit tests for validator ⏳
### Step 4: Run lint, formatting and type checks ⏳

---

## Step 2: Wire Validator into CustomerService ✅

**Files**: `src/service/CustomerService.java`
**Validation**: existing tests pass — no regressions.
**Status**: ✅ Completed

Applying **commit-step**:
```
git add src/service/CustomerService.java
git commit -m "refactor(service): use CustomerValidator in CustomerService"
```
Commit `e4f5g6h7` created locally. Not pushed.

---

## Step 3: Add Unit Tests for Validator ✅

**Files**: `test/CustomerValidatorTest.java`
**Validation**: all 12 tests pass.
**Status**: ✅ Completed

Applying **commit-step**:
```
git add test/CustomerValidatorTest.java
git commit -m "test(validation): cover CustomerValidator edge cases"
```
Commit `i8j9k0l1` created locally. Not pushed.

---

## Step 4: Validate Linting, Formatting and Type Checks ✅

**Files**: none changed
**Validation**: lint, format, type-check all clean.
**Status**: ✅ Completed

Applying **commit-step**: step produced no code change — no commit needed.

---

## Final Summary & Push Approval (request-push-approval)

All 4 steps completed ✅.

Applying **request-push-approval**:
```
Branch: 1234-add-customer-validator (3 commits ahead of main)
  a1b2c3d feat(validation): add CustomerValidator class
  e4f5g6h7 refactor(service): use CustomerValidator in CustomerService
  i8j9k0l1 test(validation): cover CustomerValidator edge cases
```

Ask user: "Push branch `1234-add-customer-validator` to remote?"

- **User confirms** → `git push -u origin 1234-add-customer-validator`; success reported.
- **User declines** → branch stays local; user is told the 3 commits are ready to push whenever they choose.

The plan file and context file are kept as a permanent record.
