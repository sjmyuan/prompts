# Example: Edit an Existing Skill — Apply Review Findings and Rename a Capability

**Scenario**: An existing skill has review findings and a noun-named capability; the user asks to apply the findings and rename it. Demonstrates **edit-skill** end-to-end (review-first composition + rename ripple).

**Applies**: **edit-skill** (routes to **create-skill-file**, **validate-created-skill**)

## Input / Context
Existing `skills/commit-message-writer/SKILL.md` with capabilities `<write-commit-message>` and `<message-verifier>`, one linked example per capability, and a guard rule routing commit requests. User: "Improve this skill. My review said the description misses triggers and `message-verifier` is a noun — fix it."

## Walkthrough (edit-skill steps)
1. **Scope** — target only the user-provided `commit-message-writer` files; never a same-named live copy.
2. **Read + inventory** — capabilities `<write-commit-message>`, `<message-verifier>`; examples `write-subject.md`, `validate-message.md`; guide rows for both examples.
3. **Triage** — open-ended "improve" → run `review-skill`'s **review-skill-file** (read-only).
   Findings: 🟡 description trigger lacks "validate"; 🔴 `<message-verifier>` is a noun per **naming-conventions**.
4. **Classify** — finding 1 = description fix; finding 2 = rename.
5. **Route (existing-file mode)** — **create-skill-file**: edit the description to a two-part template self-scoring ≥9 ("…Use when writing, validating, or refining a commit message."); rename `<message-verifier>` → `<verify-message>` in `<capabilities>` and the routing rule. Preserve all other sections byte-for-byte.
6. **Ripple** — update `examples/validate-message.md` `**Applies**: **verify-message**` (was **message-verifier**) and its guide-row wording.
7. **Validate after each change** — re-run **validate-created-skill**: description ≥9, action-verb names, example coverage intact, no dangling refs.
8. **Re-measure** — changed files within **size-limits**.

## Expected Output
- Description trigger now covers validating and refining.
- `<verify-message>` replaces `<message-verifier>` across capabilities, rules, and the example `Applies` line.
- Validation report shows no 🔴 findings remaining.
