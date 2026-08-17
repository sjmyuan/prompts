# Example: Create a Commit-Message Writer Skill

**Scenario**: Greenfield creation — the user asks for a brand-new copilot skill with no source material. Requirements are gathered from scratch, then a full SKILL.md is produced.

**Applies**: **collect-skill-requirements**, **create-skill-file**

## Input / Context
User request: "Create a skill that writes consistent git commit messages with conventional-commit prefixes and a 72-character subject line."

## Requirements Summary (collect-skill-requirements)
| Item | Confirmed value |
|---|---|
| Skill name | `write-commit-message` (imperative verb, kebab-case) |
| Description | "Write consistent git commit messages with conventional prefixes and a 72-char subject limit. Use when writing, fixing, or refining a commit message." |
| When-to-use scenarios | bug fix, feature, breaking change, multi-file change |
| Capabilities | `<write-commit-message>` |
| Knowledge | prefix table, 72-char wrap rule, footer format |
| Rules | 1 rule routing commit-writing requests |
| Reference needs | none — rubrics are small |

The user confirms this summary before creation proceeds.

## Post-Write Checks
- Prose written per **writing-style** — directive voice, BLUF, hard caps, no banned phrases.
- SKILL.md measured per **size-limits** (≤12,000 chars / 150 lines); over-budget drafts fixed per **size-remediation** (extract → dedupe → trim) before finalizing.

## Expected Output — `skills/write-commit-message/SKILL.md` (abridged)
```markdown
---
name: write-commit-message
description: Write consistent git commit messages with conventional prefixes and a 72-character subject limit. Use when writing, fixing, or refining a commit message.
---
<when-to-use-this-skill>
- User needs a commit message for a bug fix
- User needs a commit message for a feature
- User needs a commit message with a breaking change
- User needs to fix or refine an existing commit message
</when-to-use-this-skill>
<knowledge>
<commit-format>
... prefix table, wrap rule, footer format ...
</commit-format>
</knowledge>
<capabilities>
<write-commit-message>
1. Detect the change type from the diff.
2. Write the subject line within the 72-char limit.
3. Add a body and BREAKING CHANGE footer when needed.
</write-commit-message>
</capabilities>
<rules>
<rule>When the user needs a commit message, use **write-commit-message**.</rule>
</rules>
```
