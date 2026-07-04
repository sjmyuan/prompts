---
name: svg-editor
description: Create SVG diagrams with professional PPT-quality layout, clear connections, and no overlapping elements. Use when creating flowcharts, architecture diagrams, comparison diagrams, pyramid diagrams, step-flow diagrams, container diagrams, sequence diagrams, concept diagrams, charts, or donut charts as SVG, or when fixing layout/styling issues in existing SVGs.
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

**Two SVG authoring approaches** — Use the right tool for the diagram type:

| Approach | Used for | Method |
|---|---|---|
| **Script-based** | Flowcharts, architecture diagrams, sequence diagrams, concept diagrams, bar/line/pie charts | Python scripts compute positions, paths, and SVG elements. See [reference/computation-snippets.md](reference/computation-snippets.md). |
| **Hand-crafted** | Comparison diagrams, pyramid diagrams, step-flow diagrams, container diagrams, donut charts, complex custom layouts | Agent writes SVG directly following the visual patterns in `examples/`. No scripts needed. |

**Design standards**: 16:9 aspect ratio (960×540), PPT-style shadows/gradients, system-ui/Segoe UI font stack, WCAG AA contrast, 5–8 elements max. See [reference/design-standards.md](reference/design-standards.md) for full details.

**Script modules** (`scripts/`): standalone `.py` files — no package, no orchestrator. Dependencies: `pip install svgwrite networkx matplotlib`.

| Module | Library | Purpose | Key functions |
|---|---|---|---|
| `svg_builder.py` | **svgwrite** | SVG elements for nodes, edges, labels, title bars | `generate_node_svg()`, `generate_edge_svg()`, `generate_title_bar()`, `generate_arrow_marker()`, `get_shape_dimensions()` |
| `graph_layout.py` | **networkx** | Grid/auto layout, viewBox, overlap resolution | `flow_layout()`, `auto_layout()`, `resolve_overlaps()`, `compute_viewbox()`, `distribute_along_circle()` |
| `chart_builder.py` | **matplotlib** | Bar, line, pie charts as SVG strings | `render_bar_chart()`, `render_line_chart()`, `render_pie_chart()` |
| `routing.py` | custom | Orthogonal/bezier paths, endpoint validation | `orthogonal_path()`, `connection_endpoints()`, `path_to_svg_d()`, `bezier_path()` |
| `geometry.py` | custom | BBox math, overlap detection | `overlap()`, `find_overlapping()`, `center()`, `connection_point()` |
| `labeling.py` | custom | Label placement on connections | `label_position()`, `compute_all_labels()` |
| `colors.py` | custom | WCAG contrast, PPT palette, gradient/shadow defs | `wcag_aa_check()`, `get_gradient_defs()`, `get_shadow_filter()`, `PPT_PALETTE` |

**SVG assembly pattern** (all types): `<svg>` with `viewBox` and `font-family` on root → `<defs>` (shadow filter + gradients + arrow markers) → background → title → layers/sections → connections/lines → shapes/nodes → labels/text → `</svg>`.

**Common visual conventions** (from hand-crafted examples):
- Set `font-family` on the root `<svg>` element: `font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"`
- Use `dominant-baseline="middle"` on all centered text inside shapes for vertical centering
- Use `text-anchor="middle"` with centered `x` values for title text
- Define linear gradients in `<defs>` for panel backgrounds and section headers
- Layer backgrounds (`<rect>` with `rx`) behind grouped elements for visual panels
- Use `<filter id="shadow">` with `feDropShadow` for depth on key elements
- Panel headers: full-width colored `<rect>` at top of panel area, same `rx` as panel, with matching extension rect below
- Add bottom annotations/legend boxes with dashed borders for additional context
- Use `<g id="...">` in `<defs>` for reusable icons/avatars
- Color-code sections semantically (red for problems/warnings, green for success, blue for info, orange for warnings)

**Load [reference/computation-snippets.md](reference/computation-snippets.md) when you need to compute positions, route connections, generate SVG elements, validate overlaps/contrast, or compute viewBox.**

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Executing **create-flowchart** | Step-by-step flowchart creation instructions | [reference/create-flowchart.md](reference/create-flowchart.md) |
| Executing **create-architecture-diagram** | Step-by-step architecture diagram instructions | [reference/create-architecture-diagram.md](reference/create-architecture-diagram.md) |
| Executing **create-sequence-diagram** | Step-by-step sequence diagram instructions | [reference/create-sequence-diagram.md](reference/create-sequence-diagram.md) |
| Executing **create-concept-diagram** | Step-by-step concept diagram instructions | [reference/create-concept-diagram.md](reference/create-concept-diagram.md) |
| Executing **create-chart** | Step-by-step chart creation instructions | [reference/create-chart.md](reference/create-chart.md) |
| Executing **create-comparison-diagram** | Step-by-step comparison diagram instructions | [reference/create-comparison-diagram.md](reference/create-comparison-diagram.md) |
| Executing **create-pyramid-diagram** | Step-by-step pyramid diagram instructions | [reference/create-pyramid-diagram.md](reference/create-pyramid-diagram.md) |
| Executing **create-step-flow-diagram** | Step-by-step step-flow diagram instructions | [reference/create-step-flow-diagram.md](reference/create-step-flow-diagram.md) |
| Executing **create-container-diagram** | Step-by-step container diagram instructions | [reference/create-container-diagram.md](reference/create-container-diagram.md) |
| Executing **create-donut-chart** | Step-by-step donut chart instructions | [reference/create-donut-chart.md](reference/create-donut-chart.md) |
| Executing **analyze-and-fix-layout** | Step-by-step layout fix instructions | [reference/analyze-and-fix-layout.md](reference/analyze-and-fix-layout.md) |
| Executing **modify-existing-svg** or **upgrade-to-ppt-quality** | Step-by-step SVG modification/upgrade instructions | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Need example output for any diagram type | Example SVG/markdown files for each diagram type | [examples/](examples/) |
| Need help with arrow/arrowhead connections | Arrow marker geometry, refX/refY, orient=auto, common mistakes | [examples/arrow-connections-example.md](examples/arrow-connections-example.md) |
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

<create-comparison-diagram>
**Objective**: Generate a PPT-quality comparison diagram as raw SVG — side-by-side panels comparing two or more concepts, approaches, or states. Hand-crafted approach (no scripts).

**Steps**:
1. **Identify the comparison structure**: Determine number of columns (2 or 3), column headers, and items per column. Extract diagram title.
2. **Plan layout**: Use a wide viewBox (800–960 wide). Allocate equal widths per column (~300–350px) with 20–40px gap. Leave 40–50px top for title and 40–50px bottom for summary/legend.
3. **Draw backgrounds and headers**:
   - Full-width background `<rect>` with `fill="#f8f9fa"` or light gradient.
   - Column headers: colored `<rect>` with matching extension below for clean header-panel merge.
   - Semantic colors: red/orange for problem/negative columns, blue for neutral/info, green for positive/solution.
4. **Draw items within each column**: Each item is a `<rect>` with white fill, colored stroke, `rx="6"`–`rx="8"`. Include an icon circle (`<circle>`) with icon text inside (X/✓/⚠/✕ etc.) and description text. Add inline tags like "常见" or "危险" at the end edge.
5. **Add bottom summary boxes**: Dashed-border `<rect>` per column with `stroke-dasharray="4,3"` summarizing the column's conclusion.
6. **Add center divider** (optional): `<line>` with VS badge for two-column comparisons.
7. **Define gradients and defs**: Create `<linearGradient>` entries for each column's background. Define `<marker>` entries for arrows if used.
8. **Finalize**: Verify alignment (same y-coordinates for same-row items across columns), text contrast, and no overlapping elements. Output raw SVG.

**Reference examples**: `examples/diagnosis-comparison.svg`, `examples/supply-vs-demand-thinking.svg`, `examples/channel-better-than-block-decision-flow.svg`, `examples/solve-vs-align-decision-mode.svg`

Load [reference/create-comparison-diagram.md](reference/create-comparison-diagram.md) for detailed steps.
</create-comparison-diagram>

<create-pyramid-diagram>
**Objective**: Generate a PPT-quality pyramid diagram as raw SVG — layered trapezoids stacked vertically representing hierarchy or levels. Hand-crafted approach (no scripts).

**Steps**:
1. **Identify layers**: Determine the number of layers (typically 3–5), layer names, and descriptions. Extract diagram title.
2. **Plan layout**: Use a tall viewBox (720–800 high). Pyramid base at bottom, apex at top. Each layer is a centered trapezoid (`<polygon>`) wider at bottom, narrower at top.
3. **Compute polygon points**: For each layer, compute the four corner points. The bottom layer spans the full width (e.g., `60,420` to `660,420`). Each successive layer narrows symmetrically (e.g., subtract 60–100px from each side per layer). Keep consistent vertical spacing (60–80px per layer).
4. **Draw layers**: Each layer is a `<polygon>` with gradient fill and colored stroke. Add a subtle highlight polygon at the bottom edge of each layer with `opacity="0.15"`.
5. **Add layer labels**: Centered `<text>` per layer with bold name and smaller description below.
6. **Add side annotations**: Circle badges with layer initial (S/R/K) and error type name on the right side, connected implicitly by alignment. Use matching semantic colors per layer (green→skill, orange→rule, red→knowledge).
7. **Add side indicators** (optional): Left-side vertical bar with "认知负荷" label, arrow indicators pointing high/low.
8. **Add divider lines**: Dashed horizontal lines between layers for visual separation.
9. **Finalize**: Verify pyramid is symmetric, labels are centered, colors are semantic. Output raw SVG.

**Reference examples**: `examples/srk-pyramid.svg`

Load [reference/create-pyramid-diagram.md](reference/create-pyramid-diagram.md) for detailed steps.
</create-pyramid-diagram>

<create-step-flow-diagram>
**Objective**: Generate a PPT-quality horizontal step-flow diagram as raw SVG — numbered steps arranged left-to-right showing a sequence. Hand-crafted approach (no scripts).

**Steps**:
1. **Identify steps**: Determine the number of steps (4–6), step titles, and key bullet points per step. Extract diagram title.
2. **Plan layout**: Use a wide viewBox (960 wide, 300–360 high). Distribute steps evenly horizontally. Each step box is ~130–160px wide with ~190px height. Leave 50–60px top for title, 30–40px bottom for legend.
3. **Draw step boxes**: Each step is a `<rect>` with gradient fill, colored stroke `rx="12"`, and `filter="url(#shadow)"` for depth. Use distinct gradient colors per step (indigo→green→orange→red→purple, or similar progression).
4. **Add numbered circles**: `<circle>` with white fill and number text inside at the top-center of each step box. Use the box's gradient's dominant color for the circle fill.
5. **Add step content**: Bold title text, subtitle text below, a thin `<line>` separator, and 2–4 bullet-point style `<text>` lines inside each box.
6. **Draw connecting arrows**: `<line>` elements with `marker-end="url(#arrow)"` between adjacent step boxes. Arrow markers defined in `<defs>` with `refX="10" refY="4"`.
7. **Add feedback/loop arrows** (optional): `<path>` with dashed stroke below the steps forming a loop from last step back to first step, with label text.
8. **Add bottom legend**: Full-width `<rect>` at bottom with centered insight text.
9. **Finalize**: Verify even horizontal spacing, alignment of circles and text, arrow tips touching box edges. Output raw SVG.

**Reference examples**: `examples/five-step-flow.svg`

Load [reference/create-step-flow-diagram.md](reference/create-step-flow-diagram.md) for detailed steps.
</create-step-flow-diagram>

<create-container-diagram>
**Objective**: Generate a PPT-quality container/boundary diagram as raw SVG — a bounded region containing items, with external elements positioned around it. Hand-crafted approach (no scripts).

**Steps**:
1. **Identify structure**: Determine the main container (central bounded area), items inside the container, and external elements positioned around it. Extract diagram title.
2. **Plan layout**: Use a standard viewBox (800 wide, 500 high). The container is a large `<rect>` with dashed stroke occupying the center ~80% of the canvas. External elements sit outside the container on all four sides.
3. **Draw the container**: Large `<rect>` with `stroke-dasharray="8,4"`, light background fill, `rx="12"`. Add a label badge on the container's top border (a small `<rect>` with text overlapping the border line).
4. **Draw internal items**: Grouped `<rect>` elements inside the container with consistent styling. Optionally apply a secondary dashed boundary around internal groups (e.g., big companies).
5. **Draw external elements**: Positioned around the container (top-left, top-right, left-mid, right-mid, bottom-left, bottom-right) as smaller `<rect>` boxes. Connect them to the container with `<line>` arrows pointing outward (away from container) or inward (toward container).
6. **Add strategy flow** (optional): At the bottom, a horizontal path flow showing the sequence of actions (e.g., "切入细分市场 → 站稳脚跟 → 逐步扩展") with pill-shaped rounded rects and connecting arrows.
7. **Define defs**: Arrow markers with appropriate colors. Shadow filters if needed.
8. **Finalize**: Verify container border is dashed, external elements are evenly distributed, labels fit within boxes, arrow connections are clear. Output raw SVG.

**Reference examples**: `examples/niche-market-strategy.svg`, `examples/feedback-architecture.svg`

Load [reference/create-container-diagram.md](reference/create-container-diagram.md) for detailed steps.
</create-container-diagram>

<create-donut-chart>
**Objective**: Generate a PPT-quality donut chart as raw SVG — proportional segments with annotations. Hand-crafted approach (no scripts).

**Steps**:
1. **Identify data**: Determine total value, segment values/percentages, and labels. Extract chart title and data source.
2. **Plan layout**: Use a viewBox 800 wide, 470–500 high. Center donut at approximately `(330, 210)` with radius ~80px and stroke-width ~40px. Leave room for side annotations and bottom data box.
3. **Draw background donut**: Full circle `<circle>` with light gray `stroke="#EEEEEE"` as the base ring.
4. **Draw colored segments**: For each segment, use a `<circle>` with `stroke-dasharray` and `stroke-dashoffset` to create proportional arcs. Rotate by -90 degrees to start from top. Use `stroke-linecap="butt"` for clean segment edges.
   - Calculate dash array: `segment_length = percentage * PI * 2 * radius`, `total = PI * 2 * radius`
   - Each subsequent segment's offset = previous segment's offset - segment_length
5. **Draw center hole**: Smaller `<circle>` with white fill and `stroke="#E0E0E0"` over the center, creating the donut hole. Add total value label inside.
6. **Add annotation boxes**: Side `<rect>` boxes with colored circles/badges, connected to their respective donut segments with `<line>` arrows. Include percentage, title, and 2-3 bullet points.
7. **Add bottom data box**: `<rect>` at the bottom with data source or additional context text.
8. **Finalize**: Verify segment proportions visually match data, annotation arrows point to correct segments, text is readable. Output raw SVG.

**Reference examples**: `examples/survival-rate-chart.svg`

Load [reference/create-donut-chart.md](reference/create-donut-chart.md) for detailed steps.
</create-donut-chart>

</capabilities>

<rules>
<rule>**Script-based diagrams (flowchart, architecture, sequence, concept, chart):** Positions, paths, SVG elements, viewBox, overlaps, contrast — MUST compute via scripts. NEVER add/subtract coordinates, verify alignment, or compute midpoints mentally. Trust script output.</rule>
<rule>**Hand-crafted diagrams (comparison, pyramid, step-flow, container, donut):** Agent writes SVG directly following the visual patterns in `examples/`. Coordinate positioning is done by careful spatial reasoning, not scripts. Use the reference files for detailed steps.</rule>
<rule>**Assembly-only SVG writing (script-based types).** Nodes, edges, markers, defs MUST use `svg_builder.generate_node_svg()`, `svg_builder.generate_edge_svg()`, etc. For charts, use `chart_builder.render_*_chart()` — do NOT write chart SVG manually.</rule>
<rule>When computing geometry, routing, SVG generation, viewBox, or validation for script-based types → load [reference/computation-snippets.md](reference/computation-snippets.md).</rule>
<rule>When creating a hand-crafted diagram type → load the corresponding reference file and consult the matching example SVG in `examples/` for visual guidance.</rule>
<rule>When user describes a process flow with decisions → apply **create-flowchart**.</rule>
<rule>When user describes a system with tiers/layers → apply **create-architecture-diagram**.</rule>
<rule>When user asks for a side-by-side or panel comparison → apply **create-comparison-diagram**.</rule>
<rule>When user describes a layered/hierarchical stack or pyramid structure → apply **create-pyramid-diagram**.</rule>
<rule>When user describes numbered steps or a horizontal process sequence → apply **create-step-flow-diagram**.</rule>
<rule>When user describes a bounded region/territory with items inside and outside → apply **create-container-diagram**.</rule>
<rule>When user describes interactions between actors over time → apply **create-sequence-diagram**.</rule>
<rule>When user describes a central topic with branches → apply **create-concept-diagram**.</rule>
<rule>When user provides data for visual representation → apply **create-chart**.</rule>
<rule>When user asks for a donut/proportional chart with annotations → apply **create-donut-chart**.</rule>
<rule>When user provides SVG with overlapping elements → apply **analyze-and-fix-layout**.</rule>
<rule>When user wants to change colors/text/elements in existing SVG → apply **modify-existing-svg**.</rule>
<rule>When user wants PPT styling on existing SVG → apply **upgrade-to-ppt-quality**.</rule>
<rule>When request spans multiple diagram types → apply capabilities sequentially, compose into one SVG.</rule>
</rules>
