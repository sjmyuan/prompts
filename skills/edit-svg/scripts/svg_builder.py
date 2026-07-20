"""
SVG diagram element builder using svgwrite.

Install: pip install svgwrite

Replaces svg_shapes.py — all SVG elements are generated via the svgwrite
library instead of manual string concatenation. Exposes the same public
function signatures so call-sites need only update the import name.
"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

import svgwrite
from svgwrite.text import TSpan

from colors import PPT_PALETTE, get_shadow_filter

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_FONT_FAMILY = "Segoe UI, -apple-system, Helvetica Neue, Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif"


# ---------------------------------------------------------------------------
# CJK width helper (shared across this module)
# ---------------------------------------------------------------------------


def _cjk_len(text: str) -> int:
    """Effective length of text counting CJK chars as double width."""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in text)


def _to_str(element) -> str:
    """Serialize a svgwrite element to an SVG string fragment."""
    return ET.tostring(element.get_xml(), encoding="unicode")


def _dwg() -> svgwrite.Drawing:
    """Return a throw-away Drawing used only as an element factory."""
    return svgwrite.Drawing()


# ---------------------------------------------------------------------------
# Shape dimensions (pure math — no library needed)
# ---------------------------------------------------------------------------


def get_shape_dimensions(
    text: str,
    shape_type: str = "process",
    ppt_mode: bool = True,
    char_width: float = 9.0,
    min_width: float = 100.0,
    min_height: float = 48.0,
    line_height: float = 22.0,
    padding_x: float = 28.0,
    padding_y: float = 16.0,
) -> Dict[str, float]:
    """Compute shape dimensions based on text content and shape type.

    Supports multi-line text (\n-separated) and CJK characters.
    CJK characters count as double width for accurate dimension calculation.
    """
    lines = text.split("\n")
    max_eff = max(_cjk_len(line) for line in lines) if lines else 1
    num_lines = len(lines)

    if ppt_mode:
        h = max(min_height, num_lines * line_height + padding_y)
        w = max(min_width, max_eff * char_width + padding_x)
    else:
        h = max(40.0, num_lines * 18 + 12)
        w = max(80.0, max_eff * 8 + 20)

    if shape_type == "decision":
        w = max(w, 80.0)
        h = w
    elif shape_type == "data":
        h = max(h, 60.0)
    elif shape_type == "connector":
        w = 30.0
        h = 30.0
    elif shape_type == "fork":
        w = max(w, 160.0)
        h = 8.0

    return {"width": w, "height": h}


# ---------------------------------------------------------------------------
# Node type colors
# ---------------------------------------------------------------------------


def get_node_type_colors(shape_type: str, ppt_mode: bool = True) -> Dict[str, str]:
    """Return fill, stroke, text_color, and gradient_id for a node type."""
    if ppt_mode:
        palette: Dict[str, Dict[str, Any]] = {
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
        palette = {
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

    return palette.get(
        shape_type,
        {
            "fill": PPT_PALETTE["blue_fill_start"],
            "stroke": PPT_PALETTE["primary"],
            "text_color": PPT_PALETTE["text_primary"],
            "gradient_id": "gradBlue",
        },
    )


# ---------------------------------------------------------------------------
# SVG element generators — implemented via svgwrite
# ---------------------------------------------------------------------------


def _add_text_to_group(
    g,
    text: str,
    cx: float,
    cy: float,
    font_family: str,
    font_size: float,
    fill: str,
) -> None:
    """Add a text element (single or multi-line) to an svgwrite group.

    For single-line text, uses ``alignment-baseline="middle"`` on ``<text>``.
    For multi-line text, uses ``dy``-based ``<tspan>`` elements with a baseline
    offset of ~0.32\\ *font\\_size for visual centering.
    """
    d = _dwg()
    lines = text.split("\n")
    num_lines = len(lines)

    if num_lines == 1:
        g.add(
            d.text(
                text,
                insert=(cx, cy),
                text_anchor="middle",
                alignment_baseline="middle",
                font_family=font_family,
                font_size=font_size,
                fill=fill,
            )
        )
        return

    line_h = font_size + 7
    total_text_h = num_lines * line_h
    first_line_center = cy - total_text_h / 2 + line_h / 2
    base_off = font_size * 0.32
    text_y = first_line_center + base_off

    text_elem = d.text(
        "",
        insert=(cx, text_y),
        text_anchor="middle",
        font_family=font_family,
        font_size=font_size,
        fill=fill,
    )
    text_elem.add(TSpan(lines[0], x=[cx]))
    for line in lines[1:]:
        text_elem.add(TSpan(line, x=[cx], dy=[line_h]))
    g.add(text_elem)


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
    """Generate the SVG element string for a diagram node via svgwrite."""
    d = _dwg()
    c = colors or get_node_type_colors(shape_type, ppt_mode)
    fill = f"url(#{c['gradient_id']})" if c.get("gradient_id") else c["fill"]
    stroke = c["stroke"]
    tc = c["text_color"]
    shadow = {"filter": "url(#shadow)"} if ppt_mode else {}

    g = d.g(id=node_id, class_=f"node {shape_type}")

    if shape_type in ("start", "end"):
        g.add(
            d.rect(
                insert=(x, y),
                size=(width, height),
                rx=height / 2,
                ry=height / 2,
                fill=fill,
                stroke=stroke,
                stroke_width=1.5,
                **shadow,
            )
        )
    elif shape_type == "decision":
        cx, cy = x + width / 2, y + height / 2
        pts = [(cx, y), (x + width, cy), (cx, y + height), (x, cy)]
        g.add(
            d.polygon(points=pts, fill=fill, stroke=stroke, stroke_width=1.5, **shadow)
        )
    elif shape_type == "fork":
        g.add(
            d.rect(
                insert=(x, y),
                size=(width, height),
                fill=stroke,
                stroke=stroke,
                stroke_width=1,
            )
        )
    elif shape_type == "connector":
        r = min(width, height) / 2
        g.add(
            d.circle(
                center=(x + r, y + r),
                r=r,
                fill=fill,
                stroke=stroke,
                stroke_width=1.5,
                **shadow,
            )
        )
    else:
        g.add(
            d.rect(
                insert=(x, y),
                size=(width, height),
                rx=6,
                fill=fill,
                stroke=stroke,
                stroke_width=1.5,
                **shadow,
            )
        )

    cx, cy = x + width / 2, y + height / 2
    font_size = 13 if len(text.split("\n")) > 1 else 14

    _add_text_to_group(g, text, cx, cy, _FONT_FAMILY, font_size, tc)
    return _to_str(g)


def generate_edge_svg(
    edge_id: str,
    path_d: str,
    color: str = "#555555",
    stroke_width: float = 2.0,
    dashed: bool = False,
) -> str:
    """Generate the SVG element string for a connection edge via svgwrite."""
    d = _dwg()
    extra: Dict[str, Any] = {}
    if dashed:
        extra["stroke_dasharray"] = "8,4"
    path = d.path(
        d=path_d,
        id=edge_id,
        fill="none",
        stroke=color,
        stroke_width=stroke_width,
        marker_end="url(#arrow)",
        **extra,
    )
    return _to_str(path)


def generate_arrow_marker(
    marker_id: str = "arrow",
    color: str = "#555555",
    arrow_width: float = 10.0,
    arrow_height: float = 10.0,
    tip_ref: bool = True,
) -> str:
    """Generate the SVG arrow marker definition string via svgwrite.

    The arrow is a triangle pointing right (in marker-local coordinates):
        Base:  vertical line from (0, 0) to (0, arrow_height)
        Tip:   at (arrow_width, arrow_height/2)

    When tip_ref=True (default): refX/refY are set to the arrow **tip**, so the
    line endpoint touches the target shape edge and the arrowhead extends
    backward. This is the standard convention for diagrams.

    When tip_ref=False: refX/refY are set to the **center of the base**, so the
    line ends at the base and the arrow tip extends forward.

    With orient="auto" and markerUnits="strokeWidth":
      - If the line goes RIGHT  → arrow points right  (tip at +x)
      - If the line goes DOWN   → arrow points down   (tip rotated 90° CW)
      - If the line goes LEFT   → arrow points left   (tip rotated 180°)
      - If the line goes UP     → arrow points up     (tip rotated 270° CW)

    The actual size on screen = (width, height) * stroke-width.
    """
    d = _dwg()
    half_h = arrow_height / 2.0

    # Build the marker element
    marker_attrs: Dict[str, Any] = {
        "id": marker_id,
        "viewBox": f"0 0 {arrow_width} {arrow_height}",
        "orient": "auto",
        "markerUnits": "strokeWidth",
        "markerWidth": str(arrow_width),
        "markerHeight": str(arrow_height),
    }

    if tip_ref:
        # Arrow TIP connects to line endpoint (tip touches target shape)
        marker_attrs["refX"] = str(arrow_width)
        marker_attrs["refY"] = str(half_h)
    else:
        # Arrow BASE center connects to line endpoint
        marker_attrs["refX"] = "0"
        marker_attrs["refY"] = str(half_h)

    marker = d.marker(**marker_attrs)
    marker.add(
        d.path(
            d=f"M 0 0 L {arrow_width} {half_h} L 0 {arrow_height} z",
            fill=color,
        )
    )
    return _to_str(marker)


def generate_label_svg(
    label: str,
    x: float,
    y: float,
    font_size: int = 12,
    bg_color: str = "#FFFFFF",
    text_color: str = "#333333",
) -> str:
    """Generate an edge label SVG element with background via svgwrite.

    Accounts for CJK characters (double width) in label width calculation.
    """
    d = _dwg()
    pad = 4
    w = max(20, _cjk_len(label) * 7 + pad * 2)
    h = font_size + pad * 2
    g = d.g(class_="edge-label")
    g.add(
        d.rect(
            insert=(x - w / 2, y - h / 2),
            size=(w, h),
            rx=3,
            fill=bg_color,
            stroke="#CCCCCC",
            stroke_width=0.5,
        )
    )
    g.add(
        d.text(
            label,
            insert=(x, y),
            text_anchor="middle",
            dominant_baseline="central",
            font_family=_FONT_FAMILY,
            font_size=font_size,
            fill=text_color,
        )
    )
    return _to_str(g)


def generate_title_bar(title: str, width: float = 960, bar_height: float = 44) -> str:
    """Generate the SVG title bar element string via svgwrite."""
    d = _dwg()
    g = d.g(id="title-bar")
    g.add(
        d.rect(
            insert=(0, 0), size=(width, bar_height), fill=PPT_PALETTE["title_bar_bg"]
        )
    )
    g.add(
        d.text(
            title,
            insert=(width / 2, bar_height / 2),
            text_anchor="middle",
            dominant_baseline="central",
            font_family=_FONT_FAMILY,
            font_size=20,
            font_weight="bold",
            fill=PPT_PALETTE["title_bar_text"],
        )
    )
    return _to_str(g)


def generate_section_panel(
    x: float,
    y: float,
    width: float,
    height: float,
    label: str = "",
) -> str:
    """Generate a section background panel with optional label via svgwrite."""
    d = _dwg()
    g = d.g(class_="section-panel")
    g.add(
        d.rect(
            insert=(x, y),
            size=(width, height),
            rx=8,
            fill=PPT_PALETTE["bg_panel"],
            stroke="none",
        )
    )
    if label:
        g.add(
            d.text(
                label,
                insert=(x + 14, y + 22),
                text_anchor="start",
                font_family=_FONT_FAMILY,
                font_size=14,
                font_weight="bold",
                fill=PPT_PALETTE["text_secondary"],
            )
        )
    return _to_str(g)


def get_default_font_stack() -> str:
    """Return the default PPT font-family string."""
    return _FONT_FAMILY
