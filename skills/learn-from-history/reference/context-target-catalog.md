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

**Suitability**: Project-specific conventions, build/test commands, architecture rules, known quirks of this codebase. **This is the most common target for PR-derived and git-history-derived lessons**, as they are typically project-scoped.

**Lesson types that fit here**:
- "This project requires Node 20+ because of the `import.meta.dirname` usage"
- "Run build before integration tests"
- "The auth module uses a custom JWT validation, not the framework default"
- "Never import from `@deprecated/utils` — use `@utils/v2` instead"
- "When implementing stories involving the payment module, always add a rollback test" (PR-derived)
- "All API responses from the billing service can return partial data; always handle the `partial` flag" (git-history-derived)

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
- Code-change-derived patterns that are domain-specific (e.g., a PR revealed a constraint in a framework the skill covers) → add to knowledge section

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
- "When analyzing a PR against a story, always check the test files first" (PR-derived)

**Format**: Rules in a rules section or instructions in the main body, depending on the file structure.

**Example entry**:
```markdown
When modifying files in the database layer, always run the migration check script
before committing changes.
```

**Do NOT put here**: Domain knowledge (use skills), project conventions (use project notes).

---

## Target Type: Skill File (Capability Section)

**Suitability**: Multi-step procedures extracted from historical sources that describe how to accomplish a recurring task following team conventions. These become named capabilities within the skill's `<capabilities>` section.

**Lesson types that fit here**:
- An implementation recipe extracted from multiple PRs (e.g., "how to add a new API endpoint in this codebase")
- A described procedure extracted from Slack/Teams (e.g., "how to deploy a hotfix")
- A refined capability produced by abstracting multiple similar procedures (e.g., merging "deploy service" and "deploy hotfix" into a general "deploy to environment" capability)

**Format**: Must follow capability conventions:
- **Name**: Action-verb phrase in kebab-case inside angle brackets (e.g., `<deploy-hotfix>`)
- **Objective**: One sentence describing the goal
- **Steps**: Numbered list, each starting with an imperative action verb
- **Parameters** (optional): Table of what varies per instance
- **Evolution note** (if refined via the refine phase of `extract-and-refine-capability`): What was merged and why

**Example entry** (in capabilities section):
```markdown
<deploy-hotfix>
**Objective**: Deploy a critical fix to production quickly while following the team's hotfix protocol.

**Steps**:
1. Create a hotfix branch from the latest release tag: `git checkout -b hotfix/<issue-id> <release-tag>`
2. Apply the fix and commit with prefix `hotfix:`
3. Open a PR against `main` — request expedited review from the on-call engineer
4. After approval, merge to `main` and immediately tag: `git tag -a v<version>-hotfix<seq>`
5. Trigger the deploy pipeline for the new tag and monitor the #alerts channel for 15 minutes

**Parameters**:
| Parameter | Description | Example |
|---|---|---|
| `<issue-id>` | Jira issue or bug ID | `ENG-421` |
| `<release-tag>` | Latest release tag to branch from | `v2.3.1` |
| `<version>` | New version after the hotfix | `2.3.2` |
| `<seq>` | Hotfix sequence number for this version | `1` |
</deploy-hotfix>
```

**Do NOT put here**: Single-step actions (capture as knowledge), generic best practices, personal preferences.

---

## Target Type: Project-Level Persistent Notes (How-To Guide)

**Suitability**: Procedures that are project-specific but don't belong to a domain skill. When no relevant skill exists, procedures can be stored as how-to guides in project-level notes.

**Lesson types that fit here**:
- A project-specific setup or onboarding procedure (e.g., "how to set up the local dev environment")
- A cross-cutting procedure that spans multiple domains (e.g., "how to add a new microservice to the cluster")
- A procedure discovered from communication tool history that's too operational for a domain skill

**Format**: Section heading with the task name, followed by numbered steps with any prerequisites and parameters noted.

**Example entry**:
```markdown
## How to add a new microservice to the cluster

1. Create the service repo from the `microservice-template` GitHub template
2. Add the service to `infra/service-registry.yaml` with port and health-check endpoint
3. Add CI config: copy `.github/workflows/deploy-template.yml` and set `SERVICE_NAME`
4. Register the service in the API gateway at `gateway/routes.yaml`
5. Deploy the gateway first, then the new service
```

**Do NOT put here**: Domain-specific procedures that fit in a skill (use skill files), personal workflow preferences (use personal notes).
