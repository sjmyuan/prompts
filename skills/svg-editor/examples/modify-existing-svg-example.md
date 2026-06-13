# Example: Editing an Existing SVG — Style and Content Updates

**Scenario**: A user has an existing SVG diagram of a simple CI/CD pipeline and wants to update its appearance — change the color scheme from blue/orange to a modern teal/purple palette, update the "Deploy" stage text to "Deploy & Release", and add a new "Security Scan" step between "Test" and "Deploy".

**Trigger**: "I have this CI/CD pipeline SVG. Can you change the colors to teal and purple, update 'Deploy' to say 'Deploy & Release', and add a 'Security Scan' step between Test and Deploy?"

**Applies**: **modify-existing-svg**

---

## Input

The user provides this existing SVG:

```svg
<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#546E7A"/>
    </marker>
  </defs>

  <rect x="40" y="100" width="140" height="60" rx="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="110" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Code Commit</text>

  <path d="M 180 130 L 240 130" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <rect x="240" y="100" width="140" height="60" rx="6" fill="#FFF3E0" stroke="#E65100" stroke-width="2"/>
  <text x="310" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Build</text>

  <path d="M 380 130 L 440 130" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <rect x="440" y="100" width="140" height="60" rx="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="510" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Test</text>

  <path d="M 580 130 L 640 130" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <rect x="640" y="100" width="140" height="60" rx="6" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>
  <text x="710" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Deploy</text>
</svg>
```

## Modification Plan (Internal)

### Step 1-2: Parse and understand

| Element | Current style | Requested change |
|---|---|---|
| Code Commit | Fill `#E3F2FD`, Stroke `#1565C0` (blue) | → Teal palette |
| Build | Fill `#FFF3E0`, Stroke `#E65100` (orange) | → Purple palette |
| Test | Fill `#E3F2FD`, Stroke `#1565C0` (blue) | → Teal palette |
| Deploy | Fill `#E8F5E9`, Stroke `#2E7D32` (green) | → Teal palette (to be moved) |
| New "Security Scan" | — | Insert between Test and Deploy |
| Arrows | Stroke `#546E7A` (blue-grey) | → Match new palette |
| Label "Deploy" | → Change to "Deploy & Release" | Text update |

### Step 3-4: Apply modifications

1. **Color scheme change**: Teal (`#E0F2F1` / `#00897B`) for process steps, Purple (`#F3E5F5` / `#7B1FA2`) for distinct stages
2. **Reposition elements**: Insert "Security Scan" between Test and Deploy
   - Original positions: Test ends at x=580, Deploy starts at x=640
   - Shift Deploy right by 160px (to x=800) to make room
   - Place "Security Scan" at x=640 with same dimensions
3. **Add new connection arrows**: Test → Security Scan, Security Scan → Deploy
4. **Update text**: Change "Deploy" label

## Expected Output

```svg
<svg viewBox="0 0 960 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#00897B"/>
    </marker>
  </defs>

  <!-- Code Commit (teal) -->
  <rect x="40" y="100" width="140" height="60" rx="6" fill="#E0F2F1" stroke="#00897B" stroke-width="2"/>
  <text x="110" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Code Commit</text>

  <path d="M 180 130 L 240 130" stroke="#00897B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Build (purple — distinct stage) -->
  <rect x="240" y="100" width="140" height="60" rx="6" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2"/>
  <text x="310" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Build</text>

  <path d="M 380 130 L 440 130" stroke="#00897B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Test (teal) -->
  <rect x="440" y="100" width="140" height="60" rx="6" fill="#E0F2F1" stroke="#00897B" stroke-width="2"/>
  <text x="510" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Test</text>

  <path d="M 580 130 L 640 130" stroke="#00897B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- NEW: Security Scan (teal) -->
  <rect x="640" y="100" width="140" height="60" rx="6" fill="#E0F2F1" stroke="#00897B" stroke-width="2"/>
  <text x="710" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Security Scan</text>

  <path d="M 780 130 L 800 130" stroke="#00897B" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Deploy & Release (teal, shifted right) -->
  <rect x="800" y="100" width="140" height="60" rx="6" fill="#E0F2F1" stroke="#00897B" stroke-width="2"/>
  <text x="870" y="135" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Deploy &amp; Release</text>
</svg>
```

## Summary of Changes

| Change | Details |
|---|---|
| Color palette | Blue/orange/green → teal (`#00897B`) / purple (`#7B1FA2`) theme |
| Text update | "Deploy" → "Deploy & Release" |
| New element | Added "Security Scan" step (teal, 140×60) between Test and Deploy |
| Layout shift | Deploy shifted right from x=640 to x=800 to accommodate new step |
| New connections | Added arrows: Test → Security Scan, Security Scan → Deploy |
| viewBox expanded | 800×300 → 960×300 to fit all elements with adequate padding |
| Arrow color updated | `#546E7A` → `#00897B` to match new palette |
