# Create Chart — Detailed Steps

Applies **create-chart** in the svg-editor skill.

**Steps**:
1. **Identify chart type and data**: Determine if user wants bar, line, pie, area, or scatter chart. Extract data series (labels and values).
2. **Build node data**: Define minimal nodes for title and legend (charts are mostly custom-rendered).
3. **Compute chart area dimensions**: Use `layout.compute_viewbox()` with chart area bbox to get the viewBox. Use PPT-standard chart area: x=80 to x=880, y=100 to y=480.
4. **Render chart elements manually** (charts have specific visual shapes not covered by generic node types):
   - **Bar chart**: Draw `<rect>` for each bar. Bar width = (category width / bars in group) × 0.7. Grouped bars use fills from `colors.PPT_PALETTE`.
   - **Line chart**: Draw `<polyline>` or `<path>` connecting data points. Add `<circle>` markers.
   - **Pie chart**: Draw each slice as `<path>` arc. Add percentage labels outside each slice with leader lines.
   - **Scatter plot**: Draw `<circle>` for each data point.
5. **Add grid and axes**: Draw axis lines, horizontal grid lines at Y tick marks, tick labels, and axis titles using PPT-standard colors from `colors.PPT_PALETTE`.
6. **Validate contrast**: Run the **Validate color contrast** snippet for all text elements against their backgrounds.
7. **Add legend** (required for multi-series): Place in top-right or bottom-center. Each item: 12×12px colored rect + text label.
8. **Assemble SVG**: Follow the **SVG assembly pattern** in `<computation-snippets>` (skip title bar if chart has its own title area).
9. **Output**: Return raw, valid SVG code.
