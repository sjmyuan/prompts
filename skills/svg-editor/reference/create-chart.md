# Create Chart — Detailed Steps

Applies **create-chart** in the svg-editor skill.

**Steps**:
1. **Identify chart type and data**: Determine whether the user wants a bar chart (vertical/horizontal/stacked/grouped), line chart, pie chart, area chart, or scatter plot. Extract data series (labels and values).
2. **Plan axes and grid**:
   - **Bar/Line charts**: X-axis = categories, Y-axis = values. Compute Y-axis scale (max value rounded up to a clean number, with 4–6 tick marks). Reserve 60–80px for Y-axis labels on the left and 40px for X-axis labels at the bottom.
   - **Pie charts**: No axes. Center the pie in the available space. Pie radius = min(width, height) / 2 - 40px.
   - **Drawing area**: Subtract axis margins to get the inner plotting area.
3. **Draw grid and axes**:
   - Draw X and Y axis lines (solid, `#37474F`, stroke-width=2).
   - Draw horizontal grid lines at each Y tick mark (dashed or very light `#E0E0E0`, stroke-width=1).
   - Add tick labels for Y-axis (right-aligned, font-size=12px) and X-axis (centered under each category, font-size=12px).
   - Add axis titles if needed (font-size=14px, bold).
4. **Render data**:
   - **Bar chart**: Draw `<rect>` for each bar. Bar width = (category width / number of bars in group) × 0.7. Grouped bars use different fills from `<color-palettes>` in SKILL.md.
   - **Line chart**: Draw `<polyline>` or `<path>` connecting data points. Add `<circle>` markers at each data point. Fill area under the line for area charts using `<polygon>` with opacity=0.15.
   - **Pie chart**: Draw each slice as a `<path>` arc. Compute start/end angles proportionally. Add slice labels with percentage values outside each slice, connected by a short line leader.
   - **Scatter plot**: Draw `<circle>` for each data point. Use color to distinguish series.
5. **Add legend** (required for multi-series charts):
   - Place legend in top-right corner or bottom-center below the chart.
   - Each legend item: colored rectangle (12×12px) + text label, arranged horizontally or vertically.
6. **Set viewBox** and output raw SVG.
