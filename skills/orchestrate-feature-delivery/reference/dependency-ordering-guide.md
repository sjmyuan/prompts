# Dependency Ordering Guide

Detailed rules for **order-feature-delivery** in `orchestrate-feature-delivery`.

## Edge classification

| Edge | Condition | Example | Develop | Merge |
|---|---|---|---|---|
| **merge-blocked** (hard) | B consumes a concrete artifact that exists only after A's PR merges | B calls a new endpoint added by A | after A's contract is defined | only after A merges |
| **contract-first** (soft) | A and B agree on the interface up front; B builds against stubs | B implements against an interface A will provide | in parallel | B after A |
| **conflict** | both change the same files in the same repo | both edit `auth/service.go` | serialize or split | — |
| **independent** | no coupling between the features | unrelated modules | parallel | any order |

Prefer **contract-first** (agreed interface + stubs) to maximize parallelism. Escalate to **merge-blocked** only when the interface cannot be agreed or stubbed up front.

## Wave computation

1. Build a directed graph: edge A → B means **B's merge** depends on A's merge.
2. `Wave(A) = 0` if A has no incoming edges; otherwise `1 + max(Wave(dependencies of A))`.
3. All features in the same wave run in parallel; a feature in wave *n* waits only for its own dependencies in earlier waves.
4. The longest dependency chain (highest wave count) is the rollout's **critical path** — flag it to the user.

## Develop vs merge

- **Develop in parallel**: features that can be built simultaneously — independent features in any wave, plus contract-first features even across waves (they develop against agreed stubs).
- **Merge-ordered**: merge sequence always respects the DAG; soft (contract-first) edges still order merges, they just don't block development.
- Report both lists per feature: "start developing now" vs "merge only after [F_x] merges".

## Intra-feature merge order

For a feature spanning multiple repos, order its PR merges:

1. **Contract / shared-library repo first** — defines the interface others consume.
2. **Data / migration repo next** — schema consumers depend on it.
3. **Consumer service repos last** — merge immediately after their dependencies.

Prefer the order that lets downstream cells merge right after, minimizing blocking.

## Conflict resolution

- Two features changing the same files in the same repo must be **serialized** or one slice **split** into its own feature.
- Record the conflict edge explicitly in the delivery index so parallel agents do not run conflicting cells simultaneously.
