# Example: Saving Spike Artifacts into One Per-Spike Folder

**Scenario**: A payment-migration spike (4 areas) has produced its findings docs, 4 ADRs, and a solution doc. The user asks: "Keep all spike artifacts in one folder so we can version them together." The assistant places every artifact in the spike's folder per **spike-artifact-layout**.

**What makes this distinct**: Every other example focuses on *producing* an artifact; this one shows *where* each artifact lands once produced — the per-spike folder that downstream consumers (**orchestrate-feature-delivery**, sub-agents, reviewers) read paths from.

**Applies**: **spike-artifact-layout** (knowledge convention) — applied by every producing capability when it saves its output

## Input (artifacts produced)

- Findings docs (per-area): service-boundaries, communication, database, migration-strategy
- ADRs: ADR-001 (decomposition), ADR-002 (communication), ADR-003 (database), ADR-004 (migration)
- Solution doc (hub)

## Resulting spike folder

```
spikes/payment-migration/
├── adrs/
│   ├── adr-001-service-decomposition.md
│   ├── adr-002-inter-service-communication.md
│   ├── adr-003-database-decomposition.md
│   └── adr-004-migration-strategy.md
├── solution.md
└── docs/
    ├── findings-service-boundaries.md
    ├── findings-communication.md
    ├── findings-database.md
    └── findings-migration-strategy.md
```

## Assistant confirmation (conversation level — not written into any artifact)

> "Saved all 4 findings docs to `spikes/payment-migration/docs/`, the 4 ADRs to `adrs/`, and the solution doc to `solution.md`. Cross-references between artifacts now use relative paths inside the spike folder."

**Notes**:
- The delivery index for this epic is written by **orchestrate-feature-delivery** at `deliveries/<epic-name>/index.md` — a separate top-level `deliveries/` folder, not the spike folder.
- Modularized solution sub-docs (if the solution doc is split per **solution-doc-modularity**) would land in `solution-doc/` next to the hub.
