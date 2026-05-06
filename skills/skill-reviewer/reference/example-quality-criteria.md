# Example Quality Criteria

An example file is well-formed when it meets all of the following criteria:

| Criterion | What to check |
|---|---|
| Clear scenario heading | States the skill domain, the trigger condition, and what makes this case distinct from other examples |
| Realistic, non-trivial input | Representative of actual user requests — not a toy or hello-world scenario |
| Output matches capability steps | The structure and content of the output follow the steps of the capability it demonstrates |
| Traceable to a named capability | A reader can identify which capability produced this output |
| No contradictions with the parent skill | The example output does not violate any rule or knowledge entry in the same skill |

**Common example quality violations**:
- Output structure does not match the steps in the corresponding capability (structural drift)
- Scenario is trivially simple for a capability designed to handle complex cases
- Scenario description is missing or vague — the reader cannot tell which trigger condition is being demonstrated
- Example output contradicts a rule or knowledge constraint in the parent skill
- Example was written for an older version of the skill and references renamed or removed capabilities
