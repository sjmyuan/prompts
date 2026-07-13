# Charts — API Reference

Applies **create-scripted-diagram** in the edit-svg skill.

`chart_builder` (backed by matplotlib) generates a complete, PPT-styled SVG for bar, line, and pie charts in one call.

## API

```bash
# Bar chart
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from chart_builder import render_bar_chart
print(render_bar_chart(['Q1','Q2','Q3','Q4'], [120,145,98,175], 'Quarterly Revenue', ylabel='USD (k)'))
"

# Line chart (multi-series)
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

**Output**: Return the SVG string directly. No manual assembly needed.
