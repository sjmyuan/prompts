"""
Label placement utilities for SVG diagram connections.

Computes optimal label positions along connection paths,
checks for overlaps with shapes and other labels.
"""

import math
from typing import Tuple, List, Dict, Any, Optional

from geometry import (
    BBox,
    Point,
    overlap_with_margin,
    find_overlapping,
)
from routing import (
    midpoint_of_segment,
    segment_is_horizontal,
)


def label_position(
    waypoints: List[Point],
    text: str,
    font_size: float = 12.0,
    existing_labels: Optional[List[BBox]] = None,
    shape_bboxes: Optional[List[BBox]] = None,
    char_width: float = 7.0,
) -> Dict[str, Any]:
    """Find the optimal position for a connection label.

    Places the label at the midpoint of the longest straight segment,
    offset perpendicular to the line direction. Uses a white background
    rect to mask the line underneath.

    Args:
        waypoints: Connection path waypoints
        text: Label text
        font_size: Font size in px
        existing_labels: Bboxes of already-placed labels (to avoid overlap)
        shape_bboxes: Bboxes of shapes (to avoid overlap)
        char_width: Estimated width per character in px

    Returns:
        Dict with 'x', 'y', 'bg_rect' (bbox of background rect),
        'text_offset_x', 'text_offset_y', 'side' (above/below/left/right).
    """
    existing_labels = existing_labels or []
    shape_bboxes = shape_bboxes or []

    text_width = len(text) * char_width + 4  # + padding
    text_height = font_size + 4

    if len(waypoints) < 2:
        # Fallback: place near last point
        pt = waypoints[-1] if waypoints else (0, 0)
        return _place_label(pt, pt, "right", text_width, text_height)

    # Try longest segment first, then fall back to shorter segments
    seg_indices = sorted(
        range(len(waypoints) - 1),
        key=lambda i: _segment_length(waypoints[i], waypoints[i + 1]),
        reverse=True,
    )

    all_obstacles = list(shape_bboxes) + list(existing_labels)

    for seg_idx in seg_indices:
        p1 = waypoints[seg_idx]
        p2 = waypoints[seg_idx + 1]
        seg_len = _segment_length(p1, p2)

        if seg_len < text_width:
            continue  # Segment too short for text

        mid = midpoint_of_segment(waypoints, seg_idx)
        is_horiz = segment_is_horizontal(waypoints, seg_idx)

        # Try placements
        if is_horiz:
            sides = ["above", "below"]
        else:
            sides = ["right", "left"]

        for side in sides:
            result = _place_label(p1, p2, side, text_width, text_height)
            label_bbox = result["bg_rect"]

            # Check overlap with obstacles
            overlaps = False
            for obs in all_obstacles:
                if overlap_with_margin(label_bbox, obs, 2.0):
                    overlaps = True
                    break

            if not overlaps:
                return result

    # Fallback: place at start of connection, offset
    return _place_label(waypoints[0], waypoints[-1], "right", text_width, text_height)


def _segment_length(p1: Point, p2: Point) -> float:
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _place_label(
    p1: Point, p2: Point, side: str, text_width: float, text_height: float
) -> Dict[str, Any]:
    """Place a label relative to a line segment."""
    mx = (p1[0] + p2[0]) / 2.0
    my = (p1[1] + p2[1]) / 2.0

    offset = 12.0  # perpendicular offset from line

    if side == "above":
        bg_x = mx - text_width / 2.0
        bg_y = my - offset - text_height
        text_x = mx
        text_y = my - offset - text_height / 2.0
    elif side == "below":
        bg_x = mx - text_width / 2.0
        bg_y = my + offset
        text_x = mx
        text_y = my + offset + text_height / 2.0
    elif side == "right":
        bg_x = mx + offset
        bg_y = my - text_height / 2.0
        text_x = mx + offset + text_width / 2.0
        text_y = my
    else:  # 'left'
        bg_x = mx - offset - text_width
        bg_y = my - text_height / 2.0
        text_x = mx - offset - text_width / 2.0
        text_y = my

    return {
        "x": text_x,
        "y": text_y + text_height / 2.0,  # SVG text y is baseline
        "bg_rect": (bg_x, bg_y, text_width, text_height),
        "side": side,
    }


def label_overlap_check(
    labels: List[Dict[str, Any]], shape_bboxes: List[BBox], tolerance: float = 2.0
) -> List[Dict[str, Any]]:
    """Check all placed labels for overlaps with shapes or other labels.

    Returns list of overlap issues found.
    """
    issues = []
    for i, label in enumerate(labels):
        lb = label.get("bg_rect")
        if not lb:
            continue

        # Check against shapes
        for j, sbox in enumerate(shape_bboxes):
            if overlap_with_margin(lb, sbox, tolerance):
                issues.append(
                    {
                        "type": "label-shape-overlap",
                        "label_idx": i,
                        "shape_idx": j,
                        "label_bbox": lb,
                        "shape_bbox": sbox,
                    }
                )

        # Check against other labels
        for k in range(i + 1, len(labels)):
            lb2 = labels[k].get("bg_rect")
            if lb2 and overlap_with_margin(lb, lb2, tolerance):
                issues.append(
                    {
                        "type": "label-label-overlap",
                        "label_i": i,
                        "label_j": k,
                        "label_i_bbox": lb,
                        "label_j_bbox": lb2,
                    }
                )

    return issues


def compute_all_labels(
    connections: List[Dict[str, Any]], shape_bboxes: List[BBox], font_size: float = 12.0
) -> List[Dict[str, Any]]:
    """Compute label positions for all connections with labels.

    Each connection dict should have:
        - 'waypoints': list of (x, y) tuples
        - 'label': text string (optional)

    Returns list of label dicts with positions, in placement order.
    Processes connections one by one, avoiding previously placed labels.
    """
    labels = []
    placed_label_bboxes = []

    for conn in connections:
        text = conn.get("label", "")
        if not text:
            continue

        waypoints = conn.get("waypoints", [])
        if len(waypoints) < 2:
            continue

        result = label_position(
            waypoints=waypoints,
            text=text,
            font_size=font_size,
            existing_labels=placed_label_bboxes,
            shape_bboxes=shape_bboxes,
        )
        result["text"] = text
        result["conn_id"] = conn.get("id", "")
        labels.append(result)
        placed_label_bboxes.append(result["bg_rect"])

    return labels


# ---------------------------------------------------------------------------
# Quick label dimension estimation & manual placement (for cross-column edges)
# ---------------------------------------------------------------------------


def est_label_dims(label: str, font_size: float = 11) -> Tuple[float, float]:
    """Estimate label (width, height) from text length. CJK = double width."""
    eff = sum(2 if ord(c) > 0x2E80 else 1 for c in label)
    return (eff * 7 + 8, font_size + 8)


def compute_label_position(
    waypoints: List[Tuple[float, float]],
    label: str,
    font_size: float = 11,
) -> Tuple[float, float, float, float]:
    """Compute label (x, y, w, h) on a path, avoiding node overlap.

    Places on the vertical corridor segment (waypoints[1]→[2]) offset right,
    or on the last horizontal segment offset above as fallback.
    """
    lw, lh = est_label_dims(label, font_size)
    if len(waypoints) >= 3:
        my = (waypoints[1][1] + waypoints[2][1]) / 2
        return (waypoints[1][0] + lw / 2 + 8, my - lh / 2, lw, lh)
    if len(waypoints) >= 2:
        mx = (waypoints[-2][0] + waypoints[-1][0]) / 2
        my = (waypoints[-2][1] + waypoints[-1][1]) / 2
        return (mx - lw / 2, my - 10 - lh, lw, lh)
    return (0, 0, lw, lh)


def label_overlaps_node(
    label_bbox: Tuple[float, float, float, float],
    nodes: List[Dict[str, Any]],
) -> bool:
    """Check if label bbox overlaps any node bbox."""
    lx, ly, lw, lh = label_bbox
    for n in nodes:
        nx, ny, nw, nh = n["bbox"]
        if not (lx + lw < nx or lx > nx + nw or ly + lh < ny or ly > ny + nh):
            return True
    return False
