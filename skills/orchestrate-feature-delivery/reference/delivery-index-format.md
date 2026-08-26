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
- **Rework of**: F2 (optional — rework cell that fixes a delivered feature; see **Rework after implementation**)
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
| Cell | Branch | PR | Commit | Status | Agent | Plan location |
|---|---|---|---|---|---|---|
| repo-a/F1 | 1234-f1-api | — | — | planned | agent-A | deliveries/<epic-name>/repo-a/wallet-contracts/ |
| repo-b/F2 | f2-schema | #42 | e5f6a7b | in-progress | agent-B | deliveries/<epic-name>/repo-b/wallet-service/ |
| repo-c/F4 | — | — | — | unplanned | — | — |
```

Plan locations use the feature's **kebab-case name** (e.g. `wallet-contracts` for F1), never its ID (`F1`). **Branch**, **PR**, and **Commit** are pointers — always tracked in the index (easy to find, easy to verify); work history stays in `plan.md` / `context.md`. The branch is recorded when the cell is planned; the **Commit** (head commit from the execution handoff) once the cell first commits; the PR reference (number or URL) once a PR is opened — `—` until then. A cell is **done** only when its merged PR includes the recorded head commit (or the user confirms verified).

## Per-cell scope brief

Each cell carries a brief that seeds **plan-development-task**:

- **Feature**: ID + name + one-line description
- **Repo**: repo name
- **Scope**: change-summary items + ADR refs + target-state section
- **Spike references**: the file paths + section pointers (from **Spike References**) the agent should load for full context
- **Dependency context**: what must be merged before this cell's PR (other repos / features)
- **Constraints**: one PR per repo per feature (soft — may merge with other features when convenient)
- **Branch**: the branch name to use for this cell, matching the **repo's branch convention** (per **branch-and-push-conventions**); created during the agent's Prepare Environment step, pushed only after user confirmation
- **PR**: the pull-request reference (number or URL) to record in the index once the PR is opened (per **branch-and-push-conventions**); `—` until then
- **Commit**: the head commit the execution agent reports on handoff, recorded in the index (per **branch-and-push-conventions**); `—` until the first commit

## Status lifecycle

- **unplanned** → **planned**: a planning agent wrote `plan.md` + `context.md`
- **planned** → **in-progress**: an execution agent started
- **in-progress** → **done**: PR merged (with the recorded head commit) / code verified
- POC cells: **in-progress** → **poc-ready** (evaluation report written) → **adopted** (promote → merge → done) or **rejected** (closed); a replaced feature is marked **superseded**
- any → **failed** (reason): recover by re-plan or retry
- any → **blocked** (blocker): waits for a dependency merge or user decision

## Ready-to-dispatch predicate

- **Ready to develop**: all dependency cells are **planned** (contracts agreed — contract-first and independent cells develop in parallel; merge-blocked cells wait for the dependency's contract).
- **Ready to execute**: cell is **planned** AND its plan file is verified on disk at the recorded Plan location (the plan-first gate).
- **Ready to merge**: all dependency cells are **done** (merged).
- Status must be **unplanned** (→ planner) or **planned** with a verified plan file (→ executor).

## Status semantics

| Status | Meaning | Orchestrator action |
|---|---|---|
| **unplanned** | No plan files yet | Dispatch the **planner** (plan-development-task) |
| **planned** | `plan.md` + `context.md` exist (verified on disk) | Dispatch the **executor** (execute-plan) — only after the plan-file gate passes |
| **in-progress** | Execution running — incl. implemented-but-not-yet-merged cells awaiting push approval | Resume from the last step in the active `rework-<date>.md` (per the `context.md` manifest), or `plan.md` if no rework; pre-merge rework needs no index change |
| **poc-ready** | POC implemented + evaluation report written | Wait for the user to record **adopted**/**rejected** in the index |
| **adopted** | POC proved the option | Promote (merge → done) or feed the **poc-gated** feature |
| **rejected** | POC failed the criteria | Close the cell; delivery proceeds on the other option |
| **superseded** | Existing implementation replaced by an adopted POC | Skip; keep as history |
| **done** | Merged / verified (PR + head commit recorded) | Skip; unlock downstream cells |
| **failed** | Agent error (reason recorded) | Ask user: re-plan or retry |
| **blocked** | Waiting on blocker (recorded) | Wait; re-check when blocker clears |

## POC cells

A POC proves one option of one ADR as a **standalone feature** (see **poc-definition** in the SKILL.md knowledge). Record it in the index with `Type: poc` + the metadata above, and track statuses per the lifecycle above.

- **Compare POCs**: sibling POC cells (one per option) run in parallel in an early wave; the implementing feature depends on its POC via a **poc-gated** edge and is never dispatched before the decision.
- **Decision gate**: at **poc-ready**, the user reads the evaluation report vs success criteria and records **adopted**/**rejected** directly in the index — the orchestrator never evaluates or decides; the ADR records the outcome.
- **Adopt**: **POC-as-implementation** — promote the branch (merge → done; mark `replaces` **superseded**); **POC-as-decision-input** — close the POC, dispatch the **poc-gated** feature with the decided option.
- **Reject**: close the cell (branch archived or discarded); delivery proceeds on the other option.

## ADR changes mid-delivery

ADRs are **versionless** — drift is signaled by the **adr-writer** agent's return or the user's report, never by diffing the ADR. Routing by status: **reference/orchestration-guide.md** (ADR changes). Record each cell's re-route (status + note) in the index before dispatching.

## Rework after implementation

The index tracks **state only** — rework never adds work history to a status cell. Record rework per the cell's status (see **rework-modes** in the SKILL.md knowledge); the details (trigger, ADR focus, boundary, steps) live in a sibling `rework-<date>.md` — written by **plan-development-task**, never repeated in the index. `plan.md` is the frozen original; each rework gets its own file so it never grows. A `## Reworks` manifest in `context.md` lists every rework file + status (see **plan-file-format.md** in **plan-development-task**).

**Post-merge (cell done)** — original cell unchanged, rework is its own cell:

- Keep the original cell exactly as-is (status **done**; no note, no history).
- Add the rework as a new feature/cell (e.g., `F2-r1`) in a **new wave** after the original feature, with metadata `**Rework of**: F2`; it depends on the original cell's PR (already merged).
- Its plan location points at the rework file: `deliveries/<epic-name>/order-service/wallet-service/rework-2026-08-08.md`.

**Pre-merge (cell in-progress — implemented but not pushed/merged)** — no index change:

- Keep the cell's identity and **in-progress** status; no new feature/wave, no note.
- A sibling `rework-<date>.md` is written (implemented steps never modified) — that file is the record; the cell proceeds to push approval after the rework.
