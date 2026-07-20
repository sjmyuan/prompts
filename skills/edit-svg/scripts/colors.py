"""
Color utilities for SVG diagrams.

Includes WCAG contrast ratio computation, color palette definitions,
and validation functions.
"""

from typing import Tuple, Dict


def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert a hex color string (#RRGGBB or #RGB) to (R, G, B) in 0-255 range."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: #{hex_color}")
    return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


def rgb_to_hex(r: float, g: float, b: float) -> str:
    """Convert RGB (0-255) to hex color string."""
    return f"#{int(r):02X}{int(g):02X}{int(b):02X}"


def relative_luminance(hex_color: str) -> float:
    """Compute WCAG relative luminance of a color.

    Args:
        hex_color: Color in #RRGGBB format

    Returns:
        Relative luminance value between 0 and 1.
    """
    r, g, b = hex_to_rgb(hex_color)

    def linearize(c: float) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """Compute WCAG contrast ratio between foreground and background colors.

    Args:
        fg: Foreground color (hex)
        bg: Background color (hex)

    Returns:
        Contrast ratio (1.0 to 21.0). 4.5 = AA for normal text, 3.0 = AA for large text.
    """
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_aa_check(fg: str, bg: str, is_large_text: bool = False) -> Dict:
    """Check if a color pair meets WCAG AA contrast requirements.

    Args:
        fg: Foreground color (hex)
        bg: Background color (hex)
        is_large_text: True if text is large (>=18px or >=14px bold)

    Returns:
        Dict with 'pass', 'ratio', 'level', 'required' fields.
    """
    ratio = contrast_ratio(fg, bg)
    required = 3.0 if is_large_text else 4.5
    return {
        "pass": ratio >= required,
        "ratio": round(ratio, 2),
        "level": "AA",
        "required": required,
    }


def wcag_aaa_check(fg: str, bg: str, is_large_text: bool = False) -> Dict:
    """Check if a color pair meets WCAG AAA contrast requirements."""
    ratio = contrast_ratio(fg, bg)
    required = 4.5 if is_large_text else 7.0
    return {
        "pass": ratio >= required,
        "ratio": round(ratio, 2),
        "level": "AAA",
        "required": required,
    }


def validate_all_text_colors(
    text_elements: list, fill_color: str, bg_color: str = "#FFFFFF"
) -> list:
    """Validate contrast for all text elements against their backgrounds.

    Args:
        text_elements: List of dicts with 'color' (hex) and 'font_size' fields
        fill_color: Default shape fill color (used if no bg specified per element)
        bg_color: Overall canvas background color

    Returns:
        List of issues found.
    """
    issues = []
    for i, el in enumerate(text_elements):
        fg = el.get("color", "#000000")
        el_bg = el.get("bg", fill_color)
        font_size = el.get("font_size", 14)
        is_large = font_size >= 18 or (font_size >= 14 and el.get("bold", False))

        result = wcag_aa_check(fg, el_bg, is_large)
        if not result["pass"]:
            issues.append(
                {
                    "element_idx": i,
                    "fg": fg,
                    "bg": el_bg,
                    "ratio": result["ratio"],
                    "required": result["required"],
                    "text": el.get("text", ""),
                }
            )
    return issues


# PPT Professional color palette
PPT_PALETTE = {
    "primary": "#1A73E8",  # Blue
    "secondary": "#34A853",  # Green
    "accent": "#F9AB00",  # Yellow/Orange
    "danger": "#EA4335",  # Red
    "purple": "#8E24AA",  # Purple
    "blue_fill_start": "#E8F0FE",
    "blue_fill_end": "#D2E3FC",
    "green_fill_start": "#E6F4EA",
    "green_fill_end": "#CEEAD6",
    "yellow_fill_start": "#FEF7E0",
    "yellow_fill_end": "#FDE293",
    "purple_fill_start": "#F3E8FD",
    "purple_fill_end": "#E1D0F7",
    "red_fill_start": "#FCE8E6",
    "red_fill_end": "#F8C9C4",
    "bg_white": "#FFFFFF",
    "bg_light": "#F8F9FA",
    "bg_panel": "#F5F5F5",
    "text_primary": "#202124",
    "text_secondary": "#424242",
    "text_tertiary": "#757575",
    "text_on_dark": "#FFFFFF",
    "border_default": "#DADCE0",
    "border_strong": "#3C4043",
    "connection": "#5F6368",
    "connection_dashed": "#9AA0A6",
    "grid": "#E8EAED",
    "title_bar_bg": "#1A73E8",
    "title_bar_text": "#FFFFFF",
}


def get_fill_gradient_id(color_key: str) -> str:
    """Get the gradient ID name for a given color category."""
    gradient_map = {
        "blue": "gradBlue",
        "green": "gradGreen",
        "yellow": "gradYellow",
        "purple": "gradPurple",
        "red": "gradRed",
    }
    return gradient_map.get(color_key, "gradBlue")


def get_gradient_defs() -> str:
    """Generate SVG <defs> for all PPT gradient fills.

    Returns:
        SVG string with <linearGradient> elements.
    """
    gradients = [
        ("gradBlue", PPT_PALETTE["blue_fill_start"], PPT_PALETTE["blue_fill_end"]),
        ("gradGreen", PPT_PALETTE["green_fill_start"], PPT_PALETTE["green_fill_end"]),
        (
            "gradYellow",
            PPT_PALETTE["yellow_fill_start"],
            PPT_PALETTE["yellow_fill_end"],
        ),
        (
            "gradPurple",
            PPT_PALETTE["purple_fill_start"],
            PPT_PALETTE["purple_fill_end"],
        ),
        ("gradRed", PPT_PALETTE["red_fill_start"], PPT_PALETTE["red_fill_end"]),
    ]
    lines = []
    for gid, start, end in gradients:
        lines.append(
            f'    <linearGradient id="{gid}" x1="0%" y1="0%" x2="0%" y2="100%">'
        )
        lines.append(f'      <stop offset="0%" stop-color="{start}"/>')
        lines.append(f'      <stop offset="100%" stop-color="{end}"/>')
        lines.append(f"    </linearGradient>")
    return "\n".join(lines)


def get_shadow_filter() -> str:
    """Generate SVG <filter> for PPT-style drop shadow."""
    return (
        '    <filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">\n'
        '      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="#000000" flood-opacity="0.12"/>\n'
        "    </filter>"
    )
