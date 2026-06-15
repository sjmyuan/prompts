"""
Main computation orchestrator for SVG diagram layout.

Usage:
    python3 scripts/compute_all.py '<json_description>'

The JSON description should contain:
    {
        "diagram_type": "flowchart" | "architecture" | "sequence" | "concept" | "chart",
        "viewbox": {"width": 960, "height": 540},  // optional, defaults to 960x540
        "title": "Diagram Title",
        "nodes": [
            {
                "id": "start",
                "type": "start",  // start, end, process, decision, subprocess, document, data, connector, fork
                "text": "Start",
                "width": 130,
                "height": 48,
                "row": 0, "col": 0  // optional for grid layout
            },
            ...
        ],
        "edges": [
            {
                "id": "e1",
                "from": "start",
                "to": "process1",
                "label": "Yes",  // optional
                "style": "solid"  // solid | dashed
            },
            ...
        ]
    }

Output: JSON with computed positions, paths, labels, and validation results.
"""

import json
import sys
import os
import sys
from typing import Dict, Any, List

# Ensure scripts directory is on the path for direct execution
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

try:
    from .geometry import (
        BBox,
        Point,
        center,
        connection_point,
        overlap,
        find_overlapping,
        union_bbox,
        bbox_to_rect,
        inflate_bbox,
        distance,
    )
    from .routing import (
        orthogonal_path,
        connection_endpoints,
        path_to_svg_d,
        detect_intersections,
        endpoint_valid,
        bezier_path,
        longest_straight_segment,
        midpoint_of_segment,
        segment_is_horizontal,
    )
    from .layout import (
        flow_layout,
        decision_branch_positions,
        resolve_overlaps,
        force_directed_layout,
        compute_viewbox,
        distribute_along_circle,
    )
    from .labeling import compute_all_labels, label_position
    from .colors import (
        contrast_ratio,
        wcag_aa_check,
        PPT_PALETTE,
        get_gradient_defs,
        get_shadow_filter,
    )
    from .svg_shapes import (
        generate_node_svg,
        generate_edge_svg,
        generate_label_svg,
        generate_title_bar,
        generate_arrow_marker,
        get_shape_dimensions,
        get_node_type_colors,
    )
except ImportError:
    from geometry import (
        BBox,
        Point,
        center,
        connection_point,
        overlap,
        find_overlapping,
        union_bbox,
        bbox_to_rect,
        inflate_bbox,
        distance,
    )
    from routing import (
        orthogonal_path,
        connection_endpoints,
        path_to_svg_d,
        detect_intersections,
        endpoint_valid,
        bezier_path,
        longest_straight_segment,
        midpoint_of_segment,
        segment_is_horizontal,
    )
    from layout import (
        flow_layout,
        decision_branch_positions,
        resolve_overlaps,
        force_directed_layout,
        compute_viewbox,
        distribute_along_circle,
    )
    from labeling import compute_all_labels, label_position
    from colors import (
        contrast_ratio,
        wcag_aa_check,
        PPT_PALETTE,
        get_gradient_defs,
        get_shadow_filter,
    )
    from svg_shapes import (
        generate_node_svg,
        generate_edge_svg,
        generate_label_svg,
        generate_title_bar,
        generate_arrow_marker,
        get_shape_dimensions,
        get_node_type_colors,
    )


def compute_diagram(desc: Dict[str, Any]) -> Dict[str, Any]:
    """Compute all positions, paths, and labels for a diagram.

    Args:
        desc: Diagram description dict.

    Returns:
        Dict with 'nodes', 'edges', 'labels', 'viewbox', 'defs', 'validation'.
    """
    diagram_type = desc.get("diagram_type", "flowchart")
    title = desc.get("title", "")
    nodes_input = desc.get("nodes", [])
    edges_input = desc.get("edges", [])
    viewbox_config = desc.get("viewbox", {"width": 960, "height": 540})
    flow_direction = desc.get("flow_direction", "top-to-bottom")
    ppt_mode = desc.get("ppt_mode", True)

    # --- Step 1: Compute node positions ---
    nodes = list(nodes_input)  # shallow copy, we'll mutate

    if diagram_type == "flowchart":
        # Use grid-based flow layout
        node_gap = 130.0 if ppt_mode else 100.0
        branch_gap = 260.0 if ppt_mode else 220.0
        start_offset_x = 100.0
        start_offset_y = 140.0 if ppt_mode else 100.0  # +60 for title bar
        nodes = flow_layout(
            nodes,
            flow_direction,
            node_gap,
            branch_gap,
            (start_offset_x, start_offset_y),
        )

        # Handle decision branches (nodes with type='decision' have special routing)
        decision_nodes = [n for n in nodes if n.get("type") == "decision"]
        for dn in decision_nodes:
            dn_id = dn["id"]
            outgoing = [e for e in edges_input if e.get("from") == dn_id]
            if len(outgoing) >= 2:
                # Position branch nodes relative to decision
                yes_edge = next(
                    (e for e in outgoing if e.get("branch") == "yes"), outgoing[0]
                )
                no_edge = next(
                    (e for e in outgoing if e.get("branch") == "no"), outgoing[1]
                )
                yes_node = next((n for n in nodes if n["id"] == yes_edge["to"]), None)
                no_node = next((n for n in nodes if n["id"] == no_edge["to"]), None)
                if yes_node and no_node:
                    result = decision_branch_positions(dn, yes_node, no_node)
                    # Update in-place
                    for n in nodes:
                        if n["id"] == result["yes"]["id"]:
                            n.update(
                                {
                                    k: v
                                    for k, v in result["yes"].items()
                                    if k not in ("id",)
                                }
                            )
                        if n["id"] == result["no"]["id"]:
                            n.update(
                                {
                                    k: v
                                    for k, v in result["no"].items()
                                    if k not in ("id",)
                                }
                            )

    elif diagram_type == "concept":
        # Radial layout around a central node
        central = next((n for n in nodes if n.get("role") == "central"), nodes[0])
        cx, cy = viewbox_config["width"] / 2, viewbox_config["height"] / 2
        central["x"] = cx - central.get("width", 140) / 2
        central["y"] = cy - central.get("height", 50) / 2
        central["bbox"] = (
            central["x"],
            central["y"],
            central.get("width", 140),
            central.get("height", 50),
        )

        branch_nodes = [n for n in nodes if n.get("role") != "central"]
        radius = min(viewbox_config["width"], viewbox_config["height"]) * 0.35
        positions = distribute_along_circle((cx, cy), radius, len(branch_nodes))
        for i, bn in enumerate(branch_nodes):
            px, py = positions[i]
            w = bn.get("width", 130)
            h = bn.get("height", 48)
            bn["x"] = px - w / 2
            bn["y"] = py - h / 2
            bn["bbox"] = (bn["x"], bn["y"], w, h)

    elif diagram_type == "chart":
        # Charts have axes-based layout — handled in chart-specific reference
        pass

    # --- Step 2: Validate node positions (overlap detection) ---
    all_bboxes = [n.get("bbox") for n in nodes if n.get("bbox")]
    overlaps_found = []
    for i in range(len(all_bboxes)):
        for j in range(i + 1, len(all_bboxes)):
            if (
                all_bboxes[i]
                and all_bboxes[j]
                and overlap(all_bboxes[i], all_bboxes[j])
            ):
                overlaps_found.append(
                    {
                        "node_i": nodes[i]["id"],
                        "node_j": nodes[j]["id"],
                        "bbox_i": all_bboxes[i],
                        "bbox_j": all_bboxes[j],
                    }
                )

    if overlaps_found:
        # Try force-directed resolution
        resolved = force_directed_layout(all_bboxes, min_gap=30.0, iterations=30)
        for i, n in enumerate(nodes):
            if i < len(resolved):
                n["bbox"] = resolved[i]
                n["x"] = resolved[i][0]
                n["y"] = resolved[i][1]

    # --- Step 3: Compute connection paths ---
    node_map = {n["id"]: n for n in nodes}
    connections = []
    for edge in edges_input:
        src_node = node_map.get(edge["from"])
        dst_node = node_map.get(edge["to"])
        if not src_node or not dst_node:
            continue

        src_bbox = src_node.get("bbox")
        dst_bbox = dst_node.get("bbox")
        if not src_bbox or not dst_bbox:
            continue

        src_pt, dst_pt, src_side, dst_side = connection_endpoints(
            src_bbox, dst_bbox, flow_direction
        )

        # Collect obstacle bboxes (exclude source and target)
        obstacles = [
            n.get("bbox")
            for n in nodes
            if n["id"] != edge["from"] and n["id"] != edge["to"] and n.get("bbox")
        ]

        if diagram_type in ("concept", "sequence"):
            # Use bezier curves for concept/sequence
            path_str = bezier_path(src_pt, dst_pt)
            waypoints = [src_pt, dst_pt]
        else:
            waypoints = orthogonal_path(
                src_pt, dst_pt, src_side, dst_side, clearance=25.0, obstacles=obstacles
            )
            path_str = path_to_svg_d(waypoints)

        conn = {
            "id": edge.get("id", f"e_{edge['from']}_{edge['to']}"),
            "from": edge["from"],
            "to": edge["to"],
            "label": edge.get("label", ""),
            "style": edge.get("style", "solid"),
            "src_point": src_pt,
            "dst_point": dst_pt,
            "src_side": src_side,
            "dst_side": dst_side,
            "waypoints": waypoints,
            "path_d": path_str,
            "bezier": diagram_type in ("concept", "sequence"),
        }
        connections.append(conn)

    # --- Step 4: Validate connections ---
    connection_issues = []

    # Line intersection detection
    all_waypoints = [c["waypoints"] for c in connections]
    shape_bboxes = [n.get("bbox") for n in nodes if n.get("bbox")]
    intersections = detect_intersections(all_waypoints, shape_bboxes)
    for iss in intersections:
        connection_issues.append(iss)

    # Endpoint validation
    for conn in connections:
        dst_node = node_map.get(conn["to"])
        if dst_node and dst_node.get("bbox"):
            result = endpoint_valid(conn["waypoints"], dst_node["bbox"])
            if not result["valid"]:
                connection_issues.append(
                    {
                        "type": "endpoint",
                        "conn_id": conn["id"],
                        "issues": result["issues"],
                    }
                )

    # --- Step 5: Compute label positions ---
    labels = compute_all_labels(connections, shape_bboxes, font_size=12.0)

    # --- Step 6: Compute viewBox ---
    all_element_bboxes = list(shape_bboxes)
    for conn in connections:
        for pt in conn["waypoints"]:
            all_element_bboxes.append((pt[0] - 5, pt[1] - 5, 10, 10))
    for lbl in labels:
        all_element_bboxes.append(lbl.get("bg_rect"))

    title_bar_h = 70.0 if ppt_mode else 0.0
    footer_h = 20.0
    target_ar = 16.0 / 9.0 if ppt_mode else None

    vx, vy, vw, vh = compute_viewbox(
        all_element_bboxes,
        padding=40,
        target_aspect=target_ar,
        title_bar_height=title_bar_h,
        footer_height=footer_h,
    )

    # Override with configured viewbox if larger
    vw = max(vw, viewbox_config.get("width", 960))
    vh = max(vh, viewbox_config.get("height", 540))

    viewbox = {"x": vx, "y": vy, "width": vw, "height": vh}

    # --- Step 7: Generate SVG defs ---
    defs = {}
    if ppt_mode:
        defs["shadow_filter"] = get_shadow_filter()
        defs["gradients"] = get_gradient_defs()

    # --- Step 8: Color validation (for text elements) ---
    color_issues = []
    from colors import validate_all_text_colors

    text_elements = []
    for node in nodes:
        if node.get("text"):
            text_elements.append(
                {
                    "text": node["text"],
                    "color": node.get("text_color", PPT_PALETTE["text_primary"]),
                    "bg": node.get("fill", PPT_PALETTE["blue_fill_start"]),
                    "font_size": 14.0,
                    "bold": node.get("type") in ("start", "end"),
                }
            )
    for lbl in labels:
        text_elements.append(
            {
                "text": lbl.get("text", ""),
                "color": PPT_PALETTE["text_secondary"],
                "bg": "#FFFFFF",
                "font_size": 11.0,
                "bold": False,
            }
        )

    color_issues = validate_all_text_colors(
        text_elements, PPT_PALETTE["blue_fill_start"]
    )

    # --- Step 9: Generate SVG fragments ---
    node_map = {n["id"]: n for n in nodes}

    svg_nodes = []
    for n in nodes:
        colors = get_node_type_colors(n.get("type", "process"), ppt_mode)
        svg_shape = generate_node_svg(
            node_id=n["id"],
            shape_type=n.get("type", "process"),
            text=n.get("text", ""),
            x=n.get("x", 0),
            y=n.get("y", 0),
            width=n.get("width", 140),
            height=n.get("height", 50),
            ppt_mode=ppt_mode,
            colors=colors,
        )
        svg_nodes.append(
            {
                "id": n["id"],
                "type": n.get("type", "process"),
                "text": n.get("text", ""),
                "x": round(n.get("x", 0), 1),
                "y": round(n.get("y", 0), 1),
                "width": round(n.get("width", 140), 1),
                "height": round(n.get("height", 50), 1),
                "bbox": (
                    tuple(round(v, 1) for v in n["bbox"]) if n.get("bbox") else None
                ),
                "fill": colors["fill"],
                "stroke": colors["stroke"],
                "text_color": colors["text_color"],
                "svg_shape": svg_shape,
                "colors": colors,
            }
        )

    line_color = PPT_PALETTE["connection"]
    dashed_color = PPT_PALETTE["connection_dashed"]
    svg_edges = []
    for c in connections:
        color = dashed_color if c["style"] == "dashed" else line_color
        svg_line = generate_edge_svg(
            edge_id=c["id"],
            path_d=c["path_d"],
            style=c["style"],
            color=color,
            ppt_mode=ppt_mode,
            bezier=c["bezier"],
            label=c["label"],
        )
        svg_edges.append(
            {
                "id": c["id"],
                "from": c["from"],
                "to": c["to"],
                "label": c["label"],
                "style": c["style"],
                "path_d": c["path_d"],
                "bezier": c["bezier"],
                "waypoints": [(round(p[0], 1), round(p[1], 1)) for p in c["waypoints"]],
                "svg_line": svg_line,
            }
        )

    svg_labels = []
    for l in labels:
        svg_label = generate_label_svg(
            text=l.get("text", ""),
            x=round(l["x"], 1),
            y=round(l["y"], 1),
            bg_rect=tuple(round(v, 1) for v in l["bg_rect"]),
        )
        svg_labels.append(
            {
                "conn_id": l.get("conn_id", ""),
                "text": l.get("text", ""),
                "x": round(l["x"], 1),
                "y": round(l["y"], 1),
                "bg_rect": tuple(round(v, 1) for v in l["bg_rect"]),
                "side": l.get("side", ""),
                "svg_label": svg_label,
            }
        )

    # SVG markers and title bar
    svg_markers = (
        generate_arrow_marker(color=line_color)
        + "\n"
        + generate_arrow_marker(color=dashed_color, marker_id="arrow-dashed")
    )
    svg_title = (
        generate_title_bar(title, viewbox["width"]) if ppt_mode and title else ""
    )

    # --- Assemble output ---
    output = {
        "diagram_type": diagram_type,
        "title": title,
        "ppt_mode": ppt_mode,
        "viewbox": viewbox,
        "nodes": svg_nodes,
        "edges": svg_edges,
        "labels": svg_labels,
        "defs": defs,
        "svg_markers": svg_markers,
        "svg_title_bar": svg_title,
        "validation": {
            "node_overlaps": overlaps_found,
            "connection_issues": connection_issues,
            "color_issues": color_issues,
            "all_clear": (
                len(overlaps_found) == 0
                and len(connection_issues) == 0
                and len(color_issues) == 0
            ),
        },
    }

    return output


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {"error": "Usage: python3 compute_all.py '<json_description>'"},
                indent=2,
            )
        )
        sys.exit(1)

    try:
        desc = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}, indent=2))
        sys.exit(1)

    try:
        result = compute_diagram(desc)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
