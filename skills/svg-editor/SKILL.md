---
name: svg-editor
description: Create SVG diagrams with professional PPT-quality layout, clear connections, and no overlapping elements. Use when creating flowcharts, architecture diagrams, sequence diagrams, concept diagrams, or charts as SVG, or when fixing layout or styling issues in existing SVGs.
---

<when-to-use-this-skill>
- User wants to create a flowchart, process diagram, or workflow diagram as SVG
- User wants to create an architecture diagram, system design diagram, or component diagram as SVG
- User wants to create a sequence diagram or interaction diagram as SVG
- User wants to create a concept diagram, mind map, or visual explanation as SVG
- User wants to create a chart, graph, or data visualization as SVG
- User wants to fix overlapping elements, improve connection clarity, or adjust spacing in an existing SVG
- User wants to edit, modify, or update an existing SVG diagram
- User wants an existing SVG upgraded to PPT-presentation quality
</when-to-use-this-skill>

<knowledge>

**🔴 ZERO-TOLERANCE: All geometric computations MUST use Python scripts** — never compute coordinates, bounding boxes, path strings, or dimensions manually. See [reference/computation-snippets.md](reference/computation-snippets.md) for full calling guide and snippet patterns.

**Design standards**: 16:9 aspect ratio (960×540), PPT-style shadows/gradients, Segoe UI font stack, WCAG AA contrast, 5–8 elements max. See [reference/design-standards.md](reference/design-standards.md) for full details.

**Scripts** (`scripts/`): standalone `.py` files — no package, no orchestrator.

**Dependencies**: `pip install svgwrite networkx matplotlib`  
(`pygraphviz` optional — enables hierarchical Graphviz layout; falls back to spring layout if absent)

| Module | Library | Purpose | Key functions |
|---|---|---|---|
| `svg_builder.py` | **svgwrite** | SVG elements for nodes, edges, labels, title bars | `generate_node_svg()`, `generate_edge_svg()`, `generate_title_bar()`, `generate_arrow_marker()`, `get_shape_dimensions()` |
| `graph_layout.py` | **networkx** | Grid/auto layout, viewBox, overlap resolution | `flow_layout()`, `auto_layout()`, `resolve_overlaps()`, `compute_viewbox()`, `distribute_along_circle()` |
| `chart_builder.py` | **matplotlib** | Bar, line, pie charts as SVG strings | `render_bar_chart()`, `render_line_chart()`, `render_pie_chart()` |
| `routing.py` | custom | Orthogonal/bezier paths, endpoint validation | `orthogonal_path()`, `connection_endpoints()`, `path_to_svg_d()`, `bezier_path()` |
| `geometry.py` | custom | BBox math, overlap detection | `overlap()`, `find_overlapping()`, `center()`, `connection_point()` |
| `labeling.py` | custom | Label placement on connections | `label_position()`, `compute_all_labels()` |
| `colors.py` | custom | WCAG contrast, PPT palette, gradient/shadow defs | `wcag_aa_check()`, `get_gradient_defs()`, `get_shadow_filter()`, `PPT_PALETTE` |

**SVG assembly pattern**: `<svg>` → `<defs>` (shadow filter + gradients + arrow marker) → title bar → connections → shapes → labels → `</svg>`.

**Chart shortcut**: for bar/line/pie charts, call `chart_builder.render_*_chart()` which returns a complete standalone SVG — no manual assembly required.

**Load [reference/computation-snippets.md](reference/computation-snippets.md) when you need to compute positions, route connections, generate SVG elements, validate overlaps/contrast, or compute viewBox.**

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Executing **create-flowchart** | Step-by-step flowchart creation instructions | [reference/create-flowchart.md](reference/create-flowchart.md) |
| Executing **create-architecture-diagram** | Step-by-step architecture diagram instructions | [reference/create-architecture-diagram.md](reference/create-architecture-diagram.md) |
| Executing **create-sequence-diagram** | Step-by-step sequence diagram instructions | [reference/create-sequence-diagram.md](reference/create-sequence-diagram.md) |
| Executing **create-concept-diagram** | Step-by-step concept diagram instructions | [reference/create-concept-diagram.md](reference/create-concept-diagram.md) |
| Executing **create-chart** | Step-by-step chart creation instructions | [reference/create-chart.md](reference/create-chart.md) |
| Executing **analyze-and-fix-layout** | Step-by-step layout fix instructions | [reference/analyze-and-fix-layout.md](reference/analyze-and-fix-layout.md) |
| Executing **modify-existing-svg** or **upgrade-to-ppt-quality** | Step-by-step SVG modification/upgrade instructions | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Need example output for any diagram type | Example SVG files for each diagram type | [examples/](examples/) |
| Need script calling patterns or snippets | Full script calling guide with example snippets | [reference/computation-snippets.md](reference/computation-snippets.md) |
| Need design standards or layout principles | PPT design requirements and layout principles | [reference/design-standards.md](reference/design-standards.md) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-flowchart>
**Objective**: Generate a PPT-quality flowchart as raw SVG. Build node/edge data with grid positions, compute all geometry via scripts, assemble.

**Steps**:
1. Analyze process → identify nodes (rows/cols) and edges. Extract title.
2. Build node list with `id`, `type`, `text`, `row`, `col`. Build edge list with `from`, `to`, optional `label`.
3. **Compute positions, routes, SVG elements, viewBox, and validate all via scripts** (load [reference/computation-snippets.md](reference/computation-snippets.md)).
4. Assemble per SVG assembly pattern. Output raw SVG.

Load [reference/create-flowchart.md](reference/create-flowchart.md) for detailed steps.
</create-flowchart>

<create-architecture-diagram>
**Objective**: Generate a PPT-quality system architecture diagram as raw SVG. Group components into tiers, compute geometry via scripts.

**Steps**:
1. Identify tiers/layers and components. Assign `row` per layer, `col` per component.
2. Build node/edge data. Add layer background panels (manual draw).
3. **Compute positions, routes, SVG elements, viewBox, and validate all via scripts** (load [reference/computation-snippets.md](reference/computation-snippets.md)).
4. Assemble and output raw SVG.

Load [reference/create-architecture-diagram.md](reference/create-architecture-diagram.md) for details.
</create-architecture-diagram>

<create-sequence-diagram>
**Objective**: Generate a PPT-quality sequence diagram as raw SVG. Define participants and messages, compute via scripts.

**Steps**:
1. List participants (all `row:0`) and chronological messages.
2. Build node/edge data. Add lifelines/activation bars (manual draw).
3. **Compute positions, routes, SVG elements, viewBox, and validate all via scripts** (load [reference/computation-snippets.md](reference/computation-snippets.md)).
4. Assemble and output raw SVG.

Load [reference/create-sequence-diagram.md](reference/create-sequence-diagram.md) for details.
</create-sequence-diagram>

<create-concept-diagram>
**Objective**: Generate a PPT-quality concept diagram/mind map as raw SVG. Central node with radial branches, compute via scripts.

**Steps**:
1. Identify central concept and branch nodes. Mark central node.
2. Build node/edge data.
3. **Compute radial positions, routes, SVG elements, viewBox, and validate all via scripts** (load [reference/computation-snippets.md](reference/computation-snippets.md)).
4. Assemble and output raw SVG.

Load [reference/create-concept-diagram.md](reference/create-concept-diagram.md) for details.
</create-concept-diagram>

<create-chart>
**Objective**: Generate a PPT-quality bar/line/pie chart as raw SVG. Build data series, compute layout via scripts, render chart shapes manually.

**Steps**:
1. Determine chart type and extract data.
2. Call `chart_builder.render_bar_chart()` / `render_line_chart()` / `render_pie_chart()` — returns a complete SVG. No manual axis or path construction needed.
3. **Compute scales, bar widths, positions via script** (load [reference/computation-snippets.md](reference/computation-snippets.md)). Validate contrast.
4. Add legend. Assemble and output raw SVG.

Load [reference/create-chart.md](reference/create-chart.md) for details.
</create-chart>

<analyze-and-fix-layout>
**Objective**: Analyze existing SVG, fix overlapping elements and poor connections. All adjustments via scripts.

**Steps**:
1. Parse SVG, extract bounding boxes.
2. **Detect overlaps via `geometry.find_overlapping()`, detect connection issues via `routing.detect_intersections()`** (load [reference/computation-snippets.md](reference/computation-snippets.md)).
3. Fix via `graph_layout.resolve_overlaps()`, re-route via `routing.orthogonal_path()`, expand viewBox via `graph_layout.compute_viewbox()`.
4. Regenerate SVG elements via scripts. Validate and output.

Load [reference/analyze-and-fix-layout.md](reference/analyze-and-fix-layout.md) for detailed steps.
</analyze-and-fix-layout>

<modify-existing-svg>
**Objective**: Modify an existing SVG — change colors, text, fonts, styling, or add/remove/rearrange elements. All new geometry via scripts.

Load [reference/modify-existing-svg.md](reference/modify-existing-svg.md) for detailed steps.
</modify-existing-svg>

<upgrade-to-ppt-quality>
**Objective**: Upgrade an existing SVG to PPT quality — shadows, gradients, title bar, 16:9, PPT typography. All defs/shapes via scripts.

Load [reference/modify-existing-svg.md](reference/modify-existing-svg.md) for detailed steps.
</upgrade-to-ppt-quality>

</capabilities>

<rules>
<rule>**Zero manual coordinate math.** Positions, paths, SVG elements, viewBox, overlaps, contrast — ALWAYS compute via scripts. NEVER add/subtract coordinates, verify alignment, or compute midpoints mentally.</rule>
<rule>**Trust script output.** Do NOT re-verify script results with mental math. If unsure, run a validation script.</rule>
<rule>**Assembly-only SVG writing.** Nodes, edges, markers, defs MUST use `svg_builder.generate_node_svg()`, `svg_builder.generate_edge_svg()`, etc. For charts, use `chart_builder.render_*_chart()` — do NOT write chart SVG manually.</rule>
<rule>When computing geometry, routing, SVG generation, viewBox, or validation → load [reference/computation-snippets.md](reference/computation-snippets.md).</rule>
<rule>When user describes a process flow with decisions → apply **create-flowchart**.</rule>
<rule>When user describes a system with tiers/layers → apply **create-architecture-diagram**.</rule>
<rule>When user describes interactions between actors over time → apply **create-sequence-diagram**.</rule>
<rule>When user describes a central topic with branches → apply **create-concept-diagram**.</rule>
<rule>When user provides data for visual representation → apply **create-chart**.</rule>
<rule>When user provides SVG with overlapping elements → apply **analyze-and-fix-layout**.</rule>
<rule>When user wants to change colors/text/elements in existing SVG → apply **modify-existing-svg**.</rule>
<rule>When user wants PPT styling on existing SVG → apply **upgrade-to-ppt-quality**.</rule>
<rule>When request spans multiple diagram types → apply capabilities sequentially, compose into one SVG.</rule>
</rules>
