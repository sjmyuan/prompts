# Plan Output Format

Used by **compile-actionable-plan** to structure the final plan.

```markdown
## Refined Idea
[One-paragraph summary of the refined idea]

## Delta
[One line: what changed from the original idea]

## Goals
- [Goal 1 — with its measurable success signal]

## Challenges & Solutions
| Challenge | Solution |
|---|---|
| [Challenge] | [Solution] |

## Decisions & Deferred
- **Chose:** [decision 1]
- **Dropped:** [what was not pursued]
- **Open:** [open questions]

## Key Components
- [Component 1]

## Next Steps
1. [Highest-priority step first]
2. [Next step; add a dependency note when order matters]
```

## Guidance
- Number Next Steps in execution order; note dependencies when they matter.
- Carry each goal's measurable success signal from **identify-goals** into the Goals list.
- **Delta** is one line showing the value the session added.
- **Decisions & Deferred** records choices, dropped ideas, and open questions.
- Keep the plan scannable: tables over prose, one claim per bullet.
