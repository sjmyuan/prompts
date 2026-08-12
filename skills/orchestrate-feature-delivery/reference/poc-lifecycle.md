# POC Lifecycle

Rules for POC cells in `orchestrate-feature-delivery` (**define-poc-scope**, **evaluate-poc-results**).

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

- **poc-ready**: execution finished the evaluation report; no merge yet.
- **adopted**: user/team chose the option → **POC-as-implementation** (promote → merge → done) or **POC-as-decision-input** (dispatch the **poc-gated** feature).
- **rejected**: option not proven → close the cell, archive/discard the branch, proceed on the other option.

## Decision gate

1. Read the evaluation report + success criteria from the index.
2. Present evidence vs each criterion — the user/team decides; the orchestrator never auto-decides.
3. Record the outcome in the ADR via **adr-writer** (draft-adr); update the index.

## Adoption models

- **POC-as-implementation**: the POC branch becomes the shipped feature — on adopt, ask before pushing/PR, merge, mark `replaces` **superseded**.
- **POC-as-decision-input**: the POC only informs the choice — on adopt, close the POC and dispatch the **poc-gated** feature with the decided option.
