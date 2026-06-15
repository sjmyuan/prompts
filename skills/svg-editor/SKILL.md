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
Core rules for arranging elements. All geometric computations MUST use Python snippets, never manual reasoning.

- **Canvas**: `viewBox="0 0 960 540"` default. Leave 20–40px padding on all edges.
- **Spacing**: Minimum 20px gap between adjacent shapes. Group-related: 10–15px internal, 30–40px external.
- **Connection corridor**: Minimum 40px gap between shapes that need connection lines. Multi-line corridors: 60px+.
- **Line clearance at turns**: Any line bend must be ≥25px away from any other element's edge.
- **Alignment**: Same-level elements aligned to common baseline. Text centered within shapes.
- **Sizing**: Same semantic type → uniform size. Compute via `svg_shapes.get_shape_dimensions()`.
- **Z-order**: Render connections before shapes (lines appear underneath). Text labels on top.
- **Overlap avoidance**: Use `geometry.overlap()` / `geometry.find_overlapping()` — never manually check overlaps.
</svg-layout-principles>

<computation-snippets>
All geometric calculations — positions, paths, labels, colors, and SVG element generation — MUST be done by running Python snippets, never by AI reasoning or manual coordinate math.

**Scripts directory**: `skills/svg-editor/scripts/` — standalone `.py` files, no package, no orchestrator.

| Module | Purpose | Key functions |
|---|---|---|
| `svg_shapes.py` | SVG element strings for nodes, edges, labels, markers, title bars | `generate_node_svg()`, `generate_edge_svg()`, `generate_label_svg()`, `generate_title_bar()`, `generate_arrow_marker()`, `get_shape_dimensions()`, `get_node_type_colors()` |
| `geometry.py` | Bounding box math, overlap detection, intersections | `overlap()`, `find_overlapping()`, `connection_point()`, `center()`, `distance()`, `segment_line_intersection()` |
| `routing.py` | Orthogonal/bezier path computation, endpoint validation | `orthogonal_path()`, `connection_endpoints()`, `path_to_svg_d()`, `bezier_path()`, `detect_intersections()`, `endpoint_valid()` |
| `layout.py` | Grid/radial layout, force-directed overlap resolution, viewBox | `flow_layout()`, `decision_branch_positions()`, `resolve_overlaps()`, `force_directed_layout()`, `compute_viewbox()`, `distribute_along_circle()` |
| `labeling.py` | Label placement on connection paths | `label_position()`, `compute_all_labels()`, `label_overlap_check()` |
| `colors.py` | WCAG contrast, PPT palette, gradient/shadow defs | `contrast_ratio()`, `wcag_aa_check()`, `get_gradient_defs()`, `get_shadow_filter()`, `PPT_PALETTE` |

**Calling convention** — always use `python3 -c` with `sys.path.insert`:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from module_name import function_name
result = function_name(...)
print(result)
"
```

**Common snippet patterns** (use these verbatim when building diagrams):

**Compute node positions (flowchart grid)**:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from layout import flow_layout
from svg_shapes import get_shape_dimensions
nodes = [
    {'id': 'start', 'type': 'start', 'text': 'Start', 'row': 0, 'col': 0},
    {'id': 'p1', 'type': 'process', 'text': 'Step 1', 'row': 1, 'col': 0},
]
for n in nodes:
    dims = get_shape_dimensions(n['text'], n['type'], ppt_mode=True)
    n.update(dims)
nodes = flow_layout(nodes, 'top-to-bottom', node_gap=130, branch_gap=260, start_offset=(100, 140))
for n in nodes:
    print(f\"{n['id']}: x={n['x']:.0f} y={n['y']:.0f} w={n['width']:.0f} h={n['height']:.0f}\")
"
```

**Check shape overlaps**:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from geometry import find_overlapping
bboxes = [(100,140,130,48), (250,140,140,50)]
issues = find_overlapping(bboxes, margin=10)
print(f'Overlaps: {issues}')
"
```

**Route a connection between two shapes**:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from routing import connection_endpoints, orthogonal_path, path_to_svg_d
src_bbox = (100, 140, 130, 48)
dst_bbox = (250, 270, 140, 50)
src_pt, dst_pt, src_side, dst_side = connection_endpoints(src_bbox, dst_bbox)
waypoints = orthogonal_path(src_pt, dst_pt, src_side, dst_side)
print(path_to_svg_d(waypoints))
"
```

**Generate SVG for a shape**:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from svg_shapes import generate_node_svg, generate_edge_svg, generate_arrow_marker, generate_title_bar
node_svg = generate_node_svg('id', 'process', 'My Text', x=100, y=140, width=130, height=48)
edge_svg = generate_edge_svg('e1', 'M 165 188 L 320 188', style='solid')
marker = generate_arrow_marker()
title = generate_title_bar('Diagram Title', 960)
print(node_svg)
"
```

**Validate color contrast**:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from colors import wcag_aa_check
result = wcag_aa_check('#202124', '#E8F0FE')
print(f'Pass: {result[\"pass\"]}, Ratio: {result[\"ratio\"]}')
"
```

**Compute viewBox for SVG**:
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from layout import compute_viewbox
bboxes = [(100,140,130,48), (250,270,140,50), (100,270,130,48)]
vx, vy, vw, vh = compute_viewbox(bboxes, padding=40, target_aspect=16/9, title_bar_height=70)
print(f'viewBox=\"0 0 {vw} {vh}\"')
"
```

**SVG assembly pattern** (after computing all parts):
1. `<svg viewBox="...">` from computed viewBox
2. `<defs>` with `colors.get_shadow_filter()` + `colors.get_gradient_defs()` + arrow markers
3. Title bar from `svg_shapes.generate_title_bar(title, width)`
4. Connection `<path>` elements from `svg_shapes.generate_edge_svg()`
5. Shape elements from `svg_shapes.generate_node_svg()`
6. Label elements from `svg_shapes.generate_label_svg()`
7. `</svg>`</computation-snippets>

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
| Need to compute node positions, route connections, generate SVG elements, or validate layout | Python snippet modules for each computation task | [scripts/](scripts/) |
</context-loading-guide>

</knowledge>

<capabilities>

<create-flowchart>
**Objective**: Generate a PPT-presentation-quality flowchart, process diagram, or workflow as raw SVG.

**Steps**:
1. **Analyze the process**: Identify start/end nodes, process steps, decisions, branches, and flow direction from user description. Extract a diagram title.
2. **Build node/edge data**: Construct a list of nodes (with `id`, `type`, `text`, `row`, `col`) and edges (with `from`, `to`, optional `label`, `branch`).
3. **Compute positions via snippet**: Run the **Compute node positions** snippet from `<computation-snippets>` to get `x`, `y`, `width`, `height`, `bbox` for each node.
4. **Route connections**: For each edge, run the **Route a connection** snippet with the source/dest node bounding boxes to get SVG path strings.
5. **Generate SVG elements**: Run the **Generate SVG for a shape** snippet for each node and edge.
6. **Validate**: Run the **Check shape overlaps** and **Validate color contrast** snippets. Fix any issues.
7. **Compute viewBox**: Run the **Compute viewBox** snippet with all element bounding boxes.
8. **Assemble SVG**: Follow the **SVG assembly pattern** in `<computation-snippets>`.
9. **Output**: Return raw, valid SVG code with no surrounding explanation.

Load **reference/create-flowchart.md** for detailed step-by-step instructions.
</create-flowchart>

<create-architecture-diagram>
**Objective**: Generate a PPT-quality system architecture, component, or deployment diagram as raw SVG. Build node/edge data, call inline snippets from `<computation-snippets>` to compute positions/connections/SVG fragments, then assemble. Load **reference/create-architecture-diagram.md** for details.
</create-architecture-diagram>

<create-sequence-diagram>
**Objective**: Generate a PPT-quality sequence diagram showing message passing as raw SVG. Build node/edge data, call inline snippets from `<computation-snippets>` to compute positions/connections/SVG fragments, then assemble. Load **reference/create-sequence-diagram.md** for details.
</create-sequence-diagram>

<create-concept-diagram>
**Objective**: Generate a PPT-quality concept diagram, mind map, or visual explanation as raw SVG. Build node/edge data with central and branch nodes, call inline snippets from `<computation-snippets>` to compute radial positions/connections/SVG fragments, then assemble. Load **reference/create-concept-diagram.md** for details.
</create-concept-diagram>

<create-chart>
**Objective**: Generate a PPT-quality chart, graph, or data visualization as raw SVG. Build data series, compute positions/viewBox via snippets from `<computation-snippets>`, then render chart-specific elements (axes, bars, slices) manually. Load **reference/create-chart.md** for details.
</create-chart>

<analyze-and-fix-layout>
**Objective**: Analyze an existing SVG and fix overlapping elements, unclear connections, or poor spacing. Apply PPT-quality styling to the repaired output.

**Steps**:
1. **Parse SVG**: Identify all significant elements and their bounding boxes.
2. **Detect overlaps**: Run the **Check shape overlaps** snippet from `<computation-snippets>` with extracted bounding boxes.
3. **Detect connection issues**: Run the **Route a connection** snippet to check path intersections via `routing.detect_intersections()`.
4. **Fix**: Adjust positions, re-route connections via `routing.orthogonal_path()`, expand viewBox via `layout.compute_viewbox()`.
5. **Regenerate**: Re-run **Generate SVG for a shape** snippet with corrected positions.
6. **Validate**: Re-check overlaps and contrasts, verify no elements overflow viewBox.
7. **Output**: Return the complete corrected SVG.

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
<rule>When computing node positions, routing connections, generating SVG elements, or computing viewBox, ALWAYS use the corresponding snippets from `<computation-snippets>` — never manually calculate coordinates or write raw SVG.</rule>
<rule>When checking for overlapping elements, ALWAYS run the **Check shape overlaps** snippet — never visually estimate.</rule>
<rule>When validating connection endpoints or detecting line intersections, ALWAYS use `routing.detect_intersections()` or run the **Route a connection** snippet.</rule>
<rule>When validating color contrast, ALWAYS run the **Validate color contrast** snippet — never estimate visually.</rule>
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
