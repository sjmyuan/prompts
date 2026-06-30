# Computation Snippets — Script Calling Guide

> **🔴 ZERO-TOLERANCE RULE: No manual coordinate math.** Every bounding box, path string, position offset, dimension, color value, and SVG element string MUST come from a Python script execution. Never add/subtract coordinates mentally, verify path alignment, compute center points, or manually check path connections. Run the script, capture output, assemble the pieces. **Trust the script output.**

## Scripts Directory

`skills/svg-editor/scripts/` — standalone `.py` files, no package, no orchestrator.

**Dependencies**: `pip install svgwrite networkx matplotlib`  
(`pygraphviz` optional — enables Graphviz hierarchical layout)

| Module | Library | Purpose | Key functions |
|---|---|---|---|
| `svg_builder.py` | **svgwrite** | SVG elements for nodes, edges, labels, markers, title bars | `generate_node_svg()`, `generate_edge_svg()`, `generate_label_svg()`, `generate_title_bar()`, `generate_arrow_marker()`, `get_shape_dimensions()`, `get_node_type_colors()` |
| `graph_layout.py` | **networkx** | Grid/auto layout, viewBox, overlap resolution | `flow_layout()`, `auto_layout()`, `decision_branch_positions()`, `resolve_overlaps()`, `compute_viewbox()`, `distribute_along_circle()` |
| `chart_builder.py` | **matplotlib** | Complete chart SVG strings | `render_bar_chart()`, `render_line_chart()`, `render_pie_chart()` |
| `routing.py` | custom | Orthogonal/bezier path computation, endpoint validation | `orthogonal_path()`, `connection_endpoints()`, `path_to_svg_d()`, `bezier_path()`, `detect_intersections()`, `endpoint_valid()` |
| `geometry.py` | custom | Bounding box math, overlap detection, intersections | `overlap()`, `find_overlapping()`, `connection_point()`, `center()`, `distance()`, `segment_line_intersection()` |
| `labeling.py` | custom | Label placement on connection paths | `label_position()`, `compute_all_labels()`, `label_overlap_check()` |
| `colors.py` | custom | WCAG contrast, PPT palette, gradient/shadow defs | `contrast_ratio()`, `wcag_aa_check()`, `get_gradient_defs()`, `get_shadow_filter()`, `PPT_PALETTE` |

## Calling Convention

Always use `python3 -c` with `sys.path.insert`:

```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from module_name import function_name
result = function_name(...)
print(result)
"
```

## SVG Assembly Pattern

1. `<svg viewBox="...">` from `graph_layout.compute_viewbox()`
2. `<defs>` with `colors.get_shadow_filter()` + `colors.get_gradient_defs()` + `svg_builder.generate_arrow_marker()`
3. Title bar from `svg_builder.generate_title_bar(title, width)`
4. Connection `<path>` elements from `svg_builder.generate_edge_svg()`
5. Shape elements from `svg_builder.generate_node_svg()`
6. Label elements from `svg_builder.generate_label_svg()`
7. `</svg>`

> **Chart shortcut**: for bar/line/pie charts, call `chart_builder.render_*_chart()` instead — returns a complete standalone SVG, skipping the manual assembly above.

## Arrow Marker Geometry (Critical for Correct Connections)

**Understanding the arrow marker is essential to avoid misaligned arrowheads.** The marker is a triangle drawn in its own coordinate system and placed at the end of a `<path>` via `marker-end="url(#arrow)"`.

### Marker Coordinate System

```
Marker-local coordinates (arrow points RIGHT):
   (0,0) ─────────────────── (arrow_width, 0)
   │  ▲                      /
   │  │ base               /
   │  ▼                  /  ← tip at (arrow_width, arrow_height/2)
   (0, arrow_height) ───
```

The arrow path: `M 0 0 L {arrow_width} {arrow_height/2} L 0 {arrow_height} z`

### The refX / refY Problem

`refX` and `refY` define which point in the marker aligns with the **line endpoint**.

| Setting | Line connects to | Visual effect | Use case |
|---|---|---|---|
| `refX=0, refY=0` **(SVG default, WRONG for arrows)** | Top-left corner of triangle base | Arrow visually offset from line | Never — this is the bug |
| `refX=arrow_width, refY=half_h` **(tip_ref=True, RECOMMENDED)** | Arrow **tip** | Tip touches target shape edge, arrowhead extends backward along the line | **Standard diagrams** — arrow tip touches the target shape |
| `refX=0, refY=half_h` **(tip_ref=False)** | Center of arrow **base** | Line ends at base, tip extends forward | When the line should visibly stop before the target |

### How orient="auto" Rotates the Arrow

With `orient="auto"`, SVG examines the line's last segment direction and rotates the marker accordingly. The marker's x-axis always aligns with the line direction:

| Line direction | Arrow rotation | refX direction | refY direction |
|---|---|---|---|
| → (right) | 0° (no rotation) | → right | ↓ down |
| ↓ (down) | 90° CW | ↓ down | ← left |
| ← (left) | 180° | ← left | ↑ up |
| ↑ (up) | 270° CW | ↑ up | → right |

### markerUnits="strokeWidth" — Size Scaling

With `markerUnits="strokeWidth"`, all marker coordinates are multiplied by the stroke width of the line. Example:
- `arrow_width=10, stroke-width=2` → actual arrow width = 20 user-space units
- `arrow_width=10, stroke-width=1.5` → actual arrow width = 15 user-space units

**Rule of thumb**: For a typical diagram with stroke-width=2, an `arrow_width` of 8–10 produces a well-proportioned arrowhead.

### Correct Call Pattern

```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from svg_builder import generate_arrow_marker

# Standard arrow: tip touches the target shape edge
# This goes in <defs> and is referenced by generate_edge_svg() as marker-end
print(generate_arrow_marker('arrow', '#555555', arrow_width=10, arrow_height=10, tip_ref=True))
"
```

When using `generate_edge_svg()`, the arrow marker `#arrow` is automatically referenced via `marker_end="url(#arrow)"`. The edge path's last point should be on the **edge of the target shape** — the arrow tip will be placed exactly there.

### Verifying Arrow Alignment

To programmatically verify that an arrow will connect correctly:

```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from routing import connection_endpoints
from geometry import BBox

src = (100, 200, 130, 48)   # source bbox
dst = (300, 400, 130, 48)   # target bbox
src_pt, dst_pt, src_side, dst_side = connection_endpoints(src, dst, 'top-to-bottom')
# dst_pt is on the EDGE of the target shape
# With refX=arrow_width (tip_ref=True), the arrow TIP will be exactly at dst_pt
print(f'Source exit: {src_pt}, side={src_side}')
print(f'Target entry: {dst_pt}, side={dst_side}')
print(f'Arrow tip will be at: {dst_pt}')
"
```

## Common Script Calls

**Compute node positions (grid layout):**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from graph_layout import flow_layout
from svg_builder import get_shape_dimensions
nodes = [{'id':'start','type':'start','text':'Start','row':0,'col':0}]
for n in nodes:
    dims = get_shape_dimensions(n['text'], n['type'], ppt_mode=True)
    n.update(dims)
nodes = flow_layout(nodes, 'top-to-bottom', node_gap=130, branch_gap=260, start_offset=(100,140))
for n in nodes: print(f\"{n['id']}: x={n['x']:.0f} y={n['y']:.0f} w={n['width']:.0f} h={n['height']:.0f}\")
"
```

**Compute node positions (automatic layout via networkx):**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from graph_layout import auto_layout
from svg_builder import get_shape_dimensions
nodes = [{'id':'A','type':'process','text':'Step A'},{'id':'B','type':'process','text':'Step B'}]
edges = [{'from':'A','to':'B'}]
for n in nodes:
    n.update(get_shape_dimensions(n['text'], n['type']))
# layout_type: 'hierarchical' (needs pygraphviz), 'spring', or 'radial'
nodes = auto_layout(nodes, edges, layout_type='spring')
for n in nodes: print(f\"{n['id']}: x={n['x']:.0f} y={n['y']:.0f}\")
"
```

**Route connection:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from routing import connection_endpoints, orthogonal_path, path_to_svg_d
src_pt, dst_pt, src_side, dst_side = connection_endpoints(src_bbox, dst_bbox)
waypoints = orthogonal_path(src_pt, dst_pt, src_side, dst_side)
print(path_to_svg_d(waypoints))
"
```

**Generate SVG elements:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from svg_builder import generate_node_svg, generate_edge_svg
print(generate_node_svg('id', 'process', 'Text', x=100, y=140, width=130, height=48))
print(generate_edge_svg('e1', 'M 165 188 L 320 188'))
"
```

**Render a chart (returns complete SVG — no manual assembly needed):**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from chart_builder import render_bar_chart
svg = render_bar_chart(['Q1','Q2','Q3','Q4'], [120,145,98,175], 'Quarterly Revenue', ylabel='USD (k)')
print(svg)
"
```

**Validate overlap:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from geometry import find_overlapping
print(find_overlapping(bboxes, margin=10))
"
```

**Validate contrast:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from colors import wcag_aa_check
print(wcag_aa_check('#202124', '#E8F0FE'))
"
```

**Compute viewBox:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from graph_layout import compute_viewbox
vx, vy, vw, vh = compute_viewbox(bboxes, padding=40, target_aspect=16/9, title_bar_height=70)
print(f'viewBox=\"0 0 {vw} {vh}\"')
"
```
