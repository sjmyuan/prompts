---
name: fan-out-agents
description: Dispatch several independent, similar sub-tasks to parallel copies of the same agent and merge the results. Use when parallelizing, splitting, scaling out, or fanning out broad work across same-type sub-agents.
---

<when-to-use-this-skill>
- A task decomposes into several independent, similar sub-tasks (modules, entry points, repos, or candidates) that one agent would otherwise cover serially
- The agent wants to parallelize a broad investigation or review by dispatching parallel copies of itself, then merging the reports
- Mid-task the agent notices several independent things it can do in parallel and fans out on its own, without being asked
- The agent merges the returned reports of several same-type sub-agents into one coherent answer
- Do NOT load when the sub-tasks are genuinely serial, each result feeds the next, or too small to justify fan-out — run them directly
- Do NOT load when another pipeline owns orchestration (e.g. `conduct-spike` per-area dispatch, `orchestrate-feature-delivery` waves) — those orchestrate already
</when-to-use-this-skill>

<knowledge>

<fan-out-model>
A **fan-out** runs several independent, similar units of work as parallel copies of the host agent, then merges the reports into one answer. It is not heterogeneous orchestration: cross-role pipelines (spike per-area dispatch, feature-delivery waves) own their dispatch and never route here. Fan-out is **read-only / report-producing** — clones never mutate shared files or state; work that writes shared targets runs directly or in a pipeline that owns conflict handling. Fan-out leaves no artifacts, index, or tracking file. One level deep — clones are leaf tasks and never re-fan-out.
</fan-out-model>

<trigger-signals>
Fan out when several signals hold — separable targets, independently answerable sub-questions, similar work, enough effort — and skip when any anti-signal holds. Full signal checklist: **reference/fan-out-guide.md**.
</trigger-signals>

<auto-split-principle>
Splitting is fully automatic — never ask the user to pre-decompose or confirm areas. Partition the task into disjoint areas that together cover the whole task. When you cannot form confidently disjoint, covering areas, run the task directly — a guessed split wastes parallel reads and silently drops coverage. Split heuristics + sanity check: **reference/fan-out-guide.md**.
</auto-split-principle>

<inline-brief-contract>
The host authors each clone's brief inline from generic invariants — no fixed template file. Every brief is **self-contained** — clones inherit neither the host's session history nor each other's context; the brief carries every fact a clone needs. Each states the area's scope boundary (in/out), the sub-question, the return contract per the host's own reporting doctrine, and a leaf instruction. Briefs are the only deconfliction between clones, which never see each other.
</inline-brief-contract>

<merge-discipline>
Merging is where quality is won or lost. The host reads short reports and never redoes a clone's reads. Deduplicate overlapping claims, reconcile shared boundaries with a direct spot-check, and spot-check at least one claim per area against primary sources — clones can make systematic errors, not just boundary overlaps. Surface conflicts rather than hiding them; never present a coherent whole that papers over a contradiction. Presentation stays in the host's own doctrine — this skill imposes none.
</merge-discipline>

<platform-dispatch>
Detect whether the platform lets the host spawn copies of itself as sub-agents. When it does, dispatch all clones **in one response** — multiple dispatches in a single turn run in parallel; one per turn runs sequentially. When it does not, run the same split serially — still better than an unplanned sweep. Fallback detail: **reference/fan-out-guide.md**.
</platform-dispatch>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Deciding whether to fan out, splitting, or merging | Signal checklist, split heuristics, brief invariants, merge rules | [reference/fan-out-guide.md](reference/fan-out-guide.md) |
| Walking a broad codebase question fanned across three investigation clones | Host split, briefs, clone reports, merged answer | [examples/fan-out-investigation.md](examples/fan-out-investigation.md) |
| Walking a large multi-module review fanned across review clones | Host split of a PR, merged findings by severity | [examples/fan-out-review.md](examples/fan-out-review.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<fan-out-tasks>
**Objective**: Run several independent similar sub-tasks as parallel clones and merge their reports into one answer.

1. Detect fan-out-ability against **trigger-signals** — independent, similar, and large enough.
2. Run the task directly when signals fail, dispatch is unavailable, or a safe split is impossible.
3. Split the task into disjoint covering areas per **auto-split-principle**, sanity-checking disjointness and coverage.
4. Compose one inline brief per area per **inline-brief-contract**.
5. Dispatch all clones concurrently per **platform-dispatch** — all dispatches in one response.
6. Collect each clone's report as it returns; wait in bounded stretches and chase any clone that finishes without reporting.
7. Merge and reconcile the reports per **merge-discipline**.
8. Present the single merged answer using the host's reporting doctrine, with a coverage summary listing unresolved cross-area conflicts.
9. Validate: areas were disjoint and covering, every report was used, conflicts surfaced, and the answer answers the original task directly.
</fan-out-tasks>

</capabilities>
