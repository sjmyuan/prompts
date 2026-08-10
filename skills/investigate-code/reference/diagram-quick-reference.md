# Diagram Quick Reference

Choose the diagram type that best explains the concept. Draw all diagrams with Mermaid. Full C4 and sequence conventions are in [c4-model-conventions.md](c4-model-conventions.md) and [sequence-diagram-conventions.md](sequence-diagram-conventions.md).

## Writing Robust Labels

Most broken diagrams come from special characters in labels — a semicolon (`;`) in a description is the #1 cause. Mermaid parses `; " # ( ) [ ] { } |` as **syntax, not text**.

1. **Reword** — never put risky characters in a label. Replace `;` with `,` / `，` / `·` (e.g. "handles orders; manages refunds" → "handles orders, manages refunds"); drop or reword `()`; avoid `#` and `"`.
2. **Quote** — when real syntax is required (API paths, method calls), wrap in quotes: `A["POST /orders"]`, `Rel(a, b, "POST /payments", "HTTPS")`. Never emit unquoted text containing syntax characters.
3. **Escape (last resort)** — inside quotes only: `#59;` for `;`, `#quot;` for `"`, `#35;` for `#`, `#40;` / `#41;` for `(` / `)`.
4. **Line breaks** — use `<br/>`, never a raw newline inside a label.
5. **Self-check** — scan every label for `; " # ( ) [ ] { } |` before output; reword or escape any hit. Shorten risky labels and move detail to the caption.

## Architecture & Structure

| Diagram | Syntax | Key elements |
|---|---|---|
| **C2 Container** | Mermaid `C4Container` | `Person()`, `Container()`, `ContainerDb()`, `System_Boundary()`, `Rel(from, to, "protocol")` |
| **C3 Component** | Mermaid `C4Component` | `Component()`, `ComponentDb()`, `Container_Boundary()`, `Rel()`; `_Ext` suffix for external deps |

## Interaction & Flow

| Diagram | Syntax | Key elements |
|---|---|---|
| **Sequence** | Mermaid `sequenceDiagram` | `actor`, `participant`, `database`, `->>` (sync), `-)` (async), `-->>` (return), `alt/loop/par` |
| **Flowchart** | Mermaid `flowchart` | `([...])` (start/end), `[...]` (process), `{...}` (decision), `-->|label|` (arrow) |

## Other Useful Diagrams

| Diagram | Syntax | Use for |
|---|---|---|
| **State diagram** | Mermaid `stateDiagram-v2` | Object lifecycle, status transitions, state machines |
| **Class/ER diagram** | Mermaid `classDiagram` / `erDiagram` | Data models, entity relationships, class hierarchies |
| **Gantt chart** | Mermaid `gantt` | Timelines, process phases, parallel workstreams |
| **Mindmap** | Mermaid `mindmap` | Hierarchical breakdowns, feature trees, taxonomy |
