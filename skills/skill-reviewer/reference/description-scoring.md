# Description Quality Scoring

Score each dimension 0–2 and sum for a total out of 10:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| **Trigger phrase present** | No "Use when…" or "Use for…" clause | Clause present but buried mid-sentence or implicit | Clause is explicit and positioned at the end |
| **Intent verb coverage** | No intent verbs stated | Covers some but not all `<when-to-use-this-skill>` verbs | Every intent verb (review / fix / create / improve / diagnose…) is represented |
| **Scenario coverage** | >1 scenario in `<when-to-use-this-skill>` has no matching keyword in `description` | Exactly 1 scenario uncovered | All scenarios covered bidirectionally — no gaps, no orphaned trigger terms |
| **Over-trigger risk** | `description` fires for clearly unrelated requests | Borderline — could match an adjacent skill | Tight scope; only matches intended scenarios |
| **Conciseness** | >50 words total | 30–50 words | ≤30 words; scannable in one pass |

**Interpretation**:
- **9–10**: Production-ready
- **6–8**: Usable; address gaps before publishing
- **≤5**: Likely to mis-fire or fail to load — rework required; flag as 🔴 Major
