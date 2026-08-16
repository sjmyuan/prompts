# Example Coverage and Quality Standards

Used by **create-skill-examples** and **validate-created-skill** (examples step 5).

## Coverage requirements
- Every distinct capability must have at least one linked example
- Examples should cover key scenarios, not just happy-path inputs
- Example labels must reference current capability names (no stale/renamed references)

## Quality requirements
Each example file must meet:
- **Clear scenario heading**: states the skill domain, the trigger condition, and what makes this case distinct
- **Realistic, non-trivial input**: representative of actual user requests — not a toy or hello-world scenario
- **Output matches capability steps**: structure and content follow the capability's steps
- **Traceable to a named capability**: a reader can identify which capability produced this output
- **No contradictions with the parent skill**: the output does not violate any rule or knowledge entry in the same skill
