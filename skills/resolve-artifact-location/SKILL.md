---
name: resolve-artifact-location
description: Resolve the base folder for spike and delivery docs from workspace conventions, confirming with the user. Use when choosing, inheriting, resuming, or placing a spike, delivery, or plan-folder location.
---

<when-to-use-this-skill>
- Choosing where a new spike folder (`spikes/<spike-name>/`) will live when the user gave no path
- Choosing where a new delivery index (`deliveries/<epic-name>/`) will live when no base was given — normally inherit the spike's recorded base instead
- Resuming or continuing a spike or epic and re-deriving its recorded base root without re-asking
- Placing standalone plan/feature docs (plan-development-task / execute-plan) that have no orchestrator cell folder
- Do NOT load when the user already named the exact folder — use it directly
</when-to-use-this-skill>

<knowledge>

<base-root>
A **base root** is a directory that holds decision artifacts as siblings:

| Sibling | Holds |
|---|---|
| `spikes/<spike-name>/` | spike output |
| `deliveries/<epic-name>/` | delivery index + plan folders |
| `feature-implementations/` | standalone plan/context docs |

Consumers append their per-kind folder under the resolved base and record the base so later sessions inherit it. The codebase under investigation is NOT an anchor — only convention, a declared docs home, or a docs/wiki root signal a candidate.
</base-root>

<resolution-precedence>
Resolution order — explicit user path → durable record → discovery. Full precedence, discovery signals, ranking tiers, and decision rules: **reference/resolution-guide.md**.
</resolution-precedence>

<durable-record-contract>
The caller records the returned base in its durable artifact so resume and downstream never re-ask:

| Artifact kind | Record field |
|---|---|
| Spike | `scope.md` — `Artifact root:` line at the top |
| Standalone feature | `feature-implementations/{feature-name}/` under the base, base noted in `context.md` |
| Delivery | inherited from the spike's recorded base (deliveries/ sits next to spikes/) |

Reading skills: `continue-prior-spike` and `orchestrate-feature-delivery` read these records instead of calling resolve again.
</durable-record-contract>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Running discovery, ranking, or the auto-vs-confirm decision | Full procedure, signal tiers, exclusions, confirmation UX | [reference/resolution-guide.md](reference/resolution-guide.md) |
| Walking through a resolve round on a multi-root workspace | Convention auto-select, delivery inherit, greenfield ask | [examples/resolve-base-root.md](examples/resolve-base-root.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<resolve-root>
**Objective**: Return a user-confirmed artifact base root for a new spike, delivery, or feature folder.

1. If the user named an exact path, use it and return it.
2. If a durable record stores the base (`scope.md` `Artifact root:`, an existing index or plan folder), return it — never re-search.
3. Discover candidate base roots per **reference/resolution-guide.md** (workspace enumeration, exclusions, signals).
4. Rank candidates and keep only the top tier per the guide.
5. Auto-select only a sole unambiguous top-tier winner and state the assumption in one line.
6. Otherwise present the ranked shortlist (≤4: path, reason, marked default) and ask the user to confirm or pick.
7. Return the confirmed base root and direct the caller to record it per the **durable-record-contract**.
8. Validate the choice — not excluded, matches the user's confirmation, and exists or is creatable.
</resolve-root>

</capabilities>
