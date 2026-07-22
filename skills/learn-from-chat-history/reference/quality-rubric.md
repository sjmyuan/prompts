# Lesson Quality Rubric

Every candidate lesson must pass ALL five dimensions. If any dimension fails, the candidate is rejected.

## Dimension 1: Reusability

Would this lesson apply across multiple future sessions or scenarios?

| Score | Criteria | Examples |
|---|---|---|
| ✅ Pass | Applies to a class of problems, not just one instance | "Always use `--no-pager` with git commands in scripts" |
| ❌ Fail | Specific to one file, one bug, or one moment in time | "Line 42 of `auth.ts` had a typo — fixed it" |

**Rejection rule**: If the lesson would only help in an identical repeat of the current session, reject it.

---

## Dimension 2: Non-obviousness

Would a competent practitioner in this domain already know this?

| Score | Criteria | Examples |
|---|---|---|
| ✅ Pass | Requires specific experience with this project, tool, or domain to know | "This library's `connect()` is not thread-safe despite docs implying otherwise" |
| ❌ Fail | Common knowledge for anyone working in this stack | "Use `const` instead of `let` when the variable doesn't change" |

**Rejection rule**: If a reasonable developer with 2+ years of experience in this stack would already know it, reject it.

---

## Dimension 3: Actionability

Can this be expressed as a concrete rule, knowledge entry, or procedure step?

| Score | Criteria | Examples |
|---|---|---|
| ✅ Pass | Can be written as a clear directive, fact, or step | "Run the full build before running integration tests" |
| ❌ Fail | Too abstract to turn into a usable instruction | "We should be more careful about error handling" |

**Rejection rule**: If you cannot draft a concrete, one-paragraph statement that someone could follow, reject it.

---

## Dimension 4: Non-duplication

Is this lesson absent from all currently loaded context?

| Score | Criteria |
|---|---|
| ✅ Pass | Not present in any loaded skill, agent file, persistent notes, or project doc |
| ❌ Fail | Already documented somewhere in the current context |

**Verification process**:
1. Check personal persistent notes
2. Check project-level persistent notes
3. Check loaded skill files
4. Check loaded agent/instruction files
5. Check project documentation (README, ADRs, etc.)

**Rejection rule**: If the same or substantially similar information already exists, reject it. Near-duplicates count as duplicates.

---

## Dimension 5: Specificity

Is the lesson specific enough to be useful AND general enough to be reusable?

| Score | Criteria | Examples |
|---|---|---|
| ✅ Pass | Specific enough to guide action, general enough to apply broadly | "This codebase uses Zod for all API input validation; never use Joi or Yup" |
| ❌ Fail (too vague) | No concrete guidance | "Write better tests" |
| ❌ Fail (too specific) | Only applies to one exact situation | "In `UserService.createUser()`, pass `includeProfile=true` on line 87" |

**Rejection rule**: If you can't nail down what someone should DO with this information, or if it only applies once, reject it.

---

## Summary Decision Matrix

| Reusability | Non-obviousness | Actionability | Non-duplication | Specificity | Verdict |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | **Accept** |
| ❌ | — | — | — | — | Reject — not reusable |
| ✅ | ❌ | — | — | — | Reject — too obvious |
| ✅ | ✅ | ❌ | — | — | Reject — not actionable |
| ✅ | ✅ | ✅ | ❌ | — | Reject — already documented |
| ✅ | ✅ | ✅ | ✅ | ❌ | Reject — wrong specificity level |
