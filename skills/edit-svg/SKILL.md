---
name: edit-svg
description: Create SVG diagrams with professional PPT-quality layout, clear connections, and no overlapping elements. Use when creating, editing, modifying, upgrading, or fixing flowcharts, architecture diagrams, comparison diagrams, pyramid diagrams, step-flow diagrams, container diagrams, sequence diagrams, concept diagrams, charts, or donut charts as SVG.
---

<when-to-use-this-skill>
- User wants to create a flowchart, process diagram, or workflow diagram as SVG
- User wants to create an architecture diagram, system design diagram, or component diagram as SVG
- User wants to create a comparison diagram, side-by-side layout, or panel comparison as SVG
- User wants to create a pyramid diagram, layered structure, or hierarchical stack as SVG
- User wants to create a step-flow diagram, numbered step sequence, or horizontal process flow as SVG
- User wants to create a container diagram, boundary diagram, or zone-based layout as SVG
- User wants to create a sequence diagram or interaction diagram as SVG
- User wants to create a concept diagram, mind map, or visual explanation as SVG
- User wants to create a chart, graph, data visualization, or donut chart as SVG
- User wants to fix overlapping elements, improve connection clarity, or adjust spacing in an existing SVG
- User wants to edit, modify, or update an existing SVG diagram
- User wants an existing SVG upgraded to PPT-presentation quality

<knowledge>

**Two SVG authoring approaches**:

| Approach | Used for | Method |
|---|---|---|
| **Script-based** | Flowcharts, architecture, sequence, concept, bar/line/pie charts | Python scripts compute positions, paths, SVG elements. Load [reference/computation-snippets.md](reference/computation-snippets.md). |
| **Hand-crafted** | Comparison, pyramid, step-flow, container, donut charts | Write SVG directly following visual patterns in `examples/`. No scripts. |

**Design standards**: 16:9 (960×540), PPT shadows/gradients, `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`, WCAG AA contrast, 5–8 elements max. See [reference/design-standards.md](reference/design-standards.md).

**SVG assembly pattern**: `<svg viewBox="..." font-family="...">` → `<defs>` (shadow + gradients + arrow markers) → background → title → layers → connections → shapes → labels → `</svg>`.

**Key conventions**: Set `font-family` on root `<svg>`. Use `dominant-baseline="middle"` + `text-anchor="middle"` for centered text. Layer `<rect rx>` backgrounds for panels. Use `<filter id="shadow">` with `feDropShadow`. Panel headers: full-width colored `<rect>` at panel top with same `rx`. Color-code semantically (red=problems, green=success, blue=info, orange=warnings).

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Creating a flowchart | Detailed flowchart creation steps | [reference/create-flowchart.md](reference/create-flowchart.md) |
| Creating an architecture diagram | Detailed architecture diagram steps | [reference/create-architecture-diagram.md](reference/create-architecture-diagram.md) |
| Creating a sequence diagram | Detailed sequence diagram steps | [reference/create-sequence-diagram.md](reference/create-sequence-diagram.md) |
| Creating a concept diagram | Detailed concept diagram steps | [reference/create-concept-diagram.md](reference/create-concept-diagram.md) |
| Creating a bar/line/pie chart | Detailed chart creation steps | [reference/create-chart.md](reference/create-chart.md) |
| Creating a comparison diagram | Detailed comparison diagram steps | [reference/create-comparison-diagram.md](reference/create-comparison-diagram.md) |
| Creating a pyramid diagram | Detailed pyramid diagram steps | [reference/create-pyramid-diagram.md](reference/create-pyramid-diagram.md) |
| Creating a step-flow diagram | Detailed step-flow diagram steps | [reference/create-step-flow-diagram.md](reference/create-step-flow-diagram.md) |
| Creating a container diagram | Detailed container diagram steps | [reference/create-container-diagram.md](reference/create-container-diagram.md) |
| Creating a donut chart | Detailed donut chart steps | [reference/create-donut-chart.md](reference/create-donut-chart.md) |
| Fixing layout overlaps or connection issues | Layout analysis and fix steps | [reference/analyze-and-fix-layout.md](reference/analyze-and-fix-layout.md) |
| Modifying or upgrading an existing SVG | Modification and PPT upgrade steps | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Need script calling patterns or geometry computation | Script calling guide, assembly pattern, arrow geometry | [reference/computation-snippets.md](reference/computation-snippets.md) |
| Need design standards or example output | PPT design rules and diagram examples | [reference/design-standards.md](reference/design-standards.md) and [examples/](examples/) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-flowchart>
Generate a PPT-quality flowchart as raw SVG. Build node/edge data with grid positions, compute all geometry via scripts, assemble per SVG pattern.
</create-flowchart>

<create-architecture-diagram>
Generate a PPT-quality system architecture diagram as raw SVG. Group components into tiers, build node/edge data, compute all geometry via scripts.
</create-architecture-diagram>

<create-sequence-diagram>
Generate a PPT-quality sequence diagram as raw SVG. Define participants and chronological messages, add lifelines, compute all geometry via scripts.
</create-sequence-diagram>

<create-concept-diagram>
Generate a PPT-quality concept diagram/mind map as raw SVG. Central node with radial branches, compute all positions and geometry via scripts.
</create-concept-diagram>

<create-chart>
Generate a PPT-quality bar/line/pie chart as raw SVG. Call `chart_builder.render_bar_chart()` / `render_line_chart()` / `render_pie_chart()` — returns complete SVG. Validate contrast via `colors.wcag_aa_check()`.
</create-chart>

<create-comparison-diagram>
Generate a PPT-quality comparison diagram as raw SVG — side-by-side panels (2–3 columns) with colored headers, items, and summary boxes. Hand-crafted (no scripts).
</create-comparison-diagram>

<create-pyramid-diagram>
Generate a PPT-quality pyramid diagram as raw SVG — layered trapezoids (3–5 layers) with gradient fills, labels, and side annotations. Hand-crafted (no scripts).
</create-pyramid-diagram>

<create-step-flow-diagram>
Generate a PPT-quality horizontal step-flow diagram as raw SVG — numbered steps (4–6) left-to-right with connecting arrows. Hand-crafted (no scripts).
</create-step-flow-diagram>

<create-container-diagram>
Generate a PPT-quality container/boundary diagram as raw SVG — bounded region with internal items and external elements connected by arrows. Hand-crafted (no scripts).
</create-container-diagram>

<create-donut-chart>
Generate a PPT-quality donut chart as raw SVG — proportional segments using `stroke-dasharray`/`stroke-dashoffset` with annotation boxes. Hand-crafted (no scripts).
</create-donut-chart>

<analyze-and-fix-layout>
Analyze existing SVG for overlaps and connection issues. Detect via `geometry.find_overlapping()`, fix via `graph_layout.resolve_overlaps()`, re-route via `routing.orthogonal_path()`, expand viewBox via `graph_layout.compute_viewbox()`. All via scripts.
</analyze-and-fix-layout>

<modify-existing-svg>
Modify an existing SVG — change colors, text, fonts, styling, or add/remove/rearrange elements. All new geometry via scripts. Load [reference/modify-existing-svg.md](reference/modify-existing-svg.md).
</modify-existing-svg>

<upgrade-to-ppt-quality>
Upgrade an existing SVG to PPT quality — shadows, gradients, title bar, 16:9, PPT typography. All defs/shapes via scripts. Load [reference/modify-existing-svg.md](reference/modify-existing-svg.md).
</upgrade-to-ppt-quality>

</capabilities>

<rules>
<rule>When creating script-based types (flowchart, architecture, sequence, concept, chart) → compute ALL positions, paths, and SVG elements via Python scripts. Never compute coordinates mentally. Load [reference/computation-snippets.md](reference/computation-snippets.md).</rule>
<rule>When creating hand-crafted types (comparison, pyramid, step-flow, container, donut) → write SVG directly following visual patterns in `examples/`. Load the corresponding reference file and example SVG for guidance.</rule>
<rule>When the request spans multiple diagram types → apply capabilities sequentially and compose into one SVG.</rule>
</rules>
