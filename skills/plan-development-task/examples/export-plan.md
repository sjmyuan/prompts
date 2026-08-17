# Example: Exporting a Confirmed Plan to Files

**Scenario**: A simple bug-fix plan has been confirmed by the user. **export-plan** persists it to a feature folder as `plan.md` + `context.md` so **execute-plan** can carry it out.

**Applies**: **export-plan**

## Confirmed Input

- Change type: **Bug Fix**
- Root cause confirmed; Scope Boundary ratified
- Branch/base recorded: `fix-null-pointer` / `main`

## Feature Folder

`docs/feature-implementations/fix-null-pointer-in-transformer/`

## plan.md

```markdown
## Scope Boundary
**In scope**: `DataImportedHandler` null-guard logic and its tests
**Out of scope**: transformer, publisher, other handlers
**Rule**: no step, error-recovery fix, or review fix may change anything beyond **In scope**
**Minor exceptions**: doc/comment-only edits; test-only changes for this plan's own tests

1. **Prepare Environment** — branch `fix-null-pointer` off `main`; clean tree; deps installed; baseline tests pass
2. **Write tests** for null-safety in `DataImportedHandler`
3. **Confirm test failure**
4. **Fix code** — guard the null pointer on missing payload
5. **Verify fix** — all tests pass
6. **Clean up** unused code and tests
7. **Validate** linting, formatting, type-checking
```

## context.md

```markdown
# Fix null pointer in DataImportedHandler

**Change type:** Bug fix

**Original request:** "Outgoing events crash when the transform result is null on missing payload."

**Root cause:** `DataImportedHandler` dereferences a null transform result on missing payload.

**TDD rationale:** Full cycle — complex logic bug requires test-first safety.

**Boundary rationale:** Change confined to handler + its tests; publisher untouched.

**Branch/base:** `fix-null-pointer` / `main`

**Constraints:** Existing tests stay green; no behavior change beyond the null guard.
```

## Save Location

Saved to `docs/feature-implementations/fix-null-pointer-in-transformer/`; the user can now invoke **execute-plan** to run it.
