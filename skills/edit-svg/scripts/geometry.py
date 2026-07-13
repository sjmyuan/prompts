"""
Geometry utilities for SVG diagram layout calculations.

All coordinates use SVG coordinate system (y increases downward).
Bounding boxes are represented as (x, y, width, height).
Points are (x, y) tuples.
"""

import math
from typing import Tuple, List, Optional

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


def closest_edge_point(bbox: BBox, target_point: Point) -> Point:
    """Find the closest point on the edges of bbox to target_point."""
    x, y, w, h = bbox
    tx, ty = target_point
    # Clamp the target point to the bounding box edges
    clamped_x = max(x, min(tx, x + w))
    clamped_y = max(y, min(ty, y + h))

    # Determine which edge the clamped point is on
    if clamped_x == x or clamped_x == x + w:
        return (clamped_x, clamped_y)
    else:
        return (clamped_x, clamped_y)


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
