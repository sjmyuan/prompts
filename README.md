# prompts
A collection of prompts used in my daily work

## Installing agents & skills

Use [`install-agents-skills.sh`](./install-agents-skills.sh) to install the
agents and skills in this repo into a workspace or your user profile for
**Copilot** (VS Code), **OpenCode**, and/or **Claude Code**:

```sh
./install-agents-skills.sh <target> <platform> [options]

# Install everything for all three tools into your user profile
./install-agents-skills.sh user all

# Install claude agents + skills into a specific project
./install-agents-skills.sh workspace claude --project ~/work/my-app

# Preview what would happen without changing anything
./install-agents-skills.sh user all --dry-run
```

- `<target>`: `user` | `workspace`
- `<platform>`: `copilot` | `opencode` | `claude` | `all`
- Options: `--project <path>` (workspace), `--scope agents|skills|all`,
  `--force`, `--dry-run`

Agents and skills are **symlinked as whole folders** into place (never copied),
so the repo remains the source of truth — `git pull` here updates every
installed agent and skill automatically. Targets already linked to this repo
are left alone; use `--force` to replace an existing target (e.g. a file copied
by an earlier version) with a link.

Source folders (linked whole): `copilot-agents/`, `opencode-agents/`,
`claude-agents/` for agents; `skills/` for skills.

## opencode-agents

Opencode-format copies of the agents in [`claude-agents/`](./claude-agents/).
Each file follows the [opencode agents spec](https://opencode.ai/docs/agents/).

> This folder is symlinked as a whole into `.opencode/agents` (or
> `~/.config/opencode/agents`) by `install-agents-skills.sh`, so it must contain
> **only** agent files — that is why this documentation lives here rather than
> as a `README.md` inside the folder.

### Files

| Agent | Purpose | Applies skill(s) |
|---|---|---|
| `blog-assistant.md` | **Primary** — conversational blog-writing assistant that gathers ideas, fills gaps, and maintains the article document | `write-blog` |
| `prompt-engineer.md` | **Primary** — crafts and refines effective prompts and agent files by applying the SKR framework | `craft-prompt` |
| `skill-creator.md` | **Primary** — creates and reviews skills (SKILL.md) by applying the create-skill / review-skill workflows | `create-skill`, `review-skill` |
| `adr-writer.md` | Draft Architecture Decision Records | `draft-adr` |
| `code-investigator.md` | Read-only codebase investigation | `investigate-code` |
| `code-reviewer.md` | Read-only code review | `review-code` |
| `coding-assistant.md` | Plan-only / execute-only / plan-then-execute code changes | `plan-development-task`, `execute-plan` |
| `executor.md` | Execute an existing plan (never plans) | `execute-plan` |
| `learner.md` | Extract knowledge from history (self-dispatch for parallelism) | `learn-from-history` |
| `orchestrate-delivery.md` | **Primary** — delivery orchestrator that dispatches the plan/execute/spike/ADR/solution-doc sub-agents and tracks the delivery index | `orchestrate-feature-delivery` |
| `planner.md` | Produce + persist a TDD plan (never executes) | `plan-development-task`, `investigate-code` |
| `solution-doc-writer.md` | Compile solution documents (C4, sequence, RAID/RACI) | `write-solution-doc` |
| `spike-conductor.md` | Orchestrate spike investigations + verify sub-agent results | `conduct-spike`, `question-everything` |

### Opencode agent spec (summary)

- One markdown file per agent; **the filename becomes the agent name** (e.g. `code-reviewer.md` → `code-reviewer`).
- Required frontmatter: `description`.
- `mode`: `primary` | `subagent` | `all` (default `all`). `orchestrate-delivery.md`, `blog-assistant.md`, and `skill-creator.md` are `primary`; the rest are `subagent` (dispatch targets).
- `permission`: per-tool `allow` | `ask` | `deny`.
- The markdown body is the agent's system prompt.

### How the conversion was done

- `name:` / `tools:` / `model: inherit` (Claude frontmatter) → `mode: subagent` + `permission:` (opencode frontmatter).
- Claude tool list → opencode permissions: `Glob/Grep/Read/List/LSP` → read-family, `Write/Edit` → `edit`, `Bash/KillShell/BashOutput` → `bash`, `TodoWrite` → `todowrite`, `Fetch` → `webfetch`; `skill: allow` everywhere, `websearch: deny` everywhere; read-only agents add `edit: deny`.
- Claude paths → opencode: `CLAUDE.md` → `AGENTS.md`, `.claude/agents/` → `.opencode/agents/`, `.claude/skills/` → `.opencode/skills/`.

### Notes

- Skills must be discoverable by opencode (`.opencode/skills/<name>/SKILL.md`, `.claude/skills/`, `.agents/skills/`, or the matching global locations) for the `skill` tool to load them.
- Subagent dispatch tables (in `spike-conductor.md` and `learner.md`) reference agents by name — those names resolve to the other files in this folder once installed.
