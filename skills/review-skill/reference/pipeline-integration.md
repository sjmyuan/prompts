# Pipeline Integration Review

When a skill references or is referenced by another skill (forming a producer→consumer pipeline), verify 4 integration points beyond the individual file structure:

1. **Handoff mechanism** — Is there a file-based export/import between the skills, or is the user the transport layer? A skill that produces plans should offer an export capability; a skill that consumes plans should define a plan-input-schema and support loading from files. If the handoff relies entirely on conversation text → 🟡 Minor (fragile — context resets lose the plan).

2. **Shared schema** — Does the downstream skill define the format it expects? The downstream skill should document its input schema (minimum fields, accepted formats). If the upstream skill produces output in a format the downstream skill doesn't explicitly accept → 🟡 Minor.

3. **Bidirectional awareness** — Do both skills reference each other? The upstream skill should mention the downstream skill in its description, skill-boundary, or rules. The downstream skill should mention the upstream skill in its description or when-to-use. Missing cross-references → 🟡 Minor.

4. **Guard clauses** — Does the downstream skill prevent premature loading? Its when-to-use or description should include a loading constraint (e.g., "Do NOT load when no plan has been generated yet"). Absence → 🟡 Minor (both skills could load simultaneously).

Apply these checks when the skill's description, when-to-use, or skill-boundary references another skill by name.
