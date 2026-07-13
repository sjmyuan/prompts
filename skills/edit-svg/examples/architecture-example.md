# Example: Three-Tier Web Application Architecture

**Scenario**: A user asks to create an architecture diagram for a three-tier web application with Client, API Gateway, Application Services, and Database layers.

**Trigger**: "Create an architecture diagram for a three-tier web app: Browser → CDN → Load Balancer → API Gateway → Auth Service + Business Service → PostgreSQL Database + Redis Cache."

**Applies**: **create-scripted-diagram** (architecture variant)

---

## Input

Create an architecture diagram showing:
- Client layer: Browser, Mobile App
- Edge layer: CDN, Load Balancer
- Application layer: API Gateway, Auth Service, Business Service
- Data layer: PostgreSQL, Redis Cache
- Communication flows from top to bottom

## Output

```svg
<svg viewBox="0 0 900 700" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#546E7A"/>
    </marker>
    <marker id="arrow-dashed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#78909C"/>
    </marker>
    <!-- Shadow filter -->
    <filter id="shadow" x="-5%" y="-5%" width="115%" height="115%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.1"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="900" height="700" fill="#FAFAFA"/>

  <!-- ========== LAYER 1: Client Layer ========== -->
  <!-- Layer background -->
  <rect x="20" y="20" width="860" height="100" rx="6" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="1"/>
  <rect x="20" y="20" width="860" height="28" rx="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="1"/>
  <rect x="20" y="42" width="860" height="6" fill="#E3F2FD"/>
  <text x="40" y="38" font-family="Arial, sans-serif" font-size="13" fill="#1565C0" font-weight="bold">Client Layer</text>

  <!-- Browser -->
  <rect x="120" y="60" width="160" height="45" rx="6" ry="6" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="200" y="82" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">🌐 Web Browser</text>

  <!-- Mobile App -->
  <rect x="520" y="60" width="160" height="45" rx="6" ry="6" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="600" y="82" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">📱 Mobile App</text>

  <!-- ========== LAYER 2: Edge Layer ========== -->
  <rect x="20" y="145" width="860" height="100" rx="6" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="1"/>
  <rect x="20" y="145" width="860" height="28" rx="6" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1"/>
  <rect x="20" y="167" width="860" height="6" fill="#E8F5E9"/>
  <text x="40" y="163" font-family="Arial, sans-serif" font-size="13" fill="#2E7D32" font-weight="bold">Edge / Infrastructure Layer</text>

  <!-- CDN -->
  <rect x="80" y="185" width="130" height="45" rx="6" ry="6" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="145" y="207" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121">CDN</text>

  <!-- Load Balancer -->
  <rect x="370" y="185" width="160" height="45" rx="6" ry="6" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="207" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121">Load Balancer</text>

  <!-- ========== LAYER 3: Application Layer ========== -->
  <rect x="20" y="270" width="860" height="180" rx="6" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="1"/>
  <rect x="20" y="270" width="860" height="28" rx="6" fill="#FFF3E0" stroke="#E65100" stroke-width="1"/>
  <rect x="20" y="292" width="860" height="6" fill="#FFF3E0"/>
  <text x="40" y="288" font-family="Arial, sans-serif" font-size="13" fill="#E65100" font-weight="bold">Application Layer</text>

  <!-- API Gateway -->
  <rect x="320" y="310" width="260" height="45" rx="6" ry="6" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="332" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121" font-weight="bold">API Gateway</text>

  <!-- Auth Service -->
  <rect x="100" y="385" width="180" height="50" rx="6" ry="6" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="190" y="407" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121">Auth Service</text>

  <!-- Business Service -->
  <rect x="380" y="385" width="200" height="50" rx="6" ry="6" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="480" y="407" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121">Business Service</text>

  <!-- Notification Service -->
  <rect x="680" y="385" width="180" height="50" rx="6" ry="6" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="770" y="407" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121">Notification Service</text>

  <!-- ========== LAYER 4: Data Layer ========== -->
  <rect x="20" y="475" width="860" height="200" rx="6" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="1"/>
  <rect x="20" y="475" width="860" height="28" rx="6" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="1"/>
  <rect x="20" y="497" width="860" height="6" fill="#F3E5F5"/>
  <text x="40" y="493" font-family="Arial, sans-serif" font-size="13" fill="#7B1FA2" font-weight="bold">Data Layer</text>

  <!-- PostgreSQL -->
  <g transform="translate(120, 545)">
    <ellipse cx="90" cy="15" rx="90" ry="15" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5"/>
    <rect x="0" y="15" width="180" height="50" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5"/>
    <ellipse cx="90" cy="65" rx="90" ry="15" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5"/>
    <rect x="0" y="15" width="180" height="50" fill="#E3F2FD" opacity="0.5"/>
    <text x="90" y="47" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121" font-weight="bold">PostgreSQL</text>
  </g>

  <!-- Redis -->
  <g transform="translate(530, 545)">
    <ellipse cx="70" cy="15" rx="70" ry="15" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5"/>
    <rect x="0" y="15" width="140" height="50" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5"/>
    <ellipse cx="70" cy="65" rx="70" ry="15" fill="#FFFFFF" stroke="#37474F" stroke-width="1.5"/>
    <rect x="0" y="15" width="140" height="50" fill="#FFF3E0" opacity="0.5"/>
    <text x="70" y="47" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121" font-weight="bold">Redis Cache</text>
  </g>

  <!-- ========== CONNECTIONS ========== -->

  <!-- Browser → CDN -->
  <path d="M 200 105 L 200 130 L 145 130 L 145 185" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <!-- Browser → Load Balancer -->
  <path d="M 200 105 L 200 130 L 450 130 L 450 185" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <!-- Mobile → Load Balancer -->
  <path d="M 600 105 L 600 130 L 450 130" stroke="#78909C" stroke-width="2" fill="none"/>

  <!-- CDN → Load Balancer -->
  <path d="M 210 207 L 370 207" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <!-- Load Balancer → API Gateway -->
  <path d="M 450 230 L 450 310" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <!-- API Gateway → Auth Service -->
  <path d="M 380 355 C 340 355, 280 370, 280 385" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <rect x="316" y="365" width="28" height="16" rx="3" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1"/>
  <text x="330" y="376" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="9" fill="#546E7A">/auth</text>

  <!-- API Gateway → Business Service -->
  <path d="M 450 355 L 450 385" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <rect x="458" y="366" width="40" height="16" rx="3" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1"/>
  <text x="478" y="377" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="9" fill="#546E7A">/api/*</text>

  <!-- API Gateway → Notification Service -->
  <path d="M 580 355 C 620 355, 680 370, 770 385" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
  <rect x="656" y="365" width="28" height="16" rx="3" fill="#FFFFFF" stroke="#90A4AE" stroke-width="1"/>
  <text x="670" y="376" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="9" fill="#546E7A">/notify</text>

  <!-- Business Service → PostgreSQL -->
  <path d="M 380 435 C 340 460, 300 530, 300 570" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <!-- Business Service → Redis -->
  <path d="M 580 410 L 600 410 L 600 570" stroke="#546E7A" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

  <!-- Auth Service → PostgreSQL -->
  <path d="M 280 435 C 300 500, 300 530, 300 570" stroke="#78909C" stroke-width="2" stroke-dasharray="6,4" fill="none" marker-end="url(#arrow-dashed)"/>

  <!-- Legend -->
  <rect x="680" y="660" width="12" height="12" fill="#546E7A"/>
  <text x="698" y="670" font-family="Arial, sans-serif" font-size="11" fill="#424242">Synchronous</text>
  <path d="M 770 666 L 810 666" stroke="#78909C" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="818" y="670" font-family="Arial, sans-serif" font-size="11" fill="#424242">Async / Event</text>
</svg>
```
