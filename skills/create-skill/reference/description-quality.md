# Description Quality: Template, Scoring, Trigger Correctness

Used by **create-skill-file** (frontmatter step 2) and **validate-created-skill** (description step 2).

## Two-part template
```
[One sentence: what the skill does and its domain.]
Use when [intent-verb₁] / [intent-verb₂] / [intent-verb₃] [object/scope].
```
- Part 1 (domain summary): tells the AI *what the skill knows*.
- Part 2 (trigger phrase): lists intent verbs matching the `<when-to-use-this-skill>` bullets.

Example:
> Review SKILL.md files for correct structure, section-purpose compliance, and absence of duplication. Use when reviewing, checking, or diagnosing trigger failures in a copilot skill file.

## Five-dimension scoring (0–2 each, total /10)

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Trigger phrase present | No "Use when…/Use for…" | Buried or implicit | Explicit, at the end |
| Intent verb coverage | No verbs | Some verbs | Every `<when-to-use-this-skill>` verb |
| Scenario coverage | >1 scenario uncovered | 1 scenario uncovered | Bidirectional, no gaps or orphans |
| Over-trigger risk | Fires on unrelated requests | Borderline | Tight scope only |
| Conciseness | >50 words | 30–50 words | ≤30 words |

**Interpretation**: 9–10 production-ready; 6–8 usable (address gaps); ≤5 rework required.

## Trigger-correctness rules
- The `description` must explicitly state *when* to load — "Use when…" or "Use for…" phrase
- Must include the primary intent verbs matching `<when-to-use-this-skill>`
- Trigger phrase must cover **all** scenarios (no under-coverage)
- Must not cover scenarios absent from `<when-to-use-this-skill>` (no over-triggering)
- `<when-to-use-this-skill>` must be present — a missing section means no post-load scope check
