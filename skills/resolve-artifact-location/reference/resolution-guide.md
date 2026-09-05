# Resolution Guide

Used by **resolve-root** for discovery, ranking, and the auto-vs-confirm decision.

## Base root

A base root holds `spikes/<spike-name>/`, `deliveries/<epic-name>/`, and `feature-implementations/` (standalone plan docs) as siblings. Resolve it once per codebase or docs home; consumers append per-kind folders under it and record the base.

## Resolution precedence

1. **Explicit user path** — use as-is; highest.
2. **Durable record** — spike `scope.md` `Artifact root:` line; an existing `deliveries/<epic>/index.md` or feature plan folder. Return without searching.
3. **Discovery** — run the checklist below.

## Discovery checklist

Enumerate every workspace root, then apply signals:

1. **List roots**: every folder the platform reports as a workspace root.
2. **Exclude**: skill-library / agent / prompt directories (parents of SKILL.md libraries or agent files), `.git`, `node_modules`, build output.
3. **Convention signal**: a root already containing a `spikes/` or `deliveries/` sibling with artifact folders of the same kind.
4. **Declared-home signal**: a root the team designates for decision docs in project context (CLAUDE.md / AGENTS.md / config), e.g. "ADRs live in docs/".
5. **Docs-repo signal**: a root whose name or role is a docs/wiki home (`docs`, `knowledge`, `wiki`, `adr`) and that holds decision-doc folders.

A code repo under investigation is a candidate **only** when it also carries one of the signals above — never by itself.

## Ranking tiers

| Tier | Signal | Meaning |
|---|---|---|
| 1 | Existing `spikes/` or `deliveries/` sibling at a root | Place next to what already exists |
| 2 | Declared home in project/team context | Team decides where decision docs live |
| 3 | Docs/wiki-named root holding decision folders | Central records home |
| 4 | The single workspace root with no signals | Weak — only when it is the only root |

Multiple roots sharing the top tier → ambiguous.

## Auto vs confirm

- **Auto-select** only when exactly one candidate sits in the top tier (a sole unambiguous winner). State the assumption in one line — e.g. "Placing next to the existing `spikes/` sibling at `<root>`." Then proceed.
- **Confirm** when two or more roots share the top tier, when no candidate reaches a floor, or when a multi-root workspace has conflicting roots. Present the ranked shortlist — ≤4 rows, each `path — why`, with the recommended row marked `(default)`. Ask the user to confirm the default, pick another, or type a custom path.
- **Greenfield** (no convention, no declared home, no docs repo): ask the user to name the location. Present **no suggested default** — a code repo root is never proposed silently.

## Confirmation UX

- Shortlist as a table: ≤4 rows of `path — reason`; the recommended row carries `(default)`.
- Accept a freeform answer — the user may type any path.
- Never create folders before confirmation.

## Persist contract

After confirmation, the caller records the base:

| Kind | Where |
|---|---|
| Spike | `scope.md` — `Artifact root:` line at the top |
| Standalone feature | `{base}/feature-implementations/{feature-name}/`, base noted in `context.md` |
| Delivery | inherit the spike's recorded base — no separate resolution |

Resume and downstream consumers read the record; only a missing record triggers discovery again.
