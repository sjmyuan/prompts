# Example: Refining an Existing Story

## Scenario
The user provides a rough draft and asks to improve it:

> "Here's my user story, can you improve it?
>
> As a user, I want to reset my password so that I can log in again.
>
> Acceptance criteria:
> - User can reset password
> - It should work correctly"

---

## Agent's Approach: Extract and Fill Gaps

Rather than starting from scratch, extract what is already defined and apply only the capabilities for missing or unclear sections.

**Already defined (partial):**
- User: "a user" — vague, needs clarification
- Functionality: "reset my password" — partially clear
- Benefit: "log in again" — minimal, needs expansion
- Acceptance criteria: present but not testable — needs Given-When-Then reformatting

**Missing or unclear:**
- Specific user role and context
- Detailed reset flow (email link? security questions? SMS?)
- Testable acceptance criteria with edge cases
- Out-of-scope items
- Prerequisites

---

## Step 1 — Refining the User

**Agent asks:**
> "A user" is quite broad. Is this any registered user who has forgotten their password, or does this also apply to users whose accounts are locked or who need to change their password proactively?

**User responds:**
> Just registered users who forgot their password and can't log in.

**Agent confirms:**
> **User**: A registered user who has forgotten their password and cannot log in.
> Confirmed? ✅

---

## Step 2 — Refining the Functionality

**Agent asks:**
> How does the reset work? Common flows include:
> 1. User enters email → receives a reset link → clicks link → sets new password
> 2. User answers security questions → sets new password
> Which flow applies here?

**User responds:**
> Email link flow. The link should expire after 1 hour.

**Agent confirms:**
> **Functionality**: A registered user enters their email address, receives a password reset link (valid for 1 hour), clicks the link, and sets a new password.
> Confirmed? ✅

---

## Step 3 — Refining the Benefit

**Agent asks:**
> The current benefit ("so that I can log in again") is accurate but minimal. Would you like to expand it — for example, to emphasize security, self-service recovery, or reducing support requests?

**User responds:**
> Reduce support tickets and let users recover their account without contacting support.

**Agent confirms:**
> **Benefit**: Users can recover their account independently without contacting support, reducing support ticket volume.
> Confirmed? ✅

---

## Step 4 — Replacing Acceptance Criteria

**Agent notes:**
> The existing criteria ("User can reset password", "It should work correctly") are not testable. Replacing them with Given-When-Then scenarios.

**Agent proposes:**

**Scenario 1: Successful password reset**
- **Given** I am a registered user on the "Forgot Password" page
- **When** I enter my registered email and click "Send Reset Link"
- **Then** I receive an email containing a password reset link within 2 minutes, and the page shows "Check your email for a reset link"

**Scenario 2: Reset link clicked within expiry window**
- **Given** I have received a valid password reset link (less than 1 hour old)
- **When** I click the link and enter a new password that meets the complexity requirements
- **Then** my password is updated and I am redirected to the login page with a success message

**Scenario 3: Expired reset link**
- **Given** I click a reset link that is more than 1 hour old
- **When** the page loads
- **Then** I see an error message "This link has expired. Please request a new one." and a prompt to restart the flow

**Scenario 4: Unregistered email**
- **Given** I enter an email address that is not registered in the system
- **When** I click "Send Reset Link"
- **Then** the page shows the same generic message "Check your email for a reset link" (to prevent email enumeration)

> Confirmed? ✅

---

## Step 5 — Out of Scope

**Agent proposes:**
- Password reset via SMS or security questions: deferred to future story
- Admin-initiated password reset: separate story
- Enforcing password history (no reuse of last N passwords): separate story

> Confirmed? ✅

---

## Step 6 — Prerequisites

**Agent proposes:**
- User registration and email storage is implemented
- Transactional email sending infrastructure is in place
- Password hashing and storage meets security requirements

> Confirmed? ✅

---

## Final Refined User Story

## User Story

**As a** registered user who has forgotten their password,
**I want** to reset my password via an emailed link,
**So that** I can recover my account independently without contacting support.

---

### Acceptance Criteria

**Scenario 1: Successful reset link request**
- **Given** I am on the "Forgot Password" page
- **When** I enter my registered email and click "Send Reset Link"
- **Then** I receive a password reset email within 2 minutes, and the page shows "Check your email for a reset link"

**Scenario 2: Successful password reset**
- **Given** I click a valid reset link (less than 1 hour old)
- **When** I enter a new password that meets complexity requirements and confirm it
- **Then** my password is updated and I am redirected to the login page with a success message

**Scenario 3: Expired reset link**
- **Given** I click a reset link that is more than 1 hour old
- **When** the page loads
- **Then** I see "This link has expired. Please request a new one." with an option to restart

**Scenario 4: Unregistered email (security)**
- **Given** I enter an email not registered in the system
- **When** I click "Send Reset Link"
- **Then** the page shows the same generic message as a successful request (preventing email enumeration)

---

### Out of Scope
- Reset via SMS or security questions: deferred to a future story
- Admin-initiated password reset: separate story
- Password history enforcement (no reuse of last N passwords): separate story

---

### Prerequisites
- User registration and email address storage is implemented
- Transactional email infrastructure (e.g., SMTP service) is in place
- Password hashing meets current security requirements (e.g., bcrypt)
