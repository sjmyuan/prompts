"""
Connection routing utilities for SVG diagrams.

Computes orthogonal paths, bezier curves, connection endpoints,
and validates connections for intersections.
"""

import math
from typing import Tuple, List, Optional, Dict, Any

from geometry import (
    BBox,
    Point,
    connection_point,
    bbox_to_rect,
    segment_line_intersection,
    segment_rect_intersection,
    inflate_bbox,
    center,
    distance,
    allocate_ports_for_edges,
    get_side_ports,
    find_closest_port,
)


def orthogonal_path(
    src: Point,
    dst: Point,
    src_side: str,
    dst_side: str,
    clearance: float = 25.0,
    obstacles: Optional[List[BBox]] = None,
    mid_offset: Optional[Tuple[float, float]] = None,
) -> List[Point]:
    """Compute an orthogonal path (horizontal/vertical segments only) from src to dst.

    Returns a list of waypoints including src and dst.
    Routes using an L-shape (1 turn) or Z-shape (2 turns) depending on alignment.
    If obstacles are provided, avoids them with C-shape (3+ turns).

    Args:
        src: Source point (on src shape edge)
        dst: Destination point (on dst shape edge)
        src_side: Which side of src shape ('bottom' means exiting downward)
        dst_side: Which side of dst shape ('top' means entering from above)
        clearance: Minimum distance from turn points to obstacle edges
        obstacles: List of bounding boxes to avoid
        mid_offset: Optional (dx, dy) offset applied to middle horizontal/vertical
                    segments to spread parallel edges apart (edge overlap avoidance).

    Returns:
        List of (x, y) waypoints forming the path.
    """
    path = [src]
    sx, sy = src
    dx, dy = dst

    obstacles = obstacles or []

    def _turn_clear(pt: Point, obs: List[BBox]) -> bool:
        """Check if a turn point is clear of all obstacles."""
        for ob in obs:
            inflated = inflate_bbox(ob, clearance)
            rx, ry, rw, rh = inflated
            if rx <= pt[0] <= rx + rw and ry <= pt[1] <= ry + rh:
                return False
        return True

    # --- Case 1: Same axis alignment ---
    if abs(sx - dx) < 1e-6:
        # Vertically aligned - direct vertical line
        if mid_offset:
            offset_x = mid_offset[0]
            # Create a Z-shape: vertical → horizontal → vertical
            # Offset the middle horizontal segment to spread parallel edges
            return [src, (sx + offset_x, sy), (dx + offset_x, dy), dst]
        return [src, dst]

    if abs(sy - dy) < 1e-6:
        # Horizontally aligned - direct horizontal line
        if mid_offset:
            offset_y = mid_offset[1]
            # Create a Z-shape: horizontal → vertical → horizontal
            # Offset the middle vertical segment to spread parallel edges
            return [src, (sx, sy + offset_y), (dx, dy + offset_y), dst]
        return [src, dst]

    # --- Case 2: L-shape (single turn) ---
    # Try turn at src-x, dst-y first
    turn1 = (sx, dy)
    if _turn_clear(turn1, obstacles):
        waypoints = [src, turn1, dst]
    else:
        # Try turn at dst-x, src-y
        turn2 = (dx, sy)
        if _turn_clear(turn2, obstacles):
            waypoints = [src, turn2, dst]
        else:
            # --- Case 3: Z-shape or C-shape ---
            # Route through a midpoint
            mid_x = (sx + dx) / 2.0
            mid_y = (sy + dy) / 2.0

            # Apply mid_offset to spread parallel edges
            ox, oy = mid_offset if mid_offset else (0.0, 0.0)

            # Try stepping out from source first, then crossing, then entering
            if src_side in ("bottom", "top"):
                # Exit vertically first, then horizontal, then vertical
                mid_y1 = sy + (40 if src_side == "bottom" else -40)
                mid_y2 = dy + (40 if dst_side == "bottom" else -40)
                # Apply offset to the horizontal segment only
                waypoints = [
                    src,
                    (sx + ox, mid_y1),
                    (dx + ox, mid_y1),
                    (dx + ox, mid_y2),
                    dst,
                ]
            else:
                # Exit horizontally first
                mid_x1 = sx + (40 if src_side == "right" else -40)
                mid_x2 = dx + (40 if dst_side == "right" else -40)
                # Apply offset to the vertical segment only
                waypoints = [
                    src,
                    (mid_x1, sy + oy),
                    (mid_x1, dy + oy),
                    (mid_x2, dy + oy),
                    dst,
                ]

        return _simplify_path(waypoints)

    # Apply mid_offset to L-shape if needed
    if mid_offset and len(waypoints) == 3:
        # Insert offset points to split the path: src → offset_mid → offset_mid2 → dst
        ox, oy = mid_offset
        mid = waypoints[1]
        if abs(waypoints[0][0] - waypoints[2][0]) < abs(
            waypoints[0][1] - waypoints[2][1]
        ):
            # Vertical-dominant L: offset the horizontal segment
            waypoints = [src, (mid[0], mid[1] + oy), (mid[0] + ox, mid[1] + oy), dst]
        else:
            # Horizontal-dominant L: offset the vertical segment
            waypoints = [src, (mid[0] + ox, mid[1]), (mid[0] + ox, mid[1] + oy), dst]

    return _simplify_path(waypoints)


def _simplify_path(waypoints: List[Point]) -> List[Point]:
    """Remove redundant collinear waypoints."""
    if len(waypoints) <= 2:
        return waypoints

    result = [waypoints[0]]
    for i in range(1, len(waypoints) - 1):
        prev = result[-1]
        curr = waypoints[i]
        nxt = waypoints[i + 1]

        # Keep the point if it's not collinear with prev and next
        if not _collinear(prev, curr, nxt):
            result.append(curr)

    result.append(waypoints[-1])
    return result


def _collinear(p1: Point, p2: Point, p3: Point) -> bool:
    """Check if three points are collinear (within tolerance)."""
    return (
        abs((p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1]))
        < 1e-6
    )


def bezier_path(src: Point, dst: Point, curvature: float = 0.3) -> str:
    """Compute a smooth cubic bezier curve path string between two points.

    Args:
        src: Source point
        dst: Destination point
        curvature: How much the curve bends (0 = straight, 1 = very curved)

    Returns:
        SVG path 'd' attribute string for a cubic bezier.
    """
    sx, sy = src
    dx, dy = dst
    mid_y = (sy + dy) / 2.0
    dx_offset = abs(dx - sx) * curvature

    cx1 = sx
    cy1 = mid_y
    cx2 = dx
    cy2 = mid_y

    return f"M {sx:.1f} {sy:.1f} C {cx1:.1f} {cy1:.1f}, {cx2:.1f} {cy2:.1f}, {dx:.1f} {dy:.1f}"


def connection_endpoints(
    src_bbox: BBox,
    dst_bbox: BBox,
    flow_direction: str = "top-to-bottom",
    ports_per_side: int = 0,
) -> Tuple[Point, Point, str, str]:
    """Determine the best connection endpoints between two shape bounding boxes.

    When ``ports_per_side`` is 0 (default), returns the center of each
    selected side (4-point model, backward-compatible behavior).

    When ``ports_per_side > 0``, selects the optimal sub-port on each side
    using ``get_side_ports()`` + ``find_closest_port()``, implementing the
    sub-point selection from flowchart.md \\u00a73.4.

    Returns:
        (src_point, dst_point, src_side, dst_side)
    """
    src_center_pt = center(src_bbox)
    dst_center_pt = center(dst_bbox)

    def _pick(bbox: BBox, side: str, target: Point) -> Point:
        if ports_per_side > 0:
            ports = get_side_ports(bbox, side, ports_per_side)
            idx = find_closest_port(ports, target, set(), prefer_side=side)
            return ports[idx]
        return connection_point(bbox, side)

    if flow_direction == "top-to-bottom":
        # Default: source bottom → target top
        src_pt = _pick(src_bbox, "bottom", dst_center_pt)
        dst_pt = _pick(dst_bbox, "top", src_center_pt)
        return src_pt, dst_pt, "bottom", "top"

    elif flow_direction == "left-to-right":
        src_pt = _pick(src_bbox, "right", dst_center_pt)
        dst_pt = _pick(dst_bbox, "left", src_center_pt)
        return src_pt, dst_pt, "right", "left"

    else:
        # Auto-detect based on relative positions
        dx_center = dst_center_pt[0] - src_center_pt[0]
        dy_center = dst_center_pt[1] - src_center_pt[1]

        if abs(dx_center) >= abs(dy_center):
            if dx_center > 0:
                return (
                    _pick(src_bbox, "right", dst_center_pt),
                    _pick(dst_bbox, "left", src_center_pt),
                    "right",
                    "left",
                )
            else:
                return (
                    _pick(src_bbox, "left", dst_center_pt),
                    _pick(dst_bbox, "right", src_center_pt),
                    "left",
                    "right",
                )
        else:
            if dy_center > 0:
                return (
                    _pick(src_bbox, "bottom", dst_center_pt),
                    _pick(dst_bbox, "top", src_center_pt),
                    "bottom",
                    "top",
                )
            else:
                return (
                    _pick(src_bbox, "top", dst_center_pt),
                    _pick(dst_bbox, "bottom", src_center_pt),
                    "top",
                    "bottom",
                )


def path_to_svg_d(waypoints: List[Point]) -> str:
    """Convert a list of waypoints to an SVG path 'd' attribute string."""
    if not waypoints:
        return ""
    parts = [f"M {waypoints[0][0]:.1f} {waypoints[0][1]:.1f}"]
    for pt in waypoints[1:]:
        parts.append(f"L {pt[0]:.1f} {pt[1]:.1f}")
    return " ".join(parts)


def detect_intersections(
    connections: List[List[Point]],
    shape_bboxes: List[BBox],
) -> List[Dict[str, Any]]:
    """Detect all line-line and line-shape intersections.

    Args:
        connections: List of connection paths, each is a list of waypoints
        shape_bboxes: Bounding boxes of all shapes on the canvas

    Returns:
        List of intersection reports: [{'type': 'line-line', 'conn_i': 0, 'conn_j': 1,
        'segment_i': (p1,p2), 'segment_j': (p3,p4), 'point': (x,y)}, ...]
    """
    problems = []

    # Line-line intersections
    for i in range(len(connections)):
        for j in range(i + 1, len(connections)):
            path_i = connections[i]
            path_j = connections[j]

            for si in range(len(path_i) - 1):
                seg_i = (path_i[si], path_i[si + 1])
                for sj in range(len(path_j) - 1):
                    seg_j = (path_j[sj], path_j[sj + 1])
                    pt = segment_line_intersection(
                        seg_i[0], seg_i[1], seg_j[0], seg_j[1]
                    )
                    if pt:
                        problems.append(
                            {
                                "type": "line-line",
                                "conn_i": i,
                                "conn_j": j,
                                "segment_i": si,
                                "segment_j": sj,
                                "point": pt,
                            }
                        )

    # Line-shape intersections
    for i, conn in enumerate(connections):
        for si in range(len(conn) - 1):
            seg = (conn[si], conn[si + 1])
            for j, bbox in enumerate(shape_bboxes):
                if segment_rect_intersection(seg[0], seg[1], bbox):
                    problems.append(
                        {
                            "type": "line-shape",
                            "conn_i": i,
                            "segment_i": si,
                            "shape_j": j,
                            "shape_bbox": bbox,
                        }
                    )

    return problems


def _segment_with_extreme(waypoints: List[Point], key: str) -> int:
    """Return the index of the segment with extreme (min or max) length."""
    if len(waypoints) < 2:
        return -1
    extreme_val = float("inf") if key == "min" else -1.0
    extreme_idx = 0
    compare = (lambda d, e: d < e) if key == "min" else (lambda d, e: d > e)
    for i in range(len(waypoints) - 1):
        d = distance(waypoints[i], waypoints[i + 1])
        if compare(d, extreme_val):
            extreme_val = d
            extreme_idx = i
    return extreme_idx


def shortest_straight_segment(waypoints: List[Point]) -> int:
    """Return the index of the shortest straight segment in a path."""
    return _segment_with_extreme(waypoints, "min")


def longest_straight_segment(waypoints: List[Point]) -> int:
    """Return the index of the longest straight segment in a path."""
    return _segment_with_extreme(waypoints, "max")


def midpoint_of_segment(waypoints: List[Point], seg_idx: int) -> Point:
    """Return the midpoint of a segment in the path."""
    p1 = waypoints[seg_idx]
    p2 = waypoints[seg_idx + 1]
    return ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)


def segment_is_horizontal(waypoints: List[Point], seg_idx: int) -> bool:
    """Check if a segment is horizontal."""
    p1 = waypoints[seg_idx]
    p2 = waypoints[seg_idx + 1]
    return abs(p1[1] - p2[1]) < abs(p1[0] - p2[0])


def endpoint_valid(
    conn_waypoints: List[Point], dst_bbox: BBox, tolerance: float = 2.0
) -> Dict[str, Any]:
    """Validate that a connection's endpoint is properly on the target shape edge.

    Returns:
        Dict with 'valid' (bool), 'gap' (float), 'penetration' (float), 'issues' (list).
    """
    issues = []
    if len(conn_waypoints) < 2:
        return {"valid": False, "gap": 0, "penetration": 0, "issues": ["No waypoints"]}

    endpoint = conn_waypoints[-1]
    entry_point = conn_waypoints[-2]
    dx, dy, dw, dh = dst_bbox

    # Check if endpoint is on the bbox edge
    on_left = abs(endpoint[0] - dx) <= tolerance and dy <= endpoint[1] <= dy + dh
    on_right = (
        abs(endpoint[0] - (dx + dw)) <= tolerance and dy <= endpoint[1] <= dy + dh
    )
    on_top = abs(endpoint[1] - dy) <= tolerance and dx <= endpoint[0] <= dx + dw
    on_bottom = (
        abs(endpoint[1] - (dy + dh)) <= tolerance and dx <= endpoint[0] <= dx + dw
    )

    on_edge = on_left or on_right or on_top or on_bottom

    if not on_edge:
        # Check if it's inside
        inside = dx < endpoint[0] < dx + dw and dy < endpoint[1] < dy + dh
        if inside:
            issues.append("Endpoint inside shape")
            penetration = min(
                abs(endpoint[0] - dx),
                abs(endpoint[0] - (dx + dw)),
                abs(endpoint[1] - dy),
                abs(endpoint[1] - (dy + dh)),
            )
            return {
                "valid": False,
                "gap": 0,
                "penetration": penetration,
                "issues": issues,
            }
        else:
            issues.append("Endpoint not on shape edge")
            # Calculate gap
            if endpoint[0] < dx:
                gap_x = dx - endpoint[0]
            elif endpoint[0] > dx + dw:
                gap_x = endpoint[0] - (dx + dw)
            else:
                gap_x = 0
            if endpoint[1] < dy:
                gap_y = dy - endpoint[1]
            elif endpoint[1] > dy + dh:
                gap_y = endpoint[1] - (dy + dh)
            else:
                gap_y = 0
            gap = math.hypot(gap_x, gap_y)
            return {"valid": False, "gap": gap, "penetration": 0, "issues": issues}

    # Check entry segment length
    entry_len = distance(entry_point, endpoint)
    if entry_len < 15.0:
        issues.append(f"Entry segment too short: {entry_len:.1f}px (need >=15px)")

    return {"valid": len(issues) == 0, "gap": 0, "penetration": 0, "issues": issues}


def route_with_port_allocation(
    edges: List[Dict[str, Any]],
    node_map: Dict[str, Dict[str, Any]],
    ports_per_side: int = 3,
    clearance: float = 25.0,
    obstacles: Optional[List[BBox]] = None,
) -> List[Dict[str, Any]]:
    """Route all edges using multi-port allocation to avoid connection overlap.

    This is a convenience function that combines port allocation and orthogonal
    routing in a single call. Use this instead of manually calling
    allocate_ports_for_edges() + orthogonal_path() for each edge.

    The function:
    1. Allocates distinct ports on source/destination sides for each edge,
       ensuring no two edges share the same port on the same node side.
    2. Routes each edge as an orthogonal path using the allocated port positions.
    3. For parallel edges (same from→to pair), applies mid-path offsets to
       spread them visually apart.

    Each edge dict must have: 'from', 'to', 'src_side', 'dst_side'.
    Each edge will be augmented with:
        - 'src_port', 'dst_port': allocated connection points
        - 'waypoints': list of (x, y) path waypoints
        - 'path_d': SVG path 'd' attribute string

    Args:
        edges: List of edge dicts with routing info
        node_map: Dict mapping node id → node dict with 'bbox'
        ports_per_side: Number of ports to generate per side (default 3)
        clearance: Obstacle clearance in px (default 25)
        obstacles: Optional list of bboxes to avoid (defaults to all node bboxes)

    Returns:
        The same edge list, each augmented with routing data.
    """
    obstacles = obstacles or [n["bbox"] for n in node_map.values()]

    # Step 1: Allocate ports
    edges = allocate_ports_for_edges(edges, node_map, ports_per_side)

    # Step 2: Route each edge using allocated ports
    for e in edges:
        mid_offset = e.get("mid_offset")
        waypoints = orthogonal_path(
            e["src_port"],
            e["dst_port"],
            e["src_side"],
            e["dst_side"],
            clearance=clearance,
            obstacles=obstacles,
            mid_offset=mid_offset,
        )
        e["waypoints"] = waypoints
        e["path_d"] = path_to_svg_d(waypoints)

    return edges


def validate_turning_points(
    edges: List[Dict[str, Any]],
    node_bboxes: List[BBox],
    tolerance: float = 2.0,
) -> List[Dict[str, Any]]:
    """Validate that no turning point or segment aligns with any node edge.

    Checks:
    1. Turning points (non-endpoint waypoints) must not lie on any node edge.
    2. Segments must not run along a node edge (same x for vertical, same y
       for horizontal) where they overlap the node's range.

    Args:
        edges: List of edge dicts, each with 'id' and 'waypoints'
        node_bboxes: List of node bounding boxes (x, y, w, h)
        tolerance: Max distance to consider as "on the edge" (default 2)

    Returns:
        List of issue dicts: [{'edge_id': str, 'type': str, 'point': (x,y),
                               'node': int, 'side': str}, ...]
    """
    issues = []
    for e in edges:
        wps = e.get("waypoints", [])
        if len(wps) < 2:
            continue
        eid = e.get("id", "?")

        for j, (nx, ny, nw, nh) in enumerate(node_bboxes):
            left, right = nx, nx + nw
            top, bottom = ny, ny + nh

            # Check each segment for overlap with node edges
            for i in range(len(wps) - 1):
                ax, ay = wps[i]
                bx, by = wps[i + 1]
                is_horiz = abs(ay - by) < tolerance
                is_vert = abs(ax - bx) < tolerance

                if is_horiz:
                    seg_x_min, seg_x_max = min(ax, bx), max(ax, bx)
                    # Horizontal segment overlaps node top/bottom edge?
                    if (
                        abs(ay - top) <= tolerance
                        and seg_x_min < right
                        and seg_x_max > left
                    ):
                        issues.append(
                            {
                                "edge_id": eid,
                                "type": "segment-on-edge",
                                "point": ((ax + bx) / 2, ay),
                                "node": j,
                                "side": "TOP",
                                "detail": f"horiz segment at y={ay} runs along node top",
                            }
                        )
                    if (
                        abs(ay - bottom) <= tolerance
                        and seg_x_min < right
                        and seg_x_max > left
                    ):
                        issues.append(
                            {
                                "edge_id": eid,
                                "type": "segment-on-edge",
                                "point": ((ax + bx) / 2, ay),
                                "node": j,
                                "side": "BOTTOM",
                                "detail": f"horiz segment at y={ay} runs along node bottom",
                            }
                        )
                elif is_vert:
                    seg_y_min, seg_y_max = min(ay, by), max(ay, by)
                    # Vertical segment overlaps node left/right edge?
                    if (
                        abs(ax - left) <= tolerance
                        and seg_y_min < bottom
                        and seg_y_max > top
                    ):
                        issues.append(
                            {
                                "edge_id": eid,
                                "type": "segment-on-edge",
                                "point": (ax, (ay + by) / 2),
                                "node": j,
                                "side": "LEFT",
                                "detail": f"vert segment at x={ax} runs along node left",
                            }
                        )
                    if (
                        abs(ax - right) <= tolerance
                        and seg_y_min < bottom
                        and seg_y_max > top
                    ):
                        issues.append(
                            {
                                "edge_id": eid,
                                "type": "segment-on-edge",
                                "point": (ax, (ay + by) / 2),
                                "node": j,
                                "side": "RIGHT",
                                "detail": f"vert segment at x={ax} runs along node right",
                            }
                        )

            # Check turning points (not first/last waypoint)
            for i in range(1, len(wps) - 1):
                tx, ty = wps[i]
                if abs(tx - left) <= tolerance and top <= ty <= bottom:
                    issues.append(
                        {
                            "edge_id": eid,
                            "type": "turn-on-edge",
                            "point": (tx, ty),
                            "node": j,
                            "side": "LEFT",
                        }
                    )
                if abs(tx - right) <= tolerance and top <= ty <= bottom:
                    issues.append(
                        {
                            "edge_id": eid,
                            "type": "turn-on-edge",
                            "point": (tx, ty),
                            "node": j,
                            "side": "RIGHT",
                        }
                    )
                if abs(ty - top) <= tolerance and left <= tx <= right:
                    issues.append(
                        {
                            "edge_id": eid,
                            "type": "turn-on-edge",
                            "point": (tx, ty),
                            "node": j,
                            "side": "TOP",
                        }
                    )
                if abs(ty - bottom) <= tolerance and left <= tx <= right:
                    issues.append(
                        {
                            "edge_id": eid,
                            "type": "turn-on-edge",
                            "point": (tx, ty),
                            "node": j,
                            "side": "BOTTOM",
                        }
                    )
    return issues


# =========================================================================
# Auto side detection — determine src_side/dst_side from relative positions
# =========================================================================


def auto_detect_sides(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    flow_direction: str = "top-to-bottom",
) -> Tuple[str, str]:
    """Auto-detect connection sides based on relative row/col positions.

    Uses the same 8-scenario classification as the flowchart routing table:

    | Scenario | Condition | src_side | dst_side |
    |---|---|---|---|
    | SAME_COL_DOWN | src_row < dst_row, same col | bottom | top |
    | SAME_COL_UP | src_row > dst_row, same col | top | bottom |
    | SAME_ROW_RIGHT | src_col < dst_col, same row | right | left |
    | SAME_ROW_LEFT | src_col > dst_col, same row | left | right |
    | DIAG_DOWN_RIGHT | src_row < dst_row, src_col < dst_col | right | top |
    | DIAG_DOWN_LEFT | src_row < dst_row, src_col > dst_col | left | top |
    | DIAG_UP_RIGHT | src_row > dst_row, src_col < dst_col | right | bottom |
    | DIAG_UP_LEFT | src_row > dst_row, src_col > dst_col | left | bottom |

    Args:
        src_node: Source node dict with ``'row'`` and ``'col'``.
        dst_node: Destination node dict with ``'row'`` and ``'col'``.
        flow_direction: Unused (reserved); auto-detection works by position.

    Returns:
        ``(src_side, dst_side)`` — e.g. ``('bottom', 'top')`` for a
        same-column downward edge.
    """
    sr = src_node.get("row", 0)
    sc = src_node.get("col", 0)
    dr = dst_node.get("row", 0)
    dc = dst_node.get("col", 0)

    # Same column
    if sc == dc:
        if sr < dr:
            return ("bottom", "top")  # SAME_COL_DOWN
        else:
            return ("top", "bottom")  # SAME_COL_UP

    # Same row
    if sr == dr:
        if sc < dc:
            return ("right", "left")  # SAME_ROW_RIGHT
        else:
            return ("left", "right")  # SAME_ROW_LEFT

    # Diagonal
    if sr < dr:
        if sc < dc:
            return ("right", "top")  # DIAG_DOWN_RIGHT
        else:
            return ("left", "top")  # DIAG_DOWN_LEFT
    else:
        if sc < dc:
            return ("right", "bottom")  # DIAG_UP_RIGHT
        else:
            return ("left", "bottom")  # DIAG_UP_LEFT


def route_all_edges(
    edges: List[Dict[str, Any]],
    node_map: Dict[str, Dict[str, Any]],
    ports_per_side: int = 3,
    clearance: float = 25.0,
    obstacles: Optional[List[BBox]] = None,
    flow_direction: str = "top-to-bottom",
) -> List[Dict[str, Any]]:
    """Route all edges with auto-detected sides and multi-port allocation.

    This is a high-level convenience function that:
    1. Auto-detects ``src_side``/``dst_side`` for any edge where they are
       missing, using ``auto_detect_sides()`` based on relative row/col
       positions.
    2. Delegates to ``route_with_port_allocation()`` for multi-port allocation
       and orthogonal path computation.

    Each edge dict **must** have ``'from'`` and ``'to'``. If ``'src_side'``
    and/or ``'dst_side'`` are missing, they are auto-detected from the node
    positions. If present, they are respected as-is.

    Each edge will be augmented with:
        - ``src_side``, ``dst_side`` (filled in if missing)
        - ``src_port``, ``dst_port``: allocated connection points on node edges
        - ``waypoints``: list of ``(x, y)`` path waypoints
        - ``path_d``: SVG path ``'d'`` attribute string

    Args:
        edges: List of edge dicts. Each must have ``'from'`` and ``'to'``.
               May optionally have ``'src_side'`` and ``'dst_side'``.
        node_map: Dict mapping node id → node dict with ``'bbox'``,
                  ``'row'``, ``'col'``.
        ports_per_side: Number of ports to generate per node side (default 3).
        clearance: Obstacle clearance in px (default 25).
        obstacles: Optional list of bboxes to avoid (defaults to all node
                   bboxes from ``node_map``).
        flow_direction: Forward flow direction (``'top-to-bottom'`` or
                        ``'left-to-right'``).

    Returns:
        The same edge list, each augmented with routing data.

    Example::

        from routing import route_all_edges

        edges = [
            {'from': 'start', 'to': 'input'},     # sides auto-detected
            {'from': 'output', 'to': 'hil'},
            {'from': 'hil', 'to': 'ctx',          # manual override
             'src_side': 'top', 'dst_side': 'bottom'},
        ]
        node_map = {n['id']: n for n in nodes}
        edges = route_all_edges(edges, node_map)
        for e in edges:
            print(e['id'], e['path_d'])
    """
    obstacles = obstacles or [n["bbox"] for n in node_map.values()]

    # Auto-detect missing sides
    for e in edges:
        if "src_side" not in e or "dst_side" not in e:
            src = node_map.get(e["from"])
            dst = node_map.get(e["to"])
            if src is not None and dst is not None:
                ss, ds = auto_detect_sides(src, dst, flow_direction)
                e.setdefault("src_side", ss)
                e.setdefault("dst_side", ds)

    # Delegate to route_with_port_allocation
    return route_with_port_allocation(
        edges,
        node_map,
        ports_per_side=ports_per_side,
        clearance=clearance,
        obstacles=obstacles,
    )


# =========================================================================
# Flowchart scenario classification (16-scenario edge routing)
# =========================================================================
# 8 base scenarios: SAME_COL_DOWN/UP, SAME_ROW_RIGHT/LEFT,
#                    DIAG_DOWN_RIGHT/LEFT, DIAG_UP_RIGHT/LEFT
# Obstacle-aware variants: same scenarios but path selection detects
# intermediate nodes and upgrades straight→Z for collinear edges,
# or L1→L2→Z for diagonal edges.


def classify_edge(src_node: Dict[str, Any], dst_node: Dict[str, Any]) -> str:
    """Classify edge into one of 8 spatial scenarios by row/col position.

    Returns: SAME_ROW_RIGHT, SAME_ROW_LEFT, SAME_COL_DOWN, SAME_COL_UP,
             DIAG_DOWN_RIGHT, DIAG_DOWN_LEFT, DIAG_UP_RIGHT, DIAG_UP_LEFT.
    Obstacle detection is handled by generate_candidates() which detects
    intermediate nodes and upgrades the path from straight→Z (for same-col/row)
    or L1→L2→Z (for diagonal) as needed.
    """
    sr, sc = src_node["row"], src_node["col"]
    dr, dc = dst_node["row"], dst_node["col"]
    if sr == dr:
        return "SAME_ROW_RIGHT" if sc < dc else "SAME_ROW_LEFT"
    if sc == dc:
        return "SAME_COL_DOWN" if sr < dr else "SAME_COL_UP"
    if sr < dr:
        return "DIAG_DOWN_RIGHT" if sc < dc else "DIAG_DOWN_LEFT"
    return "DIAG_UP_RIGHT" if sc < dc else "DIAG_UP_LEFT"


# =========================================================================
# Obstacle detection for orthogonal path segments
# =========================================================================


def segment_intersects_element(
    seg_start: Point, seg_end: Point, elem_bbox: BBox
) -> bool:
    """Check if a horizontal/vertical segment crosses a node interior."""
    x, y, w, h = elem_bbox
    sx1, sy1 = seg_start
    sx2, sy2 = seg_end

    if abs(sy1 - sy2) < 1e-6:  # Horizontal
        if sy1 < y or sy1 > y + h:
            return False
        return max(min(sx1, sx2), x) < min(max(sx1, sx2), x + w)
    else:  # Vertical
        if sx1 < x or sx1 > x + w:
            return False
        return max(min(sy1, sy2), y) < min(max(sy1, sy2), y + h)


# =========================================================================
# Scenario path builders
# =========================================================================


def build_straight_path(
    src_node: Dict[str, Any], dst_node: Dict[str, Any], scenario: str
) -> List[Point]:
    """0-turn straight path for same-row/same-col scenarios.

    Uses ``connection_point()`` for consistent exit/entry point calculation.
    If element centers don't align (e.g., different-width elements in the same
    column), inserts a single turn to guarantee an orthogonal path.

    Note: `_detect_intermediate_nodes()` is called before this function;
    this path is only used when no obstacles block the straight line.
    """
    side_map = {
        "SAME_COL_DOWN": ("bottom", "top"),
        "SAME_COL_UP": ("top", "bottom"),
        "SAME_ROW_RIGHT": ("right", "left"),
        "SAME_ROW_LEFT": ("left", "right"),
    }
    src_side, dst_side = side_map[scenario]
    src_pt = connection_point(src_node["bbox"], src_side)
    dst_pt = connection_point(dst_node["bbox"], dst_side)

    # Ensure orthogonal: if centers align → 0-turn straight line
    sx, sy = src_pt
    dx, dy = dst_pt
    if abs(sx - dx) < 1e-6 or abs(sy - dy) < 1e-6:
        return [src_pt, dst_pt]
    # Centers misaligned → insert L-turn to guarantee orthogonality
    return [src_pt, (sx, dy), dst_pt]


def _select_sub_port(
    bbox: BBox, side: str, target_center: Point, ports_per_side: int = 3
) -> Point:
    """Select the optimal sub-port on a given side, biased toward target_center.

    Uses ``get_side_ports()`` to generate N evenly distributed ports, then
    ``find_closest_port()`` to pick the one closest to the target. This
    implements the sub-point selection logic from flowchart.md §3.4/§4.2.
    """
    ports = get_side_ports(bbox, side, ports_per_side)
    idx = find_closest_port(ports, target_center, set(), prefer_side=side)
    return ports[idx]


def build_L1_path(
    src_node: Dict[str, Any], dst_node: Dict[str, Any], scenario: str
) -> List[Point]:
    """Primary L-shaped (1-turn) path for diagonals.

    Uses sub-port selection biased toward the target node for optimal
    exit/entry points (§3.4/§4.2 of flowchart.md). For DIAG_DOWN_RIGHT,
    this naturally picks R-B + T-R (both biased toward the target corner).
    """
    sp = {
        "DIAG_DOWN_RIGHT": "right",
        "DIAG_DOWN_LEFT": "left",
        "DIAG_UP_RIGHT": "right",
        "DIAG_UP_LEFT": "left",
    }[scenario]
    dp = {
        "DIAG_DOWN_RIGHT": "top",
        "DIAG_DOWN_LEFT": "top",
        "DIAG_UP_RIGHT": "bottom",
        "DIAG_UP_LEFT": "bottom",
    }[scenario]

    dst_center = center(dst_node["bbox"])
    src_center = center(src_node["bbox"])

    src_exit = _select_sub_port(src_node["bbox"], sp, dst_center)
    dst_entry = _select_sub_port(dst_node["bbox"], dp, src_center)
    mid_x = dst_node["x"] + dst_node["width"] / 2
    mid_y = src_node["y"] + src_node["height"] / 2
    return [src_exit, (mid_x, mid_y), dst_entry]


def build_L2_path(
    src_node: Dict[str, Any], dst_node: Dict[str, Any], scenario: str
) -> List[Point]:
    """Alternate L-shaped (1-turn) path for diagonals.

    Uses sub-port selection biased toward the target node for optimal
    exit/entry points (§3.4/§4.2 of flowchart.md). For DIAG_DOWN_RIGHT,
    this naturally picks B-R + L-T (both biased toward the target corner).
    """
    sp = {
        "DIAG_DOWN_RIGHT": "bottom",
        "DIAG_DOWN_LEFT": "bottom",
        "DIAG_UP_RIGHT": "top",
        "DIAG_UP_LEFT": "top",
    }[scenario]
    dp = {
        "DIAG_DOWN_RIGHT": "left",
        "DIAG_DOWN_LEFT": "right",
        "DIAG_UP_RIGHT": "left",
        "DIAG_UP_LEFT": "right",
    }[scenario]

    dst_center = center(dst_node["bbox"])
    src_center = center(src_node["bbox"])

    src_exit = _select_sub_port(src_node["bbox"], sp, dst_center)
    dst_entry = _select_sub_port(dst_node["bbox"], dp, src_center)
    mid_x = src_node["x"] + src_node["width"] / 2
    mid_y = dst_node["y"] + dst_node["height"] / 2
    return [src_exit, (mid_x, mid_y), dst_entry]


def _find_blocking_boundary(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    all_nodes: List[Dict[str, Any]],
) -> Dict[str, float]:
    """Compute the combined boundary of all nodes between src and dst.

    Returns a dict with 'left', 'right', 'top', 'bottom' of the bounding
    box that encloses all intermediate nodes. This handles multiple-obstacle
    scenarios (flowchart.md \\u00a74.4).
    """
    between = _detect_intermediate_nodes(src_node, dst_node, all_nodes)
    if not between:
        return {}
    return {
        "left": min(n["x"] for n in between),
        "right": max(n["x"] + n["width"] for n in between),
        "top": min(n["y"] for n in between),
        "bottom": max(n["y"] + n["height"] for n in between),
    }


def build_Z_path(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    scenario: str,
    all_nodes: List[Dict[str, Any]],
    margin: float = 30,
) -> Optional[List[Point]]:
    """Z-shaped (2-turn) path navigating around obstacles.

    Handles multiple obstacles by computing the combined boundary of all
    intermediate nodes (flowchart.md \\u00a74.4). Uses sub-port selection
    for optimal exit/entry points.

    For DIAG_DOWN_RIGHT: extends right past obstacles, then down.
    For DIAG_DOWN_LEFT:  extends left past obstacles, then down.
    """
    sc = center(src_node["bbox"])
    dc = center(dst_node["bbox"])
    dst_center = center(dst_node["bbox"])
    src_center = center(src_node["bbox"])

    obs_boundary = _find_blocking_boundary(src_node, dst_node, all_nodes)
    if not obs_boundary:
        return None

    if scenario == "DIAG_DOWN_RIGHT":
        # Z1: right-bypass → A.R → (ex, cy_A) → (ex, cy_B) → B.T
        if obs_boundary["right"] > sc[0]:
            ex = obs_boundary["right"] + margin
            return [
                _select_sub_port(src_node["bbox"], "right", dst_center),
                (ex, sc[1]),
                (ex, dc[1]),
                _select_sub_port(dst_node["bbox"], "top", src_center),
            ]
        # Z2: bottom-bypass → A.B → (cx_A, ey) → (cx_B, ey) → B.T
        ey = obs_boundary["bottom"] + margin
        return [
            _select_sub_port(src_node["bbox"], "bottom", dst_center),
            (sc[0], ey),
            (dc[0], ey),
            _select_sub_port(dst_node["bbox"], "top", src_center),
        ]

    elif scenario == "DIAG_DOWN_LEFT":
        # Z1: left-bypass → A.L → (ex, cy_A) → (ex, cy_B) → B.T
        if obs_boundary["left"] < sc[0]:
            ex = obs_boundary["left"] - margin
            return [
                _select_sub_port(src_node["bbox"], "left", dst_center),
                (ex, sc[1]),
                (ex, dc[1]),
                _select_sub_port(dst_node["bbox"], "top", src_center),
            ]
        # Z2: bottom-bypass → A.B → (cx_A, ey) → (cx_B, ey) → B.T
        ey = obs_boundary["bottom"] + margin
        return [
            _select_sub_port(src_node["bbox"], "bottom", dst_center),
            (sc[0], ey),
            (dc[0], ey),
            _select_sub_port(dst_node["bbox"], "top", src_center),
        ]

    elif scenario == "DIAG_UP_RIGHT":
        # Z1: right-bypass → A.R → (ex, cy_A) → (ex, cy_B) → B.B
        if obs_boundary["right"] > sc[0]:
            ex = obs_boundary["right"] + margin
            return [
                _select_sub_port(src_node["bbox"], "right", dst_center),
                (ex, sc[1]),
                (ex, dc[1]),
                _select_sub_port(dst_node["bbox"], "bottom", src_center),
            ]
        # Z2: top-bypass → A.T → (cx_A, ey) → (cx_B, ey) → B.B
        ey = obs_boundary["top"] - margin
        return [
            _select_sub_port(src_node["bbox"], "top", dst_center),
            (sc[0], ey),
            (dc[0], ey),
            _select_sub_port(dst_node["bbox"], "bottom", src_center),
        ]

    elif scenario == "DIAG_UP_LEFT":
        # Z1: left-bypass → A.L → (ex, cy_A) → (ex, cy_B) → B.B
        if obs_boundary["left"] < sc[0]:
            ex = obs_boundary["left"] - margin
            return [
                _select_sub_port(src_node["bbox"], "left", dst_center),
                (ex, sc[1]),
                (ex, dc[1]),
                _select_sub_port(dst_node["bbox"], "bottom", src_center),
            ]
        # Z2: top-bypass → A.T → (cx_A, ey) → (cx_B, ey) → B.B
        ey = obs_boundary["top"] - margin
        return [
            _select_sub_port(src_node["bbox"], "top", dst_center),
            (sc[0], ey),
            (dc[0], ey),
            _select_sub_port(dst_node["bbox"], "bottom", src_center),
        ]

    return None


def build_perimeter_path(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    all_nodes: List[Dict[str, Any]],
    margin: float = 40,
) -> List[Point]:
    """Fallback path routing around the perimeter of all nodes.

    Uses auto-detected sides to determine exit/entry orientation, and routes
    around the right side of the overall bounding box by default.
    Uses sub-port selection for optimal connection points.
    """
    from geometry import union_bbox

    all_bboxes = [n["bbox"] for n in all_nodes]
    ux, uy, uw, uh = union_bbox(all_bboxes)
    dst_center = center(dst_node["bbox"])

    # Auto-detect exit side from src, defaulting to right
    src_side, _ = auto_detect_sides(src_node, dst_node)
    src_exit = _select_sub_port(src_node["bbox"], src_side, dst_center)
    px = ux + uw + margin
    # Enter the destination from the best side for a perimeter approach
    _, dst_side = auto_detect_sides(src_node, dst_node)
    dst_entry = _select_sub_port(dst_node["bbox"], dst_side, center(src_node["bbox"]))
    return [src_exit, (px, src_exit[1]), (px, dst_entry[1]), dst_entry]


# =========================================================================
# Path selection
# =========================================================================


def _detect_intermediate_nodes(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    all_nodes: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Return all nodes strictly between src and dst in the grid."""
    between: List[Dict[str, Any]] = []
    sr, sc_ = src_node["row"], src_node["col"]
    dr, dc = dst_node["row"], dst_node["col"]
    min_r, max_r = min(sr, dr), max(sr, dr)
    min_c, max_c = min(sc_, dc), max(sc_, dc)
    for n in all_nodes:
        if n["id"] in (src_node["id"], dst_node["id"]):
            continue
        if min_r <= n["row"] <= max_r and min_c <= n["col"] <= max_c:
            between.append(n)
    return between


def build_Z_path_for_straight(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    scenario: str,
    all_nodes: List[Dict[str, Any]],
    margin: float = 30,
    bypass_above: bool = False,
) -> Optional[List[Point]]:
    """Z-shaped (2-turn) path for straight-line scenarios blocked by obstacles.

    Entry principle: approach from the bypass side, enter B from that same side
    so the line never crosses B's body. Uses sub-port selection for optimal
    exit/entry points.

    Same-column scenarios (SAME_COL_DOWN/UP):
      - Right-bypass (default): exit from RIGHT, route right of obstacles,
        enter B from RIGHT side.
      - Left-bypass (use bypass_above=True): exit from LEFT, route left of
        obstacles, enter B from LEFT side.

    Same-row scenarios (SAME_ROW_RIGHT/LEFT):
      - Below-bypass (default): exit from BOTTOM, route below obstacles,
        enter B from TOP side (approach from below, go up into B's top edge).
      - Above-bypass (use bypass_above=True): exit from TOP, route above
        obstacles, enter B from TOP side (approach from above, go down into
        B's top edge).
    """
    sc = center(src_node["bbox"])
    dc = center(dst_node["bbox"])
    dst_center = center(dst_node["bbox"])
    src_center = center(src_node["bbox"])
    intermediates = _detect_intermediate_nodes(src_node, dst_node, all_nodes)
    if not intermediates:
        return None

    if scenario in ("SAME_COL_DOWN", "SAME_COL_UP"):
        # Column scenarios: bypass right (default) or left
        if not bypass_above:
            # Right-bypass: exit RIGHT → enter B from RIGHT
            obs_right_x = max(n["x"] + n["width"] for n in intermediates)
            ex = obs_right_x + margin
            return [
                _select_sub_port(src_node["bbox"], "right", dst_center),
                (ex, sc[1]),
                (ex, dc[1]),
                _select_sub_port(dst_node["bbox"], "right", src_center),
            ]
        else:
            # Left-bypass: exit LEFT → enter B from LEFT
            obs_left_x = min(n["x"] for n in intermediates)
            ex = obs_left_x - margin
            return [
                _select_sub_port(src_node["bbox"], "left", dst_center),
                (ex, sc[1]),
                (ex, dc[1]),
                _select_sub_port(dst_node["bbox"], "left", src_center),
            ]

    else:  # SAME_ROW_RIGHT, SAME_ROW_LEFT
        if not bypass_above:
            # Below-bypass: exit BOTTOM → approach from below → enter B from TOP
            obs_bottom_y = max(n["y"] + n["height"] for n in intermediates)
            ey = obs_bottom_y + margin
            return [
                _select_sub_port(src_node["bbox"], "bottom", dst_center),
                (sc[0], ey),
                (dc[0], ey),
                _select_sub_port(dst_node["bbox"], "top", src_center),
            ]
        else:
            # Above-bypass: exit TOP → approach from above → enter B from TOP
            obs_top_y = min(n["y"] for n in intermediates)
            ey = obs_top_y - margin
            return [
                _select_sub_port(src_node["bbox"], "top", dst_center),
                (sc[0], ey),
                (dc[0], ey),
                _select_sub_port(dst_node["bbox"], "top", src_center),
            ]


def generate_candidates(
    scenario: str,
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    all_nodes: List[Dict[str, Any]],
) -> List[Tuple[List[Point], int]]:
    """Generate candidate paths in priority order.

    Obstacle-aware: for straight-line scenarios (same-col/row),
    detects intermediate nodes and upgrades straight→Z when blocked.
    For diagonal scenarios, upgrades L1→L2→Z when blocked.

    Returns list of (waypoints, turn_count) from best to worst priority.
    """
    cand: List[Tuple[List[Point], int]] = []

    if scenario in ("SAME_COL_DOWN", "SAME_COL_UP", "SAME_ROW_RIGHT", "SAME_ROW_LEFT"):
        # Check if straight path is blocked by intermediate nodes
        straight = build_straight_path(src_node, dst_node, scenario)
        has_intermediate = False
        for n in all_nodes:
            if n["id"] in (src_node["id"], dst_node["id"]):
                continue
            for i in range(len(straight) - 1):
                if segment_intersects_element(straight[i], straight[i + 1], n["bbox"]):
                    has_intermediate = True
                    break
            if has_intermediate:
                break

        if not has_intermediate:
            # No obstacle → straight path (0 turns)
            cand.append((straight, 0))
        else:
            # Obstacle detected → skip L-shape, go directly to Z-shape
            # (1-turn path can't resolve collinear obstacle blocking)
            # Generate both Z1 (right/below) and Z2 (left/above) bypasses
            z1 = build_Z_path_for_straight(
                src_node, dst_node, scenario, all_nodes, bypass_above=False
            )
            if z1:
                cand.append((z1, 1))
            z2 = build_Z_path_for_straight(
                src_node, dst_node, scenario, all_nodes, bypass_above=True
            )
            if z2:
                cand.append((z2, 1))

    if scenario in (
        "DIAG_DOWN_RIGHT",
        "DIAG_DOWN_LEFT",
        "DIAG_UP_RIGHT",
        "DIAG_UP_LEFT",
    ):
        cand.append((build_L1_path(src_node, dst_node, scenario), 1))
        cand.append((build_L2_path(src_node, dst_node, scenario), 1))

    z = build_Z_path(src_node, dst_node, scenario, all_nodes)
    if z:
        cand.append((z, 2))

    cand.append((build_perimeter_path(src_node, dst_node, all_nodes), 3))
    return cand


def select_best_path(
    candidates: List[Tuple[List[Point], int]],
    all_nodes: List[Dict[str, Any]],
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    placed_edges: Optional[List[Dict[str, Any]]] = None,
) -> Optional[List[Point]]:
    """Score candidates and return the best path.

    Scoring: element obstacle → DISQUALIFIED; then turn_count×100 + overlaps.
    Returns None if all candidates are blocked.
    """
    placed_edges = placed_edges or []
    scored = []

    for path, turns in candidates:
        has_obs = False
        for node in all_nodes:
            if node["id"] in (src_node["id"], dst_node["id"]):
                continue
            for i in range(len(path) - 1):
                if segment_intersects_element(path[i], path[i + 1], node["bbox"]):
                    has_obs = True
                    break
            if has_obs:
                break
        if has_obs:
            continue

        oc = _count_parallel_overlaps(path, placed_edges)
        scored.append((path, turns * 100 + oc))

    if not scored:
        return None
    scored.sort(key=lambda x: x[1])
    return scored[0][0]


# =========================================================================
# Parallel overlap detection & tracking
# =========================================================================


def _ranges_overlap(a1: float, a2: float, b1: float, b2: float) -> bool:
    """Check if two ranges [a1,a2] and [b1,b2] overlap."""
    return max(a1, b1) < min(a2, b2)


_LANE_TOLERANCE = 5.0  # px — near-miss lanes within this distance count as overlaps


def _count_parallel_overlaps(
    path: List[Point], placed_edges: List[Dict[str, Any]]
) -> int:
    """Count how many segments in path overlap in parallel with placed edges.

    Uses ``_LANE_TOLERANCE`` to catch near-miss lanes (flowchart.md \\u00a75.7.1):
    segments running within 5px of an existing lane are counted as overlaps,
    encouraging the path selector to choose clearly separated lanes instead.
    """
    count = 0
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        is_h = abs(y1 - y2) < 1e-6
        for edge in placed_edges:
            for seg in edge.get("_segments", []):
                if (
                    is_h
                    and seg.get("is_horizontal")
                    and abs(seg["y"] - y1) < _LANE_TOLERANCE
                ):
                    if _ranges_overlap(
                        min(x1, x2), max(x1, x2), seg["x_min"], seg["x_max"]
                    ):
                        count += 1
                elif (
                    not is_h
                    and not seg.get("is_horizontal")
                    and abs(seg["x"] - x1) < _LANE_TOLERANCE
                ):
                    if _ranges_overlap(
                        min(y1, y2), max(y1, y2), seg["y_min"], seg["y_max"]
                    ):
                        count += 1
    return count


class OccupiedLanes:
    """Track placed edge segments for parallel overlap detection."""

    def __init__(self) -> None:
        self.horizontal: List[Dict[str, Any]] = []
        self.vertical: List[Dict[str, Any]] = []

    def register(self, edge: Dict[str, Any]) -> None:
        """Register an edge's segments from its waypoints."""
        wps = edge.get("waypoints", [])
        for i in range(len(wps) - 1):
            x1, y1 = wps[i]
            x2, y2 = wps[i + 1]
            if abs(y1 - y2) < 1e-6:
                self.horizontal.append(
                    {
                        "y": y1,
                        "x_min": min(x1, x2),
                        "x_max": max(x1, x2),
                        "edge_id": edge.get("id", "?"),
                    }
                )
            else:
                self.vertical.append(
                    {
                        "x": x1,
                        "y_min": min(y1, y2),
                        "y_max": max(y1, y2),
                        "edge_id": edge.get("id", "?"),
                    }
                )


def compute_segments(waypoints: List[Point]) -> List[Dict[str, Any]]:
    """Convert waypoints to segment dicts for overlap tracking."""
    segs: List[Dict[str, Any]] = []
    for i in range(len(waypoints) - 1):
        x1, y1 = waypoints[i]
        x2, y2 = waypoints[i + 1]
        is_h = abs(y1 - y2) < 1e-6
        segs.append(
            {
                "is_horizontal": is_h,
                "y": y1 if is_h else None,
                "x": x1 if not is_h else None,
                "x_min": min(x1, x2) if is_h else None,
                "x_max": max(x1, x2) if is_h else None,
                "y_min": min(y1, y2) if not is_h else None,
                "y_max": max(y1, y2) if not is_h else None,
            }
        )
    return segs
