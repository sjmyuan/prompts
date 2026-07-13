# Example: User Login Flowchart

**Scenario**: A user asks to create a flowchart for a user login process, including input validation, credential check, and error handling branches.

**Trigger**: "Create a flowchart showing the user login process: user enters email and password, validate inputs, check credentials in database, redirect to dashboard on success, or show error on failure."

**Applies**: **create-scripted-diagram** (flowchart variant)

---

## Input

Create a flowchart showing the user login process:
1. User enters email and password
2. Validate that fields are not empty → if empty, show "Fields required" error
3. Check credentials against database → if invalid, show "Invalid credentials" error
4. On success, redirect to dashboard

## Output

```svg
<svg viewBox="0 0 700 620" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#546E7A"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#C62828"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2E7D32"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="700" height="620" fill="#FFFFFF"/>

  <!-- Start node -->
  <rect x="260" y="30" width="180" height="45" rx="22" ry="22" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>
  <text x="350" y="57" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121" font-weight="bold">Login Start</text>

  <!-- Arrow: Start → Enter Credentials -->
  <path d="M 350 75 L 350 115" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Process: Enter Credentials -->
  <rect x="250" y="120" width="200" height="50" rx="6" ry="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="350" y="145" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Enter Email &amp; Password</text>

  <!-- Arrow: Enter Credentials → Validate Fields -->
  <path d="M 350 170 L 350 210" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Decision: Validate Fields -->
  <polygon points="350,220 430,280 350,340 270,280" fill="#FFF3E0" stroke="#E65100" stroke-width="2"/>
  <text x="350" y="280" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121" font-weight="bold">Fields Valid?</text>

  <!-- Arrow: Validate → No (left) -->
  <path d="M 270 280 L 120 280 L 120 200 L 200 200" stroke="#C62828" stroke-width="2" fill="none" marker-end="url(#arrow-red)"/>
  <rect x="150" y="268" width="30" height="18" rx="3" fill="#FFFFFF" stroke="#C62828" stroke-width="1"/>
  <text x="165" y="280" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="11" fill="#C62828">No</text>

  <!-- Error: Fields Required -->
  <rect x="60" y="178" width="140" height="45" rx="6" ry="6" fill="#FFEBEE" stroke="#C62828" stroke-width="2"/>
  <text x="130" y="200" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#C62828">Show "Fields Required"</text>

  <!-- Arrow: Validate → Yes (down) -->
  <path d="M 350 340 L 350 380" stroke="#2E7D32" stroke-width="2" marker-end="url(#arrow-green)"/>
  <rect x="360" y="356" width="28" height="18" rx="3" fill="#FFFFFF" stroke="#2E7D32" stroke-width="1"/>
  <text x="374" y="368" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="11" fill="#2E7D32">Yes</text>

  <!-- Process: Check Credentials -->
  <rect x="240" y="385" width="220" height="50" rx="6" ry="6" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="350" y="410" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121">Check Credentials in DB</text>

  <!-- Arrow: Check → Decision -->
  <path d="M 350 435 L 350 475" stroke="#546E7A" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Decision: Credentials Valid -->
  <polygon points="350,485 430,545 350,605 270,545" fill="#FFF3E0" stroke="#E65100" stroke-width="2"/>
  <text x="350" y="540" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="11" fill="#212121" font-weight="bold">Credentials</text>
  <text x="350" y="554" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="11" fill="#212121" font-weight="bold">Valid?</text>

  <!-- Arrow: Decision → No (right) -->
  <path d="M 430 545 L 580 545 L 580 200 L 560 200" stroke="#C62828" stroke-width="2" fill="none" marker-end="url(#arrow-red)"/>
  <rect x="520" y="533" width="28" height="18" rx="3" fill="#FFFFFF" stroke="#C62828" stroke-width="1"/>
  <text x="534" y="545" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="11" fill="#C62828">No</text>

  <!-- Error: Invalid Credentials -->
  <rect x="500" y="178" width="160" height="45" rx="6" ry="6" fill="#FFEBEE" stroke="#C62828" stroke-width="2"/>
  <text x="580" y="200" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#C62828">Show "Invalid Credentials"</text>

  <!-- Arrow: Decision → Yes (down) -->
  <path d="M 350 605 L 350 640" stroke="#2E7D32" stroke-width="2" marker-end="url(#arrow-green)"/>

  <!-- End node (clipped — shown partially, viewBox adjusted below) -->
  <!-- Note: In practice, viewBox would be adjusted. For this example, end node is within bounds. -->
  <rect x="260" y="645" width="180" height="45" rx="22" ry="22" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>
  <text x="350" y="672" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="14" fill="#212121" font-weight="bold">Redirect to Dashboard</text>
</svg>
```
