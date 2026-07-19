"""
High-level flowchart routing: scenario classification, path selection, overlap tracking.

This builds on routing.py and geometry.py for orthogonal path computation
and port allocation. Use these functions in your standalone diagram scripts
for automated path selection with obstacle avoidance and overlap resolution.
"""

from typing import Any, Dict, List, Optional, Tuple

from geometry import (
    BBox,
    Point,
    connection_point,
    center,
    union_bbox,
)


# =========================================================================
# Scenario classification
# =========================================================================

def classify_edge(src_node: Dict[str, Any], dst_node: Dict[str, Any]) -> str:
    """Classify edge into one of 8 spatial scenarios by row/col position.

    Returns: SAME_ROW_RIGHT, SAME_ROW_LEFT, SAME_COL_DOWN, SAME_COL_UP,
             DIAG_DOWN_RIGHT, DIAG_DOWN_LEFT, DIAG_UP_RIGHT, DIAG_UP_LEFT
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
# Obstacle detection
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
# Path building helpers
# =========================================================================

def build_straight_path(
    src_node: Dict[str, Any], dst_node: Dict[str, Any], scenario: str
) -> List[Point]:
    """0-turn straight path for same-row/same-col scenarios."""
    sc = center(src_node["bbox"])
    dc = center(dst_node["bbox"])
    if scenario in ("SAME_COL_DOWN", "SAME_COL_UP"):
        sy = src_node["y"] + (src_node["height"] if scenario == "SAME_COL_DOWN" else 0)
        dy = dst_node["y"] + (0 if scenario == "SAME_COL_DOWN" else dst_node["height"])
        return [(sc[0], sy), (dc[0], dy)]
    else:
        sx = src_node["x"] + (src_node["width"] if scenario == "SAME_ROW_RIGHT" else 0)
        dx = dst_node["x"] + (0 if scenario == "SAME_ROW_RIGHT" else dst_node["width"])
        return [(sx, sc[1]), (dx, dc[1])]


def build_L1_path(
    src_node: Dict[str, Any], dst_node: Dict[str, Any], scenario: str
) -> List[Point]:
    """Primary L-shaped (1-turn) path for diagonals."""
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
    src_exit = connection_point(src_node["bbox"], sp)
    dst_entry = connection_point(dst_node["bbox"], dp)
    mid_x = dst_node["x"] + dst_node["width"] / 2
    mid_y = src_node["y"] + src_node["height"] / 2
    return [src_exit, (mid_x, mid_y), dst_entry]


def build_L2_path(
    src_node: Dict[str, Any], dst_node: Dict[str, Any], scenario: str
) -> List[Point]:
    """Alternate L-shaped (1-turn) path for diagonals."""
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
    src_exit = connection_point(src_node["bbox"], sp)
    dst_entry = connection_point(dst_node["bbox"], dp)
    mid_x = src_node["x"] + src_node["width"] / 2
    mid_y = dst_node["y"] + dst_node["height"] / 2
    return [src_exit, (mid_x, mid_y), dst_entry]


def _find_blocking_node(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    all_nodes: List[Dict[str, Any]],
    key: str,
    best_fn,
    initial: float,
) -> Optional[Dict[str, Any]]:
    """Find the blocking node between src and dst using best_fn on key attribute."""
    best = None
    best_val = initial
    for n in all_nodes:
        if n["id"] in (src_node["id"], dst_node["id"]):
            continue
        r1, r2 = src_node["row"], dst_node["row"]
        c1, c2 = src_node["col"], dst_node["col"]
        if min(r1, r2) <= n["row"] <= max(r1, r2) and min(c1, c2) <= n["col"] <= max(c1, c2):
            val = n[key]
            if best_fn(val, best_val):
                best_val = val
                best = n
    return best


def build_Z_path(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    scenario: str,
    all_nodes: List[Dict[str, Any]],
    margin: float = 30,
) -> Optional[List[Point]]:
    """Z-shaped (2-turn) path navigating around obstacles.

    For DIAG_DOWN_RIGHT: tries extending right past obstacles, then down.
    For DIAG_DOWN_LEFT:  tries extending left past obstacles, then down.
    """
    sc = center(src_node["bbox"])
    dc = center(dst_node["bbox"])

    if scenario == "DIAG_DOWN_RIGHT":
        obs = _find_blocking_node(src_node, dst_node, all_nodes, "x", max, -1)
        if obs and obs["x"] + obs["width"] > sc[0]:
            ex = obs["x"] + obs["width"] + margin
            return [
                connection_point(src_node["bbox"], "right"),
                (ex, sc[1]), (ex, dc[1]),
                connection_point(dst_node["bbox"], "top"),
            ]
        obs2 = _find_blocking_node(src_node, dst_node, all_nodes, "y", max, -1)
        if obs2:
            ey = obs2["y"] + obs2["height"] + margin
            return [
                connection_point(src_node["bbox"], "bottom"),
                (sc[0], ey), (dc[0], ey),
                connection_point(dst_node["bbox"], "top"),
            ]

    elif scenario == "DIAG_DOWN_LEFT":
        obs = _find_blocking_node(src_node, dst_node, all_nodes, "x", min, float("inf"))
        if obs and obs["x"] < sc[0]:
            ex = obs["x"] - margin
            return [
                connection_point(src_node["bbox"], "left"),
                (ex, sc[1]), (ex, dc[1]),
                connection_point(dst_node["bbox"], "top"),
            ]
        obs2 = _find_blocking_node(src_node, dst_node, all_nodes, "y", max, -1)
        if obs2:
            ey = obs2["y"] + obs2["height"] + margin
            return [
                connection_point(src_node["bbox"], "bottom"),
                (sc[0], ey), (dc[0], ey),
                connection_point(dst_node["bbox"], "top"),
            ]

    return None


def build_perimeter_path(
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    all_nodes: List[Dict[str, Any]],
    margin: float = 40,
) -> List[Point]:
    """Fallback path routing around the perimeter of all nodes."""
    all_bboxes = [n["bbox"] for n in all_nodes]
    ux, uy, uw, uh = union_bbox(all_bboxes)
    src_exit = connection_point(src_node["bbox"], "right")
    dst_entry = connection_point(dst_node["bbox"], "top")
    px = ux + uw + margin
    return [src_exit, (px, src_exit[1]), (px, dst_entry[1]), dst_entry]


# =========================================================================
# Path selection
# =========================================================================

def generate_candidates(
    scenario: str,
    src_node: Dict[str, Any],
    dst_node: Dict[str, Any],
    all_nodes: List[Dict[str, Any]],
) -> List[Tuple[List[Point], int]]:
    """Generate candidate paths in priority order.

    Returns list of (waypoints, turn_count) from best to worst priority.
    """
    cand: List[Tuple[List[Point], int]] = []

    if scenario in ("SAME_COL_DOWN", "SAME_COL_UP", "SAME_ROW_RIGHT", "SAME_ROW_LEFT"):
        cand.append((build_straight_path(src_node, dst_node, scenario), 0))

    if scenario in ("DIAG_DOWN_RIGHT", "DIAG_DOWN_LEFT", "DIAG_UP_RIGHT", "DIAG_UP_LEFT"):
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

    Scoring:
    1. Element obstacle → DISQUALIFIED
    2. Turn count × 100 + parallel overlaps → final score (lower = better)
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
# Parallel overlap detection
# =========================================================================

def _ranges_overlap(a1: float, a2: float, b1: float, b2: float) -> bool:
    return max(a1, b1) < min(a2, b2)


def _count_parallel_overlaps(
    path: List[Point], placed_edges: List[Dict[str, Any]]
) -> int:
    """Count how many segments in path overlap in parallel with placed edges."""
    count = 0
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        is_h = abs(y1 - y2) < 1e-6
        for edge in placed_edges:
            for seg in edge.get("_segments", []):
                if is_h and seg.get("is_horizontal") and abs(seg["y"] - y1) < 1e-6:
                    if _ranges_overlap(min(x1, x2), max(x1, x2), seg["x_min"], seg["x_max"]):
                        count += 1
                elif not is_h and not seg.get("is_horizontal") and abs(seg["x"] - x1) < 1e-6:
                    if _ranges_overlap(min(y1, y2), max(y1, y2), seg["y_min"], seg["y_max"]):
                        count += 1
    return count


# =========================================================================
# OccupiedLanes — track placed edge segments
# =========================================================================

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
                self.horizontal.append({
                    "y": y1, "x_min": min(x1, x2), "x_max": max(x1, x2),
                    "edge_id": edge.get("id", "?"),
                })
            else:
                self.vertical.append({
                    "x": x1, "y_min": min(y1, y2), "y_max": max(y1, y2),
                    "edge_id": edge.get("id", "?"),
                })


def compute_segments(waypoints: List[Point]) -> List[Dict[str, Any]]:
    """Convert waypoints to segment dicts for overlap tracking."""
    segs: List[Dict[str, Any]] = []
    for i in range(len(waypoints) - 1):
        x1, y1 = waypoints[i]
        x2, y2 = waypoints[i + 1]
        is_h = abs(y1 - y2) < 1e-6
        segs.append({
            "is_horizontal": is_h,
            "y": y1 if is_h else None,
            "x": x1 if not is_h else None,
            "x_min": min(x1, x2) if is_h else None,
            "x_max": max(x1, x2) if is_h else None,
            "y_min": min(y1, y2) if not is_h else None,
            "y_max": max(y1, y2) if not is_h else None,
        })
    return segs


# =========================================================================
# Same-column skip-detection routing
# =========================================================================

def route_same_column(
    src_node: Dict[str, Any], dst_node: Dict[str, Any], skip_count: int = 0
) -> List[Point]:
    """Route same-column forward edges with skip detection.

    - No intermediate + same center_x → straight line (0 turns)
    - No intermediate + different center_x → L-shape (1 turn)
    - Has intermediate → Z-shape (2+ turns)
    """
    sx = src_node["x"] + src_node["width"] / 2
    sy = src_node["y"] + src_node["height"]
    dx = dst_node["x"] + dst_node["width"] / 2
    dy = dst_node["y"]

    if abs(sx - dx) < 2:
        if skip_count > 0:
            off = 25
            my = (sy + dy) / 2
            return [(sx, sy), (sx + off, sy), (sx + off, my), (sx - off, my), (sx - off, dy), (sx, dy)]
        return [(sx, sy), (dx, dy)]
    else:
        if skip_count > 0:
            my = sy + 20
            return [(sx, sy), (sx, my), (dx, my), (dx, dy)]
        return [(sx, sy), (dx, sy), (dx, dy)]
