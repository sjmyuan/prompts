"""
Chart SVG generation using matplotlib.

Install: pip install matplotlib

Use for bar, line, and pie charts instead of writing chart SVG paths manually.
Each function returns a complete SVG string ready to embed or save standalone.
"""

import io
from typing import List, Dict, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# PPT color sequence (matches colors.PPT_PALETTE)
PPT_COLORS = [
    "#4472C4",
    "#ED7D31",
    "#A5A5A5",
    "#FFC000",
    "#70AD47",
    "#255E91",
    "#9DC3E6",
    "#F4B183",
    "#FFD966",
    "#C9E0B4",
]


def _apply_ppt_style(ax, title: str, xlabel: str, ylabel: str) -> None:
    """Apply PPT-consistent styling to a matplotlib axes object."""
    ax.set_title(title, fontsize=20, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=11)


def _fig_to_svg(fig) -> str:
    """Serialize a matplotlib Figure to an SVG string and close it."""
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()


def render_bar_chart(
    categories: List[str],
    values: List[float],
    title: str,
    xlabel: str = "",
    ylabel: str = "",
    colors: Optional[List[str]] = None,
    figsize: tuple = (9.6, 5.4),
) -> str:
    """Render a bar chart and return the complete SVG string."""
    fig, ax = plt.subplots(figsize=figsize)
    bar_colors = (colors or PPT_COLORS)[: len(values)]
    bars = ax.bar(categories, values, color=bar_colors, width=0.6)
    ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=11)
    _apply_ppt_style(ax, title, xlabel, ylabel)
    return _fig_to_svg(fig)


def render_line_chart(
    x_values: List,
    y_series: List[Dict],
    title: str,
    xlabel: str = "",
    ylabel: str = "",
    figsize: tuple = (9.6, 5.4),
) -> str:
    """Render a multi-series line chart and return the complete SVG string.

    y_series format: [{"label": "Series A", "values": [1, 2, 3]}, ...]
    """
    fig, ax = plt.subplots(figsize=figsize)
    for i, series in enumerate(y_series):
        ax.plot(
            x_values,
            series["values"],
            label=series["label"],
            color=PPT_COLORS[i % len(PPT_COLORS)],
            linewidth=2,
            marker="o",
            markersize=5,
        )
    if len(y_series) > 1:
        ax.legend(fontsize=11)
    _apply_ppt_style(ax, title, xlabel, ylabel)
    return _fig_to_svg(fig)


def render_pie_chart(
    labels: List[str],
    values: List[float],
    title: str,
    colors: Optional[List[str]] = None,
    figsize: tuple = (9.6, 5.4),
) -> str:
    """Render a pie chart and return the complete SVG string."""
    fig, ax = plt.subplots(figsize=figsize)
    pie_colors = (colors or PPT_COLORS)[: len(values)]
    ax.pie(
        values,
        labels=labels,
        colors=pie_colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        textprops={"fontsize": 11},
    )
    ax.set_title(title, fontsize=20, fontweight="bold", pad=12)
    return _fig_to_svg(fig)
