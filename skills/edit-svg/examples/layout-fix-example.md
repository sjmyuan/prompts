# Example: Fixing Overlapping Elements in a Network Topology SVG

**Scenario**: A user provides an existing SVG diagram of a network topology where elements overlap, connection lines pass through shapes, and text extends beyond its container bounds.

**Trigger**: "The SVG diagram I have has overlapping boxes and the connection lines go through the middle of other boxes. Can you fix the layout?"

**Applies**: **modify-existing-svg** (layout fix variant)

---

## Input

The user provides this SVG with layout issues:

```svg
<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#546E7A"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="160" height="50" rx="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="100" y="50" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="14" fill="#212121">Web Server</text>

  <rect x="30" y="100" width="160" height="50" rx="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="110" y="130" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="14" fill="#212121">Application Server</text>

  <rect x="300" y="20" width="160" height="50" rx="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="380" y="50" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="14" fill="#212121">Database Server</text>

  <rect x="10" y="190" width="200" height="50" rx="6" fill="#FFF3E0" stroke="#E65100" stroke-width="2"/>
  <text x="110" y="220" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="14" fill="#212121">Load Balancer</text>

  <!-- Issues: Line from Web Server to App Server passes through overlap zone -->
  <path d="M 100 70 L 100 100" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Issue: Line connecting across with no clear routing -->
  <path d="M 180 45 L 300 45" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Issue: Line goes through other elements -->
  <path d="M 110 150 L 110 190" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Issue: Overlapping text/label -->
  <text x="220" y="130" text-anchor="middle" font-family="Arial" font-size="11" fill="#C62828">This label overlaps with other elements</text>
</svg>
```

## Analysis (What the capability produces internally)

### Step 1-3: Bounding box and overlap detection

| Element | Bounding box | Issues |
|---|---|---|
| Web Server | (20,20) 160×50 | — |
| Application Server | (30,100) 160×50 | Overlaps with Web Server in X-axis (30..180 vs 20..180), too close vertically |
| Database Server | (300,20) 160×50 | — |
| Load Balancer | (10,190) 200×50 | Overlaps with Application Server in X-axis (10..210 vs 30..190) |
| "This label..." | (220,120) ~180×20 | Extends into Application Server and Database Server space |

### Step 4-5: Fix strategy

1. **Increase vertical spacing**: Push Application Server down from y=100 to y=130
2. **Reposition Load Balancer**: Center it below both servers, shift to x=150
3. **Move overlapping label**: Remove inline label, connection label should use bg rect
4. **Re-route connections**: Use orthogonal routing to avoid crossings

## Fixed Output

```svg
<svg viewBox="0 0 600 450" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#546E7A"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2E7D32"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="600" height="450" fill="#FFFFFF"/>

  <!-- ========== TIER 1: Web Tier ========== -->
  <rect x="20" y="20" width="860" height="28" rx="4" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="1"/>
  <text x="35" y="38" font-family="Arial, sans-serif" font-size="12" fill="#757575" font-weight="bold">Web Tier</text>

  <rect x="150" y="55" width="180" height="50" rx="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="240" y="85" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Web Server</text>

  <!-- ========== TIER 2: Application Tier ========== -->
  <rect x="20" y="130" width="860" height="28" rx="4" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="1"/>
  <text x="35" y="148" font-family="Arial, sans-serif" font-size="12" fill="#757575" font-weight="bold">Application Tier</text>

  <rect x="150" y="165" width="180" height="50" rx="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="240" y="195" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Application Server</text>

  <!-- ========== TIER 3: Data Tier ========== -->
  <rect x="20" y="250" width="860" height="28" rx="4" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="1"/>
  <text x="35" y="268" font-family="Arial, sans-serif" font-size="12" fill="#757575" font-weight="bold">Data Tier</text>

  <rect x="150" y="285" width="180" height="50" rx="6" fill="#FFF3E0" stroke="#E65100" stroke-width="2"/>
  <text x="240" y="315" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Database Server</text>

  <!-- ========== LOAD BALANCER ========== -->
  <rect x="370" y="165" width="200" height="50" rx="6" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>
  <text x="470" y="195" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Load Balancer</text>

  <!-- ========== CONNECTIONS (orthogonal, no overlaps) ========== -->
  <!-- Web → App -->
  <path d="M 240 105 L 240 165" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- App → DB -->
  <path d="M 240 215 L 240 285" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Web → Load Balancer -->
  <path d="M 330 80 L 370 80 L 370 190" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <rect x="340" y="175" width="30" height="16" rx="3" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1"/>
  <text x="355" y="186" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="9" fill="#546E7A">traffic</text>

  <!-- App → Load Balancer (bidirectional) -->
  <path d="M 330 190 L 370 190" stroke="#2E7D32" stroke-width="2" marker-end="url(#arrow-green)"/>
  <rect x="340" y="183" width="24" height="16" rx="3" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1"/>
  <text x="352" y="194" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="9" fill="#2E7D32">health</text>

  <!-- Load Balancer → DB (via App tier) -->
  <path d="M 470 215 L 470 250 L 330 250 L 330 285" stroke="#78909C" stroke-width="2" stroke-dasharray="6,4" fill="none" marker-end="url(#arrow)"/>
  <rect x="380" y="243" width="80" height="16" rx="3" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1"/>
  <text x="420" y="254" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="9" fill="#78909C">read-replica</text>
</svg>
```
