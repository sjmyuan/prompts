# Agent File Formats by Platform

Copilot, Claude, and opencode agent files share a SKR body but differ in frontmatter, file suffix, and tool declarations.

## Platform comparison

| Platform | File suffix | Frontmatter required | Tool declaration |
|---|---|---|---|
| Claude | `.md` | `description` | `tools` list |
| Opencode | `.md` | `description`, `mode`, `permission` | `permission` map |
| Copilot | `.agent.md` | `name`, `description` | none (default toolset) |

## Claude format

```
---
name: agent-name
description: "One-line purpose"
tools: Read, Write, Edit, Bash, Glob, Grep
model: inherit
---
```

- `tools`: allowlist; omit for the default toolset
- `model: inherit`: recommended

## Opencode format

```
---
description: "One-line purpose"
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

- `mode`: `primary` | `subagent` | `all` (default `all`)
- `permission`: per-tool `allow` | `ask` | `deny`
- read-only agents add `edit: deny`

## Copilot format

```
---
name: agent-name
description: 'One-line purpose'
---
```

- no tool field; Copilot agents use the default toolset

## Tool mapping

| Task need | Claude `tools` | Opencode `permission` |
|---|---|---|
| Read files | Read | `read: allow` |
| Search | Glob, Grep | `glob: allow`, `grep: allow` |
| Edit files | Write, Edit | `edit: allow` |
| Run commands | Bash | `bash: allow` |
| Track tasks | TodoWrite | `todowrite: allow` |
| Fetch URLs | Fetch | `webfetch: allow` |
| Load skills | (skill tool) | `skill: allow` |
| Web search | — | `websearch: deny` |
