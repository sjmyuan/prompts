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
    src_bbox: BBox, dst_bbox: BBox, flow_direction: str = "top-to-bottom"
) -> Tuple[Point, Point, str, str]:
    """Determine the best connection endpoints between two shape bounding boxes.

    Returns:
        (src_point, dst_point, src_side, dst_side)
    """
    src_cx, src_cy = center(src_bbox)
    dst_cx, dst_cy = center(dst_bbox)
    sx, sy, sw, sh = src_bbox
    dx, dy, dw, dh = dst_bbox

    if flow_direction == "top-to-bottom":
        # Default: source bottom-center → target top-center
        src_pt = connection_point(src_bbox, "bottom")
        dst_pt = connection_point(dst_bbox, "top")
        return src_pt, dst_pt, "bottom", "top"

    elif flow_direction == "left-to-right":
        src_pt = connection_point(src_bbox, "right")
        dst_pt = connection_point(dst_bbox, "left")
        return src_pt, dst_pt, "right", "left"

    else:
        # Auto-detect based on relative positions
        dx_center = dst_cx - src_cx
        dy_center = dst_cy - src_cy

        if abs(dx_center) >= abs(dy_center):
            if dx_center > 0:
                return (
                    connection_point(src_bbox, "right"),
                    connection_point(dst_bbox, "left"),
                    "right",
                    "left",
                )
            else:
                return (
                    connection_point(src_bbox, "left"),
                    connection_point(dst_bbox, "right"),
                    "left",
                    "right",
                )
        else:
            if dy_center > 0:
                return (
                    connection_point(src_bbox, "bottom"),
                    connection_point(dst_bbox, "top"),
                    "bottom",
                    "top",
                )
            else:
                return (
                    connection_point(src_bbox, "top"),
                    connection_point(dst_bbox, "bottom"),
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
    ignore_shared_endpoints: bool = True,
) -> List[Dict[str, Any]]:
    """Detect all line-line and line-shape intersections.

    Args:
        connections: List of connection paths, each is a list of waypoints
        shape_bboxes: Bounding boxes of all shapes on the canvas
        ignore_shared_endpoints: If True, don't flag intersections at shared endpoints

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


def shortest_straight_segment(waypoints: List[Point]) -> int:
    """Return the index of the shortest straight segment in a path."""
    if len(waypoints) < 2:
        return -1
    min_dist = float("inf")
    min_idx = 0
    for i in range(len(waypoints) - 1):
        d = distance(waypoints[i], waypoints[i + 1])
        if d < min_dist:
            min_dist = d
            min_idx = i
    return min_idx


def longest_straight_segment(waypoints: List[Point]) -> int:
    """Return the index of the longest straight segment in a path."""
    if len(waypoints) < 2:
        return -1
    max_dist = -1.0
    max_idx = 0
    for i in range(len(waypoints) - 1):
        d = distance(waypoints[i], waypoints[i + 1])
        if d > max_dist:
            max_dist = d
            max_idx = i
    return max_idx


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
