# Delivery State Machine

Canonical statuses and transitions for every cell in `orchestrate-feature-delivery`. The delivery index is the single source of truth; **update-delivery-index** and **reference/orchestration-guide.md** apply these transitions.

## Cell statuses

| Status | Meaning |
|---|---|
| **unplanned** | No plan files yet |
| **planned** | `plan.md` + `context.md` exist, verified on disk |
| **in-progress** | Execution running or complete, not yet verified |
| **verified** | Independent verification gate passed; awaits merge |
| **done** | PR merged (recorded head commit included) or user-confirmed |
| **failed** | Agent error (reason recorded) |
| **blocked** | Waiting on a dependency merge or user decision |
| **poc-ready** | POC implemented + evaluation report written, gate passed |
| **adopted** / **rejected** | User-recorded POC decision |
| **superseded** | Existing implementation replaced by an adopted POC |

## Transitions

`unplanned → planned → in-progress → verified → done`, plus recoverable `failed` / `blocked`.

- **in-progress** covers execution running or complete, not yet verified.
- **verified** requires the independent verification gate (**verify-cell**) to pass.
- POC cells fork: `verified → poc-ready → adopted | rejected`; adopted → promote → merge → `done`.
- A replaced cell is **superseded**.
- The user records POC **adopted**/**rejected** in the index — the orchestrator never decides.

## Readiness predicates

| Predicate | Condition |
|---|---|
| **develop-ready** | All dependency cells are **planned** (contracts agreed) |
| **execute-ready** | Cell is **planned** AND its plan file is verified on disk |
| **verify-ready** | Cell is **in-progress** AND `plan.md` shows every step ✅ with the `## Execution` handoff recorded |
| **merge-ready** | Cell is **verified** AND all dependency cells are **done** |

## Gate waiver

The independent gate is mandatory. A user may explicitly waive it for a specific cell; record the waiver (cell, reason, who) in the index before marking **done**. Never waive silently.
