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
| Writing style | ✅ directive voice, BLUF, no banned phrases |
| Size | 🟡 SKILL.md 12,400/12,000 chars — over char budget |
| Conciseness | ✅ one line = one idea |
| Evaluation process | ✅ `<write-commit-message>` ends with a verify step |
| Example coverage | 🔴 `<verify-message>` has no linked example |
| Rules routing | ✅ "when → capability", no content restated |

## Issues Found & Fix
- Size overrun (🟡 Minor) → apply **size-remediation**: extract the footer-format table to `reference/commit-format.md`, re-measure, then re-validate.
- Missing example for `<verify-message>` (🔴 Major) → return to **create-skill-examples**, add `examples/verify-message.md`, then re-validate.

## Final
Validation passes after the fixes; report the final file tree to the user.
