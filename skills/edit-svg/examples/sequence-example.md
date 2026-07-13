# Example: User Registration Sequence Diagram

**Scenario**: A user asks to create a sequence diagram for a user registration flow showing interactions between the client, auth service, database, and email service.

**Trigger**: "Create a sequence diagram for user registration: Client → Auth Service → validate input → DB (check if email exists) → DB (create user) → Email Service (send verification email) → return success."

**Applies**: **create-sequence-diagram**

---

## Input

Create a sequence diagram for user registration:
- Participants: Client, Auth Service, Database, Email Service
- Messages:
  1. Client → Auth Service: POST /register (email, password)
  2. Auth Service → Auth Service: Validate input
  3. Auth Service → Database: SELECT check email exists
  4. Database → Auth Service: return (not found)
  5. Auth Service → Database: INSERT new user
  6. Database → Auth Service: return (user created)
  7. Auth Service → Email Service: send verification email (async)
  8. Email Service → Auth Service: email queued (async return)
  9. Auth Service → Client: 201 Created + token

## Output

```svg
<svg viewBox="0 0 850 520" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-solid" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#1565C0"/>
    </marker>
    <marker id="arrow-open" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="none" stroke="#1565C0" stroke-width="1.5"/>
      <path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="#1565C0" stroke-width="1.5"/>
    </marker>
    <marker id="arrow-return" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="none" stroke="#78909C" stroke-width="1.5"/>
      <path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="#78909C" stroke-width="1.5"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="850" height="520" fill="#FFFFFF"/>

  <!-- ========== PARTICIPANTS (Header) ========== -->

  <!-- Client -->
  <rect x="50" y="20" width="120" height="40" rx="4" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="110" y="45" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121" font-weight="bold">Client</text>
  <!-- Lifeline -->
  <line x1="110" y1="60" x2="110" y2="480" stroke="#90A4AE" stroke-width="1.5" stroke-dasharray="6,4"/>

  <!-- Auth Service -->
  <rect x="240" y="20" width="150" height="40" rx="4" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="315" y="45" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121" font-weight="bold">Auth Service</text>
  <!-- Lifeline -->
  <line x1="315" y1="60" x2="315" y2="480" stroke="#90A4AE" stroke-width="1.5" stroke-dasharray="6,4"/>

  <!-- Database -->
  <rect x="470" y="20" width="120" height="40" rx="4" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="530" y="45" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121" font-weight="bold">Database</text>
  <!-- Lifeline -->
  <line x1="530" y1="60" x2="530" y2="480" stroke="#90A4AE" stroke-width="1.5" stroke-dasharray="6,4"/>

  <!-- Email Service -->
  <rect x="660" y="20" width="150" height="40" rx="4" fill="#E3F2FD" stroke="#1565C0" stroke-width="2"/>
  <text x="735" y="45" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="13" fill="#212121" font-weight="bold">Email Service</text>
  <!-- Lifeline -->
  <line x1="735" y1="60" x2="735" y2="480" stroke="#90A4AE" stroke-width="1.5" stroke-dasharray="6,4"/>

  <!-- ========== MESSAGES ========== -->

  <!-- 1. Client → Auth Service: POST /register -->
  <line x1="110" y1="90" x2="305" y2="90" stroke="#1565C0" stroke-width="2" marker-end="url(#arrow-solid)"/>
  <text x="207" y="82" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#1565C0">POST /register</text>
  <!-- Activation: Auth Service -->
  <rect x="309" y="90" width="12" height="120" fill="#BBDEFB" stroke="#1565C0" stroke-width="1"/>

  <!-- 2. Auth Service self: Validate input -->
  <path d="M 315 110 L 345 110 L 345 130 L 321 130" stroke="#1565C0" stroke-width="1.5" fill="none" marker-end="url(#arrow-solid)"/>
  <text x="340" y="124" text-anchor="start" font-family="Arial, sans-serif" font-size="10" fill="#546E7A">Validate</text>

  <!-- 3. Auth Service → Database: SELECT check email -->
  <line x1="321" y1="150" x2="520" y2="150" stroke="#1565C0" stroke-width="2" marker-end="url(#arrow-solid)"/>
  <text x="420" y="142" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#1565C0">SELECT email exists</text>
  <!-- Activation: Database -->
  <rect x="524" y="150" width="12" height="40" fill="#BBDEFB" stroke="#1565C0" stroke-width="1"/>

  <!-- 4. Database → Auth Service: not found -->
  <line x1="530" y1="170" x2="327" y2="170" stroke="#78909C" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#arrow-return)"/>
  <text x="428" y="164" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#78909C">not found</text>

  <!-- 5. Auth Service → Database: INSERT user -->
  <line x1="321" y1="190" x2="520" y2="190" stroke="#1565C0" stroke-width="2" marker-end="url(#arrow-solid)"/>
  <text x="420" y="182" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#1565C0">INSERT new user</text>
  <!-- Activation: Database -->
  <rect x="524" y="190" width="12" height="40" fill="#BBDEFB" stroke="#1565C0" stroke-width="1"/>

  <!-- 6. Database → Auth Service: user created -->
  <line x1="530" y1="210" x2="327" y2="210" stroke="#78909C" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#arrow-return)"/>
  <text x="428" y="204" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#78909C">user created</text>

  <!-- 7. Auth Service → Email Service: send verification (async) -->
  <line x1="327" y1="230" x2="725" y2="230" stroke="#1565C0" stroke-width="1.5" marker-end="url(#arrow-open)"/>
  <text x="526" y="222" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#1565C0">send verification email</text>
  <!-- Activation: Email Service -->
  <rect x="729" y="230" width="12" height="40" fill="#BBDEFB" stroke="#1565C0" stroke-width="1"/>

  <!-- 8. Email Service → Auth Service: email queued (async return) -->
  <line x1="735" y1="250" x2="333" y2="250" stroke="#78909C" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#arrow-return)"/>
  <text x="534" y="244" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#78909C">email queued</text>

  <!-- 9. Auth Service → Client: 201 Created -->
  <line x1="321" y1="270" x2="120" y2="270" stroke="#1565C0" stroke-width="2" marker-end="url(#arrow-solid)"/>
  <text x="220" y="262" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#1565C0">201 Created + token</text>

  <!-- ========== ALT FRAME for validation failure ========== -->
  <rect x="30" y="295" width="790" height="70" rx="4" fill="none" stroke="#90A4AE" stroke-width="1.5" stroke-dasharray="4,4"/>
  <rect x="30" y="295" width="50" height="20" rx="3" fill="#90A4AE"/>
  <text x="55" y="309" text-anchor="middle" dominant-baseline="middle" font-family="Arial, sans-serif" font-size="10" fill="#FFFFFF" font-weight="bold">alt</text>
  <text x="90" y="313" font-family="Arial, sans-serif" font-size="11" fill="#546E7A" font-style="italic">[email exists]</text>

  <!-- 9b. Auth Service → Client: 409 Conflict -->
  <line x1="315" y1="335" x2="120" y2="335" stroke="#C62828" stroke-width="1.5" marker-end="url(#arrow-solid)"/>
  <text x="217" y="328" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#C62828">409 Conflict: Email already registered</text>

  <!-- Legend -->
  <rect x="30" y="390" width="800" height="50" fill="#F5F5F5" rx="4"/>
  <line x1="60" y1="410" x2="120" y2="410" stroke="#1565C0" stroke-width="2" marker-end="url(#arrow-solid)"/>
  <text x="130" y="414" font-family="Arial, sans-serif" font-size="11" fill="#424242">Synchronous call</text>
  <line x1="260" y1="410" x2="320" y2="410" stroke="#1565C0" stroke-width="1.5" marker-end="url(#arrow-open)"/>
  <text x="330" y="414" font-family="Arial, sans-serif" font-size="11" fill="#424242">Async call</text>
  <line x1="470" y1="410" x2="530" y2="410" stroke="#78909C" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#arrow-return)"/>
  <text x="540" y="414" font-family="Arial, sans-serif" font-size="11" fill="#424242">Return message</text>
  <rect x="690" y="402" width="12" height="16" fill="#BBDEFB" stroke="#1565C0" stroke-width="1"/>
  <text x="710" y="414" font-family="Arial, sans-serif" font-size="11" fill="#424242">Activation</text>
</svg>
```
