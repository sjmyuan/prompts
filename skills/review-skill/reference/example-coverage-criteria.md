# Example Coverage Criteria

A well-covered examples section spans the skill's key scenarios. Check for these gaps:

| Gap | Severity |
|---|---|
| A named capability has no corresponding example | 🔴 Major — agent has no output model for that workflow |
| Examples cover only simple/happy-path inputs | 🟡 Minor — edge cases are unguided |
| Example count is fewer than distinct capabilities | 🟡 Minor — at least one scenario is unrepresented |
| Example labels reference outdated or renamed capabilities | 🟢 Nit — drift between names |

**Minimum viable coverage**: every distinct capability (or meaningfully different scenario variant) should have at least one linked example.
