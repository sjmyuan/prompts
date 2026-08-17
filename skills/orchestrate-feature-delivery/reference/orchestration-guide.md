# Orchestration Guide

Rules for **orchestrate-delivery**, **resume-delivery**, and **update-delivery-index** in `orchestrate-feature-delivery`.

## Agent dispatch

- **Always delegate — never do the work yourself.** The orchestrator only dispatches and tracks. Every delivery task maps to a dedicated agent:

| Task | Delegated agent (role → example) | Applies | Result |
|---|---|---|---|
| Spike a rework | spike agent → **spike-conductor** | **conduct-spike** | focused findings / ADR / solution-doc updates + change summary |
| Plan a cell | planning agent → **coding-assistant** | **plan-development-task** | `plan.md` + `context.md` |
| Execute a cell | execution agent → **coding-assistant** | **execute-plan** | code changes + commits |
| Update solution doc | solution-doc agent → **solution-doc-writer** | **write-solution-doc** | revised sections, rewrite in place |
| Update ADR | ADR agent → **adr-writer** | **draft-adr** | revised ADR, rewrite in place |

- **One cell per agent.** Planning agents apply **plan-development-task** and write `deliveries/<epic-name>/{repo}/{feature-name}/plan.md` + `context.md` (feature folder named by the kebab-case feature name, e.g. `wallet-contracts`). Execution agents apply **execute-plan** and run the plan.
- **Artifact updates are delegated too.** When a plan or execution surfaces changes to the spike's solution doc or ADRs, dispatch a **solution-doc-writer** / **adr-writer** agent for the update — never edit those artifacts from the orchestrator.
- **Full context in every brief.** Each agent brief carries the cell's scope brief plus its **spike references** (paths to the relevant change-summary items, ADR files, and solution-doc section). Agents load these on demand — do not inline entire solution docs into the brief.
- **Persist references to context.md.** Planning agents record the spike references in `context.md`, so execution and resume agents have durable distilled context and can load referenced artifacts when needed.
- Dispatch agents **in parallel** across cells, subject to:
  - **Develop-gating**: dispatch cells whose dependency cells are **planned** (contracts agreed); contract-first and independent cells develop in parallel.
  - **Merge-gating**: a cell merges only after its dependency cells are **done** (merged).
  - **No conflict in parallel**: never run two cells that touch the same repo with a conflict edge at the same time — serialize them.
  - **Capacity**: match the number of parallel agents to what the platform supports; ask the user when unsure.
- Use the platform's agent/sub-agent mechanism — detect what is available (e.g., coding-assistant agents) and dispatch accordingly.
- **Branches**: one branch per repo per cell, named to match the **repo's branch convention** (detect from existing branches / git config / team docs, or ask the user — never assume a prefix); recorded in the delivery index and included in the agent brief; execution agents create the branch during their Prepare Environment step and commit small-step locally (see **branch-and-push-conventions**).
- **Push gating**: never push a branch or open a PR automatically — after a cell's work is complete and ready to integrate, ask the user for confirmation first.

## Orchestration loop

1. Load the index, or create it via decompose → map → order → produce.
2. Assess state (per-cell status + develop/merge gating).
3. Select ready cells: unplanned → plan; planned → execute; skip done; note blocked.
4. Dispatch parallel agents for the ready cells.
5. Collect results; apply **update-delivery-index**.
6. Re-assess and repeat until all cells are done or the user pauses.

## Status updates

- After every agent result, update the cell status; when a PR merges, mark its cell **done** and re-check downstream cells for develop/merge-readiness.
- Never let conversation text be the source of truth — the delivery index is.

## Resume

- On resume, load the index: completed waves are skipped; in-progress cells resume from the last step in `plan.md`; failed cells are re-planned or retried with the user; blocked cells wait for their blocker.
- Report what is resumed vs skipped before dispatching.

## Failure handling

| State | Meaning | Recovery |
|---|---|---|
| **failed** | agent hit an error (record reason) | ask the user: re-plan (plan-development-task) or retry |
| **blocked** | waiting on an unmerged dependency or a user decision (record blocker) | do not dispatch until the blocker clears |
| **in-progress** | agent was interrupted mid-execution | resume from the last completed step in `plan.md` |

## POC cells

A POC proves one option of one ADR as a standalone feature (see **poc-definition**). It is planned and executed like any cell, then stops at a **decision gate** instead of merging.

- **Dispatch**: plan → **coding-assistant** (plan-development-task, POC mode); execute → **coding-assistant** (execute-plan, POC mode). Include `type: poc` + success criteria in the brief.
- **Compare POCs**: sibling POC cells (one per option) run in parallel in an early wave.
- **Decision gate**: at **poc-ready**, present the evaluation report vs success criteria to the user — the user/team decides adopt/reject, never auto-decide.
- **Adopt**: dispatch **adr-writer** (draft-adr) to record the validated option; **POC-as-implementation** — ask before pushing/PR, merge the branch, mark the `replaces` cell **superseded**; **POC-as-decision-input** — close the POC, dispatch the **poc-gated** feature with the decided option.
- **Reject**: dispatch **adr-writer** to record the outcome; close the cell **rejected**; archive or discard the branch (ask the user); delivery proceeds on the other option.
- **Sequencing**: never dispatch a **poc-gated** feature before its POC's decision.

## Rework after implementation

Two modes, chosen by the cell's status (see **rework-modes** in the SKILL.md knowledge).

**Post-merge** (cell **done** — merged/verified): history is shipped and preserved.

1. **Focused spike**: dispatch the **spike-conductor** agent (conduct-spike), scoped narrowly to the affected decision — usually the feature's governing ADR. Do not re-open the whole epic.
2. **Delegate artifact updates**: ADR changes → **adr-writer** (draft-adr); solution-doc changes → **solution-doc-writer** (write-solution-doc); change summary recomputed via conduct-spike.
3. **Update the index**: record the rework — spike's ADR focus, new change-summary items, rework feature (e.g. `F2-r1`) in a new wave, appended plan location.
4. **Append the plan**: dispatch **plan-development-task** (coding-assistant) to append a `## Rework <date>` section to the feature's existing `plan.md` — implemented steps are never modified.
5. **Execute the appended plan**: dispatch **execute-plan** (coding-assistant) to run only the new rework steps.
6. Update the index; ask the user before pushing / opening a PR.

**Pre-merge** (cell **in-progress** — implemented but not merged/committed/pushed): nothing is merged yet, same append-only rule.

1. **Scope**: no focused spike unless the issue challenges the governing ADR decision — if it does, dispatch **spike-conductor** and **adr-writer** / **solution-doc-writer** as above.
2. **Append the plan**: dispatch **plan-development-task** (coding-assistant) to append a `## Rework <date>` section to the existing `plan.md` — implemented steps are never modified; no new rework feature/wave (rework stays on the same cell).
3. **Execute the appended plan**: dispatch **execute-plan** (coding-assistant) to run only the new rework steps on the unmerged work.
4. Update the index (cell stays **in-progress**); ask the user before pushing / opening a PR.
