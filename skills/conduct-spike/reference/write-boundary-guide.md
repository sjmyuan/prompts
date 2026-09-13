# Write-Boundary Guide

Backs the **write-boundary** knowledge entry and the spike write-boundary check. A spike produces documented decisions, never production code — every write stays inside the spike folder.

## Allowed vs forbidden writes

| May write — inside the spike folder (`**/spikes/**`) | Never write |
|---|---|
| `scope.md`, `docs/findings-<area>.md`, `adrs/adr-*.md`, `solution.md` | code, config, tests, infrastructure, scripts, any file outside the spike folder |
| Throwaway diagrams embedded in spike markdown | prototypes, proof-of-concept code, or any executable artifact |

The spike folder always carries a `spikes/` path segment (`<base>/spikes/<spike-name>/`), which anchors the boundary.

## Enforcement layers

| Layer | Where | Strength |
|---|---|---|
| Path-scoped `edit` permission (allow `**/spikes/**`, deny the rest) | Spike-conductor agent | Hard block |
| Doc-scoped `edit` permission (allow `*.md`, deny the rest) | ADR/findings/solution writers | Hard block on non-docs |
| Write-boundary doctrine + rules | Skill and agent files | Intent |
| Brief Constraints + Report-back | Every dispatch brief | Intent, per dispatch |
| Boundary check | After each write capability | Detection |

Platforms without an agent permission layer rely on the doctrine and rules alone.

## Boundary check (after every write capability)

1. List changed paths with a read-only command (e.g., `git status --porcelain`).
2. Confirm every changed path contains a `spikes/` segment.
3. On any out-of-folder change: stop, do not save further artifacts, and report the offending paths to the user.
4. Ask the user to revert the out-of-folder change before the spike continues.

The check is the compensating control for `bash: allow` — shell commands can write files, so detection is mandatory.

## Recording implementation needs

A spike never implements. When the investigation concludes code, config, or tests must change:

1. Record the need as an **out-of-scope / next actions** note in `scope.md` (or the affected `solution.md` section).
2. Do not create a plan, prototype, or handoff artifact.
3. Tell the user to run `orchestrate-feature-delivery` — it drives the **planner** then the **executor** to touch code.
