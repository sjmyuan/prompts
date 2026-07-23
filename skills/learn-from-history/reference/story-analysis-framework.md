# Story Analysis Framework

When analyzing a user story against PR implementation changes, use this framework to structure the comparison.

| Analysis Lens | What to Look For | Signal Strength |
|---|---|---|
| **Missing capability** | Story assumed a library, API, or pattern that doesn't exist → what was built instead? | High — reusable for similar stories |
| **Architectural decision** | Choice of where code lives, how modules interact, which layer handles what | High — constrains future work |
| **Discovered constraint** | A limit, restriction, or gotcha found only during implementation | High — prevents repeated discovery cost |
| **Story ambiguity resolved** | The story was unclear about X; the implementation settled on Y | Medium — captures tribal knowledge |
| **Unexpected dependency** | The change required touching modules not mentioned in the story | Medium — reveals hidden coupling |
| **PR discussion / comment insight** | Rationale or constraints surfaced in review comments and story threads that aren't visible in the code diff | High — often captures the "why" behind a decision |
| **Testing approach** | How the change was validated — especially non-obvious test setups | Medium — reusable test patterns |
| **Straightforward implementation** | The change matched the story exactly with no gap | None — no lesson to extract |

The strongest lessons come from the top four rows. Focus analysis there.
