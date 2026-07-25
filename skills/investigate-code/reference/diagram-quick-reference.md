# Diagram Quick Reference

Choose the diagram type that best explains the concept. Prefer PlantUML for C4/sequence (richer syntax); use Mermaid for flowcharts and state diagrams when simpler rendering is preferred. Full C4 and sequence conventions are in [c4-model-conventions.md](c4-model-conventions.md) and [sequence-diagram-conventions.md](sequence-diagram-conventions.md).

## Architecture & Structure

| Diagram | Syntax | Key elements |
|---|---|---|
| **C2 Container** | PlantUML `!include <C4/C4_Container>` | `Person()`, `Container()`, `ContainerDb()`, `System_Boundary()`, `Rel()` |
| **C3 Component** | PlantUML `!include <C4/C4_Component>` | `Component()`, `Container_Boundary()` |

## Interaction & Flow

| Diagram | Syntax | Key elements |
|---|---|---|
| **Sequence** | PlantUML native | `participant`, `->` (sync), `-->>` (async), `-->` (return), `alt/loop/par` |
| **Flowchart** | Mermaid `flowchart` | `graph TD/LR`, `-->` (arrow), `{rhombus}` (decision), `[rectangle]` (process), `([rounded])` (start/end) |

## Other Useful Diagrams

| Diagram | Syntax | Use for |
|---|---|---|
| **State diagram** | Mermaid `stateDiagram-v2` | Object lifecycle, status transitions, state machines |
| **Class/ER diagram** | Mermaid `classDiagram` / `erDiagram` | Data models, entity relationships, class hierarchies |
| **Gantt chart** | Mermaid `gantt` | Timelines, process phases, parallel workstreams |
| **Mindmap** | Mermaid `mindmap` | Hierarchical breakdowns, feature trees, taxonomy |
