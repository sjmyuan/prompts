# Scope-Map Status Guide

Full status model for `scope.md` — backs the **scope-map** / **scope-map-status** knowledge entries and the status updates in **define-spike-scope**, **continue-prior-spike**, and **sync-update-artifacts**.

## Status model

| Status | Meaning | Stored / Derived |
|---|---|---|
| Problem `investigating` | No ADR yet | Stored (ground truth) |
| Problem `deciding` | ADR drafted, option awaiting user confirmation | Stored |
| Problem `done` | ADR + user-confirmed option | Stored |
| Area `preparing` | Findings doc not compiled | Derived |
| Area `spiking` | Findings compiled, ≥1 problem not `done` | Derived |
| Area `done` | All problems `done` | Derived |

Area status is derived from its problems + findings link — never stored separately.

## Transitions

| From | Event | To |
|---|---|---|
| Area `preparing` | Findings doc saved | Area `spiking` |
| Problem `investigating` | ADR saved | Problem `deciding` |
| Problem `deciding` | User confirms option | Problem `done` |
| Area `spiking` | All problems `done` | Area `done` |
| Problem `done` | New evidence / changed decision | Problem `deciding` |

## Validation (on save)

- A `done` problem has its ADR present.
- An area is never `done` with an open problem.

## Usage

- **define-spike-scope**: record the goal (1 sentence) and each area (`preparing`, empty findings link) with its problems (`investigating`).
- **continue-prior-spike**: read statuses to surface open problems; update statuses as each step completes.
- **sync-update-artifacts**: a changed decision reopens its problem to `deciding`.
