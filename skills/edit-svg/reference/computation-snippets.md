# Computation Snippets — Script Calling Guide

> **🔴 ZERO-TOLERANCE RULE: No manual coordinate math.** Every bounding box, path string, position offset, dimension, color value, and SVG element string MUST come from a Python script execution. Never add/subtract coordinates mentally, verify path alignment, compute center points, or manually check path connections. Run the script, capture output, assemble the pieces. **Trust the script output.**

## Scripts Directory

`skills/edit-svg/scripts/` — standalone `.py` files, no package, no orchestrator.

**Dependencies**: `pip install svgwrite networkx matplotlib`  
(`pygraphviz` optional — enables Graphviz hierarchical layout)

| Module | Library | Purpose | Key functions |
|---|---|---|---|
| `svg_builder.py` | **svgwrite** | SVG elements for nodes, edges, labels, markers, title bars | `generate_node_svg()`, `generate_edge_svg()`, `generate_label_svg()`, `generate_title_bar()`, `generate_arrow_marker()`, `get_shape_dimensions()`, `get_node_type_colors()` |
| `graph_layout.py` | **networkx** | Grid/auto layout, viewBox, overlap resolution | `flow_layout()`, `auto_layout()`, `decision_branch_positions()`, `resolve_overlaps()`, `compute_viewbox()`, `distribute_along_circle()` |
| `chart_builder.py` | **matplotlib** | Complete chart SVG strings | `render_bar_chart()`, `render_line_chart()`, `render_pie_chart()` |
| `routing.py` | custom | Orthogonal/bezier path computation, endpoint validation, multi-port routing | `orthogonal_path()`, `connection_endpoints()`, `path_to_svg_d()`, `bezier_path()`, `detect_intersections()`, `endpoint_valid()`, `route_with_port_allocation()` |
| `geometry.py` | custom | Bounding box math, overlap detection, intersections, multi-port allocation | `overlap()`, `find_overlapping()`, `connection_point()`, `center()`, `distance()`, `segment_line_intersection()`, `get_side_ports()`, `find_closest_port()`, `allocate_ports_for_edges()` |
| `labeling.py` | custom | Label placement on connection paths | `label_position()`, `compute_all_labels()`, `label_overlap_check()` |
| `colors.py` | custom | WCAG contrast, PPT palette, gradient/shadow defs | `contrast_ratio()`, `wcag_aa_check()`, `get_gradient_defs()`, `get_shadow_filter()`, `PPT_PALETTE` |

## Calling Convention

### Preferred: Standalone Python Script

For ALL diagram generation, create a dedicated `.py` file in the workspace. This enables iterative refinement without re-typing full commands.

**Script template**: Start every script with this structure:

```python
import sys
import os

# Add the skill scripts directory to the import path
sys.path.insert(0, '/Users/ganggang/work/prompts/skills/edit-svg/scripts')

from graph_layout import flow_layout, compute_viewbox
from routing import orthogonal_path, connection_endpoints, path_to_svg_d, endpoint_valid, detect_intersections, route_with_port_allocation
from geometry import connection_point, find_overlapping, BBox, get_side_ports, find_closest_port, allocate_ports_for_edges
from svg_builder import (
    generate_node_svg, generate_edge_svg, generate_label_svg,
    generate_title_bar, generate_arrow_marker, get_shape_dimensions
)
from colors import get_shadow_filter, get_gradient_defs, wcag_aa_check


def build_diagram():
    # ── Step 1: Define node/edge data ──
    nodes = [...]
    edges = [...]

    # ── Step 2: Compute dimensions and positions ──
    for n in nodes:
        dims = get_shape_dimensions(n['text'], n['type'], ppt_mode=True)
        n.update(dims)
    nodes = flow_layout(nodes, 'top-to-bottom', node_gap=130, branch_gap=260, start_offset=(100, 140))

    # Align same-row nodes to the same y-coordinate
    rows = {}
    for n in nodes:
        rows.setdefault(n['row'], []).append(n)
    for row_nodes in rows.values():
        max_h = max(n['height'] for n in row_nodes)
        base_y = min(n['y'] for n in row_nodes)
        for n in row_nodes:
            n['y'] = base_y + (max_h - n['height']) / 2
            n['bbox'] = (n['x'], n['y'], n['width'], n['height'])

    # ── Step 3: Route connections with port allocation ──
    node_map = {n['id']: n for n in nodes}
    obstacles = [n['bbox'] for n in nodes]

    # Use route_with_port_allocation() — allocates distinct ports per side per node,
    # routes orthogonal paths, and applies mid-offsets for parallel edge pairs.
    # Each edge must have: 'from', 'to', 'src_side', 'dst_side'
    edges = route_with_port_allocation(edges, node_map, ports_per_side=3, clearance=25, obstacles=obstacles)

    # ── Step 4: Validate connections ──
    for i, e in enumerate(edges):
        wps = e['waypoints']
        result = endpoint_valid(wps, node_map[e['to']]['bbox'])
        assert result['valid'], f"Edge {i} invalid: {result['issues']}"

    # ── Step 5: Generate SVG elements ──
    svg_fragments = []
    for n in nodes:
        svg_fragments.append(generate_node_svg(n['id'], n['type'], n['text'], n['x'], n['y'], n['width'], n['height']))
    for i, e in enumerate(edges):
        d = e['path_d']  # Already computed by route_with_port_allocation
        svg_fragments.append(generate_edge_svg(e.get('id', f'e{i}'), d, color=e.get('color', '#555555')))

    # ── Step 6: Generate defs and assemble ──
    viewbox = compute_viewbox([n['bbox'] for n in nodes], padding=40, target_aspect=16/9, title_bar_height=70)
    shadow = get_shadow_filter()
    gradients = get_gradient_defs()
    arrow = generate_arrow_marker('arrow', '#555555', arrow_width=10, arrow_height=10, tip_ref=True)
    title_svg = generate_title_bar('Diagram Title', viewbox[2])

    # Assemble final SVG
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox[0]} {viewbox[1]} {viewbox[2]} {viewbox[3]}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">',
        '<defs>', shadow, gradients, arrow, '</defs>',
        title_svg,
        *svg_fragments,
        '</svg>',
    ]
    return '\n'.join(svg_parts)


if __name__ == '__main__':
    svg = build_diagram()
    output_path = os.path.join(os.path.dirname(__file__), 'diagram.svg')
    with open(output_path, 'w') as f:
        f.write(svg)
    print(f'SVG saved to {output_path}')
```

### Alternative: Inline `python3 -c` (for one-off validation only)

Use inline calls only for quick validation checks after the main script has been written:

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

> **Prefer the standalone script template above** over inline calls. The snippets below show the API signatures for individual function calls — use them as reference when writing your script, not as standalone commands for complex diagrams.

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

**Route connection (default — forward edges):**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from routing import connection_endpoints, orthogonal_path, path_to_svg_d
src_pt, dst_pt, src_side, dst_side = connection_endpoints(src_bbox, dst_bbox, 'top-to-bottom')
waypoints = orthogonal_path(src_pt, dst_pt, src_side, dst_side, clearance=25, obstacles=obs_bboxes)
print(path_to_svg_d(waypoints))
"
```

**Route connection with manual side specification (feedback/cross edges):**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from routing import orthogonal_path, path_to_svg_d
from geometry import connection_point
# Specify sides manually: e.g., right-to-left or bottom-to-top
src_pt = connection_point(src_bbox, 'right')   # exit from right side
dst_pt = connection_point(dst_bbox, 'left')    # enter from left side
waypoints = orthogonal_path(src_pt, dst_pt, 'right', 'left', clearance=25, obstacles=obs_bboxes)
print(f'Waypoints: {len(waypoints)}')
print(path_to_svg_d(waypoints))
"
```

**Corridor-based routing for cross-column feedback edges** (use inside a standalone script):

```python
from geometry import connection_point

# corridor_x = midpoint between main column right edge and branch column left edge
corridor_x = 530

# For each feedback edge going from bottom of branch column to top of main column
src = node_map['BRANCH_BOTTOM_NODE']  # bottom of branch column
dst = node_map['MAIN_TOP_NODE']       # top of main column

source_exit = connection_point(src['bbox'], 'top-right')  # exit from top-right of source
target_entry = connection_point(dst['bbox'], 'bottom')     # enter from bottom of target

# Clean 4-waypoint path through shared corridor
path = [
    source_exit,
    (corridor_x, source_exit[1]),   # horizontal to corridor
    (corridor_x, target_entry[1]),  # vertical along corridor
    target_entry,                    # horizontal to target
]

# All feedback edges share the same corridor_x for visual consistency
from routing import path_to_svg_d
d = path_to_svg_d(path)
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
