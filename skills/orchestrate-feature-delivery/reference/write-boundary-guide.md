# Write-Boundary Guide

Backs the **write-boundary** knowledge entry and the delivery write-boundary check. The orchestrator maintains delivery docs only — it never writes code or any file outside the delivery folder.

## Allowed vs forbidden writes

| May write — inside the delivery folder (`**/deliveries/**`) | Never write |
|---|---|
| `index.md` | code, config, tests, infrastructure, scripts, `plan.md` / `context.md` / `rework-<date>.md`, any file outside the delivery folder |

The delivery folder always carries a `deliveries/` path segment (`<base>/deliveries/<epic-name>/`), which anchors the boundary. The `plan.md` / `context.md` / `rework-<date>.md` files inside it are owned by the dispatched **planner** and **executor** — the orchestrator never writes them; gate findings go straight to the planner and the index tracks status only.

## Enforcement layers

| Layer | Where | Strength |
|---|---|---|
| `edit` permission — `"*": "deny"`, `"**/deliveries/**": "allow"` | Orchestrator agent (opencode) | Hard block |
| `task` allowlist — planner / executor / code-reviewer / spike-conductor / adr-writer / solution-doc-writer | Orchestrator agent (opencode) | Blocks unexpected agents |
| Write-boundary doctrine + rules | Skill and agent files (all platforms) | Intent |
| Boundary check | After each index write | Detection |

Copilot and Claude agent files have no permission layer — the doctrine and rules carry the boundary there.

## Boundary check (after every index write)

1. List changed paths with a read-only command (e.g., `git status --porcelain`).
2. Confirm every changed path contains a `deliveries/` segment.
3. On any out-of-folder change: stop, do not save further updates, and report the offending paths to the user.
4. Ask the user to revert the out-of-folder change before delivery continues.

The check is the compensating control for `bash: allow` — shell commands can write files, so detection is mandatory.

## Implementation is delegated, never done here

Code changes are produced only by the dispatched **executor** (execute-plan); planning is delegated to the **planner**. When a plan or execution surfaces a change outside the delivery docs, dispatch the owning agent per **agent-dispatch** — never write it from the orchestrator.
