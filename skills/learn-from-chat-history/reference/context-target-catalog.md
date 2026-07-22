# Context Target Catalog

Each platform provides different persistent context mechanisms. This catalog describes the **types** of targets and what kinds of lessons suit each. The skill should detect which mechanisms are available on the current platform and map accordingly.

---

## Target Type: Personal Persistent Notes

**Also known as**: User preferences, global rules, personal configuration

**Suitability**: Personal preferences, workflow patterns, frequently used commands, individual coding conventions that span across projects.

**Lesson types that fit here**:
- "I prefer using `pnpm` over `npm` for all Node projects"
- "Always use `--verbose` when running tests locally"
- "I like error messages to include the file path and line number"

**Format**: Brief bullet points or single-line facts. Keep entries short — personal context may have limited window.

**Example entry**:
```markdown
## Package management
- Prefer `pnpm` over `npm` for all Node.js projects
```

**Do NOT put here**: Project-specific conventions (use project-level notes), domain knowledge (use skills), agent behavior rules (use agent files).

---

## Target Type: Project-Level Persistent Notes

**Also known as**: Workspace rules, project conventions, repo notes

**Suitability**: Project-specific conventions, build/test commands, architecture rules, known quirks of this codebase.

**Lesson types that fit here**:
- "This project requires Node 20+ because of the `import.meta.dirname` usage"
- "Run build before integration tests"
- "The auth module uses a custom JWT validation, not the framework default"
- "Never import from `@deprecated/utils` — use `@utils/v2` instead"

**Format**: Organized by topic in separate sections or files. Each covers one area (build, architecture, conventions).

**Example entry** (conventions):
```markdown
## Imports
- Never import from `@deprecated/utils` — use `@utils/v2` instead
- Barrel exports go through `index.ts` only; no deep imports
```

**Do NOT put here**: Personal preferences (use personal notes), general programming knowledge (use skills).

---

## Target Type: Skill File

**Suitability**: Domain-specific knowledge, capabilities, or rules that belong to an existing skill. The skill must already exist.

**Lesson types that fit here**:
- A new constraint or banned practice for the skill's domain → add to knowledge section
- A new routing rule → add to rules section
- A new procedure step discovered during execution → add to appropriate capability
- A new reference table or API signature → add to knowledge section or create a reference file

**Format**: Must follow skill conventions:
- Facts and reference tables → knowledge section
- Procedural steps → capabilities section, as a named capability
- Routing triggers → rules section, format: "When [scenario] → apply [capability]"

**Example entry** (in knowledge section):
```markdown
## Known limitations
- The edit-svg skill cannot handle SVG files with embedded JavaScript.
  If an SVG contains script tags, reject it and ask the user to provide a pure SVG.
```

**Do NOT put here**: Personal preferences, one-off commands, non-domain facts.

---

## Target Type: Agent/Instruction File

**Suitability**: Agent behavior rules, tool restrictions, workflow preferences that apply to a specific agent mode or assistant.

**File examples**: `.agent.md`, `.instructions.md`, system prompt configuration

**Lesson types that fit here**:
- "Never use shell execution for git operations — use git-specific tools directly"
- "When reviewing PRs, always check for SQL injection first"
- "This agent should always confirm before creating files in critical directories"

**Format**: Rules in a rules section or instructions in the main body, depending on the file structure.

**Example entry**:
```markdown
When modifying files in the database layer, always run the migration check script
before committing changes.
```

**Do NOT put here**: Domain knowledge (use skills), project conventions (use project notes).

---

## Target Type: Prompt File

**Suitability**: Prompt templates, role definitions, output format specifications.

**File examples**: `.prompt.md`, prompt configuration

**Lesson types that fit here**:
- "The prompt for this task should include a constraint about maximum output length"
- "Add a step to verify the output format before presenting results"

**Format**: Depends on the prompt file structure; typically Markdown with sections.

---

## Target Type: Project Documentation

**Suitability**: Project-level facts that all contributors should know.

**File examples**: README, ADR, Architecture Doc

**Lesson types that fit here**:
- A new prerequisite discovered during setup
- A known limitation that should be documented
- A configuration detail that took effort to discover
- An architectural decision that emerged from implementation

**Format**: Depends on the document type. For README: add to the relevant section. For ADRs: use the standard ADR template.

**Example entry** (in README):
```markdown
## Prerequisites
- Node.js ≥ 20.0.0 (required for `import.meta.dirname`)
- pnpm ≥ 8.0.0
```

---

## Target Type: Session-Scoped Context

**Suitability**: Task-specific context for the current conversation only. Rarely used for lessons — most worthwhile lessons should go to more persistent targets.

**Lesson types that fit here** (rare):
- "We decided to use approach B for this feature; the reasoning is in the conversation above"
- "The current task is blocked on PR #342 being merged"

**Format**: Brief notes; will be cleared after the session ends.

**Do NOT put here**: Anything that should persist beyond this session.

---

## Target Selection Heuristic

Use this priority order when multiple targets could fit:

1. **Skill file** (most discoverable, domain-scoped)
2. **Agent/Instruction file** (behavior-specific, auto-loaded)
3. **Project-level persistent notes** (project-scoped, persistent)
4. **Personal persistent notes** (cross-project, personal)
5. **Project documentation** (human-readable, shared)
6. **Prompt file** (template-specific)
7. **Session-scoped context** (temporary; last resort)

When in doubt, prefer the **more specific** target. A lesson about miniprogram development goes into the miniprogram skill, not personal notes. A lesson about git workflow goes into personal notes, not the project README.
