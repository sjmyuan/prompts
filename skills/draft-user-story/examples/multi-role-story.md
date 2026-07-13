# Example: Complex Multi-Role Story

## Scenario
The user says: "I need a user story for an approval workflow where employees submit expense reports and managers approve or reject them."

---

## Step 1 — Defining the User

**Agent asks:**
> This scenario involves at least two roles — the employee submitting and the manager approving. Should this be one story covering both sides, or separate stories per role? And are there any other actors (e.g., finance team, automated reminders)?

**User responds:**
> Two separate stories — one for the employee submitting, one for the manager approving. Let's start with the employee.

**Agent confirms:**
> **User (Story 1)**: A logged-in employee who wants to submit an expense report for reimbursement.
> Confirmed? ✅

---

## Step 2 — Defining the Functionality

**Agent asks:**
> What does the employee need to do to submit? For example: fill in a form, attach receipts, select a category, assign a manager? What fields are required vs. optional?

**User responds:**
> Fill in amount, date, category, description, and attach a receipt image. The manager is auto-assigned based on org chart. Submit button sends it for approval.

**Agent confirms:**
> **Functionality**: An employee fills in expense details (amount, date, category, description), attaches a receipt image, and submits the report. The approving manager is auto-assigned based on the org chart.
> Confirmed? ✅

---

## Step 3 — Defining the Benefit

**Agent asks:**
> What's the primary value for the employee — faster reimbursement, visibility into status, reduced paperwork?

**User responds:**
> They can submit expenses digitally from anywhere and track approval status in real time instead of using paper forms.

**Agent confirms:**
> **Benefit**: Enables employees to submit expenses digitally from anywhere and track the approval status in real time, replacing paper-based processes.
> Confirmed? ✅

---

## Step 4 — Defining Acceptance Criteria

**Agent proposes:**

**Scenario 1: Successful submission**
- **Given** I am a logged-in employee on the expense submission form
- **When** I fill in all required fields (amount, date, category, description), attach a receipt, and click "Submit"
- **Then** the expense report is saved, submitted to my auto-assigned manager, and I see a confirmation with the report ID and "Pending Approval" status

**Scenario 2: Missing required field**
- **Given** I am on the expense submission form
- **When** I click "Submit" without filling in a required field
- **Then** the form highlights the missing field(s) with an error message and does not submit

**Scenario 3: Unsupported file type for receipt**
- **Given** I attach a file that is not an image (e.g., .exe, .zip)
- **When** I click "Submit"
- **Then** an error message states "Only image files (JPG, PNG, PDF) are accepted" and the submission is blocked

**Scenario 4: Status tracking**
- **Given** I have submitted an expense report
- **When** I navigate to "My Expenses"
- **Then** I can see the report listed with its current status (Pending Approval / Approved / Rejected)

> Confirmed? ✅

---

## Step 5 — Defining Out of Scope

**Agent proposes:**
- Manager approval/rejection flow: covered in a separate story
- Finance team payment processing: separate story
- Multi-level approval chains: deferred to future iteration
- Expense policy rule enforcement (e.g., max amount per category): separate story

> Confirmed? ✅

---

## Step 6 — Defining Prerequisites

**Agent proposes:**
- Employee authentication and session management must be implemented
- Org chart data and manager assignment logic must be available
- File upload infrastructure (image storage) must be in place

> Confirmed? ✅

---

## Final User Story

## User Story

**As a** logged-in employee,
**I want** to submit an expense report with receipt attachment,
**So that** I can request reimbursement digitally and track the approval status in real time.

---

### Acceptance Criteria

**Scenario 1: Successful submission**
- **Given** I am a logged-in employee on the expense submission form
- **When** I fill in all required fields (amount, date, category, description), attach a receipt, and click "Submit"
- **Then** the expense report is saved, assigned to my manager, and I see a confirmation with the report ID and "Pending Approval" status

**Scenario 2: Missing required field**
- **Given** I am on the expense submission form
- **When** I click "Submit" without filling in a required field
- **Then** the form highlights the missing field(s) with an inline error message and does not submit

**Scenario 3: Unsupported file type for receipt**
- **Given** I attach a non-image file (e.g., .exe, .zip) as a receipt
- **When** I click "Submit"
- **Then** an error message states "Only image files (JPG, PNG, PDF) are accepted" and submission is blocked

**Scenario 4: Status tracking**
- **Given** I have a submitted expense report
- **When** I navigate to "My Expenses"
- **Then** I can see the report listed with its current status (Pending Approval / Approved / Rejected)

---

### Out of Scope
- Manager approval/rejection flow: covered in a separate story
- Finance payment processing: separate story
- Multi-level approval chains: deferred to future iteration
- Expense policy rule enforcement: separate story

---

### Prerequisites
- Employee authentication and session management is implemented
- Org chart data and manager auto-assignment logic is available
- File upload and image storage infrastructure is in place
