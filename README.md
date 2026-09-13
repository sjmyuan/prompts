# gg-daily-workbench
A collection of agents and skills used in my daily work

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
| `algorithm-assistant.md` | **Primary** — conversational algorithm design assistant that clarifies, explores cases, brainstorms, explains, and designs algorithms bilingually | `design-algorithm` |
| `blog-assistant.md` | **Primary** — conversational blog-writing assistant that gathers ideas, fills gaps, and maintains the article document | `write-blog` |
| `user-story-writer.md` | **Primary** — conversational user-story writer that drafts, refines, and updates user stories (incl. Jira/Azure DevOps) | `draft-user-story` |
| `prompt-engineer.md` | **Primary** — crafts and refines effective prompts and agent files by applying the SKR framework | `craft-prompt` |
| `skill-creator.md` | **Primary** — creates, edits, and reviews skills (SKILL.md) by applying the create-skill / review-skill workflows | `create-skill`, `review-skill` |
| `adr-writer.md` | Draft Architecture Decision Records | `draft-adr` |
| `code-investigator.md` | **Primary** — read-only codebase investigation | `investigate-code` |
| `code-reviewer.md` | **Primary** — read-only code review | `review-code` |
| `executor.md` | Execute an existing plan (never plans) | `execute-plan` |
| `learner.md` | Extract knowledge from history (self-dispatch for parallelism) | `learn-from-history` |
| `orchestrate-delivery.md` | **Primary** — delivery orchestrator that dispatches the plan/execute/spike/ADR/solution-doc sub-agents and tracks the delivery index | `orchestrate-feature-delivery` |
| `planner.md` | Produce + persist a TDD plan (never executes) | `plan-development-task`, `investigate-code` |
| `solution-doc-writer.md` | Compile solution documents (C4, sequence, RAID/RACI) | `write-solution-doc` |
| `spike-conductor.md` | **Primary** — orchestrate spike investigations + verify sub-agent results | `conduct-spike`, `question-everything` |

### Opencode agent spec (summary)

- One markdown file per agent; **the filename becomes the agent name** (e.g. `code-reviewer.md` → `code-reviewer`).
- Required frontmatter: `description`.
- `mode`: `primary` | `subagent` | `all` (default `all`). `algorithm-assistant.md`, `blog-assistant.md`, `code-investigator.md`, `code-reviewer.md`, `orchestrate-delivery.md`, `prompt-engineer.md`, `skill-creator.md`, `spike-conductor.md`, and `user-story-writer.md` are `primary`; the rest are `subagent` (dispatch targets).
- `permission`: per-tool `allow` | `ask` | `deny`.
- The markdown body is the agent's system prompt.

### How the conversion was done

- `name:` / `tools:` / `model: inherit` (Claude frontmatter) → `mode: subagent` + `permission:` (opencode frontmatter).
- Claude tool list → opencode permissions: `Glob/Grep/Read/List/LSP` → read-family, `Write/Edit` → `edit`, `Bash/KillShell/BashOutput` → `bash`, `TodoWrite` → `todowrite`, `WebFetch` → `webfetch`; `skill: allow` everywhere, `websearch: deny` everywhere; read-only agents add `edit: deny`.
- Claude paths → opencode: `CLAUDE.md` → `AGENTS.md`, `.claude/agents/` → `.opencode/agents/`, `.claude/skills/` → `.opencode/skills/`.

### Notes

- Skills must be discoverable by opencode (`.opencode/skills/<name>/SKILL.md`, `.claude/skills/`, `.agents/skills/`, or the matching global locations) for the `skill` tool to load them.
- Subagent dispatch tables (in `spike-conductor.md` and `learner.md`) reference agents by name — those names resolve to the other files in this folder once installed.

## Agent dispatch per platform

An agent that dispatches sub-agents must declare the capability in its frontmatter, or the dispatch silently fails on that platform:

| Platform | Mechanism | Declaration |
|---|---|---|
| opencode | `task` permission allowlist | `task: { "*": deny, "<agent>": allow }` |
| Claude Code | `Task` tool (renamed `Agent`; `Task` remains an alias) | include `Task` (or `Agent`) in the comma-separated `tools:` list |
| VS Code Copilot | `agents` list + the `agent` tool | `agents: ['planner', ...]` (omit `tools` to keep all tools) |

Dispatching agents and their targets:

| Agent | Dispatches |
|---|---|
| `orchestrate-delivery` | planner, executor, code-reviewer, spike-conductor, adr-writer, solution-doc-writer |
| `spike-conductor` | code-investigator, adr-writer, solution-doc-writer |
| `learner` | learner (self-dispatch) |
| `code-reviewer` | code-reviewer (fan-out) |
| `code-investigator` | code-investigator (fan-out) |

- **Self-dispatch / fan-out**: opencode and Claude allow an agent to invoke itself by default; VS Code Copilot requires the `chat.subagents.allowInvocationsFromSubagents` setting for a self-referential `agents` entry.
- opencode defaults unspecified tools to `allow`; the explicit `task` allowlists above exist only where dispatch is restricted.

