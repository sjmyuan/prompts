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

When feedback edges must go from bottom of one column back to top of another column, identify the x-coordinate of the gap between the main column and branch column(s).

### Single edge
Route through the corridor: exit source node horizontally to corridor x → go vertically along corridor → enter target node from below. This produces clean 4-waypoint paths.

### Multiple edges (multi-lane)
When multiple distinct feedback edges traverse the same gap corridor, they MUST use **offset lanes** to avoid overlapping:

1. Compute the gap corridor x as `(col0_max_right + col1_min_left) / 2`.
2. Create 3-4 lanes with 18px spacing:
   ```
   lane_c  = gap_corridor       # center lane
   lane_l  = gap_corridor - 18  # left lane
   lane_r  = gap_corridor + 18  # right lane
   lane_rr = gap_corridor + 36  # far right lane
   ```
3. Assign each edge to a unique lane.
4. **Stagger horizontal exit segments** from shared source nodes: use different y-levels for different edges exiting from the same node side. For example, use `node_center_y` for one edge and `node_bottom - 0.15*height` for another.

### Turning point clearance
**Critical**: After routing, verify that NO turning point (waypoint that is not a connection endpoint) shares an x or y coordinate with any node's edge:
```
for each turning point (tx, ty), for each node (nx, ny, nw, nh):
    assert tx != nx and tx != nx+nw  # not on left/right edge
    assert ty != ny and ty != ny+nh  # not on top/bottom edge
```
If a turning point aligns with a node edge, add a **short approach segment** (≥15px, validated by `endpoint_valid()`) to offset the horizontal/vertical segment away from the edge. For example, to enter a node's bottom edge cleanly:
```
# Bad: horizontal at y=bottom runs along node's bottom edge
(sx, sy) → (corridor, sy) → (corridor, bottom) → (target_x, bottom)

# Good: horizontal offset by 16px, short vertical approach
(sx, sy) → (corridor, sy) → (corridor, bottom-16) → (target_x, bottom-16) → (target_x, bottom)
```

## Side-Entry Through-Node Problem (Critical)

**When an edge enters a wide target node from the LEFT or RIGHT side, the horizontal approach segment will pass THROUGH the node interior.** This is a common and serious defect that is easy to miss during code review.

### Root Cause

`generate_edge_svg()` uses `marker-end="url(#arrow)"` with `refX=arrow_width` (tip_ref=True). The arrow TIP is placed at the path endpoint, which must be on the node edge for the tip to touch the shape. However, the path line itself is drawn all the way to that endpoint. For side-entry edges, this means the last horizontal segment goes from the corridor (or previous turn) all the way to the node's far-side edge — passing through the entire node width.

**With `refX=10, stroke-width=2`**: the arrow is 20 units long. The line is drawn 20 units into the node before the arrowhead covers it. The rest of the approach segment is visible line passing through the node body.

```
# PROBLEMATIC: line passes through CM (x=160-485) at y=418
(565, 418) → (160, 418)
# The horizontal segment from x=565 to x=160 goes right through CM (160-485)
```

### Solution: Top/Bottom Entry with Approach Segment

Instead of entering from the side, route the edge to a point **above or below** the target node, then drop in with a short vertical approach segment:

```
# FIXED: route above CM (y=400), then 16px vertical approach into CM top
(565, 572) → (565, 384) → (322.5, 384) → (322.5, 400)
# Horizontal at y=384 is above CM; vertical from 384→400 is a clean 16px approach
```

The approach segment must be ≥15px (enforced by `endpoint_valid()`). Use 16px as a safe minimum.

### When Side-Entry Is Unavoidable

If an edge MUST enter from the side (e.g., same-row cross-column connection), route the approach point to a y-level that is NOT at the node's top/bottom edge. Enter at mid-height instead:

```
# OK: enters CTX at mid-height (y=560), not at bottom edge (y=584)
(553, 606) → (553, 560) → (372.5, 560)
# Horizontal at y=560 stops at CTX right edge (372.5)
# The line approaches from outside CTX's x-range, only touching at the edge
```

Verify with: for each node the last horizontal segment enters, the segment's y must either be outside the node's y-range, or the segment's x-range must not overlap the node's x-range (except at the endpoint).

## Column Gap Enforcement

`flow_layout()` computes column positions based on `branch_gap` but the resulting gap may be insufficient for corridor-routed diagrams. Always verify and enforce a minimum gap:

```python
col0_right = max(n['x'] + n['width'] for n in col0_nodes)
col1_left = min(n['x'] for n in col1_nodes)
MIN_GAP = 140  # Minimum for corridor routing with labels
if col1_left - col0_right < MIN_GAP:
    shift = MIN_GAP - (col1_left - col0_right)
    for n in col1_nodes:
        n['x'] += shift
        n['bbox'] = (n['x'], n['y'], n['width'], n['height'])
# Recompute corridor_x AFTER shifting
col0_right = max(n['x'] + n['width'] for n in col0_nodes)
col1_left = min(n['x'] for n in col1_nodes)
corridor_x = (col0_right + col1_left) / 2
```

Use 140–160px for diagrams with corridor-routed edges and CJK labels; use 100–120px for diagrams with only forward edges.

## Manual Label Placement for Complex Edges

For cross-column feedback edges, backward edges, and edges with long labels, automatic label placement via `labeling.py` frequently produces node overlaps. Prefer explicit per-edge position computation:

```python
# For labels on vertical corridor segments (most reliable):
wps = edge['path']
my = (wps[1][1] + wps[2][1]) / 2  # midpoint of vertical segment
lw, lh = est_label_dims(label, fs=11)
mx = wps[1][0] + lw/2 + 8  # offset right of the vertical line

# For labels on horizontal segments below/above nodes:
hy = wps[2][1]  # y of the horizontal segment
hx_mid = (wps[1][0] + wps[2][0]) / 2
label_y = hy - 10  # above the horizontal line
```

After placing each label, verify it doesn't overlap any node bbox. For labels on the same row as nodes, ensure the label y-range is entirely above or below all nodes in that row.

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

## Column & Row Center Alignment

All nodes must be centered both **horizontally (within column)** and **vertically (within row)**. Do NOT position by top/left edges — position by centers.

### Per-column horizontal centering
1. Compute dimensions for all nodes first.
2. For each column, find the maximum node width.
3. Compute column center x: `col_center_x = col_left + max_width_in_col / 2`.
4. Set each node's x: `node['x'] = col_center_x - node['width'] / 2`.

This ensures all nodes in the same column share an identical `center_x` regardless of their individual widths.

### Per-row vertical centering
1. For each row, compute `center_y = start_y + row * node_gap`.
2. Set each node's y: `node['y'] = center_y - node['height'] / 2`.

This ensures all nodes in the same row share an identical `center_y`. Nodes with different heights (e.g., 48px single-line vs 60px multi-line) are automatically centered.

### Combined result
```python
col_max_width = {}
for n in nodes:
    col_max_width[n['col']] = max(col_max_width.get(n['col'], 0), n['width'])

for n in nodes:
    col_left = start_offset[0] + n['col'] * branch_gap
    col_center_x = col_left + col_max_width[n['col']] / 2
    n['x'] = col_center_x - n['width'] / 2
    center_y = start_offset[1] + n['row'] * node_gap
    n['y'] = center_y - n['height'] / 2
    n['bbox'] = (n['x'], n['y'], n['width'], n['height'])
```

### Edge routing for same-column forward edges
After centering, same-column nodes have identical `center_x`. This means forward edges between adjacent rows can be **straight vertical lines** (no turns needed). However, when nodes in the same column have differing `center_x` due to previous non-centered layouts, apply **skip detection**:

```python
def route_same_column(src_node, dst_node, skip_count=0):
    sx = src_node['x'] + src_node['width'] / 2
    sy = src_node['y'] + src_node['height']
    dx = dst_node['x'] + dst_node['width'] / 2
    dy = dst_node['y']
    if abs(sx - dx) < 2:
        if skip_count > 0:
            # Has intermediate nodes → Z-shape with 2 turns
            off = 25
            mid_y = (sy + dy) / 2
            return [(sx, sy), (sx+off, sy), (sx+off, mid_y), (sx-off, mid_y), (sx-off, dy), (sx, dy)]
        else:
            # No intermediate → straight line
            return [(sx, sy), (dx, dy)]
    else:
        if skip_count > 0:
            # Has intermediate → Z-shape at clearance
            mid_y = sy + 20
            return [(sx, sy), (sx, mid_y), (dx, mid_y), (dx, dy)]
        else:
            # No intermediate → L-shape (1 turn), horizontal first
            return [(sx, sy), (dx, sy), (dx, dy)]
```

`skip_count` = number of nodes in the same column whose rows lie between source and destination rows.

## Edge Connection Routing — Side Specification Rules

The most common diagram defects come from connection endpoints on wrong sides of nodes. Follow these rules strictly:
- For forward edges (top→bottom in same column): Use `connection_endpoints()` with `flow_direction='top-to-bottom'` → source exits bottom, target enters top.
- For sideways feeds (left→right across columns, same row): Use `src_side='right', dst_side='left'` — source exits right, target enters left.
- For feedback edges (right→left across columns): ALWAYS specify `src_side='left', dst_side='right'` explicitly (source exits left side, target enters right side). Never rely on auto-detection.
- For reverse upward edges (bottom→top, same column): ALWAYS specify `src_side='top', dst_side='bottom'` explicitly.
- After routing, run `routing.endpoint_valid(waypoints, dst_bbox)` on every edge — the `'valid'` field must be `True`. If any edge shows a wrong-side connection, fix the side specification and re-route.
- Run `routing.detect_intersections()` on all routed connections. If intersections exist among feedback/cross edges, switch to corridor-based routing.
