# Example: Scope-Map Status Lifecycle Through a Spike

**Scenario**: A single-area spike ("How to replace the session store?") runs from scope definition to completion. This example shows how `scope.md` statuses move as each capability saves its artifact, and how new evidence reopens a `done` problem.

**Applies**: **scope-map-status** (knowledge convention) — updated by **compile-findings-doc**, **draft-problem-adrs**, and **sync-update-artifacts**

**What makes this distinct**: Other examples show artifact content; this one shows only the `scope.md` status dashboard as it evolves — the stored problem statuses and the derived area status.

---

## Point 1 — After define-spike-scope

Goal: replace the in-process session store with a shared, scalable store.
Area `preparing` (no findings yet); problems `investigating` (no ADR).

```markdown
## Area: Session storage — `preparing`
**Findings**: —
- `investigating` How to choose the session store? → (no ADR)
- `investigating` How to migrate existing sessions? → (no ADR)
```

## Point 2 — After compile-findings-doc

Findings doc saved → area `spiking`. Problems still `investigating` (no ADR).

```markdown
## Area: Session storage — `spiking`
**Findings**: docs/findings-session-storage.md
- `investigating` How to choose the session store? → (no ADR)
- `investigating` How to migrate existing sessions? → (no ADR)
```

## Point 3 — After draft-problem-adrs (awaiting confirmation)

Each ADR saved → its problem `deciding`. Area stays `spiking` (open problems).

```markdown
## Area: Session storage — `spiking`
**Findings**: docs/findings-session-storage.md
- `deciding` How to choose the session store? → adrs/adr-session-storage-01-store-choice.md
- `deciding` How to migrate existing sessions? → adrs/adr-session-storage-02-migration.md
```

## Point 4 — After user confirmation

User confirms both options → problems `done`; all problems `done` → area `done`.

```markdown
## Area: Session storage — `done`
**Findings**: docs/findings-session-storage.md
- `done` How to choose the session store? → adrs/adr-session-storage-01-store-choice.md
- `done` How to migrate existing sessions? → adrs/adr-session-storage-02-migration.md
```

## Point 5 — New evidence reopens a problem

A later measurement shows the chosen store's failover exceeds the SLA → **sync-update-artifacts** reopens the store-choice problem `done` → `deciding`; the area returns to `spiking`; the ADR and solution doc are rewritten in place.

```markdown
## Area: Session storage — `spiking`
**Findings**: docs/findings-session-storage.md
- `deciding` How to choose the session store? → adrs/adr-session-storage-01-store-choice.md
- `done` How to migrate existing sessions? → adrs/adr-session-storage-02-migration.md
```

## Rules in play

- A `done` problem always has its ADR; an area is never `done` with an open problem.
- Area status is derived from its problems and findings link — never stored.
- Statuses track saved artifacts, not in-flight dispatches.
