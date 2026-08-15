# Delivery Index Format

The delivery index is written at **`deliveries/<epic-name>/index.md`** — one folder per epic (no `docs/` prefix), named after the spiked epic (`<epic-name>` = spike name). The spike's own artifacts stay untouched in the spike folder (`spikes/<spike-name>/`; ADRs in `adrs/`, solution + change summary at the root, findings in `docs/`) and are referenced from the index via **Spike References**. The index is the epic's **single source of truth for state** — the orchestrator reads it to decide next actions, updates it as agents report, and uses its **Spike References** so every agent brief can point agents at the full spike output.

## Concise writing

The index is table-first; prose states takeaways only (see **reference/writing-style.md**).

- **Summary**: one line — `N features · M repos · W waves · critical path: F_x → F_y`.
- **Feature description**: one sentence; dependencies/statuses live in tables.
- **Spike References**: one bullet per artifact (path — what it provides).
- No narrative paragraphs, no process narration ("I dispatched…"), no meta-commentary.

## Delivery layout

```
deliveries/<epic-name>/               # one folder per epic (no docs/ prefix)
├── <repo-name>/                      # one folder per repo
│   ├── <feature-name>/               # one folder per feature for this repo
│   │   ├── context.md                # distilled spike context + spike references
│   │   └── plan.md                   # TDD plan (plan-development-task)
│   └── ...
└── index.md                          # delivery index (single source of truth)
```

## Structure

```markdown
# Delivery Index: [Spike Goal]

## Summary
[N features · M repos · W waves · critical path: F_x → F_y]

## Spike References
- **Change summary**: [path — the full change list]
- **Solution doc**: [path — target-state section per feature]
- **ADRs**: [paths — one per decision problem (area-prefixed)]

## Repos
- repo-a — [what changes here]
- repo-b — [...]

## Features
### F1: [kebab-case-name] — Wave [n]
- **Description**: [one line]
- **ADRs**: [adr-<area>-<NN>-<problem>.md ...]
- **Change summary items**: [item ids]
- **Type**: `poc` (optional) — **ADR**: adr-<area>-<NN>-<problem>.md · **Option**: [option] · **Success criteria**: [measurable] · **Replaces**: F2 (optional) · **Compare**: F5 (optional, sibling POC)
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
| repo-a/F1 | 1234-f1-api | planned | agent-A | deliveries/<epic-name>/repo-a/wallet-contracts/ |
| repo-b/F2 | f2-schema | in-progress | agent-B | deliveries/<epic-name>/repo-b/wallet-service/ |
| repo-c/F4 | — | unplanned | — | — |
```

Plan locations use the feature's **kebab-case name** (e.g. `wallet-contracts` for F1), never its ID (`F1`).

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
- POC cells: **in-progress** → **poc-ready** (evaluation report written) → **adopted** (promote → merge → done) or **rejected** (closed); a replaced feature is marked **superseded**
- any → **failed** (reason): recover by re-plan or retry
- any → **blocked** (blocker): waits for a dependency merge or user decision

## Ready-to-dispatch predicate

- **Ready to develop** (dispatch plan/execute): all dependency cells are **planned** (contracts agreed — contract-first and independent cells develop in parallel; merge-blocked cells wait for the dependency's contract).
- **Ready to merge**: all dependency cells are **done** (merged).
- Status must be **unplanned** (→ plan) or **planned** (→ execute).

## Status semantics

| Status | Meaning | Orchestrator action |
|---|---|---|
| **unplanned** | No plan files yet | Dispatch a planning agent (plan-development-task) |
| **planned** | `plan.md` + `context.md` exist | Dispatch an execution agent (execute-plan) |
| **in-progress** | Execution running — incl. implemented-but-not-yet-merged cells awaiting push approval | Resume from the last completed step; pre-merge rework appends like post-merge |
| **poc-ready** | POC implemented + evaluation report written | Wait for the user to record **adopted**/**rejected** in the index |
| **adopted** | POC proved the option | Promote (merge → done) or feed the **poc-gated** feature |
| **rejected** | POC failed the criteria | Close the cell; delivery proceeds on the other option |
| **superseded** | Existing implementation replaced by an adopted POC | Skip; keep as history |
| **done** | Merged / verified | Skip; unlock downstream cells |
| **failed** | Agent error (reason recorded) | Ask user: re-plan or retry |
| **blocked** | Waiting on blocker (recorded) | Wait; re-check when blocker clears |

## POC cells

A POC proves one option of one ADR as a **standalone feature** (see **poc-definition** in the SKILL.md knowledge). Record it in the index with `Type: poc` + the metadata above, and track statuses per the lifecycle above.

- **Compare POCs**: sibling POC cells (one per option) run in parallel in an early wave; the implementing feature depends on its POC via a **poc-gated** edge and is never dispatched before the decision.
- **Decision gate**: at **poc-ready**, the user reads the evaluation report vs success criteria and records **adopted**/**rejected** directly in the index — the orchestrator never evaluates or decides; the ADR records the outcome.
- **Adopt**: **POC-as-implementation** — promote the branch (merge → done; mark `replaces` **superseded**); **POC-as-decision-input** — close the POC, dispatch the **poc-gated** feature with the decided option.
- **Reject**: close the cell (branch archived or discarded); delivery proceeds on the other option.

## Rework after implementation

Record rework according to the cell's status (see **rework-modes** in the SKILL.md knowledge).

**Post-merge (cell done)** — record without erasing history:

- Keep the original cell status **done** and append a **Rework** note, e.g. `Rework: F2-r1 · adr-wallet-01-payment-failure-handling.md focused spike · appended plan deliveries/<epic-name>/order-service/wallet-service/plan.md (## Rework 2026-08-08)`.
- Add the rework as a new feature/cell (e.g., `F2-r1`) in a **new wave** after the original feature — it depends on the original cell's PR (already merged).
- The appended plan lives at the end of the feature's existing `plan.md` (or a sibling `rework-plan.md`); implemented steps are never modified.

**Pre-merge (cell in-progress — implemented but not merged/committed/pushed)** — same append-only rule, no new feature/wave:

- Keep the cell's identity and **in-progress** status; no new feature/wave.
- Note the rework, e.g. `Rework: appended plan deliveries/<epic-name>/order-service/order-wallet-integration/plan.md (## Rework 2026-08-08)`.
- A `## Rework <date>` section is appended to the existing `plan.md` (implemented steps never modified); the cell proceeds to push approval after the rework.
