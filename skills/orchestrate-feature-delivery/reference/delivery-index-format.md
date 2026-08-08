# Delivery Index Format

The delivery index is written next to the spike artifacts (same folder as the change summary / solution doc). It is the epic's **single source of truth for state** — the orchestrator reads it to decide next actions, updates it as agents report, and uses its **Spike References** so every agent brief can point agents at the full spike output.

## Structure

```markdown
# Delivery Index: [Spike Goal]

## Summary
[N features · M repos · W waves · critical path: F_x → F_y]

## Spike References
- **Change summary**: [path — the full change list]
- **Solution doc**: [path — target-state section per feature]
- **ADRs**: [paths — one per decision area]

## Repos
- repo-a — [what changes here]
- repo-b — [...]

## Features
### F1: [kebab-case-name] — Wave [n]
- **Description**: [one line]
- **ADRs**: [ADR-00X ...]
- **Change summary items**: [item ids]
- **Repos**: repo-a (PR) · repo-c (PR)
- **Intra-feature merge order**: repo-c → repo-a
- **Dependencies**: blocked-by [F2] (merge-blocked) · blocks [F4]
- **Develop / merge**: develop now · merge after [F2] merges

## Waves
### Wave 0 (parallel)
- F1, F3
### Wave 1 (merge after wave 0)
- F2 (after F1 merges)

## Cell plan status
| Cell | Branch | Status | Agent | Plan location |
|---|---|---|---|---|
| repo-a/F1 | 1234-f1-api | planned | agent-A | docs/feature-implementations/repo-a/f1/ |
| repo-b/F2 | f2-schema | in-progress | agent-B | docs/feature-implementations/repo-b/f2/ |
| repo-c/F4 | — | unplanned | — | — |
```

## Per-cell scope brief

Each cell carries a brief that seeds **plan-development-task**:

- **Feature**: ID + name + one-line description
- **Repo**: repo name
- **Scope**: change-summary items + ADR refs + target-state section
- **Spike references**: the file paths + section pointers (from **Spike References**) the agent should load for full context
- **Dependency context**: what must be merged before this cell's PR (other repos / features)
- **Constraints**: one PR per repo per feature (soft — may merge with other features when convenient)
- **Branch**: the branch name to use for this cell, matching the **repo's branch convention** (per **branch-and-push-conventions**); created during the agent's Prepare Environment step, pushed only after user confirmation

## Status lifecycle

- **unplanned** → **planned**: a planning agent wrote `plan.md` + `context.md`
- **planned** → **in-progress**: an execution agent started
- **in-progress** → **done**: PR merged / code verified
- any → **failed** (reason): recover by re-plan or retry
- any → **blocked** (blocker): waits for a dependency merge or user decision

## Ready-to-dispatch predicate

A cell is ready when: **all wave-dependency cells are done** AND status is **unplanned** or **planned**.

## Status semantics

| Status | Meaning | Orchestrator action |
|---|---|---|
| **unplanned** | No plan files yet | Dispatch a planning agent (plan-development-task) |
| **planned** | `plan.md` + `context.md` exist | Dispatch an execution agent (execute-plan) |
| **in-progress** | Execution running | Resume from the last completed step |
| **done** | Merged / verified | Skip; unlock downstream cells |
| **failed** | Agent error (reason recorded) | Ask user: re-plan or retry |
| **blocked** | Waiting on blocker (recorded) | Wait; re-check when blocker clears |

## Rework after implementation

When an issue is found on a **done** cell, record the rework without erasing history:

- Keep the original cell status **done** and append a **Rework** note, e.g. `Rework: F2-r1 · ADR-002 focused spike · appended plan docs/feature-implementations/order-service/f2/plan.md (## Rework 2026-08-08)`.
- Add the rework as a new feature/cell (e.g., `F2-r1`) in a **new wave** after the original feature — it depends on the original cell's PR (already merged).
- The appended plan lives at the end of the feature's existing `plan.md` (or a sibling `rework-plan.md`); implemented steps are never modified.
