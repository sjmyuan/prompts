# Example: Validate a Newly Created Skill Before Delivery

**Scenario**: A skill was just created and the user wants a quality check before presenting it. Demonstrates **validate-created-skill** producing a validation report.

**Applies**: **validate-created-skill**

## Input / Context
Freshly created `skills/commit-message-writer/SKILL.md` plus its examples and references, ready for a pre-delivery check.

## Expected Output — validation report
| Check | Result |
|---|---|
| Structure & order | ✅ sections present in order |
| Description score | ✅ 9/10, trigger covers all scenarios |
| Capability naming | ✅ `<write-commit-message>` action verb |
| Knowledge placement | ✅ rubric extracted, guide condition-first |
| Example coverage | 🟡 1 of 2 capabilities have examples |
| Rules routing | ✅ "when → capability", no content restated |

## Issue Found & Fix
- Missing example for `<verify-message>` → return to **create-skill-examples**, add `examples/verify-message.md`, then re-validate.

## Final
Validation passes after the fix; report the final file tree to the user.
