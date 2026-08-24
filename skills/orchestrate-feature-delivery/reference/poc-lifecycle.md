# POC Lifecycle

Rules for POC cells in `orchestrate-feature-delivery` (**define-poc-scope**).

## POC cell metadata

| Field | Meaning |
|---|---|
| `type` | `poc` — the cell proves an ADR option, not a normal feature |
| `adr` | Governing ADR |
| `option` | The option under proof (from the ADR's considered options) |
| `success-criteria` | Measurable evidence the gate judges (perf, complexity, migration cost) |
| `replaces` | Optional — existing feature/implementation superseded on adoption |
| `compare` | Optional — sibling POC cells for other options (run in parallel) |

## Status transitions

`unplanned → planned → in-progress → poc-ready → adopted | rejected` (plus `failed`/`blocked`). A replaced feature is marked **superseded**.

- **poc-ready**: execution finished the evaluation report; no merge yet — awaits the user's recorded decision.
- **adopted**: user/team chose the option → **POC-as-implementation** (promote → merge → done) or **POC-as-decision-input** (dispatch the **poc-gated** feature).
- **rejected**: option not proven → close the cell, archive/discard the branch, proceed on the other option.

## Decision gate

The orchestrator never evaluates or decides. At **poc-ready**, the user reads the evaluation report vs **success-criteria** and records **adopted** or **rejected** directly in the index. If the governing ADR changes while the POC is in flight, its success criteria may be moot — surface the change to the user first (see **handle-adr-change**). Once recorded, the orchestrator reacts:

1. Dispatch **adr-writer** (draft-adr) to record the outcome in the ADR.
2. **Adopted** — apply the matching adoption model below.
3. **Rejected** — close the cell (archive/discard the branch — ask the user); delivery proceeds on the other option.
4. Apply **update-delivery-index**.

## Adoption models

- **POC-as-implementation**: the POC branch becomes the shipped feature — on adopt, ask before pushing/PR, merge, mark `replaces` **superseded**.
- **POC-as-decision-input**: the POC only informs the choice — on adopt, close the POC and dispatch the **poc-gated** feature with the decided option.
