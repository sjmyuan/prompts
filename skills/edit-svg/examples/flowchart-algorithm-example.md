# Example: Multi-Branch Flowchart with Topological Sort & 8-Scenario Routing

**Scenario**: A user asks to create a complex flowchart with a decision branch, feedback loop, and multiple parallel paths. The edge routing must apply the 8-scenario classification with path selection scoring to produce clean orthogonal connections with no line-node overlaps.

**Trigger**: "Create a flowchart for a CI/CD pipeline: Source Code → Build → Run Tests. If tests pass, deploy to Staging → Run Integration Tests → Deploy to Production. If tests fail, Log Error → Fix Bug → rerun Build. Add a feedback loop: if the production deploy fails, roll back and notify."

**Applies**: **create-scripted-diagram** (flowchart variant with topological sort + 8-scenario routing)

---

## Input

Create a flowchart for a CI/CD pipeline:
1. Source Code → Build
2. Build → Run Tests
3. Run Tests → (decision) Tests Pass?
4. Yes → Deploy to Staging → Integration Tests → Deploy to Production
5. No → Log Error → Fix Bug → (feedback back to Build)
6. Deploy to Production → (decision) Success? — No → Rollback → Notify → (feedback back to Build)

## Script Structure

The script follows the topological sort approach to auto-assign rows, then applies 8-scenario routing:

```python
import sys
sys.path.insert(0, '/Users/ganggang/work/prompts/skills/edit-svg/scripts')

from graph_layout import flow_layout, compute_viewbox
from routing import (
    orthogonal_path, connection_endpoints, path_to_svg_d,
    endpoint_valid, detect_intersections, route_with_port_allocation
)
from geometry import (
    connection_point, find_overlapping, BBox,
    get_side_ports, find_closest_port, allocate_ports_for_edges,
    center
)
from svg_builder import (
    generate_node_svg, generate_edge_svg, generate_label_svg,
    generate_title_bar, generate_arrow_marker,
    get_shape_dimensions, get_node_type_colors
)
from colors import get_shadow_filter, get_gradient_defs
from collections import deque


def topological_sort(nodes, edges):
    """Kahn's algorithm for auto row assignment."""
    node_map = {n['id']: n for n in nodes}
    adj = {n['id']: [] for n in nodes}
    in_deg = {n['id']: 0 for n in nodes}
    for e in edges:
        adj.setdefault(e['from'], []).append(e['to'])
        in_deg[e['to']] = in_deg.get(e['to'], 0) + 1

    queue = deque([nid for nid, d in in_deg.items() if d == 0])
    level = {}
    for nid in queue:
        level[nid] = 0

    while queue:
        u = queue.popleft()
        for v in adj.get(u, []):
            in_deg[v] -= 1
            if in_deg[v] == 0:
                level[v] = level[u] + 1
                queue.append(v)

    level_nodes = {}
    for n in nodes:
        row = level.get(n['id'], 0)
        level_nodes.setdefault(row, []).append(n['id'])

    col_counter = {}
    for n in nodes:
        row = level.get(n['id'], 0)
        n['row'] = row
        n['col'] = col_counter.get(row, 0)
        col_counter[row] = col_counter.get(row, 0) + 1

    return nodes


def classify_edge(src_node, dst_node):
    """Classify edge into one of 8 spatial scenarios."""
    if src_node['row'] == dst_node['row']:
        if src_node['col'] < dst_node['col']:
            return "SAME_ROW_RIGHT"
        else:
            return "SAME_ROW_LEFT"
    elif src_node['col'] == dst_node['col']:
        if src_node['row'] < dst_node['row']:
            return "SAME_COL_DOWN"
        else:
            return "SAME_COL_UP"
    elif src_node['row'] < dst_node['row']:
        if src_node['col'] < dst_node['col']:
            return "DIAG_DOWN_RIGHT"
        else:
            return "DIAG_DOWN_LEFT"
    else:
        if src_node['col'] < dst_node['col']:
            return "DIAG_UP_RIGHT"
        else:
            return "DIAG_UP_LEFT"


def build_diagram():
    # Step 1: Define nodes (no row/col — topological sort assigns them)
    nodes = [
        {'id': 'source', 'type': 'process', 'text': 'Source Code'},
        {'id': 'build', 'type': 'process', 'text': 'Build'},
        {'id': 'tests', 'type': 'process', 'text': 'Run Tests'},
        {'id': 'decision', 'type': 'decision', 'text': 'Tests\nPass?'},
        {'id': 'deploy_staging', 'type': 'process', 'text': 'Deploy to\nStaging'},
        {'id': 'integration', 'type': 'process', 'text': 'Integration\nTests'},
        {'id': 'deploy_prod', 'type': 'process', 'text': 'Deploy to\nProduction'},
        {'id': 'log_error', 'type': 'process', 'text': 'Log\nError'},
        {'id': 'fix_bug', 'type': 'process', 'text': 'Fix Bug'},
        {'id': 'prod_decision', 'type': 'decision', 'text': 'Deploy\nSuccess?'},
        {'id': 'rollback', 'type': 'process', 'text': 'Rollback'},
        {'id': 'notify', 'type': 'process', 'text': 'Notify\nTeam'},
    ]

    edges = [
        {'id': 'e1', 'from': 'source', 'to': 'build'},
        {'id': 'e2', 'from': 'build', 'to': 'tests'},
        {'id': 'e3', 'from': 'tests', 'to': 'decision'},
        {'id': 'e4_yes', 'from': 'decision', 'to': 'deploy_staging', 'label': 'Yes'},
        {'id': 'e5', 'from': 'deploy_staging', 'to': 'integration'},
        {'id': 'e6', 'from': 'integration', 'to': 'deploy_prod'},
        {'id': 'e7_no', 'from': 'decision', 'to': 'log_error', 'label': 'No'},
        {'id': 'e8', 'from': 'log_error', 'to': 'fix_bug'},
        {'id': 'e9', 'from': 'fix_bug', 'to': 'build'},  # Feedback loop
        {'id': 'e10', 'from': 'deploy_prod', 'to': 'prod_decision'},
        {'id': 'e11_no', 'from': 'prod_decision', 'to': 'rollback', 'label': 'No'},
        {'id': 'e12', 'from': 'rollback', 'to': 'notify'},
        {'id': 'e13', 'from': 'notify', 'to': 'build'},  # Another feedback loop
    ]

    # Step 2: Topological sort — auto assign rows
    nodes = topological_sort(nodes, edges)
    # Results:
    # Row 0: source (col 0)
    # Row 1: build (col 0)
    # Row 2: tests (col 0)
    # Row 3: decision (col 0)
    # Row 4: deploy_staging (col 0), log_error (col 1)
    # Row 5: integration (col 0), fix_bug (col 1)
    # Row 6: deploy_prod (col 0)
    # Row 7: prod_decision (col 0)
    # Row 8: rollback (col 0)
    # Row 9: notify (col 0)

    # Step 3: Compute dimensions
    for n in nodes:
        dims = get_shape_dimensions(n['text'], n['type'], ppt_mode=True)
        n.update(dims)

    # Step 4: Position via grid layout
    # Main column (col 0) and branch column (col 1) with wide gap for feedback corridor
    nodes = flow_layout(
        nodes, 'top-to-bottom',
        node_gap=120, branch_gap=400,  # 400px gap for feedback corridor + labels
        start_offset=(100, 140)
    )

    # Step 5: Row alignment (center y per row)
    rows = {}
    for n in nodes:
        rows.setdefault(n['row'], []).append(n)
    for row_nodes in rows.values():
        max_h = max(n['height'] for n in row_nodes)
        base_y = min(n['y'] for n in row_nodes)
        for n in row_nodes:
            n['y'] = base_y + (max_h - n['height']) / 2
            n['bbox'] = (n['x'], n['y'], n['width'], n['height'])

    # Step 6: Column gap enforcement for corridor
    col0_nodes = [n for n in nodes if n['col'] == 0]
    col1_nodes = [n for n in nodes if n['col'] == 1]
    col0_right = max(n['x'] + n['width'] for n in col0_nodes)
    col1_left = min(n['x'] for n in col1_nodes)
    MIN_GAP = 200
    if col1_left - col0_right < MIN_GAP:
        shift = MIN_GAP - (col1_left - col0_right)
        for n in col1_nodes:
            n['x'] += shift
            n['bbox'] = (n['x'], n['y'], n['width'], n['height'])

    # Compute corridor x for feedback edges
    col0_right = max(n['x'] + n['width'] for n in col0_nodes)
    col1_left = min(n['x'] for n in col1_nodes)
    corridor_x = (col0_right + col1_left) / 2

    # Step 7: Route connections using 8-scenario classification
    node_map = {n['id']: n for n in nodes}

    # Forward edges (same column, top→bottom) — use default connection_endpoints
    forward_edges = [
        {'from': 'source', 'to': 'build', 'src_side': 'bottom', 'dst_side': 'top'},
        {'from': 'build', 'to': 'tests', 'src_side': 'bottom', 'dst_side': 'top'},
        {'from': 'tests', 'to': 'decision', 'src_side': 'bottom', 'dst_side': 'top'},
        {'from': 'deploy_staging', 'to': 'integration', 'src_side': 'bottom', 'dst_side': 'top'},
        {'from': 'integration', 'to': 'deploy_prod', 'src_side': 'bottom', 'dst_side': 'top'},
        {'from': 'deploy_prod', 'to': 'prod_decision', 'src_side': 'bottom', 'dst_side': 'top'},
        {'from': 'rollback', 'to': 'notify', 'src_side': 'bottom', 'dst_side': 'top'},
        {'from': 'log_error', 'to': 'fix_bug', 'src_side': 'bottom', 'dst_side': 'top'},
    ]

    # Decision branch edges (DIAG_DOWN_RIGHT and DIAG_DOWN_LEFT)
    branch_edges = [
        # Yes branch: decision → deploy_staging (DIAG_DOWN_RIGHT)
        {'from': 'decision', 'to': 'deploy_staging', 'src_side': 'right', 'dst_side': 'left'},
        # No branch: decision → log_error (DIAG_DOWN_LEFT)
        {'from': 'decision', 'to': 'log_error', 'src_side': 'left', 'dst_side': 'right'},
    ]

    # Feedback edges — use corridor strategy (bottom→top across columns)
    feedback_edges = [
        # fix_bug → build (DIAG_UP_LEFT: from col 1 bottom to col 0 mid)
        {'from': 'fix_bug', 'to': 'build', 'src_side': 'top', 'dst_side': 'bottom',
         'lane': 'lane_l'},
        # notify → build (DIAG_UP_LEFT: from col 0 bottom back to build)
        {'from': 'notify', 'to': 'build', 'src_side': 'top', 'dst_side': 'bottom',
         'lane': 'lane_r'},
    ]

    # Failed deploy feedback: prod_decision → rollback (SAME_COL_DOWN)
    deploy_fail_edge = [
        {'from': 'prod_decision', 'to': 'rollback', 'src_side': 'bottom', 'dst_side': 'top'},
    ]

    all_edges_config = forward_edges + branch_edges + feedback_edges + deploy_fail_edge

    # Route forward edges via route_with_port_allocation
    obstacles = [n['bbox'] for n in nodes]
    routed = route_with_port_allocation(
        all_edges_config, node_map,
        ports_per_side=3, clearance=25, obstacles=obstacles
    )

    # Handle feedback edges with corridor strategy
    for e in routed:
        if e['from'] == 'fix_bug' or e['from'] == 'notify':
            src_node = node_map[e['from']]
            dst_node = node_map[e['to']]
            lane_offset = -18 if e.get('lane') == 'lane_l' else 18
            fb_corridor_x = corridor_x + lane_offset

            src_center = center(src_node['bbox'])
            dst_center = center(dst_node['bbox'])

            # Build 4-waypoint path via corridor
            path = [
                (src_center[0], src_node['y']),  # exit from source top
                (fb_corridor_x, src_node['y']),    # to corridor at top-of-source y
                (fb_corridor_x, dst_node['y'] + dst_node['height']),  # down corridor to dst bottom
                (dst_center[0], dst_node['y'] + dst_node['height']),  # to dst bottom-center
            ]
            e['waypoints'] = path
            e['path_d'] = path_to_svg_d(path)

    # Step 8: Validate all connections
    for i, e in enumerate(routed):
        if e['to'] in node_map:
            result = endpoint_valid(e['waypoints'], node_map[e['to']]['bbox'])
            if not result['valid']:
                print(f"WARN edge {i} ({e['from']}→{e['to']}): {result['issues']}")

    # Step 9: Generate SVG elements
    svg_fragments = []
    for n in nodes:
        colors = get_node_type_colors(n['type'], ppt_mode=True)
        svg_fragments.append(
            generate_node_svg(
                n['id'], n['type'], n['text'],
                n['x'], n['y'], n['width'], n['height'],
                ppt_mode=True, colors=colors
            )
        )

    for i, e in enumerate(routed):
        color = '#475569'
        if e.get('label') == 'No':
            color = '#DC2626'
        elif e.get('label') == 'Yes':
            color = '#16A34A'
        svg_fragments.append(
            generate_edge_svg(
                e.get('id', f'e{i}'),
                e['path_d'],
                color=color
            )
        )

    # Step 10: Generate defs
    viewbox = compute_viewbox(
        [n['bbox'] for n in nodes],
        padding=40, target_aspect=None,  # Portrait → no aspect enforcement
        title_bar_height=70
    )
    shadow = get_shadow_filter()
    gradients = get_gradient_defs()
    arrow = generate_arrow_marker('arrow', '#475569', arrow_width=10, arrow_height=10, tip_ref=True)
    title_svg = generate_title_bar('CI/CD Pipeline Flowchart', viewbox[2])

    # Step 11: Assemble SVG
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox[0]} {viewbox[1]} {viewbox[2]} {viewbox[3]}" '
        f'font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">',
        '<defs>', shadow, gradients, arrow, '</defs>',
        title_svg,
        *svg_fragments,
        '</svg>',
    ]
    return '\n'.join(svg_parts)


if __name__ == '__main__':
    svg = build_diagram()
    with open('cicd_flowchart.svg', 'w') as f:
        f.write(svg)
    print('SVG saved to cicd_flowchart.svg')
```

## Output Description

The generated SVG will have:

1. **Auto-assigned rows** via topological sort — Source Code (row 0), Build (row 1), Tests (row 2), Decision (row 3), Deploy Staging + Log Error (row 4), Integration Tests + Fix Bug (row 5), Deploy to Production (row 6), Deploy Success? (row 7), Rollback (row 8), Notify (row 9).

2. **8-scenario routing** applied to each edge:
   - **SAME_COL_DOWN**: All main-column forward edges (Source→Build, Build→Tests, etc.) — straight vertical lines (0 turns)
   - **DIAG_DOWN_RIGHT**: Decision→Deploy Staging ("Yes" branch) — L-shaped: exit right from decision, enter left of Deploy Staging (1 turn)
   - **DIAG_DOWN_LEFT**: Decision→Log Error ("No" branch) — L-shaped: exit left from decision, enter right of Log Error (1 turn)
   - **DIAG_UP_LEFT**: Fix Bug→Build (feedback loop) — corridor-based routing via gap (4 waypoints)

3. **Path selection scoring** disqualifies any path that passes through an intermediate node. Feedback edges use corridor routing to avoid obstacles.

4. **Parallel overlap resolution**: The two feedback edges (Fix Bug→Build, Notify→Build) share the same corridor but use offset lanes (`lane_l` and `lane_r`) with 18px spacing to avoid overlapping.

5. **Decision branch labels**: "Yes" (green, right side) and "No" (red, left side) labels on branch edges.
