# Create Chart — Detailed Steps

Applies **create-chart** in the svg-editor skill.

**Steps**:
0. **Use `chart_builder` — do NOT write chart SVG manually.** `chart_builder` (backed by matplotlib) generates a complete, PPT-styled SVG for bar, line, and pie charts in one call.
1. **Identify chart type and data**: Determine if user wants bar, line, or pie chart. Extract categories, series, and a title.
2. **Call the appropriate `chart_builder` function** and print the result:
   ```bash
   # Bar chart
   python3 -c "
   import sys; sys.path.insert(0, 'scripts')
   from chart_builder import render_bar_chart
   print(render_bar_chart(['Q1','Q2','Q3','Q4'], [120,145,98,175], 'Quarterly Revenue', ylabel='USD (k)'))
   "

   # Line chart
   python3 -c "
   import sys; sys.path.insert(0, 'scripts')
   from chart_builder import render_line_chart
   series = [{'label': 'Revenue', 'values': [120,145,98,175]}, {'label': 'Cost', 'values': [80,90,85,95]}]
   print(render_line_chart(['Q1','Q2','Q3','Q4'], series, 'Revenue vs Cost', ylabel='USD (k)'))
   "

   # Pie chart
   python3 -c "
   import sys; sys.path.insert(0, 'scripts')
   from chart_builder import render_pie_chart
   print(render_pie_chart(['APAC','EMEA','AMER'], [35,28,37], 'Revenue by Region'))
   "
   ```
3. **Output**: Return the SVG string produced by `chart_builder`. No manual assembly is needed.
