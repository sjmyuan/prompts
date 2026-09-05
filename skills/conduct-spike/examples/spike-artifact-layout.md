# Example: Saving Spike Artifacts into One Per-Spike Folder

**Scenario**: A payment-migration spike (4 areas) has produced its findings docs, ADRs, and a solution doc. The user asks: "Keep all spike artifacts in one folder so we can version them together." The assistant places every artifact in the spike's folder per **spike-artifact-layout**.

**What makes this distinct**: Every other example focuses on *producing* an artifact; this one shows *where* each artifact lands once produced — and how the **scope map** (`scope.md`) ties areas → findings docs → problems → ADRs together, doubling as a live status dashboard (per **scope-map-status**) for the grouped-by-area solution doc. Downstream consumers (**orchestrate-feature-delivery**, sub-agents, reviewers) read paths from this folder.

**Applies**: **spike-artifact-layout** + **scope-map** (knowledge conventions) — applied by every producing capability when it saves its output

## Input (artifacts produced)

- Scope map: 4 areas; the database area holds 2 problems
- Findings docs (per area): service-boundaries, communication, database, migration-strategy
- ADRs: one per problem, area-prefixed — 5 total (database area → 2)
- Solution doc (hub, decisions grouped by area)

## Resulting spike folder

```
spikes/payment-migration/
├── scope.md
├── adrs/
│   ├── adr-service-decomposition-01-split-monolith.md
│   ├── adr-communication-01-service-communication.md
│   ├── adr-database-01-break-up-database.md
│   ├── adr-database-02-schema-migration.md
│   └── adr-migration-01-zero-downtime-migration.md
├── solution.md
└── docs/
    ├── findings-service-boundaries.md
    ├── findings-communication.md
    ├── findings-database.md
    └── findings-migration-strategy.md
```

`scope.md` (canonical area → problem map + live status dashboard — see **scope-map-status**):

```markdown
# Spike Scope: Payment Migration
**Goal**: Determine the target architecture for decomposing the payment monolith.

Problem status: `investigating` (no ADR) → `deciding` (ADR, awaiting confirmation) → `done` (confirmed).
Area status (derived): `preparing` (findings doc missing) · `spiking` (a problem open) · `done` (all problems done).

## Area: Service decomposition — `done`
**Findings**: docs/findings-service-boundaries.md
- `done` How to split the monolith? → adr-service-decomposition-01-split-monolith.md
## Area: Inter-service communication — `done`
**Findings**: docs/findings-communication.md
- `done` How to handle service-to-service communication? → adr-communication-01-service-communication.md
## Area: Database decomposition — `spiking`
**Findings**: docs/findings-database.md
- `done` How to break up the monolithic database? → adr-database-01-break-up-database.md
- `deciding` How to migrate the schema safely? → adr-database-02-schema-migration.md
## Area: Migration strategy — `done`
**Findings**: docs/findings-migration-strategy.md
- `done` How to migrate with zero downtime? → adr-migration-01-zero-downtime-migration.md
```

## Assistant confirmation (conversation level — not written into any artifact)

> "Saved the scope map to `scope.md`, all 4 findings docs to `docs/`, the 5 ADRs to `adrs/` (area-prefixed, one per problem), and the solution doc to `solution.md` with each area's ADR decisions grouped under its heading. Cross-references between artifacts use relative paths inside the spike folder."

**Notes**:
- The spike folder sits under an artifact base root (resolved via `resolve-artifact-location` when unnamed) and records `Artifact root:` at the top of `scope.md`.
- The delivery index for this epic is written by **orchestrate-feature-delivery** at the same base's `deliveries/<epic-name>/index.md` — a sibling of `spikes/`, not inside the spike folder.
