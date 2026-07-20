"""
Graph layout using networkx.

Install: pip install networkx
For hierarchical layout: pip install pygraphviz  (optional, recommended for flowcharts)

Replaces layout.py — automatic layouts delegate to networkx algorithms.
Grid-based and viewBox utilities are kept as lightweight custom helpers
because they are simpler than the equivalent networkx primitives.
"""

import math
from collections import deque
from typing import Tuple, List, Dict, Any, Optional

import networkx as nx

from geometry import (
    BBox,
    Point,
    find_overlapping,
    union_bbox,
)

# ---------------------------------------------------------------------------
# Grid layout — explicit row/col assignments, no library needed
# ---------------------------------------------------------------------------


def flow_layout(
    nodes: List[Dict[str, Any]],
    flow_direction: str = "top-to-bottom",
    node_gap: float = 120.0,
    branch_gap: float = 240.0,
    start_offset: Tuple[float, float] = (120, 140),
) -> List[Dict[str, Any]]:
    """Position flowchart nodes by row/col grid.

    Each node dict must have 'id', 'width', 'height', 'row', 'col'.
    Adds 'x', 'y', 'bbox' to each node and returns the list.
    """
    ox, oy = start_offset
    for node in nodes:
        row = node.get("row", 0)
        col = node.get("col", 0)
        w = node.get("width", 140)
        h = node.get("height", 50)
        if flow_direction == "top-to-bottom":
            x = ox + col * branch_gap
            y = oy + row * node_gap
        else:
            x = ox + row * node_gap
            y = oy + col * branch_gap
        node["x"] = x
        node["y"] = y
        node["bbox"] = (x, y, w, h)
    return nodes


def decision_branch_positions(
    decision_node: Dict[str, Any],
    yes_node: Dict[str, Any],
    no_node: Dict[str, Any],
    node_gap: float = 120.0,
) -> Dict[str, Any]:
    """Position yes/no branch nodes relative to a decision diamond."""
    dx, dy = decision_node["x"], decision_node["y"]
    dw, dh = decision_node["width"], decision_node["height"]

    yes_x = dx + dw + 60
    yes_y = dy + dh + 40
    yes_node["x"] = yes_x
    yes_node["y"] = yes_y
    yes_node["bbox"] = (
        yes_x,
        yes_y,
        yes_node.get("width", 140),
        yes_node.get("height", 50),
    )

    no_x = dx - no_node.get("width", 140) - 60
    no_y = dy + dh + 40
    no_node["x"] = no_x
    no_node["y"] = no_y
    no_node["bbox"] = (no_x, no_y, no_node.get("width", 140), no_node.get("height", 50))

    return {"yes": yes_node, "no": no_node}


# ---------------------------------------------------------------------------
# Automatic layout via networkx
# ---------------------------------------------------------------------------


def auto_layout(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    layout_type: str = "hierarchical",
    canvas: Tuple[float, float] = (960, 540),
    title_bar_height: float = 50,
    margin: float = 80,
) -> List[Dict[str, Any]]:
    """Compute node positions automatically using networkx layout algorithms.

    layout_type options:
      'hierarchical' — Graphviz dot (best for flowcharts/architectures).
                       Requires: pip install pygraphviz
                       Falls back to spring layout if pygraphviz unavailable.
      'spring'       — Force-directed spring (good for concept/network diagrams).
      'radial'       — Shell/concentric layout (good for hub-and-spoke diagrams).
    """
    G = nx.DiGraph()
    for n in nodes:
        G.add_node(n["id"])
    for e in edges:
        G.add_edge(e["from"], e["to"])

    if layout_type == "hierarchical":
        try:
            from networkx.drawing.nx_agraph import graphviz_layout

            raw = graphviz_layout(G, prog="dot")
        except (ImportError, Exception):
            raw = nx.spring_layout(G, seed=42)
    elif layout_type == "radial":
        raw = nx.shell_layout(G)
    else:  # 'spring'
        raw = nx.spring_layout(G, seed=42)

    # Scale networkx positions to the SVG canvas
    W, H = canvas
    effective_h = H - title_bar_height - margin * 2
    xs = [p[0] for p in raw.values()]
    ys = [p[1] for p in raw.values()]
    span_x = (max(xs) - min(xs)) or 1.0
    span_y = (max(ys) - min(ys)) or 1.0
    scale_x = (W - margin * 2) / span_x
    scale_y = effective_h / span_y

    pos_map = {
        nid: (
            margin + (px - min(xs)) * scale_x,
            title_bar_height + margin + (py - min(ys)) * scale_y,
        )
        for nid, (px, py) in raw.items()
    }

    for node in nodes:
        cx, cy = pos_map[node["id"]]
        w = node.get("width", 140)
        h = node.get("height", 50)
        node["x"] = cx - w / 2
        node["y"] = cy - h / 2
        node["bbox"] = (node["x"], node["y"], w, h)

    return nodes


# ---------------------------------------------------------------------------
# Circle distribution (kept custom — simpler than networkx shell_layout)
# ---------------------------------------------------------------------------


def distribute_along_circle(
    center_point: Point,
    radius: float,
    count: int,
    start_angle: float = -90.0,
) -> List[Point]:
    """Distribute ``count`` points evenly around a circle."""
    cx, cy = center_point
    return [
        (
            cx + radius * math.cos(math.radians(start_angle + 360.0 / count * i)),
            cy + radius * math.sin(math.radians(start_angle + 360.0 / count * i)),
        )
        for i in range(count)
    ]


# ---------------------------------------------------------------------------
# Overlap resolution (rectangle-aware — no equivalent in networkx)
# ---------------------------------------------------------------------------


def resolve_overlaps(
    placed_bboxes: List[BBox],
    new_bbox: BBox,
    min_gap: float = 20.0,
    max_iterations: int = 20,
) -> BBox:
    """Find a non-overlapping position for new_bbox by pushing away from overlaps."""
    rx, ry, rw, rh = new_bbox
    for _ in range(max_iterations):
        overlapping = find_overlapping(placed_bboxes, (rx, ry, rw, rh), min_gap)
        if not overlapping:
            break
        for idx in overlapping:
            ob = placed_bboxes[idx]
            ox, oy, ow, oh = ob
            ocx, ocy = ox + ow / 2.0, oy + oh / 2.0
            rcx, rcy = rx + rw / 2.0, ry + rh / 2.0
            ddx = rcx - ocx
            ddy = rcy - ocy
            if abs(ddx) * oh > abs(ddy) * ow:
                rx = ox + ow + min_gap if ddx > 0 else ox - rw - min_gap
            else:
                ry = oy + oh + min_gap if ddy > 0 else oy - rh - min_gap
    return (rx, ry, rw, rh)


# ---------------------------------------------------------------------------
# ViewBox computation (pure math — no library needed)
# ---------------------------------------------------------------------------


def compute_viewbox(
    all_bboxes: List[BBox],
    padding: int = 40,
    target_aspect: Optional[float] = None,
    title_bar_height: float = 0.0,
    footer_height: float = 0.0,
) -> Tuple[int, int, int, int]:
    """Compute (vx, vy, vw, vh) from all element bounding boxes."""
    if not all_bboxes:
        return (0, 0, 960, 540)

    content_bbox = union_bbox(all_bboxes)
    cx, cy, cw, ch = content_bbox

    vx = cx - padding
    vy = cy - padding - title_bar_height
    vw = cw + 2 * padding
    vh = ch + 2 * padding + title_bar_height + footer_height

    if vx < 0:
        vw += abs(vx)
        vx = 0
    if vy < 0:
        vh += abs(vy)
        vy = 0

    vw = int(math.ceil(vw / 50.0) * 50)
    vh = int(math.ceil(vh / 50.0) * 50)

    if target_aspect:
        current_aspect = vw / vh if vh > 0 else 1.0
        if current_aspect < target_aspect:
            vw = int(vh * target_aspect)
        elif current_aspect > target_aspect:
            vh = int(vw / target_aspect)
        vw = int(math.ceil(vw / 50.0) * 50)
        vh = int(math.ceil(vh / 50.0) * 50)

    return (0, 0, max(vw, 400), max(vh, 300))


# ---------------------------------------------------------------------------
# Topological sort helpers
# ---------------------------------------------------------------------------


def _kahn_levels(adj: Dict[str, List[str]], in_deg: Dict[str, int]) -> Dict[str, int]:
    """Run Kahn's algorithm to compute topological levels.

    Returns dict mapping node id → level (0-based). Nodes in cycles
    or unreachable are assigned level 0.
    """
    q = deque([nid for nid, d in in_deg.items() if d == 0])
    level: Dict[str, int] = {nid: 0 for nid in q}
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            in_deg[v] -= 1
            if in_deg[v] == 0:
                level[v] = level[u] + 1
                q.append(v)
    return level


def _kahn_levels_with_cycles(
    adj: Dict[str, List[str]], in_deg: Dict[str, int], node_ids: List[str]
) -> Dict[str, int]:
    """Run Kahn's algorithm with cycle resolution via BFS fallback."""
    level = _kahn_levels(adj, in_deg)

    # BFS from processed nodes to assign levels to cycle nodes
    processed = set(level.keys())
    remaining = [nid for nid in node_ids if nid not in level]
    if remaining:
        bfs_q: deque = deque(processed)
        visited = set(processed)
        bfs_level = dict(level)
        while bfs_q:
            u = bfs_q.popleft()
            for v in adj.get(u, []):
                if v not in visited:
                    visited.add(v)
                    bfs_level[v] = bfs_level.get(u, 0) + 1
                    bfs_q.append(v)
        for nid in node_ids:
            if nid not in bfs_level:
                bfs_level[nid] = 0
        level = bfs_level
    return level


def topological_sort(
    nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Assign row numbers via Kahn's topological sort.

    Returns nodes with 'row' and 'col' added. Skips if already assigned.
    Handles cycles (falls back to input order) and disconnected subgraphs.
    """
    if all("row" in n for n in nodes):
        return nodes

    adj: Dict[str, List[str]] = {n["id"]: [] for n in nodes}
    in_deg: Dict[str, int] = {n["id"]: 0 for n in nodes}
    for e in edges:
        adj.setdefault(e["from"], []).append(e["to"])
        in_deg[e["to"]] = in_deg.get(e["to"], 0) + 1

    level = _kahn_levels(adj, in_deg)

    col_counter: Dict[int, int] = {}
    for n in nodes:
        row = level.get(n["id"], 0)
        n["row"] = row
        n["col"] = col_counter.get(row, 0)
        col_counter[row] = col_counter.get(row, 0) + 1
    return nodes


# ---------------------------------------------------------------------------
# Grid cell layout — compute cell sizes, position elements centered
# ---------------------------------------------------------------------------


def compute_grid_cells(
    nodes: List[Dict[str, Any]], padding_x: float = 40, padding_y: float = 60
) -> Tuple[Dict[int, float], Dict[int, float]]:
    """Compute cell dimensions (w, h) from max width/height per column/row."""
    col_max_w: Dict[int, float] = {}
    row_max_h: Dict[int, float] = {}
    for n in nodes:
        c, r = n.get("col", 0), n.get("row", 0)
        col_max_w[c] = max(col_max_w.get(c, 0), n["width"])
        row_max_h[r] = max(row_max_h.get(r, 0), n["height"])
    return (
        {c: w + padding_x for c, w in col_max_w.items()},
        {r: h + padding_y for r, h in row_max_h.items()},
    )


def position_elements(
    nodes: List[Dict[str, Any]],
    cell_w: Dict[int, float],
    cell_h: Dict[int, float],
    start_offset: Tuple[float, float] = (120, 140),
) -> List[Dict[str, Any]]:
    """Center each element within its grid cell. Adds 'x', 'y', 'bbox'."""
    ox, oy = start_offset
    for n in nodes:
        col, row = n.get("col", 0), n.get("row", 0)
        gx = ox + sum(cell_w.get(c, 0) for c in range(col))
        gy = oy + sum(cell_h.get(r, 0) for r in range(row))
        n["x"] = gx + (cell_w[col] - n["width"]) / 2
        n["y"] = gy + (cell_h[row] - n["height"]) / 2
        n["bbox"] = (n["x"], n["y"], n["width"], n["height"])
    return nodes


def align_rows(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Vertically center all nodes in each row to the same y."""
    rows: Dict[int, List[Dict[str, Any]]] = {}
    for n in nodes:
        rows.setdefault(n["row"], []).append(n)
    for rn in rows.values():
        max_h = max(n["height"] for n in rn)
        base_y = min(n["y"] for n in rn)
        for n in rn:
            n["y"] = base_y + (max_h - n["height"]) / 2
            n["bbox"] = (n["x"], n["y"], n["width"], n["height"])
    return nodes


def center_align_nodes(
    nodes: List[Dict[str, Any]],
    start_offset: Tuple[float, float] = (120, 140),
    branch_gap: float = 240,
    node_gap: float = 120,
) -> List[Dict[str, Any]]:
    """Position nodes by center_x per column and center_y per row."""
    ox, oy = start_offset
    col_mw: Dict[int, float] = {}
    for n in nodes:
        col_mw[n["col"]] = max(col_mw.get(n["col"], 0), n["width"])
    for n in nodes:
        cl = ox + n["col"] * branch_gap
        n["x"] = cl + col_mw[n["col"]] / 2 - n["width"] / 2
        n["y"] = oy + n["row"] * node_gap - n["height"] / 2
        n["bbox"] = (n["x"], n["y"], n["width"], n["height"])
    return nodes


def enforce_column_gap(nodes: List[Dict[str, Any]], min_gap: float = 140) -> float:
    """Ensure minimum gap between col 0 and col 1. Shifts col 1 if needed.

    Returns corridor_x (midpoint between the two columns).
    """
    c0 = [n for n in nodes if n.get("col") == 0]
    c1 = [n for n in nodes if n.get("col") == 1]
    if not c0 or not c1:
        return 0
    c0r = max(n["x"] + n["width"] for n in c0)
    c1l = min(n["x"] for n in c1)
    if c1l - c0r < min_gap:
        shift = min_gap - (c1l - c0r)
        for n in c1:
            n["x"] += shift
            n["bbox"] = (n["x"], n["y"], n["width"], n["height"])
    c0r = max(n["x"] + n["width"] for n in c0)
    c1l = min(n["x"] for n in c1)
    return (c0r + c1l) / 2


# ---------------------------------------------------------------------------
# Edge classification — separate forward from feedback edges by topology
# ---------------------------------------------------------------------------


def classify_edges_by_topology(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Classify edges into forward, feedback, and same-row categories.

    Uses a two-pass approach:
    1. First, compute a rough topological level for each node using ALL edges.
       Nodes stuck in cycles get estimated levels via BFS from zero-in-degree nodes.
    2. Then classify each edge by comparing source vs destination levels:
       - forward:  src_level < dst_level  (goes downstream)
       - feedback: src_level > dst_level  (goes upstream, against flow)
       - same-row: src_level == dst_level (horizontal connection)

    Returns:
        (forward_edges, feedback_edges, same_row_edges)
    """
    # Build adjacency and in-degree
    adj: Dict[str, List[str]] = {n["id"]: [] for n in nodes}
    in_deg: Dict[str, int] = {n["id"]: 0 for n in nodes}
    for e in edges:
        f, t = e["from"], e["to"]
        if f in adj and t in adj:
            adj[f].append(t)
            in_deg[t] = in_deg.get(t, 0) + 1

    # Compute topological levels with cycle resolution
    level = _kahn_levels_with_cycles(adj, in_deg, [n["id"] for n in nodes])

    # Classify edges
    forward: List[Dict[str, Any]] = []
    feedback: List[Dict[str, Any]] = []
    same_row: List[Dict[str, Any]] = []

    for e in edges:
        sl = level.get(e["from"], 0)
        dl = level.get(e["to"], 0)
        if sl < dl:
            e["_topo_type"] = "forward"
            forward.append(e)
        elif sl > dl:
            e["_topo_type"] = "feedback"
            feedback.append(e)
        else:
            e["_topo_type"] = "same-row"
            same_row.append(e)

    return forward, feedback, same_row


# ---------------------------------------------------------------------------
# Auto layout — assign row/col from edge topology, then compute positions
# ---------------------------------------------------------------------------


def dag_layout(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    flow_direction: str = "top-to-bottom",
    node_gap: float = 120.0,
    branch_gap: float = 260.0,
    start_offset: Tuple[float, float] = (100, 100),
    col_gap_min: float = 150.0,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """One-shot layout for pure DAGs (no feedback loops).

    A convenience wrapper around ``assign_flow_layout()`` that marks **all**
    edges as ``'forward'`` — suitable when the graph is a true directed
    acyclic graph with no backward connections.

    If your graph has feedback loops, use ``assign_flow_layout()`` directly
    with explicit ``_topo_type='feedback'`` on backward edges.

    Example::

        nodes, edges = dag_layout(nodes, edges)
    """
    for e in edges:
        e.setdefault("_topo_type", "forward")
    return assign_flow_layout(
        nodes,
        edges,
        flow_direction=flow_direction,
        node_gap=node_gap,
        branch_gap=branch_gap,
        start_offset=start_offset,
        col_gap_min=col_gap_min,
    )


def assign_flow_layout(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    flow_direction: str = "top-to-bottom",
    node_gap: float = 120.0,
    branch_gap: float = 260.0,
    start_offset: Tuple[float, float] = (100, 100),
    col_gap_min: float = 150.0,
    edge_type_key: str = "_topo_type",
    feedback_types: Tuple[str, ...] = ("feedback", "same-row"),
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Auto-assign row/col from edge topology, then compute pixel positions.

    This is the primary entry point for diagram layout. It replaces the manual
    ``row``/``col`` specification pattern — just pass nodes and edges, and this
    function figures out the grid placement automatically.

    **How it works**:
    1. Collects edges whose ``edge_type_key`` value is **not** in
       ``feedback_types`` — these are treated as **topology edges** that define
       the flow direction. Edges with ``"feedback"`` or ``"same-row"`` type are
       excluded from topology and only used for visual routing.
    2. Runs **Kahn's topological sort** on topology edges to assign rows.
    3. Assigns columns by detecting **parallel branches**: within each row,
       nodes that descend from different parent branches get separate columns.
    4. Computes pixel positions, aligns rows, centers columns, enforces gaps.

    **Pre-classifying edges**: If your graph contains feedback loops, mark
    feedback edges explicitly so they don't distort the topology::

        edges = [
            {'from': 'a', 'to': 'b'},                          # auto → forward
            {'from': 'z', 'to': 'a', '_topo_type': 'feedback'}, # excluded
        ]

    If ``edge_type_key`` is not set on an edge, ``classify_edges_by_topology()``
    is called to auto-detect forward/feedback/same-row. This works well for
    DAGs but may misclassify edges in graphs with complex feedback loops.
    For such cases, pre-set the type key explicitly.

    Nodes that already have ``'row'`` and ``'col'`` set are preserved as-is
    and will not be repositioned by this function.

    Args:
        nodes: List of node dicts. Each must have ``'id'`` and ``'text'``.
               ``'width'`` and ``'height'`` should be pre-computed via
               ``get_shape_dimensions()``. If ``'row'`` and ``'col'`` are
               already set, they are preserved.
        edges: List of edge dicts. Each must have ``'from'`` and ``'to'``.
               Optionally set ``edge_type_key`` (default ``'_topo_type'``)
               to ``'feedback'`` or ``'same-row'`` to exclude from topology.
        flow_direction: ``'top-to-bottom'`` (default) or ``'left-to-right'``.
        node_gap: Vertical (or horizontal) spacing between rows in px.
        branch_gap: Horizontal (or vertical) spacing between columns in px.
        start_offset: ``(x_offset, y_offset)`` for the first node.
        col_gap_min: Min px gap between columns. 0 to skip enforcement.
        edge_type_key: Dict key used to look up an edge's pre-set type.
        feedback_types: Tuple of type values that should be excluded from
                        topology (default ``("feedback", "same-row")``).

    Returns:
        ``(nodes, edges)`` — the input lists, each augmented:
        - ``nodes``: each node gets ``row``, ``col``, ``x``, ``y``, ``bbox``.
        - ``edges``: each edge gets ``_topo_type``.

    Example with pre-classified edges::

        edges = [
            {'from': 'a', 'to': 'b'},
            {'from': 'b', 'to': 'c'},
            {'from': 'c', 'to': 'a', '_topo_type': 'feedback'},  # excluded
        ]
        nodes, edges = assign_flow_layout(nodes, edges)
        # a→b→c gets rows 0→1→2; feedback edge ignored for topology
    """
    # Preserve nodes that already have row/col
    has_explicit = all("row" in n and "col" in n for n in nodes)
    if has_explicit:
        # Already set — just compute positions
        nodes = flow_layout(nodes, flow_direction, node_gap, branch_gap, start_offset)
        nodes = align_rows(nodes)
        cols: Dict[int, List[Dict[str, Any]]] = {}
        for n in nodes:
            cols.setdefault(n["col"], []).append(n)
        for col_nodes in cols.values():
            max_w = max(n["width"] for n in col_nodes)
            col_left = min(n["x"] for n in col_nodes)
            col_center_x = col_left + max_w / 2
            for n in col_nodes:
                n["x"] = col_center_x - n["width"] / 2
                n["bbox"] = (n["x"], n["y"], n["width"], n["height"])
        if col_gap_min > 0:
            enforce_column_gap(nodes, col_gap_min)
        return nodes, edges

    # --- Step 1: Separate topology edges from non-topology edges ---
    topo_edges: List[Dict[str, Any]] = []
    non_topo_edges: List[Dict[str, Any]] = []

    for e in edges:
        etype = e.get(edge_type_key)
        if etype is None:
            topo_edges.append(e)  # auto-classify later
        elif etype in feedback_types:
            non_topo_edges.append(e)
            e["_topo_type"] = etype
        else:
            topo_edges.append(e)
            e["_topo_type"] = etype

    # Auto-classify remaining topology edges (only if there are any untyped)
    untyped = [e for e in topo_edges if e.get(edge_type_key) is None]
    if untyped:
        # Save any pre-set types to restore after auto-classification
        saved_types = {
            id(e): e.get(edge_type_key)
            for e in edges
            if e.get(edge_type_key) is not None
        }
        # Run classification on all edges
        fwd, fb, sr = classify_edges_by_topology(nodes, edges)
        # Restore pre-set types that should have been preserved
        for e in edges:
            saved = saved_types.get(id(e))
            if saved is not None:
                e[edge_type_key] = saved
        # Assign any still-untyped edges as forward
        for e in topo_edges:
            if e.get(edge_type_key) is None:
                e[edge_type_key] = "forward"
    else:
        # All topology edges already have types; just run a quick forward set
        fwd = topo_edges
        fb = [e for e in edges if e.get("_topo_type") == "feedback"]
        sr = [e for e in edges if e.get("_topo_type") == "same-row"]

    # --- Step 2: Topological sort on topology edges only ---
    adj: Dict[str, List[str]] = {n["id"]: [] for n in nodes}
    in_deg: Dict[str, int] = {n["id"]: 0 for n in nodes}
    for e in topo_edges:
        f, t = e["from"], e["to"]
        if f in adj and t in adj:
            adj[f].append(t)
            in_deg[t] = in_deg.get(t, 0) + 1

    level = _kahn_levels(adj, in_deg)
    for n in nodes:
        level.setdefault(n["id"], 0)

    # --- Step 3: Assign columns based on branch detection ---
    parent: Dict[str, Optional[str]] = {n["id"]: None for n in nodes}
    for e in topo_edges:
        parent[e["to"]] = e["from"]

    roots = [nid for nid, p in parent.items() if p is None]
    branch_id: Dict[str, int] = {}
    for root in roots:
        branch_id[root] = 0

    topo_adj: Dict[str, List[str]] = {n["id"]: [] for n in nodes}
    for e in topo_edges:
        topo_adj.setdefault(e["from"], []).append(e["to"])

    processed = set()
    bfs_q = deque(roots)
    for r in roots:
        if r not in branch_id:
            branch_id[r] = 0
    next_branch = 1

    while bfs_q:
        u = bfs_q.popleft()
        if u in processed:
            continue
        processed.add(u)
        children = topo_adj.get(u, [])
        if len(children) <= 1:
            for v in children:
                branch_id[v] = branch_id.get(u, 0)
                bfs_q.append(v)
        else:
            for i, v in enumerate(children):
                if i == 0:
                    branch_id[v] = branch_id.get(u, 0)
                else:
                    branch_id[v] = next_branch
                    next_branch += 1
                bfs_q.append(v)

    for n in nodes:
        if n["id"] not in branch_id:
            branch_id[n["id"]] = 0

    for n in nodes:
        n["row"] = level.get(n["id"], 0)
        n["col"] = branch_id.get(n["id"], 0)

    # --- Step 4: Compute positions ---
    nodes = flow_layout(nodes, flow_direction, node_gap, branch_gap, start_offset)
    nodes = align_rows(nodes)

    cols_map: Dict[int, List[Dict[str, Any]]] = {}
    for n in nodes:
        cols_map.setdefault(n["col"], []).append(n)
    for col_nodes in cols_map.values():
        max_w = max(n["width"] for n in col_nodes)
        col_left = min(n["x"] for n in col_nodes)
        col_center_x = col_left + max_w / 2
        for n in col_nodes:
            n["x"] = col_center_x - n["width"] / 2
            n["bbox"] = (n["x"], n["y"], n["width"], n["height"])

    if col_gap_min > 0:
        enforce_column_gap(nodes, col_gap_min)

    return nodes, edges
