# Example: Quarterly Sales Bar Chart

**Scenario**: A user asks to create a grouped bar chart showing quarterly sales data for two product categories across four quarters.

**Trigger**: "Create a bar chart showing quarterly sales for 2025: Q1=120, Q2=195, Q3=165, Q4=210 for Product A and Q1=80, Q2=110, Q3=145, Q4=170 for Product B."

**Applies**: **create-chart**

---

## Input

Create a grouped bar chart for 2025 quarterly sales:
- Product A: Q1=120, Q2=195, Q3=165, Q4=210
- Product B: Q1=80, Q2=110, Q3=145, Q4=170
- Title: "2025 Quarterly Sales by Product"

## Output

```svg
<svg viewBox="0 0 700 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="shadow-bar" x="-5%" y="-5%" width="120%" height="120%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.1"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="700" height="500" fill="#FFFFFF"/>

  <!-- Title -->
  <text x="350" y="30" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="#212121" font-weight="bold">2025 Quarterly Sales by Product</text>

  <!-- ========== AXES ========== -->
  <!-- Plot area: x=80 to x=660, y=55 to y=430 -->

  <!-- Y-axis -->
  <line x1="80" y1="55" x2="80" y2="430" stroke="#37474F" stroke-width="2"/>

  <!-- X-axis -->
  <line x1="80" y1="430" x2="660" y2="430" stroke="#37474F" stroke-width="2"/>

  <!-- ========== Y-AXIS GRID & LABELS ========== -->
  <!-- Scale: max value = 250, 5 ticks (0, 50, 100, 150, 200, 250) -->
  <!-- Plot height = 375px, scale = 375/250 = 1.5px per unit -->

  <!-- Y=250 (top) -->
  <line x1="80" y1="55" x2="660" y2="55" stroke="#E0E0E0" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="72" y="59" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#757575">250</text>

  <!-- Y=200 -->
  <line x1="80" y1="130" x2="660" y2="130" stroke="#E0E0E0" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="72" y="134" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#757575">200</text>

  <!-- Y=150 -->
  <line x1="80" y1="205" x2="660" y2="205" stroke="#E0E0E0" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="72" y="209" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#757575">150</text>

  <!-- Y=100 -->
  <line x1="80" y1="280" x2="660" y2="280" stroke="#E0E0E0" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="72" y="284" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#757575">100</text>

  <!-- Y=50 -->
  <line x1="80" y1="355" x2="660" y2="355" stroke="#E0E0E0" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="72" y="359" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#757575">50</text>

  <!-- Y=0 -->
  <line x1="80" y1="430" x2="660" y2="430" stroke="#E0E0E0" stroke-width="1"/>
  <text x="72" y="434" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#757575">0</text>

  <!-- Y-axis label -->
  <text x="25" y="242" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#424242" font-weight="bold" transform="rotate(-90, 25, 242)">Sales (units)</text>

  <!-- ========== BARS ========== -->
  <!-- Category width = 145px per quarter (4 quarters, total 580px / 4 = 145px) -->
  <!-- Each category: 145px wide, bars start at category_x + 20px -->
  <!-- Bar width = 48px, gap between grouped bars = 9px -->

  <!-- Q1: category_x = 95 -->
  <!-- Bar A (120 → y = 430 - 120*1.5 = 250) -->
  <rect x="115" y="250" width="48" height="180" rx="3" fill="#42A5F5" stroke="#1E88E5" stroke-width="1" filter="url(#shadow-bar)"/>
  <text x="139" y="244" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#1E88E5">120</text>

  <!-- Bar B (80 → y = 430 - 80*1.5 = 310) -->
  <rect x="172" y="310" width="48" height="120" rx="3" fill="#EF5350" stroke="#E53935" stroke-width="1" filter="url(#shadow-bar)"/>
  <text x="196" y="304" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#E53935">80</text>

  <text x="155" y="450" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121">Q1</text>

  <!-- Q2: category_x = 240 -->
  <!-- Bar A (195 → y = 430 - 195*1.5 = 137.5) -->
  <rect x="260" y="137" width="48" height="293" rx="3" fill="#42A5F5" stroke="#1E88E5" stroke-width="1" filter="url(#shadow-bar)"/>
  <text x="284" y="131" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#1E88E5">195</text>

  <!-- Bar B (110 → y = 430 - 110*1.5 = 265) -->
  <rect x="317" y="265" width="48" height="165" rx="3" fill="#EF5350" stroke="#E53935" stroke-width="1" filter="url(#shadow-bar)"/>
  <text x="341" y="259" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#E53935">110</text>

  <text x="300" y="450" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121">Q2</text>

  <!-- Q3: category_x = 385 -->
  <!-- Bar A (165 → y = 430 - 165*1.5 = 182.5) -->
  <rect x="405" y="182" width="48" height="248" rx="3" fill="#42A5F5" stroke="#1E88E5" stroke-width="1" filter="url(#shadow-bar)"/>
  <text x="429" y="176" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#1E88E5">165</text>

  <!-- Bar B (145 → y = 430 - 145*1.5 = 212.5) -->
  <rect x="462" y="212" width="48" height="218" rx="3" fill="#EF5350" stroke="#E53935" stroke-width="1" filter="url(#shadow-bar)"/>
  <text x="486" y="206" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#E53935">145</text>

  <text x="445" y="450" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121">Q3</text>

  <!-- Q4: category_x = 530 -->
  <!-- Bar A (210 → y = 430 - 210*1.5 = 115) -->
  <rect x="550" y="115" width="48" height="315" rx="3" fill="#42A5F5" stroke="#1E88E5" stroke-width="1" filter="url(#shadow-bar)"/>
  <text x="574" y="109" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#1E88E5">210</text>

  <!-- Bar B (170 → y = 430 - 170*1.5 = 175) -->
  <rect x="607" y="175" width="48" height="255" rx="3" fill="#EF5350" stroke="#E53935" stroke-width="1" filter="url(#shadow-bar)"/>
  <text x="631" y="169" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#E53935">170</text>

  <text x="590" y="450" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#212121">Q4</text>

  <!-- ========== LEGEND ========== -->
  <rect x="510" y="50" width="140" height="50" rx="4" fill="#FAFAFA" stroke="#E0E0E0" stroke-width="1"/>
  <rect x="518" y="60" width="14" height="14" rx="2" fill="#42A5F5"/>
  <text x="538" y="71" font-family="Arial, sans-serif" font-size="11" fill="#424242">Product A</text>
  <rect x="518" y="80" width="14" height="14" rx="2" fill="#EF5350"/>
  <text x="538" y="91" font-family="Arial, sans-serif" font-size="11" fill="#424242">Product B</text>
</svg>
```
