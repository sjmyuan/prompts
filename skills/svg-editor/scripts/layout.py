"""
Layout computation for SVG diagrams.

Handles grid-based positioning, overlap avoidance, force-directed adjustment,
and viewBox computation.
"""

import math
from typing import Tuple, List, Dict, Any, Optional

try:
    from .geometry import (
        BBox,
        Point,
        overlap_with_margin,
        find_overlapping,
        union_bbox,
        shift_bbox,
        center,
        inflate_bbox,
    )
except ImportError:
    from geometry import (
        BBox,
        Point,
        overlap_with_margin,
        find_overlapping,
        union_bbox,
        shift_bbox,
        center,
        inflate_bbox,
    )


def flow_layout(
    nodes: List[Dict[str, Any]],
    flow_direction: str = "top-to-bottom",
    node_gap: float = 120.0,
    branch_gap: float = 240.0,
    start_offset: Tuple[float, float] = (120, 140),
) -> List[Dict[str, Any]]:
    """Compute positions for flowchart nodes in a grid layout.

    Each node dict should have at minimum:
        - 'id': unique identifier
        - 'width': shape width in px
        - 'height': shape height in px
        - 'row': row index (0-based, top to bottom)
        - 'col': column index (0-based, left to right)

    Returns the nodes list with 'x', 'y', 'bbox' fields added.

    Args:
        nodes: List of node descriptors
        flow_direction: 'top-to-bottom' or 'left-to-right'
        node_gap: Vertical gap between node centers
        branch_gap: Horizontal gap between parallel branches (columns)
        start_offset: (x, y) offset for the first node's position
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
    branch_offset: float = 120.0,
    node_gap: float = 120.0,
) -> Dict[str, Any]:
    """Position branch nodes relative to a decision diamond.

    Yes branch goes right and down, No branch goes left and down.

    Returns dict with updated yes_node and no_node positions.
    """
    dx, dy = decision_node["x"], decision_node["y"]
    dw, dh = decision_node["width"], decision_node["height"]

    # Yes branch: right of decision
    yes_x = dx + dw + 60  # 60px gap from right vertex
    yes_y = dy + dh + 40  # below decision
    yes_node["x"] = yes_x
    yes_node["y"] = yes_y
    yes_node["bbox"] = (
        yes_x,
        yes_y,
        yes_node.get("width", 140),
        yes_node.get("height", 50),
    )

    # No branch: left of decision
    no_x = dx - no_node.get("width", 140) - 60  # 60px gap from left vertex
    no_y = dy + dh + 40
    no_node["x"] = no_x
    no_node["y"] = no_y
    no_node["bbox"] = (no_x, no_y, no_node.get("width", 140), no_node.get("height", 50))

    return {"yes": yes_node, "no": no_node}


def resolve_overlaps(
    placed_bboxes: List[BBox],
    new_bbox: BBox,
    min_gap: float = 20.0,
    max_iterations: int = 20,
) -> BBox:
    """Find a non-overlapping position for new_bbox by shifting away from overlaps.

    Uses a simple force-directed push: for each overlapping placed bbox,
    push along the axis of least overlap.

    Args:
        placed_bboxes: Already placed bounding boxes
        new_bbox: The bbox to place
        min_gap: Minimum gap between shapes
        max_iterations: Maximum push iterations

    Returns:
        Adjusted bbox (may be the same if no overlap).
    """
    result = list(new_bbox)  # mutable copy
    for _ in range(max_iterations):
        overlapping = find_overlapping(placed_bboxes, tuple(result), min_gap)
        if not overlapping:
            break

        # Push away from each overlapping bbox
        for idx in overlapping:
            ob = placed_bboxes[idx]
            ox, oy, ow, oh = ob
            rx, ry, rw, rh = result

            # Compute push direction based on center difference
            ocx, ocy = ox + ow / 2.0, oy + oh / 2.0
            rcx, rcy = rx + rw / 2.0, ry + rh / 2.0
            dx = rcx - ocx
            dy = rcy - ocy

            if abs(dx) * oh > abs(dy) * ow:
                # Push horizontally
                if dx > 0:
                    result[0] = ox + ow + min_gap
                else:
                    result[0] = ox - rw - min_gap
            else:
                # Push vertically
                if dy > 0:
                    result[1] = oy + oh + min_gap
                else:
                    result[1] = oy - rh - min_gap

    return tuple(result)


def force_directed_layout(
    bboxes: List[BBox],
    min_gap: float = 25.0,
    iterations: int = 50,
    spring_strength: float = 0.1,
) -> List[BBox]:
    """Apply force-directed repulsion to resolve all overlaps in a set of bboxes.

    Each bbox repels others if they overlap. The original positions are used
    as anchors (springs) to prevent drifting too far.

    Args:
        bboxes: Initial bounding box positions
        min_gap: Desired minimum gap between bboxes
        iterations: Number of simulation steps
        spring_strength: How strongly bboxes are pulled back to original positions

    Returns:
        List of adjusted bboxes.
    """
    n = len(bboxes)
    if n <= 1:
        return list(bboxes)

    positions = [list(b[:2]) for b in bboxes]  # (x, y) only
    sizes = [(b[2], b[3]) for b in bboxes]  # (w, h) only
    originals = [(b[0], b[1]) for b in bboxes]

    for _ in range(iterations):
        forces = [[0.0, 0.0] for _ in range(n)]

        # Repulsion between overlapping pairs
        for i in range(n):
            for j in range(i + 1, n):
                bi = (positions[i][0], positions[i][1], sizes[i][0], sizes[i][1])
                bj = (positions[j][0], positions[j][1], sizes[j][0], sizes[j][1])
                if overlap_with_margin(bi, bj, -min_gap):
                    # Push apart
                    ci = center(bi)
                    cj = center(bj)
                    dx = ci[0] - cj[0]
                    dy = ci[1] - cj[1]
                    dist = math.hypot(dx, dy) or 1.0
                    fx = dx / dist * 5.0
                    fy = dy / dist * 5.0
                    forces[i][0] += fx
                    forces[i][1] += fy
                    forces[j][0] -= fx
                    forces[j][1] -= fy

        # Spring force toward original position
        for i in range(n):
            forces[i][0] += (originals[i][0] - positions[i][0]) * spring_strength
            forces[i][1] += (originals[i][1] - positions[i][1]) * spring_strength

        # Apply forces
        for i in range(n):
            positions[i][0] += forces[i][0]
            positions[i][1] += forces[i][1]

    return [(p[0], p[1], s[0], s[1]) for p, s in zip(positions, sizes)]


def compute_viewbox(
    all_bboxes: List[BBox],
    padding: int = 40,
    target_aspect: Optional[float] = None,
    title_bar_height: float = 0.0,
    footer_height: float = 0.0,
) -> Tuple[int, int, int, int]:
    """Compute the viewBox from all element bounding boxes.

    Args:
        all_bboxes: All element bounding boxes
        padding: Padding around the content
        target_aspect: Target aspect ratio (width/height), e.g. 16/9 for PPT
        title_bar_height: Extra space reserved at top for title
        footer_height: Extra space reserved at bottom for footer

    Returns:
        (min_x, min_y, width, height) suitable for viewBox attribute.
    """
    if not all_bboxes:
        return (0, 0, 960, 540)

    content_bbox = union_bbox(all_bboxes)
    cx, cy, cw, ch = content_bbox

    # Add padding and title/footer space
    vx = cx - padding
    vy = cy - padding - title_bar_height
    vw = cw + 2 * padding
    vh = ch + 2 * padding + title_bar_height + footer_height

    # Ensure non-negative origin
    if vx < 0:
        vw += abs(vx)
        vx = 0
    if vy < 0:
        vh += abs(vy)
        vy = 0

    # Round up to nearest 50px
    vw = int(math.ceil(vw / 50.0) * 50)
    vh = int(math.ceil(vh / 50.0) * 50)

    # Enforce aspect ratio if specified
    if target_aspect:
        current_aspect = vw / vh if vh > 0 else 1.0
        if current_aspect < target_aspect:
            vw = int(vh * target_aspect)
        elif current_aspect > target_aspect:
            vh = int(vw / target_aspect)
        # Round again
        vw = int(math.ceil(vw / 50.0) * 50)
        vh = int(math.ceil(vh / 50.0) * 50)

    # Minimum size
    vw = max(vw, 400)
    vh = max(vh, 300)

    return (0, 0, vw, vh)


def distribute_along_circle(
    center_point: Point, radius: float, count: int, start_angle: float = -90.0
) -> List[Point]:
    """Distribute points evenly around a circle.

    Args:
        center_point: Center of the circle
        radius: Radius of the circle
        count: Number of points
        start_angle: Starting angle in degrees (0=right, -90=top)

    Returns:
        List of (x, y) positions.
    """
    cx, cy = center_point
    points = []
    for i in range(count):
        angle = math.radians(start_angle + (360.0 / count) * i)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points
