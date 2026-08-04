# Diagram Quick Reference

Choose the diagram type that best explains the concept. Draw all diagrams with Mermaid. Full C4 and sequence conventions are in [c4-model-conventions.md](c4-model-conventions.md) and [sequence-diagram-conventions.md](sequence-diagram-conventions.md).

## Architecture & Structure

| Diagram | Syntax | Key elements |
|---|---|---|
| **C2 Container** | Mermaid `C4Container` | `Person()`, `Container()`, `ContainerDb()`, `System_Boundary()`, `Rel(from, to, "protocol")` |
| **C3 Component** | Mermaid `C4Component` | `Component()`, `ComponentDb()`, `Container_Boundary()`, `Rel()`; `_Ext` suffix for external deps |

## Interaction & Flow

| Diagram | Syntax | Key elements |
|---|---|---|
| **Sequence** | Mermaid `sequenceDiagram` | `actor`, `participant`, `database`, `->>` (sync), `-->>` (async/return), `alt/loop/par` |
| **Flowchart** | Mermaid `flowchart` | `([...])` (start/end), `[...]` (process), `{...}` (decision), `-->|label|` (arrow) |

## Other Useful Diagrams

| Diagram | Syntax | Use for |
|---|---|---|
| **State diagram** | Mermaid `stateDiagram-v2` | Object lifecycle, status transitions, state machines |
| **Class/ER diagram** | Mermaid `classDiagram` / `erDiagram` | Data models, entity relationships, class hierarchies |
| **Gantt chart** | Mermaid `gantt` | Timelines, process phases, parallel workstreams |
| **Mindmap** | Mermaid `mindmap` | Hierarchical breakdowns, feature trees, taxonomy |
