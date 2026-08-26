# Orchestration Guide

Rules for **orchestrate-delivery**, **resume-delivery**, and **update-delivery-index** in `orchestrate-feature-delivery`.

## Agent dispatch

- **Always delegate — never do the work yourself.** The orchestrator only dispatches and tracks. Every delivery task maps to a dedicated agent:

| Task | Delegated agent (role → example) | Applies | Result |
|---|---|---|---|
| Investigate (incl. rework spike) | investigation agent → **spike-conductor** | **conduct-spike** | focused findings / ADR / solution-doc updates + change summary |
| Plan a cell | planning agent → **planner** | **plan-development-task** | `plan.md` + `context.md` |
| Execute a cell | execution agent → **executor** | **execute-plan** | code changes + commits |
| Update solution doc | solution-doc agent → **solution-doc-writer** | **write-solution-doc** | revised sections, rewrite in place |
| Update ADR | ADR agent → **adr-writer** | **draft-adr** | revised ADR, rewrite in place |

- **One cell per agent.** Planning agents apply **plan-development-task** and write `deliveries/<epic-name>/{repo}/{feature-name}/plan.md` + `context.md` (feature folder named by the kebab-case feature name, e.g. `wallet-contracts`). Execution agents apply **execute-plan** and run the plan.
- **Plan-first hard gate**: plan and execute are separate agents. Dispatch the **planner** first; verify its plan file exists on disk at the recorded Plan location; only then dispatch the **executor**. Never one agent for both plan and execute, never execute without a verified plan file, and never write or append a plan after execution.
- **Artifact updates are delegated too.** When a plan or execution surfaces changes to the spike's solution doc or ADRs, dispatch a **solution-doc-writer** / **adr-writer** agent for the update — never edit those artifacts from the orchestrator.
- **Full context in every brief.** Each agent brief carries the cell's scope brief plus its **spike references** (paths to the relevant change-summary items, ADR files, and solution-doc section). Agents load these on demand — do not inline entire solution docs into the brief.
- **Persist references to context.md.** Planning agents record the spike references in `context.md`, so execution and resume agents have durable distilled context and can load referenced artifacts when needed.
- Dispatch agents **in parallel** across cells, subject to:
  - **Develop-gating**: dispatch cells whose dependency cells are **planned** (contracts agreed); contract-first and independent cells develop in parallel.
  - **Merge-gating**: a cell merges only after its dependency cells are **done** (merged).
  - **No conflict in parallel**: never run two cells that touch the same repo with a conflict edge at the same time — serialize them.
  - **Capacity**: match the number of parallel agents to what the platform supports; ask the user when unsure.
- Use the platform's agent/sub-agent mechanism — detect what is available (e.g., planner / executor agents) and dispatch accordingly.
- **Branches**: one branch per repo per cell, named to match the **repo's branch convention** (detect from existing branches / git config / team docs, or ask the user — never assume a prefix); the branch is recorded in the delivery index and included in the agent brief (the PR reference is recorded once opened); execution agents create the branch during their Prepare Environment step and commit small-step locally (see **branch-and-push-conventions**). The **head commit** from each execution handoff is recorded in the index (a pointer, like Branch/PR).
- **Push gating**: never push a branch or open a PR automatically — after a cell's work is complete and ready to integrate, ask the user for confirmation first.

## Orchestration loop

1. Load the index, or create it via decompose → map → order → produce.
2. Assess state (per-cell status + develop/merge gating).
3. Phase 1 — dispatch the **planner** to each unplanned, develop-ready cell (skip done; note blocked).
4. Verify the **plan-first gate** — confirm each planner's plan file exists on disk before the cell advances.
5. Phase 2 — dispatch the **executor** to each planned cell whose plan file is verified.
6. Collect results; apply **update-delivery-index**.
7. Re-assess and repeat until all cells are done or the user pauses.

## Status updates

- After every agent result, update the cell status; record the **head commit** from each execution handoff; when a PR is opened, record its reference; when it merges, confirm the recorded head commit is in the merged PR before marking **done**, then re-check downstream cells for develop/merge-readiness.
- Never let conversation text be the source of truth — the delivery index is.

## ADR changes

ADRs are **versionless** — drift is signaled by the **adr-writer** agent's return or the user's report, never by diffing the ADR (see **handle-adr-change**). Route governed cells by status:

| Status | Route |
|---|---|
| unplanned | no action — planned against the current ADR when dispatched |
| planned | re-plan in place (**plan-development-task**) — nothing implemented, no history to preserve |
| in-progress | pre-merge rework if the change touches the cell's decision (sibling `rework-<date>.md`) |
| done | post-merge rework (new rework feature `F2-r1`) |
| poc cell | surface to the user — the change may invalidate success criteria |

Never dispatch a planned cell on a stale decision.

## Resume

- On resume, confirm ADR currency with the user first — if a governing ADR changed, apply **handle-adr-change** before resuming. Then load the index: completed waves are skipped; in-progress cells resume from the last step in the active `rework-<date>.md` (or `plan.md` if no rework — see the `context.md` manifest); failed cells are re-planned or retried with the user; blocked cells wait for their blocker.
- Report what is resumed vs skipped before dispatching.

## Failure handling

| State | Meaning | Recovery |
|---|---|---|
| **failed** | agent hit an error (record reason) | ask the user: re-plan (plan-development-task) or retry |
| **blocked** | waiting on an unmerged dependency or a user decision (record blocker) | do not dispatch until the blocker clears |
| **in-progress** | agent was interrupted mid-execution | resume from the last completed step in the active `rework-<date>.md` (or `plan.md` if no rework) |

## POC cells

A POC proves one option of one ADR as a standalone feature (see **poc-definition**). It is planned and executed like any cell, then stops at a **decision gate** instead of merging.

- **Dispatch**: plan → **planner** (plan-development-task, POC mode); execute → **executor** (execute-plan, POC mode). Include `type: poc` + success criteria in the brief.
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
3. **Update the index**: record only the rework cell (`F2-r1`, `Rework of: F2`) in a new wave + its plan-location pointer — the original cell stays **done**; spike focus, ADR revision, and rework steps live in the sibling `rework-<date>.md` / `context.md`.
4. **Write the rework plan**: dispatch the **planner** (**plan-development-task**) to write a sibling `rework-<date>.md` in the feature folder — `plan.md` stays the frozen original, implemented steps never modified.
5. **Execute the rework plan**: dispatch the **executor** (**execute-plan**) to run only the new rework steps.
6. Update the index; ask the user before pushing / opening a PR.

**Rework lineage**: rework features chain to the state they rework — `F2-r1` reworks `F2`; `F2-r2` reworks `F2-r1` (the latest delivered state); `Rework of:` names that state. Rework files key by date — on a same-day collision suffix `-2`, `-3` (`rework-2026-08-24-2.md`). The `context.md` `## Reworks` manifest is the canonical chain.

**Pre-merge** (cell **in-progress** — implemented but not pushed/merged): nothing is merged yet, same append-only rule.

1. **Scope**: no focused spike unless the issue challenges the governing ADR decision — if it does, dispatch **spike-conductor** and **adr-writer** / **solution-doc-writer** as above.
2. **Write the rework plan**: dispatch the **planner** (**plan-development-task**) to write a sibling `rework-<date>.md` in the feature folder — `plan.md` stays the frozen original, implemented steps never modified; no new rework feature/wave (rework stays on the same cell).
3. **Execute the rework plan**: dispatch the **executor** (**execute-plan**) to run only the new rework steps on the unmerged work.
4. No index change (cell stays **in-progress**; the sibling `rework-<date>.md` is the record); ask the user before pushing / opening a PR.
