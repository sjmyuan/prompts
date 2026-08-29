# Example: Craft an Agent File That Delegates to a Skill

**Scenario**: User wants a "release-notes-writer" agent that applies the `draft-release-notes` skill. Target platform is unspecified, so it is detected first, the platform format is loaded, then the wrapper carries only agent-scope, tool, and delegation content.

**Applies**: **craft-agent-file**

## Input / Context

User request: "Create an agent file for a release-notes-writer agent that applies the draft-release-notes skill."

Referenced skill `draft-release-notes/SKILL.md` already covers: release-note sections, changelog conventions, and the drafting procedure.

## Platform detection

Platform unspecified — ask the user. User answers: opencode.

Format loaded from **reference/agent-file-formats.md**: `.md` suffix, `description` + `mode` + `permission` frontmatter.

## Tool match

Agent task = drafting release notes from git history. Tools chosen per the opencode schema: read and search permissions for history inspection; edit permission for writing the output file.

## Frontmatter

```
---
description: "Writes release notes from git history by applying the draft-release-notes skill."
mode: primary
permission:
  read: allow
  glob: allow
  grep: allow
  list: allow
  edit: allow
  bash: allow
  todowrite: allow
  lsp: allow
  skill: allow
  webfetch: allow
  websearch: deny
---
```

## Body (wrapper content only)

Body follows the wrapper pattern from **reference/prompt-writing-style.md** — directive voice, agent-scope bullets, delegation rules only:

```
Your task is to write release notes by applying the `draft-release-notes` skill step by step.

<knowledge>

<agent-scope>
Use this agent when the user wants release notes generated, updated, or reviewed.

Do NOT use this agent for:
- **General coding** — use the coding-assistant agent
- **Blog or article writing** — use the blog-assistant agent
</agent-scope>

</knowledge>

<rules>

<rule>When the user asks for release notes, apply the skill's **draft-release-notes** capability.</rule>
<rule>When release notes exist and the user adds commits, apply the skill's **update-release-notes** capability.</rule>

</rules>
```

## Verification

- Frontmatter matches the opencode format from the reference: `description`, `mode`, `permission` present.
- No knowledge, capability steps, or routing rules from `draft-release-notes` are duplicated — the wrapper only adds agent scope and delegation.
