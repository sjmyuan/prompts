# Computation Snippets — Script Calling Guide

> **🔴 ZERO-TOLERANCE RULE: No manual coordinate math.** Every bounding box, path string, position offset, dimension, color value, and SVG element string MUST come from a Python script execution. Never add/subtract coordinates mentally, verify path alignment, compute center points, or manually check path connections. Run the script, capture output, assemble the pieces. **Trust the script output.**

## Scripts Directory

`skills/edit-svg/scripts/` — standalone `.py` files, no package, no orchestrator.

**Dependencies**: `pip install svgwrite networkx matplotlib`  
(`pygraphviz` optional — enables Graphviz hierarchical layout)

| Module | Library | Purpose | Key functions |
|---|---|---|---|
| `svg_builder.py` | **svgwrite** | SVG elements for nodes, edges, labels, markers, title bars | `generate_node_svg()`, `generate_edge_svg()`, `generate_label_svg()`, `generate_title_bar()`, `generate_arrow_marker()`, `get_shape_dimensions()`, `get_node_type_colors()` |
| `graph_layout.py` | **networkx** | Grid/auto layout, viewBox, overlap resolution | `flow_layout()`, `auto_layout()`, `dag_layout()`, `assign_flow_layout()`, `classify_edges_by_topology()`, `align_rows()`, `center_align_nodes()`, `enforce_column_gap()`, `topological_sort()`, `compute_viewbox()`, `resolve_overlaps()` |
| `chart_builder.py` | **matplotlib** | Complete chart SVG strings | `render_bar_chart()`, `render_line_chart()`, `render_pie_chart()` |
| `routing.py` | custom | Orthogonal/bezier path computation, endpoint validation, multi-port routing, auto side detection | `orthogonal_path()`, `connection_endpoints()`, `path_to_svg_d()`, `auto_detect_sides()`, `route_all_edges()`, `route_with_port_allocation()`, `endpoint_valid()`, `detect_intersections()`, `validate_turning_points()` |
| `geometry.py` | custom | Bounding box math, overlap detection, intersections, multi-port allocation, CJK text width | `overlap()`, `find_overlapping()`, `connection_point()`, `center()`, `distance()`, `cjk_len()`, `segment_line_intersection()`, `get_side_ports()`, `find_closest_port()`, `allocate_ports_for_edges()` |
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

    # ── Step 2: Compute dimensions ──
    for n in nodes:
        dims = get_shape_dimensions(n['text'], n['type'], ppt_mode=True)
        n.update(dims)

    # ── Option A: Auto layout (DAG — no feedback loops) ──
    # dag_layout() auto-assigns row/col from edge topology via topological sort,
    # then computes positions, aligns rows, centers columns, and enforces gaps.
    from graph_layout import dag_layout
    nodes, edges = dag_layout(nodes, edges, node_gap=130, branch_gap=260, start_offset=(100, 100))

    # ── Option B: Auto layout (with feedback loops) ──
    # Mark feedback edges with _topo_type='feedback' so they don't distort topology:
    #   edges = [
    #       {'from': 'a', 'to': 'b'},
    #       {'from': 'b', 'to': 'a', '_topo_type': 'feedback'},
    #   ]
    # Then use assign_flow_layout() instead of dag_layout():
    #   from graph_layout import assign_flow_layout
    #   nodes, edges = assign_flow_layout(nodes, edges, ...)

    # ── Option C: Manual row/col (for complex topologies) ──
    # Set 'row' and 'col' on each node dict, then use flow_layout directly:
    #   nodes = flow_layout(nodes, 'top-to-bottom', ...)
    #   nodes = align_rows(nodes)
    #   nodes = center_align_nodes(nodes, ...)

    # ── Step 3: Route connections ──
    node_map = {n['id']: n for n in nodes}

    # route_all_edges() auto-detects src_side/dst_side from node row/col
    # positions, allocates distinct ports, and routes orthogonal paths.
    # No manual side specification needed for most edges.
    from routing import route_all_edges
    edges = route_all_edges(edges, node_map, ports_per_side=3, clearance=25)

    # For edges that need custom routing (corridor bypass, etc.),
    # override_route() can replace auto-detected paths:
    #   from routing import path_to_svg_d
    #   e = next(ed for ed in edges if ed['id'] == 'e08')
    #   e['waypoints'] = [(x1,y1), (x2,y2), ...]
    #   e['path_d'] = path_to_svg_d(e['waypoints'])

    # ── Step 4: Validate connections ──
    from routing import endpoint_valid
    for i, e in enumerate(edges):
        wps = e['waypoints']
        result = endpoint_valid(wps, node_map[e['to']]['bbox'])
        assert result['valid'], f"Edge {i} invalid: {result['issues']}"

    # ── Step 5: Generate SVG elements ──
    svg_fragments = []
    for n in nodes:
        svg_fragments.append(generate_node_svg(n['id'], n['type'], n['text'], n['x'], n['y'], n['width'], n['height']))
    for i, e in enumerate(edges):
        d = e['path_d']
        svg_fragments.append(generate_edge_svg(e.get('id', f'e{i}'), d, color=e.get('color', '#555555')))

    # ── Step 6: Generate defs and assemble ──
    viewbox = compute_viewbox([n['bbox'] for n in nodes], padding=40, target_aspect=16/9, title_bar_height=70)
    shadow = get_shadow_filter()
    gradients = get_gradient_defs()
    arrow = generate_arrow_marker('arrow', '#555555', arrow_width=10, arrow_height=10, tip_ref=True)
    title_svg = generate_title_bar('Diagram Title', viewbox[2])

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

## New Auto-Layout Functions (v2)

### `graph_layout.assign_flow_layout()`

Auto-assigns row/col from edge topology, then computes pixel positions.

**Best for**: Graphs with some feedback loops where you can mark feedback edges.

```python
from graph_layout import assign_flow_layout

# Mark feedback edges with _topo_type='feedback'
edges = [
    {'from': 'a', 'to': 'b'},                          # forward (auto)
    {'from': 'b', 'to': 'a', '_topo_type': 'feedback'}, # excluded from topology
    {'from': 'c', 'to': 'b', '_topo_type': 'feedback'}, # excluded from topology
]
nodes, edges = assign_flow_layout(nodes, edges, node_gap=130, branch_gap=260)
```

### `graph_layout.dag_layout()`

One-shot layout for pure DAGs (no feedback loops). Marks all edges as forward.

```python
from graph_layout import dag_layout
nodes, edges = dag_layout(nodes, edges, node_gap=130, branch_gap=260)
```

### `graph_layout.classify_edges_by_topology()`

Classifies edges into forward/feedback/same-row by comparing topological levels.

```python
from graph_layout import classify_edges_by_topology
forward, feedback, same_row = classify_edges_by_topology(nodes, edges)
```

### `routing.auto_detect_sides()`

Determines connection sides from node row/col positions — no manual side specification needed.

```python
from routing import auto_detect_sides
src_side, dst_side = auto_detect_sides(src_node, dst_node)
# Returns e.g. ('bottom', 'top') for same-column downward edges
```

### `routing.route_all_edges()`

Routes all edges with auto-detected sides and multi-port allocation. Calls `auto_detect_sides()` for any edge missing `src_side`/`dst_side`, then delegates to `route_with_port_allocation()`.

```python
from routing import route_all_edges
edges = route_all_edges(edges, node_map, ports_per_side=3, clearance=25)
# Each edge now has: src_side, dst_side, src_port, dst_port, waypoints, path_d
```

For edges that need custom routing (e.g., corridor bypass for feedback loops),
override the path after `route_all_edges`:

```python
from routing import path_to_svg_d
e = next(ed for ed in edges if ed['id'] == 'e08')
e['waypoints'] = [(x1, y1), (x2, y2), ...]
e['path_d'] = path_to_svg_d(e['waypoints'])
```

---

## SVG Assembly Pattern

1. `<svg viewBox="...">` from `graph_layout.compute_viewbox()`
2. `<defs>` with `colors.get_shadow_filter()` + `colors.get_gradient_defs()` + `svg_builder.generate_arrow_marker()`
3. Title bar from `svg_builder.generate_title_bar(title, width)`
4. Connection `<path>` elements from `svg_builder.generate_edge_svg()`
5. Shape elements from `svg_builder.generate_node_svg()`
6. Label elements from `svg_builder.generate_label_svg()`
7. `</svg>`

> **Chart shortcut**: for bar/line/pie charts, call `chart_builder.render_*_chart()` instead — returns a complete standalone SVG, skipping the manual assembly above.

## Arrow Marker (Key Rules)

`generate_edge_svg()` **hardcodes** `marker-end="url(#arrow)"` — only ONE marker with `id="arrow"` should exist in `<defs>`. Use a neutral color (e.g., `#475569`).

```python
arrow = generate_arrow_marker('arrow', '#475569', arrow_width=10, arrow_height=10, tip_ref=True)
```

**`tip_ref=True`** sets `refX=arrow_width` so the arrow tip touches the node edge. The consequence: for side-entry edges (LEFT/RIGHT into wide nodes), the line passes through the node interior. See [diagram-workflow.md](diagram-workflow.md) for the side-entry avoidance pattern.

**Size scaling**: `markerUnits="strokeWidth"` multiplies marker coords by stroke width. With `stroke-width=2`, `arrow_width=10` → 20px actual. Rule of thumb: `arrow_width=8–10` for stroke-width=2.

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

## API Signature Reference

Critical function signatures that are easy to misuse:

### `connection_endpoints(src_bbox, dst_bbox, flow_direction)`

**Returns**: `(start_pt, end_pt, src_side, dst_side)` — a **4-tuple**, NOT a dict.

```python
# CORRECT: destructure as tuple
start_pt, end_pt, src_side, dst_side = connection_endpoints(src_box, dst_box, 'top-to-bottom')

# WRONG: treating as dict
# ep['start']  ← TypeError: tuple indices must be integers or slices
```

### `generate_label_svg(label, x, y, font_size=12, bg_color='#FFFFFF', text_color='#333333')`

The text fill color parameter is **`text_color`**, not `color`.

```python
# CORRECT
generate_label_svg('任务输入', 312.5, 359.0, font_size=11, text_color='#475569')

# WRONG
# generate_label_svg('任务输入', 312.5, 359.0, color='#475569')
# ← TypeError: got unexpected keyword argument 'color'
```

### `endpoint_valid(waypoints, dst_bbox)`

Returns a dict with `'valid'` (bool) and `'issues'` (list). **Entry segments must be ≥15px** or validation will warn `'Entry segment too short: X.Xpx (need >=15px)'`.

```python
result = endpoint_valid(edge['path'], dst['bbox'])
if not result['valid']:
    print(f"WARN: {result['issues']}")  # e.g., ['Entry segment too short: 10.0px (need >=15px)']
```

### `generate_edge_svg(edge_id, path_d, color='#555555', stroke_width=2.0, dashed=False)`

Always uses `marker-end="url(#arrow)"`. Only ONE `<marker id="arrow">` in `<defs>`. Multi-color arrows are not supported through this function.

### `flow_layout(nodes, direction, node_gap, branch_gap, start_offset)`

The `branch_gap` parameter may not produce sufficient inter-column gap. Always verify and manually enforce a minimum gap (see [diagram-workflow.md](diagram-workflow.md) "Column Gap Enforcement").

## Common Script Calls (Quick Reference)

Use the standalone script template for full diagrams. These snippets show individual API signatures for reference when writing your script.

| Task | Function | Import |
|---|---|---|
| Grid layout | `flow_layout(nodes, direction, node_gap, branch_gap, start_offset)` | `graph_layout` |
| Auto layout (DAG) | `dag_layout(nodes, edges, node_gap, branch_gap)` | `graph_layout` |
| Auto layout (with feedback) | `assign_flow_layout(nodes, edges, node_gap, branch_gap)` | `graph_layout` |
| Route all edges | `route_all_edges(edges, node_map, ports_per_side=3, clearance=25)` | `routing` |
| Route with port allocation | `route_with_port_allocation(edges, node_map, ports_per_side, clearance)` | `routing` |
| Connection endpoints | `connection_endpoints(src_bbox, dst_bbox, flow_direction)` → `(sp, ep, ss, ds)` tuple | `routing` |
| Orthogonal path | `orthogonal_path(src, dst, src_side, dst_side, clearance, obstacles)` | `routing` |
| Path to SVG `d` | `path_to_svg_d(waypoints)` | `routing` |
| Auto-detect sides | `auto_detect_sides(src_node, dst_node)` → `(src_side, dst_side)` | `routing` |
| Validate endpoint | `endpoint_valid(waypoints, dst_bbox)` → `{'valid': bool, 'issues': []}` | `routing` |
| Detect intersections | `detect_intersections(paths, obstacles)` | `routing` |
| Find overlapping | `find_overlapping(bboxes, margin=10)` | `geometry` |
| Resolve overlaps | `resolve_overlaps(nodes, margin=20)` | `graph_layout` |
| Center-align nodes | `center_align_nodes(nodes, start_offset, branch_gap, node_gap)` | `graph_layout` |
| Enforce column gap | `enforce_column_gap(nodes, min_gap=140)` → `corridor_x` | `graph_layout` |
| Compute viewBox | `compute_viewbox(bboxes, padding=40, target_aspect=16/9, title_bar_height=70)` | `graph_layout` |
| Get shape dims | `get_shape_dimensions(text, type, ppt_mode=True)` → `{width, height, ...}` | `svg_builder` |
| Generate node SVG | `generate_node_svg(id, type, text, x, y, width, height)` → SVG string | `svg_builder` |
| Generate edge SVG | `generate_edge_svg(id, path_d, color, stroke_width, dashed)` → SVG string | `svg_builder` |
| Generate label SVG | `generate_label_svg(label, x, y, font_size, bg_color, text_color)` → SVG string | `svg_builder` |
| Generate title bar | `generate_title_bar(title, width)` → SVG string | `svg_builder` |
| Generate arrow marker | `generate_arrow_marker(id, color, arrow_width, arrow_height, tip_ref)` → SVG string | `svg_builder` |
| WCAG AA check | `wcag_aa_check(fg_hex, bg_hex)` → bool | `colors` |
| Bar chart | `render_bar_chart(labels, values, title, ylabel)` → complete SVG | `chart_builder` |
| Line chart | `render_line_chart(labels, series, title, ylabel)` → complete SVG | `chart_builder` |
| Pie chart | `render_pie_chart(labels, values, title)` → complete SVG | `chart_builder` |
