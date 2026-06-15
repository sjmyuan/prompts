"""
SVG shape and element generation for diagram nodes and edges.

Takes computed layout data from compute_all.py and generates SVG
markup strings for shapes, markers, title bars, and labels.
"""

from typing import Dict, Any, List, Optional

try:
    from .colors import PPT_PALETTE, get_fill_gradient_id
except ImportError:
    from colors import PPT_PALETTE, get_fill_gradient_id


def get_shape_dimensions(
    text: str,
    shape_type: str = "process",
    ppt_mode: bool = True,
    char_width: float = 10.0,
    min_width: float = 100.0,
    min_height: float = 48.0,
) -> Dict[str, float]:
    """Compute shape dimensions based on text content and shape type.

    Args:
        text: Label text
        shape_type: One of start, end, process, decision, subprocess, document, data, connector
        ppt_mode: PPT mode uses larger dimensions
        char_width: Estimated width per character
        min_width: Minimum shape width
        min_height: Minimum shape height

    Returns:
        Dict with 'width' and 'height' in px.
    """
    if ppt_mode:
        h = min_height
        w = max(min_width, len(text) * char_width + 32)
    else:
        h = 40.0
        w = max(80.0, len(text) * 9 + 24)

    if shape_type == "decision":
        # Diamond needs square-ish aspect
        w = max(w, 80.0)
        h = w  # square
    elif shape_type == "data":
        h = max(h, 60.0)
    elif shape_type == "connector":
        w = 30.0
        h = 30.0
    elif shape_type == "fork":
        w = max(w, 160.0)
        h = 8.0

    return {"width": w, "height": h}


def get_node_type_colors(shape_type: str, ppt_mode: bool = True) -> Dict[str, str]:
    """Get fill, stroke, and text colors for a node type.

    Args:
        shape_type: Node type (start, end, process, decision, subprocess, document, data, connector)
        ppt_mode: Use PPT Professional palette

    Returns:
        Dict with 'fill', 'stroke', 'text_color', 'gradient_id' keys.
    """
    if ppt_mode:
        palette = {
            "start": {
                "fill": PPT_PALETTE["green_fill_start"],
                "stroke": PPT_PALETTE["secondary"],
                "text_color": PPT_PALETTE["text_primary"],
                "gradient_id": "gradGreen",
            },
            "end": {
                "fill": PPT_PALETTE["green_fill_start"],
                "stroke": PPT_PALETTE["secondary"],
                "text_color": PPT_PALETTE["text_primary"],
                "gradient_id": "gradGreen",
            },
            "process": {
                "fill": PPT_PALETTE["blue_fill_start"],
                "stroke": PPT_PALETTE["primary"],
                "text_color": PPT_PALETTE["text_primary"],
                "gradient_id": "gradBlue",
            },
            "decision": {
                "fill": PPT_PALETTE["yellow_fill_start"],
                "stroke": PPT_PALETTE["accent"],
                "text_color": PPT_PALETTE["text_primary"],
                "gradient_id": "gradYellow",
            },
            "subprocess": {
                "fill": PPT_PALETTE["blue_fill_start"],
                "stroke": PPT_PALETTE["border_strong"],
                "text_color": PPT_PALETTE["text_primary"],
                "gradient_id": "gradBlue",
            },
            "document": {
                "fill": PPT_PALETTE["yellow_fill_start"],
                "stroke": PPT_PALETTE["accent"],
                "text_color": PPT_PALETTE["text_primary"],
                "gradient_id": "gradYellow",
            },
            "data": {
                "fill": PPT_PALETTE["purple_fill_start"],
                "stroke": PPT_PALETTE["purple"],
                "text_color": PPT_PALETTE["text_primary"],
                "gradient_id": "gradPurple",
            },
            "connector": {
                "fill": PPT_PALETTE["blue_fill_start"],
                "stroke": PPT_PALETTE["primary"],
                "text_color": PPT_PALETTE["text_primary"],
                "gradient_id": None,
            },
        }
    else:
        basic_palette = {
            "start": {
                "fill": "#E8F5E9",
                "stroke": "#2E7D32",
                "text_color": "#212121",
                "gradient_id": None,
            },
            "end": {
                "fill": "#E8F5E9",
                "stroke": "#2E7D32",
                "text_color": "#212121",
                "gradient_id": None,
            },
            "process": {
                "fill": "#E3F2FD",
                "stroke": "#1565C0",
                "text_color": "#212121",
                "gradient_id": None,
            },
            "decision": {
                "fill": "#FFF3E0",
                "stroke": "#E65100",
                "text_color": "#212121",
                "gradient_id": None,
            },
            "subprocess": {
                "fill": "#E3F2FD",
                "stroke": "#37474F",
                "text_color": "#212121",
                "gradient_id": None,
            },
            "document": {
                "fill": "#FFF3E0",
                "stroke": "#E65100",
                "text_color": "#212121",
                "gradient_id": None,
            },
            "data": {
                "fill": "#F3E5F5",
                "stroke": "#7B1FA2",
                "text_color": "#212121",
                "gradient_id": None,
            },
            "connector": {
                "fill": "#E3F2FD",
                "stroke": "#1565C0",
                "text_color": "#212121",
                "gradient_id": None,
            },
        }
        palette = basic_palette

    return palette.get(
        shape_type,
        {
            "fill": PPT_PALETTE["blue_fill_start"],
            "stroke": PPT_PALETTE["primary"],
            "text_color": PPT_PALETTE["text_primary"],
            "gradient_id": "gradBlue",
        },
    )


def generate_node_svg(
    node_id: str,
    shape_type: str,
    text: str,
    x: float,
    y: float,
    width: float,
    height: float,
    ppt_mode: bool = True,
    colors: Optional[Dict[str, str]] = None,
) -> str:
    """Generate the complete SVG element string for a diagram node.

    Args:
        node_id: Unique node identifier (used for SVG id)
        shape_type: Node type (start, end, process, decision, etc.)
        text: Label text
        x: Left x position
        y: Top y position
        width: Shape width
        height: Shape height
        ppt_mode: Use PPT styling (gradients, shadows, rounded corners)
        colors: Optional color override dict (fill, stroke, text_color, gradient_id)

    Returns:
        Complete SVG element string.
    """
    if colors is None:
        colors = get_node_type_colors(shape_type, ppt_mode)

    fill = (
        f"url(#{colors['gradient_id']})"
        if (ppt_mode and colors.get("gradient_id"))
        else colors["fill"]
    )
    stroke = colors["stroke"]
    text_color = colors["text_color"]
    shadow = ' filter="url(#shadow)"' if ppt_mode else ""
    font_family = "Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif"

    cx = x + width / 2.0
    cy = y + height / 2.0

    shape_elem = ""
    text_elem = (
        f'  <text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" '
        f'dominant-baseline="central" font-family="{font_family}" '
        f'font-size="14" fill="{text_color}">{_escape_xml(text)}</text>'
    )

    if shape_type in ("start", "end"):
        # Rounded rectangle (terminator)
        rx = min(height / 2.0, 20.0)
        shape_elem = (
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
            f'rx="{rx:.1f}" ry="{rx:.1f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1.5"{shadow}/>'
        )
    elif shape_type == "decision":
        # Diamond using polygon
        pts = (
            f"{cx:.1f},{y:.1f} "
            f"{x + width:.1f},{cy:.1f} "
            f"{cx:.1f},{y + height:.1f} "
            f"{x:.1f},{cy:.1f}"
        )
        shape_elem = (
            f'  <polygon points="{pts}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1.5"{shadow}/>'
        )
    elif shape_type == "subprocess":
        # Rectangle with side bars
        shape_elem = (
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
            f'rx="4" ry="4" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1.5"{shadow}/>\n'
            f'  <line x1="{x + 6:.1f}" y1="{y + 4:.1f}" x2="{x + 6:.1f}" y2="{y + height - 4:.1f}" '
            f'stroke="{stroke}" stroke-width="2"/>\n'
            f'  <line x1="{x + width - 6:.1f}" y1="{y + 4:.1f}" '
            f'x2="{x + width - 6:.1f}" y2="{y + height - 4:.1f}" '
            f'stroke="{stroke}" stroke-width="2"/>'
        )
    elif shape_type == "document":
        # Rectangle with wavy bottom
        wave_y = y + height - 8
        shape_elem = (
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height - 8:.1f}" '
            f'rx="4" ry="4" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1.5"{shadow}/>\n'
            f'  <path d="M {x:.1f} {wave_y:.1f} Q {x + width * 0.25:.1f} {wave_y + 8:.1f}, '
            f'{x + width * 0.5:.1f} {wave_y:.1f} T {x + width:.1f} {wave_y:.1f}" '
            f'fill="none" stroke="{stroke}" stroke-width="1.5"/>'
        )
    elif shape_type == "data":
        # Cylinder (ellipse + rect + ellipse)
        top_cy = y + 10
        bottom_cy = y + height
        shape_elem = (
            f'  <ellipse cx="{cx:.1f}" cy="{top_cy:.1f}" rx="{width / 2:.1f}" '
            f'ry="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{shadow}/>\n'
            f'  <rect x="{x:.1f}" y="{top_cy:.1f}" width="{width:.1f}" '
            f'height="{height - 20:.1f}" fill="{fill}" stroke="none"/>\n'
            f'  <ellipse cx="{cx:.1f}" cy="{bottom_cy - 10:.1f}" rx="{width / 2:.1f}" '
            f'ry="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n'
            f'  <line x1="{x:.1f}" y1="{top_cy:.1f}" x2="{x:.1f}" y2="{bottom_cy - 10:.1f}" '
            f'stroke="{stroke}" stroke-width="1.5"/>\n'
            f'  <line x1="{x + width:.1f}" y1="{top_cy:.1f}" x2="{x + width:.1f}" '
            f'y2="{bottom_cy - 10:.1f}" stroke="{stroke}" stroke-width="1.5"/>'
        )
    elif shape_type == "connector":
        # Circle
        r = width / 2.0
        shape_elem = (
            f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"{shadow}/>'
        )
    elif shape_type == "fork":
        # Horizontal bar for parallel/fork
        shape_elem = (
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
            f'fill="{stroke}" stroke="{stroke}" stroke-width="1"/>'
        )
    else:
        # Default: rectangle (process)
        rx = 6.0 if ppt_mode else 4.0
        shape_elem = (
            f'  <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
            f'rx="{rx:.1f}" ry="{rx:.1f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="1.5"{shadow}/>'
        )

    return f"<!-- {node_id} ({shape_type}) -->\n{shape_elem}\n{text_elem}"


def generate_edge_svg(
    edge_id: str,
    path_d: str,
    style: str = "solid",
    color: str = "",
    ppt_mode: bool = True,
    bezier: bool = False,
    label: str = "",
) -> str:
    """Generate the SVG <path> element for a connection edge.

    Args:
        edge_id: Edge identifier
        path_d: SVG path d-attribute string
        style: 'solid' or 'dashed'
        color: Line color (defaults from palette)
        ppt_mode: Use PPT palette colors
        bezier: Whether the path is a bezier curve
        label: Optional label text

    Returns:
        SVG path element string.
    """
    if not color:
        color = PPT_PALETTE["connection"] if ppt_mode else "#546E7A"

    dash = ' stroke-dasharray="6,4"' if style == "dashed" else ""
    marker = ' marker-end="url(#arrow)"'

    line_join = ' stroke-linejoin="round"' if not bezier else ""
    fill = ' fill="none"'

    svg = (
        f'  <path d="{path_d}"{fill} stroke="{color}" stroke-width="2"'
        f"{dash}{marker}{line_join}/>"
    )

    return f"<!-- {edge_id} -->\n{svg}"


def generate_arrow_marker(
    color: str = "",
    stroke_width: float = 2.0,
    marker_id: str = "arrow",
) -> str:
    """Generate SVG arrow marker definition.

    Args:
        color: Arrow fill color
        stroke_width: Line stroke width (determines arrowhead size)
        marker_id: ID for the marker

    Returns:
        SVG <marker> element string.
    """
    if not color:
        color = PPT_PALETTE["connection"]

    ah_len = stroke_width * 4  # arrowhead length
    ah_width = stroke_width * 3  # arrowhead width
    vb_size = max(ah_len, ah_width) + 4

    return (
        f'    <marker id="{marker_id}" viewBox="0 0 {vb_size} {vb_size}" '
        f'refX="{ah_len + 1}" refY="{vb_size / 2}" '
        f'markerWidth="{vb_size}" markerHeight="{vb_size}" orient="auto">\n'
        f'      <path d="M 0 0 L {ah_len} {vb_size / 2} L 0 {vb_size} z" '
        f'fill="{color}"/>\n'
        f"    </marker>"
    )


def generate_label_svg(
    text: str,
    x: float,
    y: float,
    bg_rect: tuple,
    edge_color: str = "",
) -> str:
    """Generate SVG elements for a connection label (background rect + text).

    Args:
        text: Label text
        x: Text center x
        y: Text baseline y
        bg_rect: (bx, by, bw, bh) for the white background rect
        edge_color: Edge color for text fill

    Returns:
        SVG elements string.
    """
    if not text:
        return ""

    text_color = edge_color if edge_color else PPT_PALETTE["text_secondary"]
    font_family = "Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif"

    bx, by, bw, bh = bg_rect
    return (
        f'  <rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
        f'rx="3" fill="#FFFFFF" stroke="none"/>\n'
        f'  <text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
        f'dominant-baseline="central" font-family="{font_family}" '
        f'font-size="11" fill="{text_color}">{_escape_xml(text)}</text>'
    )


def generate_title_bar(
    title: str,
    viewbox_width: float = 960.0,
    bar_height: float = 60.0,
) -> str:
    """Generate SVG title bar for PPT-presentation quality diagrams.

    Args:
        title: Diagram title text
        viewbox_width: Width of the SVG viewBox
        bar_height: Height of the title bar

    Returns:
        SVG elements string for the title bar.
    """
    font_family = "Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif"
    title_x = viewbox_width / 2.0
    title_y = bar_height / 2.0

    return (
        f"  <!-- Title Bar -->\n"
        f'  <rect x="0" y="0" width="{viewbox_width:.1f}" height="{bar_height:.1f}" '
        f'fill="{PPT_PALETTE["title_bar_bg"]}" filter="url(#shadow)"/>\n'
        f'  <text x="{title_x:.1f}" y="{title_y:.1f}" text-anchor="middle" '
        f'dominant-baseline="central" font-family="{font_family}" '
        f'font-size="20" font-weight="bold" fill="{PPT_PALETTE["title_bar_text"]}">'
        f"{_escape_xml(title)}</text>"
    )


def generate_section_panel(
    x: float,
    y: float,
    width: float,
    height: float,
    label: str = "",
) -> str:
    """Generate a section background panel with optional label.

    Args:
        x: Left x position
        y: Top y position
        width: Panel width
        height: Panel height
        label: Optional section label text

    Returns:
        SVG elements string.
    """
    lines = [
        f'  <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="8" fill="{PPT_PALETTE["bg_panel"]}" stroke="none"/>'
    ]
    if label:
        font_family = "Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif"
        lines.append(
            f'  <text x="{x + 14:.1f}" y="{y + 22:.1f}" text-anchor="start" '
            f'font-family="{font_family}" font-size="14" font-weight="bold" '
            f'fill="{PPT_PALETTE["text_secondary"]}">{_escape_xml(label)}</text>'
        )
    return "\n".join(lines)


def _escape_xml(text: str) -> str:
    """Escape special XML characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def get_default_font_stack() -> str:
    """Return the default font-family stack for PPT diagrams."""
    return "Segoe UI, -apple-system, Helvetica Neue, Arial, sans-serif"
