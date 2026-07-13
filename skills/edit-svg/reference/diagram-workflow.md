# Diagram Workflow Reference

Applies **create-scripted-diagram** and **modify-existing-svg** in the edit-svg skill.

## Edge Routing Patterns for Multi-Column Layouts

| Edge type | Direction | Strategy | Example |
|---|---|---|---|
| Forward main chain | top→bottom | Default `connection_endpoints()` with flow direction | Start → Step1 → Step2 |
| Feed sideways | left→right | Explicit sides: `src_side='right', dst_side='left'` | Main → SidePanel |
| Horizontal feedback (right-to-left) | right→left | Explicit sides: `src_side='left', dst_side='right'` | SidePanel → Main |
| Reverse upward (bottom-to-top) | bottom→top | Explicit sides: `src_side='top', dst_side='bottom'` | BottomNode → TopNode |
| Cross-column upward | bottom-right → top-left | **Corridor strategy** — route via gap between columns | BottomRight → TopLeft |

### Corridor Strategy

When feedback edges must go from bottom of one column back to top of another column, identify the x-coordinate of the gap between the main column and branch column(s). Route all such edges through this shared vertical corridor: exit source node horizontally to corridor x → go vertically along corridor → enter target node from below. This produces clean 4-waypoint paths that avoid intermediate nodes.

## Connection Port Allocation (Multi-Port Connection System)

When multiple lines connect to the same side of a node (e.g., two edges entering the top, three edges exiting the bottom), they MUST use the **multi-port allocation system** to avoid overlap. Never let all lines converge at a single center point.

### Port Distribution

Each edge of a node has `ports_per_side` (default 3) evenly distributed fixed connection points:

```
Top edge ports (3):      [P0]────[P1]────[P2]
                         left    center   right

Bottom edge ports (3):   [P0]────[P1]────[P2]
                         left    center   right

Left edge ports (3):     [P0] ← top
                         [P1] ← center
                         [P2] ← bottom

Right edge ports (3):    [P0] ← top
                         [P1] ← center
                         [P2] ← bottom
```

Port 1 is always the center point (backward compatible). Ports 0 and N-1 are at the edge ends.

### Allocation Rules

1. **One port per line per side**: Once a port index is allocated to an edge on a node side, no other edge may use that same port on that same node side.
2. **Closest-port selection**: Each edge picks the closest unused port that minimizes path turns:
   - For `left`/`right` sides: prefer ports whose y-coordinate is closest to the target's y (minimize vertical turns).
   - For `top`/`bottom` sides: prefer ports whose x-coordinate is closest to the target's x (minimize horizontal turns).
3. **Parallel edge offset**: When multiple edges share the same `from→to` pair, the second+ edges get a `mid_offset` to spread their middle segments apart horizontally (for vertical exit/entry) or vertically (for horizontal exit/entry).

### API: `route_with_port_allocation()`

Use this convenience function in `routing.py` for all edge routing. It combines port allocation + orthogonal routing in one call:

```python
from routing import route_with_port_allocation

edges = [
    {"from": "A", "to": "B", "src_side": "bottom", "dst_side": "top"},
    {"from": "C", "to": "B", "src_side": "bottom", "dst_side": "top"},  # shares B's top
    {"from": "D", "to": "B", "src_side": "right", "dst_side": "left"},   # different side
]
node_map = {n['id']: n for n in nodes}
edges = route_with_port_allocation(edges, node_map, ports_per_side=3, clearance=25)
# Each edge now has: src_port, dst_port, waypoints, path_d
```

### API: Individual Functions (for custom needs)

For manual control, use the individual functions in `geometry.py`:

```python
from geometry import get_side_ports, find_closest_port, allocate_ports_for_edges

# Get 5 ports on the bottom of a node
ports = get_side_ports(node['bbox'], 'bottom', count=5)

# Find closest unused port to a target
idx = find_closest_port(ports, target_point, used_indices, prefer_side='bottom')

# Full allocation for all edges at once
edges = allocate_ports_for_edges(edges, node_map, ports_per_side=3)
```

### Port Count Guidelines

| Scenario | Ports per side | Reason |
|---|---|---|
| 1–2 edges per side | 3 | Center + 2 edge ports provide enough spread |
| 3–4 edges per side | 5 | More granular spacing needed |
| 5+ edges per side | 7 or more | Dense connections need fine distribution |
| Forward chain (1 in, 1 out) | 3 (default) | Single connection, center port is fine |

### Visual Validation After Port Allocation

After routing, verify in the browser:
1. **No two lines converge at the same spot on a node edge** — each line should hit a distinct port.
2. **Parallel edges spread apart** — mid-segments should be visibly offset, not overlapping.
3. **Short entry segments** — the last segment before each node should be ≥15px (enforced by `endpoint_valid()`).
4. **Minimal turning points** — lines should use the port closest to their direction to avoid unnecessary bends.

## Standalone Script File Approach

For ALL script-based diagrams, create a dedicated `.py` script file (e.g., `generate_diagram.py`) in the workspace instead of using inline `python3 -c` one-liners. This enables iterative refinement — modify script → run → view SVG → fix → repeat — without re-typing the full command each time. The script must:
- Import all needed modules from `skills/edit-svg/scripts/` via `sys.path.insert()`
- Define node/edge data structures inline
- Compute positions, route connections, generate SVG elements
- Save the output to an `.svg` file (write SVG string to file)
- Be run with `python3 generate_diagram.py`

## Iterative Validation Loop

After creating the script, run it, then open the generated SVG in browser for visual inspection. Check for:
- Lines overlapping each other (line-line intersections) — run `routing.detect_intersections()`
- Lines entering/exiting from wrong sides of nodes — run `routing.endpoint_valid()` on each edge
- Nodes in the same row not aligned to the same y-coordinate — verify all `node['y']` values per row
- Labels overlapping with nodes or other labels — run `geometry.find_overlapping()`

Fix issues in the script and re-run. Repeat until all visual quality criteria are met.

## Row Alignment Rules

All nodes in the same row must share the same y-coordinate for proper horizontal center alignment. After `flow_layout()`, group nodes by row and for each row:
1. Find the tallest node height in that row.
2. Center each node vertically within the row: `node['y'] = row_base_y + (max_row_height - node['height']) / 2`.

For single-column layouts (all nodes in col=0), the same logic applies — all nodes must share the same horizontal center x-coordinate.

## Edge Connection Routing — Side Specification Rules

The most common diagram defects come from connection endpoints on wrong sides of nodes. Follow these rules strictly:
- For forward edges (top→bottom in same column): Use `connection_endpoints()` with `flow_direction='top-to-bottom'` → source exits bottom, target enters top.
- For sideways feeds (left→right across columns, same row): Use `src_side='right', dst_side='left'` — source exits right, target enters left.
- For feedback edges (right→left across columns): ALWAYS specify `src_side='left', dst_side='right'` explicitly (source exits left side, target enters right side). Never rely on auto-detection.
- For reverse upward edges (bottom→top, same column): ALWAYS specify `src_side='top', dst_side='bottom'` explicitly.
- After routing, run `routing.endpoint_valid(waypoints, dst_bbox)` on every edge — the `'valid'` field must be `True`. If any edge shows a wrong-side connection, fix the side specification and re-route.
- Run `routing.detect_intersections()` on all routed connections. If intersections exist among feedback/cross edges, switch to corridor-based routing.
