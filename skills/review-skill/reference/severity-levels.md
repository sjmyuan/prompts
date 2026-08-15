# Severity Levels

| Level | Symbol | When to use |
|---|---|---|
| Blocker | 🚫 | Skill fails to load, activate, or produce correct output in all or most realistic scenarios |
| Major | 🔴 | Violation breaks the agent for at least one realistic scenario |
| Minor | 🟡 | Deviation reduces quality but does not break the common case |
| Nit | 🟢 | Cosmetic — naming, wording, style |
| Inconsistency | ⚠️ | Two conflicting patterns; present both and ask the user to decide |

Use 🚫 Blocker when the agent cannot complete the task at all (no capability, missing frontmatter, absent `<when-to-use-this-skill>`).
Use 🔴 Major for violations that break the skill in specific but realistic scenarios.
