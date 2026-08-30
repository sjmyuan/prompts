# Diagram Workflow Reference

Applies **create-scripted-diagram** and **modify-existing-svg** in the edit-svg skill.

## Edge Routing Patterns Quick Reference

| Edge type | Direction | Side spec | Example |
|---|---|---|---|
| Forward main chain | top→bottom | Auto-detect (default) | Start → Step1 |
| Feed sideways | left→right | `src_side='right', dst_side='left'` | Main → SidePanel |
| Feedback (right→left) | right→left | `src_side='left', dst_side='right'` | SidePanel → Main |
| Reverse upward | bottom→top | `src_side='top', dst_side='bottom'` | BottomNode → TopNode |
| Cross-column upward | bottom→top | Corridor strategy via gap between columns | BottomRight → TopLeft |
| **Simple straight flow (same-row/col)** | shared row/col center | None — bypass router | Hand-write 2-point waypoints: `[(x1, y_shared), (x2, y_shared)]` or `[(x_shared, y1), (x_shared, y2)]` |

> **Micro-jog trap**: `route_all_edges()` allocates ports at fractional side positions and picks by proximity, so two **differently-sized** nodes on the same row/column produce tiny 6–8px zigzags (e.g., `[(410,192),(370,192),(370,186),(246,186)]`). For simple same-row/same-column flows, **hand-write straight 2-point waypoints with ports at the shared row/col center** — 0 turns, visually clean. Reserve the router for multi-edge port deconfliction, complex corridors, and obstacle cases.

## Standalone Script File Approach

For ALL script-based diagrams, create a dedicated `.py` script file (e.g., `generate_diagram.py`) in the workspace. This enables iterative refinement — modify script → run → view SVG → fix → repeat.

The script must:
- Import modules from `skills/edit-svg/scripts/` via `sys.path.insert()`
- Define node/edge data structures inline
- Use `dag_layout()` or `assign_flow_layout()` for auto-layout, or `flow_layout()` + manual centering
- Route connections via `route_all_edges()` or `route_with_port_allocation()`
- After routing, run `global_refine_pass()` for iterative optimization
- Generate SVG elements and save to `.svg` file
- Be run with `python3 generate_diagram.py`

## Iterative Validation Loop

After running the script, open the SVG in the browser and check:

1. **Line-node overlap**: No edge passes through any node interior. Pixel-based obstacle detection with EPSILON tolerance now prevents false positives.
2. **Line overlap**: No two parallel lines share the same corridor position. Sub-point switching resolves overlaps without adding turns.
3. **Turning point clearance**: No turning point aligns with any node's edge.
4. **Connection sides**: Edges enter/exit from correct sides.
5. **Row alignment**: Same-row nodes share identical `center_y`; same-column nodes share identical `center_x`.
6. **Column gap**: Inter-column gap ≥140px for corridor-routed diagrams. Enforce via `enforce_column_gap()`.
7. **Label overlap**: Labels don't overlap nodes. Prefer manual position for cross-column edges.
8. **Approach segments**: Entry segments into nodes ≥15px (validated by `endpoint_valid()`).
9. **Minimal turns**: Run `global_refine_pass()` after routing to minimize total turn count.

Fix issues in script and re-run until all criteria are met.

## Programmatic Validation (no visual review)

When rendered previews are unavailable (e.g., the assistant model cannot view images), validate geometrically with a standalone `validate.py` that re-runs the diagram's layout and checks:

1. **Node-node overlap**: pairwise bbox overlap area >1px → flag.
2. **Edge-node intersection**: every edge segment vs every unrelated node bbox (`segment_rect_intersection`) → flag.
3. **Entry segment length**: last waypoint segment ≥15px (also enforced by `endpoint_valid()`).
4. **Arrow line-length audit**: every arrow-carrying segment ≥46px total (= `arrow_width × stroke_width` head + ~28px visible shaft; see [create-flowchart.md](create-flowchart.md) "Arrowhead-vs-gap rule"). Lines shorter than this look clipped.
5. **ASCII layout dump**: print nodes as `#` and edges as `-`/`|` on a coarse grid (e.g., 10px per cell) to "see" composition, symmetry, and row/column alignment.

Auditing notes:

- **Multi-line node text lives in `<tspan>` elements** — a naive ElementTree `.text` dump misses it. Audit `<tspan>` content when checking for typos/overflow.
- **SVG→PNG preview on macOS**: `cairosvg` requires the native cairo library (often absent); use `qlmanage -t -s N -o outdir file.svg` instead. The first global invocation is very slow — warm it up with one tiny single-file render first.
- **Keep the generator script** (see "Standalone Script File Approach" above): any 改图/edit request = edit script → rerun → overwrite the same output filename.

## Validation API

```python
from routing import endpoint_valid, detect_intersections, global_refine_pass
from geometry import find_overlapping

for e in edges:
    result = endpoint_valid(e['waypoints'], node_map[e['to']]['bbox'])
    assert result['valid'], f"Edge {e['id']}: {result['issues']}"

intersections = detect_intersections([e['waypoints'] for e in edges], [n['bbox'] for n in nodes])
overlaps = find_overlapping([n['bbox'] for n in nodes], margin=10)

# Global optimization — minimize total turns
edges = global_refine_pass(edges, nodes, node_map)
```

## Side Specification Rules for Manual Routing

When auto-detection fails, specify sides explicitly:

```python
from routing import orthogonal_path, path_to_svg_d
from geometry import connection_point

src_pt = connection_point(src_bbox, 'right')
dst_pt = connection_point(dst_bbox, 'left')
waypoints = orthogonal_path(src_pt, dst_pt, 'right', 'left', clearance=25, obstacles=obs_bboxes)
d = path_to_svg_d(waypoints)
```

For corridor-based cross-column feedback:

```python
corridor_x = (col0_max_right + col1_min_left) / 2
path = [
    source_exit,
    (corridor_x, source_exit[1]),
    (corridor_x, target_entry[1]),
    target_entry,
]
d = path_to_svg_d(path)
```

## Port Allocation API

```python
from geometry import get_side_ports, find_closest_port, allocate_ports_for_edges

# Manual control
ports = get_side_ports(node['bbox'], 'bottom', count=5)
idx = find_closest_port(ports, target_point, used_indices, prefer_side='bottom')

# Preferred: full allocation in one call
from routing import route_with_port_allocation
edges = route_with_port_allocation(edges, node_map, ports_per_side=3, clearance=25)
```

| Scenario | Ports per side |
|---|---|
| 1–2 edges per side | 3 |
| 3–4 edges per side | 5 |
| 5+ edges per side | 7+ |
| Forward chain (1 in, 1 out) | 3 (default) |
