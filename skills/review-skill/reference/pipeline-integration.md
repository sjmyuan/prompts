# Integration Review — Skills and Sub-Agents

A skill integrates along two axes: with **other skills** (producer→consumer pipelines) and with **sub-agents** (the skill dispatches them, or is itself loaded inside one). A skill may have either, both, or neither — verify only the axes that apply.

## Axis 1 — Skill↔Skill pipelines

When a skill references or is referenced by another skill, verify 4 points:

1. **Handoff mechanism** — file-based export/import between skills; the user is not the transport layer. A producing skill offers an export capability; a consuming skill defines an input schema and loads from files. Text-only handoff → 🟡 Minor (fragile — context resets lose the plan).
2. **Shared schema** — the downstream skill documents the format it accepts (minimum fields, formats). Mismatched format → 🟡 Minor.
3. **Bidirectional awareness** — each skill names the other in its description, skill-boundary, or rules. Missing cross-reference → 🟡 Minor.
4. **Guard clauses** — the downstream skill's when-to-use prevents premature loading (e.g., "Do NOT load when no plan has been generated yet"). Absence → 🟡 Minor (both skills could load simultaneously).

## Axis 2 — Skill↔Sub-agent integration

Two asymmetric directions with inverted trust and context flow. Gap severity: gaps that make a dispatched/embedded agent fail → 🔴 Major; incomplete-but-workable gaps → 🟡 Minor.

### Direction A — Skill dispatches sub-agents (orchestration)

The skill's capabilities dispatch agents to execute work units (e.g., `conduct-spike`, `learn-from-history`). Verify:

1. **Handoff (dispatch brief)** — the skill defines a brief template (context, scope, expected output) and carries all needed seed files, since the agent cannot see the parent conversation. Missing template → 🟡 Minor.
2. **Output contract** — the skill requires a structured return format from the agent (e.g., evidence map, draft document). Missing → 🟡 Minor.
3. **Availability detection & fallback** — the skill detects suitable agents and falls back to direct execution when none exist. No fallback → 🟡 Minor.
4. **Verification loop** — returned results are questioned and verified with a NEW same-type agent, never the original instance. No verification → 🔴 Major.
5. **Result merging** — parallel results are collected, de-duplicated, synthesized, and cross-checked across work units. Undefined → 🟡 Minor.
6. **Safety boundary** — read-only agents are told not to write files; write agents get explicit artifact paths. Missing → 🟡 Minor.

### Direction B — Skill loaded by a sub-agent (embedded execution)

A parent dispatches an agent with "load skill X, apply capability Y" (e.g., `draft-adr`, `write-solution-doc` inside `conduct-spike` briefs). Verify:

1. **Input schema** — the skill documents what a seeding brief must provide before it can execute. Undefined → 🟡 Minor.
2. **Self-containment** — the skill executes without the parent's conversational context. Depends on parent-conversation state → 🔴 Major (the dispatched agent fails headless).
3. **Return contract** — the skill states what the agent returns to the orchestrator (e.g., "return the assumed solution"). Missing → 🟡 Minor.
4. **Bidirectional awareness** — the skill names the agent types it expects, and/or the agent definition names the skill. Missing → 🟡 Minor.
5. **Guard clause** — loading without the seed input is prevented. Absence → 🟡 Minor.

## Cross-references

- `conduct-spike` **reference/multi-agent-orchestration.md** — dispatch pattern, why to dispatch even a single task
- `conduct-spike` **reference/verification-protocol.md** — verification loop, independence rules, traps
- `learn-from-history` **reference/agent-orchestration-pattern.md** — agent detection protocol, prompt templates
