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
