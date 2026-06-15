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
- User wants to edit, modify, or update an existing SVG diagram (colors, text, shapes, fonts, or styling)
- User wants SVG output that looks polished and professional enough for PowerPoint, Keynote, or Google Slides
- User wants an existing SVG upgraded to PPT-presentation quality (shadows, gradients, title hierarchy, slide-ready layout)
</when-to-use-this-skill>

<knowledge>

<ppt-design-requirements>
All SVG output must meet professional presentation standards suitable for PPT/Keynote/Google Slides.

- **Dimensions**: Default 16:9 aspect ratio (`viewBox="0 0 960 540"`). Diagram fills 60–85% of slide area. Include a **title bar** (bold centered title at top, `#1A73E8` background, white text).
- **Visual effects (PPT-style)**: Drop shadows on key shapes, soft linear gradients for fills (5–10% brightness variation), rounded corners (`rx="6"`+).
- **Typography**: Use `font-family="Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif"` everywhere. Title: 20–22px bold. Body: 14px. Annotations: 11px. Min readable: 10px.
- **Color contrast**: WCAG AA (≥4.5:1) for all text against background. Light fills with dark text. Avoid dark-on-dark or light-on-light.
- **Simplicity**: 5–8 main elements per diagram. ≤15 words per shape. Group related elements with subtle background panels. Minimum 40px between groups, 20px within groups.
</ppt-design-requirements>

<svg-layout-principles>
Core rules for arranging elements. Computation is handled by scripts; these are high-level design principles.

- **Canvas**: `viewBox="0 0 960 540"` default. Leave 20–40px padding on all edges.
- **Spacing**: Minimum 20px gap between adjacent shapes. Group-related: 10–15px internal, 30–40px external.
- **Connection corridor**: Minimum 40px gap between shapes that need connection lines. Multi-line corridors: 60px+.
- **Line clearance at turns**: Any line bend must be ≥25px away from any other element's edge.
- **Alignment**: Same-level elements aligned to common baseline. Text centered within shapes.
- **Sizing**: Same semantic type → uniform size. Compute via `svg_shapes.get_shape_dimensions()`.
- **Z-order**: Render connections before shapes (lines appear underneath). Text labels on top.
- **Overlap avoidance**: Use `python3 scripts/compute_all.py` — never manually check overlaps.
</svg-layout-principles>

<computation-scripts>
All geometric calculations — positions, paths, labels, colors, and SVG element generation — MUST be done by running Python scripts, never by AI reasoning or manual coordinate math.

**Scripts directory**: `skills/svg-editor/scripts/`

| Script | Purpose | Key output |
|---|---|---|
| `compute_all.py` | **Main orchestrator** — JSON in, complete layout + SVG fragments out | `nodes[].svg_shape`, `edges[].svg_line`, `labels[].svg_label`, `svg_markers`, `svg_title_bar` |
| `svg_shapes.py` | Generates SVG element strings for nodes, edges, labels, markers, title bars | Shape SVGs with proper colors, gradients, shadows per node type |
| `geometry.py` | Bounding box math, overlap detection, point/segment intersection | Overlap checks, connection points |
| `routing.py` | Orthogonal/bezier path computation, endpoint validation, intersection detection | Path d-strings, waypoints |
| `layout.py` | Grid/radial layout, force-directed overlap resolution, viewBox computation | Node positions, viewBox |
| `labeling.py` | Label placement on connection paths, overlap checking | Label positions with background rects |
| `colors.py` | WCAG contrast ratio, PPT palette, gradient/shadow SVG defs | Color validation, filter/gradient strings |

**Usage** — always run for new diagrams:
```bash
python3 scripts/compute_all.py '<json_description>'
```

**Input format** (JSON):
```json
{
  "diagram_type": "flowchart",
  "title": "Diagram Title",
  "ppt_mode": true,
  "nodes": [
    {"id": "start", "type": "start", "text": "Start", "row": 0, "col": 0},
    {"id": "p1", "type": "process", "text": "Step 1", "row": 1, "col": 0},
    {"id": "d1", "type": "decision", "text": "Ok?", "row": 2, "col": 0}
  ],
  "edges": [
    {"id": "e1", "from": "start", "to": "p1"},
    {"id": "e2", "from": "p1", "to": "d1", "label": "Yes"}
  ]
}
```

**Output fields**:
| Field | Description |
|---|---|
| `nodes[].svg_shape` | Complete SVG element string for this node (shape + text) |
| `edges[].svg_line` | Complete SVG `<path>` with marker and styling |
| `labels[].svg_label` | SVG `<rect>` + `<text>` for connection labels |
| `svg_markers` | Arrow marker `<defs>` (solid and dashed) |
| `svg_title_bar` | Title bar SVG elements (when `ppt_mode=true`) |
| `defs` | Shadow filter and gradient SVG definitions |
| `validation` | Overlap/intersection/color check results |
| `viewbox` | Computed `{x, y, width, height}` |

**SVG assembly** — after getting script output, just concatenate:
1. `<svg viewBox="...">` from `output.viewbox`
2. `<defs>` from `output.defs` + `output.svg_markers`
3. `output.svg_title_bar`
4. `output.edges[].svg_line` (connections first = appear underneath)
5. `output.nodes[].svg_shape` (shapes on top of lines)
6. `output.labels[].svg_label` (labels on top)
7. `</svg>`

**When to use individual scripts** (partial computations):
- `geometry.overlap()` to check specific shape overlaps
- `routing.orthogonal_path()` to re-route a single connection around an obstacle
- `colors.contrast_ratio()` to validate specific color pairs
- `svg_shapes.generate_node_svg()` to regenerate a single node shape
</computation-scripts>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Creating a flowchart with decision diamonds and branching paths | Complete flowchart example with orthogonal routing | [examples/flowchart-example.md](examples/flowchart-example.md) |
| Executing **create-flowchart** (need detailed steps) | Step-by-step flowchart creation instructions | [reference/create-flowchart.md](reference/create-flowchart.md) |
| Creating an architecture/system-design diagram with tiers | Architecture diagram example with layered layout | [examples/architecture-example.md](examples/architecture-example.md) |
| Executing **create-architecture-diagram** (need detailed steps) | Step-by-step architecture diagram instructions | [reference/create-architecture-diagram.md](reference/create-architecture-diagram.md) |
| Creating a UML-style sequence diagram with lifelines | Sequence diagram example with lifeline and activation bars | [examples/sequence-example.md](examples/sequence-example.md) |
| Executing **create-sequence-diagram** (need detailed steps) | Step-by-step sequence diagram instructions | [reference/create-sequence-diagram.md](reference/create-sequence-diagram.md) |
| Creating a concept map, mind map, or explanatory diagram | Concept diagram example with radial layout | [examples/concept-example.md](examples/concept-example.md) |
| Executing **create-concept-diagram** (need detailed steps) | Step-by-step concept diagram instructions | [reference/create-concept-diagram.md](reference/create-concept-diagram.md) |
| Creating a bar chart, pie chart, line chart, or data visualization | Chart example with axes, gridlines, and data series | [examples/chart-example.md](examples/chart-example.md) |
| Executing **create-chart** (need detailed steps) | Step-by-step chart creation instructions | [reference/create-chart.md](reference/create-chart.md) |
| Fixing overlapping elements or unclear connections in existing SVG | Layout fix example with before/after transformation | [examples/layout-fix-example.md](examples/layout-fix-example.md) |
| Executing **analyze-and-fix-layout** (need detailed steps) | Step-by-step layout analysis and fix instructions | [reference/analyze-and-fix-layout.md](reference/analyze-and-fix-layout.md) |
| Editing or modifying an existing SVG (color/text/element changes) | SVG editing example with style updates and restructuring | [examples/modify-existing-svg-example.md](examples/modify-existing-svg-example.md) |
| Executing **modify-existing-svg** (need detailed steps) | Step-by-step SVG modification instructions | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Upgrading existing SVG to PPT-presentation quality | PPT upgrade example with professional effects | [examples/layout-fix-example.md](examples/layout-fix-example.md) |
| Executing **upgrade-to-ppt-quality** (need detailed steps) | Step-by-step PPT upgrade instructions | [reference/modify-existing-svg.md](reference/modify-existing-svg.md) |
| Computing layout, paths, labels, or SVG fragments for any diagram | Python computation scripts for all geometric calculations | [scripts/compute_all.py](scripts/compute_all.py) |
| Need individual geometry/routing/layout/labeling/color functions | Python utility modules for partial computation | [scripts/](scripts/) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-flowchart>
**Objective**: Generate a PPT-presentation-quality flowchart, process diagram, or workflow as raw SVG.

**Steps**:
1. **Analyze the process**: Identify start/end nodes, process steps, decisions, branches, and flow direction from user description. Extract a diagram title.
2. **Build JSON description**: Construct JSON with `diagram_type: "flowchart"`, `ppt_mode: true`, `nodes[]` (with `id`, `type`, `text`, `row`, `col`), and `edges[]` (with `from`, `to`, optional `label` and `branch`). Omit `width`/`height` — scripts auto-compute.
3. **Run script**: Execute `python3 scripts/compute_all.py '<json>'`. Capture the JSON output.
4. **Review validation**: Check `validation.all_clear`. If `false`, fix overlaps/intersections by adjusting row/col spacing and re-running.
5. **Assemble SVG**: Concatenate `svg_markers` + `svg_title_bar` + connection `svg_line`s + node `svg_shape`s + label `svg_label`s inside `<svg viewBox="..."><defs>...</defs>...</svg>`.
6. **Output**: Return raw, valid SVG code with no surrounding explanation.

Load **reference/create-flowchart.md** for detailed step-by-step instructions.
</create-flowchart>

<create-architecture-diagram>
**Objective**: Generate a PPT-quality system architecture, component, or deployment diagram as raw SVG. Build JSON with `diagram_type: "architecture"`, run `compute_all.py`, assemble output. Load **reference/create-architecture-diagram.md** for details.
</create-architecture-diagram>

<create-sequence-diagram>
**Objective**: Generate a PPT-quality sequence diagram showing message passing as raw SVG. Build JSON with `diagram_type: "sequence"`, run `compute_all.py`, assemble output. Load **reference/create-sequence-diagram.md** for details.
</create-sequence-diagram>

<create-concept-diagram>
**Objective**: Generate a PPT-quality concept diagram, mind map, or visual explanation as raw SVG. Build JSON with `diagram_type: "concept"`, run `compute_all.py`, assemble output. Load **reference/create-concept-diagram.md** for details.
</create-concept-diagram>

<create-chart>
**Objective**: Generate a PPT-quality chart, graph, or data visualization as raw SVG. Build JSON with `diagram_type: "chart"`, run `compute_all.py`, assemble output. Load **reference/create-chart.md** for details.
</create-chart>

<analyze-and-fix-layout>
**Objective**: Analyze an existing SVG and fix overlapping elements, unclear connections, or poor spacing. Apply PPT-quality styling to the repaired output.

**Steps**:
1. **Parse SVG**: Identify all significant elements and their bounding boxes.
2. **Detect overlaps**: Run `python3 -c "from scripts.geometry import overlap; ..."` to check shape overlaps and reconstruct node/edge JSON for `compute_all.py` to detect connection issues.
3. **Fix**: Adjust positions, re-route connections via `routing.orthogonal_path()`, expand viewBox.
4. **Re-run script** with corrected JSON to regenerate clean SVG fragments.
5. **Output**: Return the complete corrected SVG.

Load **reference/analyze-and-fix-layout.md** for detailed steps.
</analyze-and-fix-layout>

<modify-existing-svg>
**Objective**: Modify an existing SVG — change colors, text, fonts, styling, or add/remove/rearrange elements. Load **reference/modify-existing-svg.md** for detailed steps.
</modify-existing-svg>

<upgrade-to-ppt-quality>
**Objective**: Upgrade an existing SVG to professional PPT quality by adding drop shadows, gradients, title bar, 16:9 dimensions, and PPT-standard typography.

**Steps**:
1. **Analyze current SVG**: Read the existing SVG. Note viewBox, colors, font families, existing `<defs>`.
2. **Set PPT viewBox**: Confirm 16:9 (960×540) with the user if aspect ratio changes.
3. **Generate PPT defs**: Call `colors.get_shadow_filter()` and `colors.get_gradient_defs()` for SVG definitions.
4. **Generate title bar**: Call `svg_shapes.generate_title_bar(title, width)`.
5. **Upgrade shapes**: Replace flat fills with gradient URLs, add `filter="url(#shadow)"`, increase `rx`/`ry`.
6. **Upgrade typography**: Replace font-family with PPT stack. Bump body font-size to 14px.
7. **Adjust spacing**: Increase gaps to 40px minimum. Add section background panels.
8. **Validate**: Check contrast via `colors.wcag_aa_check()`, verify no elements overflow viewBox.

Load **reference/modify-existing-svg.md** for detailed SVG editing patterns.
</upgrade-to-ppt-quality>

</capabilities>

<rules>
<rule>When generating ANY new SVG diagram, ALWAYS run `python3 scripts/compute_all.py` first with a JSON description. Use the output's SVG fragments (`svg_shape`, `svg_line`, `svg_label`, `svg_markers`, `svg_title_bar`) to assemble the SVG. Never manually write SVG elements or calculate coordinates.</rule>
<rule>When checking for overlapping elements, ALWAYS use `python3 -c "from scripts.geometry import overlap; ..."` — never visually estimate.</rule>
<rule>When validating connection endpoints or detecting line intersections, ALWAYS use `scripts/routing.py` functions.</rule>
<rule>When validating color contrast, ALWAYS use `python3 -c "from scripts.colors import contrast_ratio; ..."` — never estimate visually.</rule>
<rule>When the user describes a process flow with branching and decision steps, apply **create-flowchart**.</rule>
<rule>When the user describes a system with tiers, layers, or components, apply **create-architecture-diagram**.</rule>
<rule>When the user describes interactions between actors over time, apply **create-sequence-diagram**.</rule>
<rule>When the user describes a central topic with branching related concepts, apply **create-concept-diagram**.</rule>
<rule>When the user provides data values for visual representation, apply **create-chart**.</rule>
<rule>When the user provides an SVG with overlapping elements or unclear lines, apply **analyze-and-fix-layout**.</rule>
<rule>When the user wants to change colors, text, or elements in an existing SVG (without layout issues being primary), apply **modify-existing-svg**.</rule>
<rule>When the user wants professional PPT-quality styling on an existing SVG, apply **upgrade-to-ppt-quality**.</rule>
<rule>When the user's request spans multiple diagram types, apply capabilities sequentially and compose into a single SVG.</rule>
</rules>
