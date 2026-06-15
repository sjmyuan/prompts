# Create Chart — Detailed Steps

Applies **create-chart** in the svg-editor skill.

**Steps**:
1. **Identify chart type and data**: Determine if user wants bar, line, pie, area, or scatter chart. Extract data series (labels and values).
2. **Build JSON**: Use `diagram_type: "chart"`. Define nodes as chart elements and edges as connections where needed. The script handles positioning; chart-specific rendering (axes, bars, pie slices) is constructed manually from computed positions.
3. **Run compute_all.py**: Execute `python3 scripts/compute_all.py '<json>'`. Use output for viewBox and overall layout guidance.
4. **Render chart elements manually** (charts have specific visual shapes not fully covered by generic node types):
   - **Bar chart**: Draw `<rect>` for each bar. Bar width = (category width / bars in group) × 0.7. Grouped bars use fills from `colors.PPT_PALETTE`.
   - **Line chart**: Draw `<polyline>` or `<path>` connecting data points. Add `<circle>` markers.
   - **Pie chart**: Draw each slice as `<path>` arc. Add percentage labels outside each slice with leader lines.
   - **Scatter plot**: Draw `<circle>` for each data point.
5. **Add grid and axes**: Draw axis lines, horizontal grid lines at Y tick marks, tick labels, and axis titles using PPT-standard colors from `colors.PPT_PALETTE`.
6. **Add legend** (required for multi-series): Place in top-right or bottom-center. Each item: 12×12px colored rect + text label.
7. **Output**: Return raw, valid SVG code.
