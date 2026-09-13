# Rework Modes

Rework rules for `orchestrate-feature-delivery`. Rework is **always append-only** — implemented steps never change; scoped to the cell (usually its governing ADR), never the whole epic. Each rework is a sibling `rework-<date>.md` — `plan.md` stays the frozen original. Execution runs **only** the rework file's steps. `context.md` holds a `## Reworks` manifest (date, mode, cell, file, status) so resume finds the active file. The index records **state only** — the rework cell + plan pointer; details live in the rework file.

| Mode | When | Handling |
|---|---|---|
| **Post-merge** | cell **done** (merged/verified) | focused spike (**conduct-spike**) + ADR / solution-doc updates; new rework feature (e.g. `F2-r1`) in a new wave |
| **Pre-merge** | cell **in-progress** (implemented, not pushed/merged) | spike + ADR / solution-doc updates only if the issue challenges the ADR decision; rework stays on the same cell — rework steps merge with the original work |

- **Rework lineage**: `F2-r1` reworks `F2`; `F2-r2` reworks `F2-r1` (latest delivered state); `Rework of:` names it. Rework files key by date — same-day collision suffix `-2`, `-3`. The `## Reworks` manifest is the canonical chain.
- A verification-gate finding (**verify-cell**) is a **pre-merge** rework trigger while the cell is **in-progress**; the planner writes the sibling `rework-<date>.md` — the index tracks status only.
- **Post-merge index handling**: keep the original cell exactly as-is (**done**); add the rework as a new feature/cell in a new wave with `**Rework of**: F2`.
- **Pre-merge index handling**: no index change; the cell keeps its identity and **in-progress** status.
