# opencode-agents

Opencode-format copies of the agents in [`../claude-agents/`](../claude-agents/). Each file follows the [opencode agents spec](https://opencode.ai/docs/agents/).

## Files

| Agent | Purpose | Applies skill(s) |
|---|---|---|
| `adr-writer.md` | Draft Architecture Decision Records | `draft-adr` |
| `code-investigator.md` | Read-only codebase investigation | `investigate-code` |
| `code-reviewer.md` | Read-only code review | `review-code` |
| `coding-assistant.md` | Plan-only / execute-only / plan-then-execute code changes | `plan-development-task`, `execute-plan` |
| `executor.md` | Execute an existing plan (never plans) | `execute-plan` |
| `learner.md` | Extract knowledge from history (self-dispatch for parallelism) | `learn-from-history` |
| `planner.md` | Produce + persist a TDD plan (never executes) | `plan-development-task`, `investigate-code` |
| `solution-doc-writer.md` | Compile solution documents (C4, sequence, RAID/RACI) | `write-solution-doc` |
| `spike-conductor.md` | Orchestrate spike investigations + verify sub-agent results | `conduct-spike`, `question-everything` |

## Opencode agent spec (summary)

- One markdown file per agent; **the filename becomes the agent name** (e.g. `code-reviewer.md` → `code-reviewer`).
- Required frontmatter: `description` (what the agent does and when to use it).
- `mode`: `primary` | `subagent` | `all` (default `all`). All agents here are `subagent` — they are dispatch targets in the delivery pipeline, mirroring the Claude Code sub-agents.
- `permission`: per-tool `allow` | `ask` | `deny`. Keys used here: `read`, `glob`, `grep`, `list`, `edit`, `bash`, `todowrite`, `lsp`, `webfetch`, `websearch`, `skill`.
- The markdown body is the agent's system prompt.

## Install

Copy the desired agents into opencode's agent directory:

- **Per-project**: `<project>/.opencode/agents/`
- **Global**: `~/.config/opencode/agents/`

```sh
# example — install all agents globally
mkdir -p ~/.config/opencode/agents
cp /path/to/prompts/opencode-agents/*.md ~/.config/opencode/agents/
```

Then invoke a subagent with `@name` (e.g. `@planner ...`) or let a primary agent dispatch it via the Task tool.

## How the conversion was done

- `name:` / `tools:` / `model: inherit` (Claude frontmatter) → `mode: subagent` + `permission:` (opencode frontmatter). The `name` is dropped because the filename is the name; `model` is omitted so subagents inherit the invoking agent's model.
- Claude tool list → opencode permissions: `Glob/Grep/Read/List/LSP` → read-family, `Write/Edit` → `edit`, `Bash/KillShell/BashOutput` → `bash`, `TodoWrite` → `todowrite`, `Fetch` → `webfetch`. `skill: allow` is granted because these agents load skills via opencode's `skill` tool. `websearch` is denied everywhere (no source agent had it). Read-only agents (`code-investigator`, `code-reviewer`) additionally set `edit: deny`.
- Claude-specific project-context paths adapted to opencode equivalents: `CLAUDE.md` → `AGENTS.md`, `.claude/agents/` → `.opencode/agents/`, `.claude/skills/` → `.opencode/skills/`, `.claude/rules/` → `AGENTS.md` rules (opencode has no `.opencode/rules/`; rules live in `AGENTS.md`).
- Fixed stale agent-name references `coding-reviewer` → `code-reviewer` in `planner.md` and `executor.md` (the claude-agents file is `code-reviewer.md`).

## Notes

- The agents reference skills by name (`draft-adr`, `plan-development-task`, `execute-plan`, `investigate-code`, `review-code`, `write-solution-doc`, `conduct-spike`, `learn-from-history`, `question-everything`). For opencode to load them via the `skill` tool, the skills must be discoverable in `.opencode/skills/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md`, or the matching global config locations.
- Subagent dispatch tables (in `spike-conductor.md` and `learner.md`) reference agents by name — those names resolve to the other files in this folder once installed.
