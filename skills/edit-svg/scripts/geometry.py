"""
Geometry utilities for SVG diagram layout calculations.

All coordinates use SVG coordinate system (y increases downward).
Bounding boxes are represented as (x, y, width, height).
Points are (x, y) tuples.
"""

import math
from typing import Tuple, List, Optional, Dict, Any

# Type aliases
BBox = Tuple[float, float, float, float]  # (x, y, w, h)
Point = Tuple[float, float]  # (x, y)
Rect = Tuple[float, float, float, float]  # (x1, y1, x2, y2) inclusive


def bbox_to_rect(bbox: BBox) -> Rect:
    """Convert (x, y, w, h) to (x1, y1, x2, y2)."""
    x, y, w, h = bbox
    return (x, y, x + w, y + h)


def rect_to_bbox(rect: Rect) -> BBox:
    """Convert (x1, y1, x2, y2) to (x, y, w, h)."""
    x1, y1, x2, y2 = rect
    return (x1, y1, x2 - x1, y2 - y1)


def center(bbox: BBox) -> Point:
    """Return center point of a bounding box."""
    x, y, w, h = bbox
    return (x + w / 2.0, y + h / 2.0)


def overlap(bbox1: BBox, bbox2: BBox) -> bool:
    """Check if two bounding boxes overlap (including touching edges)."""
    r1 = bbox_to_rect(bbox1)
    r2 = bbox_to_rect(bbox2)
    return not (r1[2] < r2[0] or r2[2] < r1[0] or r1[3] < r2[1] or r2[3] < r1[1])


def overlap_with_margin(bbox1: BBox, bbox2: BBox, margin: float = 0.0) -> bool:
    """Check if two bounding boxes overlap, with an optional margin added to bbox2."""
    r1 = bbox_to_rect(bbox1)
    r2 = bbox_to_rect(bbox2)
    return not (
        r1[2] + margin < r2[0] - margin
        or r2[2] + margin < r1[0] - margin
        or r1[3] + margin < r2[1] - margin
        or r2[3] + margin < r1[1] - margin
    )


def find_overlapping(
    existing_bboxes: List[BBox], new_bbox: BBox, margin: float = 0.0
) -> List[int]:
    """Return indices of existing bboxes that overlap with new_bbox."""
    return [
        i
        for i, bb in enumerate(existing_bboxes)
        if overlap_with_margin(bb, new_bbox, margin)
    ]


def cjk_len(text: str) -> int:
    """Compute effective length of text counting CJK chars as double width."""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in text)


def distance(p1: Point, p2: Point) -> float:
    """Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def manhattan_distance(p1: Point, p2: Point) -> float:
    """Manhattan distance between two points."""
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def connection_point(bbox: BBox, side: str) -> Point:
    """Return the anchor connection point on a given side of the bounding box.

    Args:
        bbox: (x, y, w, h)
        side: 'top', 'bottom', 'left', 'right', 'center', or a vertex:
              'top-left', 'top-right', 'bottom-left', 'bottom-right'

    Returns:
        (x, y) point on the specified edge/side.
    """
    x, y, w, h = bbox
    cx, cy = center(bbox)

    side_map = {
        "top": (cx, y),
        "bottom": (cx, y + h),
        "left": (x, cy),
        "right": (x + w, cy),
        "center": (cx, cy),
        "top-left": (x, y),
        "top-right": (x + w, y),
        "bottom-left": (x, y + h),
        "bottom-right": (x + w, y + h),
    }
    if side not in side_map:
        raise ValueError(f"Unknown side: {side}. Valid: {list(side_map.keys())}")
    return side_map[side]


# ---------------------------------------------------------------------------
# Multi-port connection point allocation
# ---------------------------------------------------------------------------


def get_side_ports(bbox: BBox, side: str, count: int = 3) -> List[Point]:
    """Return N evenly distributed connection ports on a given edge of a bounding box.

    Ports are inset from corners using (i+1)/(count+1) distribution, matching
    the 25%/50%/75% positions described in the flowchart algorithm (flowchart.md
    \u00a73.2). This avoids placing ports at element corners (where they would
    visually overlap with border lines).

    For count=3, ports are at 25%, 50%, 75% of the edge length.
    For count=1, the single port is at 50% (center) of the edge.

    Args:
        bbox: (x, y, w, h)
        side: 'top', 'bottom', 'left', 'right'
        count: Number of ports to distribute (default 3). Must be >= 1.

    Returns:
        List of (x, y) port points, ordered from left/top to right/bottom.
    """
    x, y, w, h = bbox
    count = max(1, count)
    ports: List[Point] = []

    if side == "top":
        for i in range(count):
            frac = (i + 1) / (count + 1)
            ports.append((x + w * frac, y))
    elif side == "bottom":
        for i in range(count):
            frac = (i + 1) / (count + 1)
            ports.append((x + w * frac, y + h))
    elif side == "left":
        for i in range(count):
            frac = (i + 1) / (count + 1)
            ports.append((x, y + h * frac))
    elif side == "right":
        for i in range(count):
            frac = (i + 1) / (count + 1)
            ports.append((x + w, y + h * frac))
    else:
        raise ValueError(f"Unknown side for ports: {side}")

    return ports


def find_closest_port(
    ports: List[Point],
    target_point: Point,
    used_indices: set,
    prefer_side: Optional[str] = None,
) -> int:
    """Find the closest unused port index to a target point.

    Among all unused ports, returns the index of the port closest to
    target_point. The prefer_side hint biases selection: for 'left'/'right'
    sides, ports closer to the target's y-coordinate are preferred (minimizing
    vertical turns); for 'top'/'bottom' sides, ports closer to the target's
    x-coordinate are preferred (minimizing horizontal turns).

    Args:
        ports: List of port (x, y) points
        target_point: (x, y) reference point (typically the other endpoint)
        used_indices: Set of already-allocated port indices
        prefer_side: Optional side hint to minimize turning points:
                     'left'/'right' → prefer y-aligned ports
                     'top'/'bottom' → prefer x-aligned ports
                     None → use pure Euclidean distance

    Returns:
        Index of the closest unused port.
    """
    candidates = [i for i in range(len(ports)) if i not in used_indices]
    if not candidates:
        raise RuntimeError("All ports on this side are already allocated")

    tx, ty = target_point

    def _port_cost(idx: int) -> float:
        px, py = ports[idx]
        if prefer_side in ("left", "right"):
            # Prefer ports whose y is closest to target y (horizontal alignment)
            return abs(py - ty) + abs(px - tx) * 0.1
        elif prefer_side in ("top", "bottom"):
            # Prefer ports whose x is closest to target x (vertical alignment)
            return abs(px - tx) + abs(py - ty) * 0.1
        else:
            return math.hypot(px - tx, py - ty)

    return min(candidates, key=_port_cost)


def allocate_ports_for_edges(
    edges: List[Dict[str, Any]],
    node_map: Dict[str, Dict[str, Any]],
    ports_per_side: int = 3,
) -> List[Dict[str, Any]]:
    """Allocate connection ports for all edges to minimize overlap.

    Each edge dict must have: 'from', 'to', 'src_side', 'dst_side'.
    Each edge dict will be updated with 'src_port' and 'dst_port' (x, y points).

    Port allocation rules:
    1. Each port can be used by at most one edge (per node per side).
    2. An edge picks the closest unused port on the source side to the target,
       and the closest unused port on the destination side to the source.
    3. Ports are distributed evenly along each edge: ports[0] and ports[-1]
       are at the edge ends, interior ports are evenly spaced.
    4. For multi-edge feedback (same source & destination), offsets are applied
       to the second+ edges to split them vertically/horizontally.

    Args:
        edges: List of edge dicts with 'from', 'to', 'src_side', 'dst_side'
        node_map: Dict mapping node id → node dict with 'bbox'
        ports_per_side: Number of ports to generate per side (default 3)

    Returns:
        The same edge list, each augmented with 'src_port', 'dst_port' (Point).
    """
    # Track used ports per (node_id, side)
    used_ports: Dict[str, Dict[str, set]] = {}

    def _get_used(node_id: str, side: str) -> set:
        return used_ports.setdefault(node_id, {}).setdefault(side, set())

    # Group edges by (from_node, to_node) pairs to detect parallel feedback
    pair_groups: Dict[Tuple[str, str], List[int]] = {}
    for i, e in enumerate(edges):
        pair_groups.setdefault((e["from"], e["to"]), []).append(i)

    # Count how many edges share the same ordered pair
    pair_counts: Dict[Tuple[str, str], int] = {
        pair: len(indices) for pair, indices in pair_groups.items()
    }

    for i, e in enumerate(edges):
        src_id = e["from"]
        dst_id = e["to"]
        src_side = e.get("src_side", "bottom")
        dst_side = e.get("dst_side", "top")

        src_node = node_map[src_id]
        dst_node = node_map[dst_id]

        # Get all ports
        src_ports = get_side_ports(src_node["bbox"], src_side, ports_per_side)
        dst_ports = get_side_ports(dst_node["bbox"], dst_side, ports_per_side)

        # Determine target reference points for closest-port selection
        # Source port should be close to the destination (minimize path length)
        dst_center = center(dst_node["bbox"])
        src_center = center(src_node["bbox"])

        # Allocate source port: closest unused to destination center
        src_used = _get_used(src_id, src_side)
        src_idx = find_closest_port(
            src_ports, dst_center, src_used, prefer_side=src_side
        )
        src_used.add(src_idx)

        # Allocate destination port: closest unused to source center
        dst_used = _get_used(dst_id, dst_side)
        dst_idx = find_closest_port(
            dst_ports, src_center, dst_used, prefer_side=dst_side
        )
        dst_used.add(dst_idx)

        e["src_port"] = src_ports[src_idx]
        e["dst_port"] = dst_ports[dst_idx]
        e["src_port_idx"] = src_idx
        e["dst_port_idx"] = dst_idx

        # Handle parallel edges (same from→to): offset intermediate edges
        pair_key = (src_id, dst_id)
        pair_indices = pair_groups[pair_key]
        if len(pair_indices) > 1:
            offset_count = len(pair_indices)
            pair_pos = pair_indices.index(i)
            # Offset the middle segments of parallel edges
            # Determine offset direction based on sides
            if src_side in ("bottom", "top"):
                # Vertical exit/entry → offset horizontally
                total_offset = (pair_pos - (offset_count - 1) / 2.0) * 20.0
                e["mid_offset"] = (total_offset, 0.0)
            else:
                # Horizontal exit/entry → offset vertically
                total_offset = (pair_pos - (offset_count - 1) / 2.0) * 20.0
                e["mid_offset"] = (0.0, total_offset)

    return edges


def closest_edge_point(bbox: BBox, target_point: Point) -> Point:
    """Find the closest point on the edges of bbox to target_point.

    Projects the target point onto each of the four edges and returns
    the projected point with the smallest Euclidean distance.
    """
    x, y, w, h = bbox
    tx, ty = target_point

    candidates = [
        (tx, y),  # top edge (clamped horizontally)
        (tx, y + h),  # bottom edge
        (x, ty),  # left edge (clamped vertically)
        (x + w, ty),  # right edge
    ]
    # Clamp each candidate to the extent of its edge
    candidates[0] = (max(x, min(tx, x + w)), y)
    candidates[1] = (max(x, min(tx, x + w)), y + h)
    candidates[2] = (x, max(y, min(ty, y + h)))
    candidates[3] = (x + w, max(y, min(ty, y + h)))

    return min(candidates, key=lambda pt: (pt[0] - tx) ** 2 + (pt[1] - ty) ** 2)


def segment_line_intersection(
    p1: Point, p2: Point, p3: Point, p4: Point
) -> Optional[Point]:
    """Check if line segment p1-p2 intersects line segment p3-p4.

    Returns the intersection point if they intersect, None otherwise.
    Ignores degenerate (shared endpoint) intersections.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-10:
        return None  # Parallel or coincident

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

    # Check if intersection is within both segments (not at endpoints)
    eps = 1e-3
    if eps < t < 1.0 - eps and eps < u < 1.0 - eps:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        return (ix, iy)
    return None


def segment_rect_intersection(p1: Point, p2: Point, bbox: BBox) -> bool:
    """Check if line segment p1-p2 intersects the interior of a bounding box."""
    x, y, w, h = bbox
    rect = bbox_to_rect(bbox)

    # Check all four edges of the rectangle
    edges = [
        ((rect[0], rect[1]), (rect[2], rect[1])),  # top
        ((rect[2], rect[1]), (rect[2], rect[3])),  # right
        ((rect[2], rect[3]), (rect[0], rect[3])),  # bottom
        ((rect[0], rect[3]), (rect[0], rect[1])),  # left
    ]
    for e1, e2 in edges:
        if segment_line_intersection(p1, p2, e1, e2):
            return True
    return False


def inflate_bbox(bbox: BBox, margin: float) -> BBox:
    """Expand a bounding box by margin on all sides."""
    x, y, w, h = bbox
    return (x - margin, y - margin, w + 2 * margin, h + 2 * margin)


def union_bbox(bboxes: List[BBox]) -> BBox:
    """Compute the bounding box that contains all given bboxes."""
    if not bboxes:
        return (0, 0, 0, 0)
    rects = [bbox_to_rect(b) for b in bboxes]
    x1 = min(r[0] for r in rects)
    y1 = min(r[1] for r in rects)
    x2 = max(r[2] for r in rects)
    y2 = max(r[3] for r in rects)
    return rect_to_bbox((x1, y1, x2, y2))


def shift_bbox(bbox: BBox, dx: float, dy: float) -> BBox:
    """Translate a bounding box by (dx, dy)."""
    x, y, w, h = bbox
    return (x + dx, y + dy, w, h)
