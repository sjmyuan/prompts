# Example: Simple Single-Actor Feature Story

## Scenario
The user says: "I need a user story for exporting data as a CSV file."

---

## Step 1 — Defining the User

**Agent asks:**
> Who performs this export action? For example, is this a logged-in end user, a data analyst, an admin, or an automated process?

**User responds:**
> A logged-in business analyst who reviews monthly reports.

**Agent confirms:**
> **User**: A logged-in business analyst who reviews monthly reports using the application's reporting module.
> Does this accurately describe the user? ✅

---

## Step 2 — Defining the Functionality

**Agent asks:**
> What exactly does the analyst want to export? All records, filtered results, a specific report? And which format — just CSV or other formats too?

**User responds:**
> The currently filtered/visible report data, CSV only.

**Agent confirms:**
> **Functionality**: Export the currently filtered report data as a CSV file, triggered by a button in the reporting UI.
> Does this capture the core action? ✅

---

## Step 3 — Defining the Benefit

**Agent asks:**
> What value does this export deliver? For example: offline analysis, sharing with stakeholders, feeding data into other tools?

**User responds:**
> So analysts can process data further in Excel without manually copying it.

**Agent confirms:**
> **Benefit**: Enables analysts to process report data in external tools (e.g., Excel) without manual data entry.
> Confirmed? ✅

---

## Step 4 — Defining Acceptance Criteria

**Agent proposes:**

**Scenario 1: Successful export**
- **Given** I am a logged-in business analyst viewing a filtered report
- **When** I click the "Export as CSV" button
- **Then** a CSV file is downloaded containing only the currently filtered rows, with column headers matching the report

**Scenario 2: Empty result set**
- **Given** the current filter returns no results
- **When** I click "Export as CSV"
- **Then** a CSV file is downloaded containing only the header row, and a notification informs me the export is empty

**Scenario 3: Large dataset**
- **Given** the filtered report contains more than 10,000 rows
- **When** I click "Export as CSV"
- **Then** the file is generated and download begins within 5 seconds

> Does this cover the scenarios? ✅

---

## Step 5 — Defining Out of Scope

**Agent proposes:**
- Exporting to Excel (.xlsx) or PDF formats: deferred to a future story
- Scheduling or automating exports: separate feature
- Exporting data from non-report screens: out of scope per product decision

> Confirmed? ✅

---

## Step 6 — Defining Prerequisites

**Agent proposes:**
- The reporting module with filter functionality must be implemented
- User authentication and role-based access must be in place

> Confirmed? ✅

---

## Final User Story

## User Story

**As a** logged-in business analyst,
**I want** to export the currently filtered report data as a CSV file,
**So that** I can process it further in external tools like Excel without manual data entry.

---

### Acceptance Criteria

**Scenario 1: Successful export**
- **Given** I am a logged-in business analyst viewing a filtered report
- **When** I click the "Export as CSV" button
- **Then** a CSV file is downloaded containing only the currently filtered rows, with column headers matching the report

**Scenario 2: Empty result set**
- **Given** the current filter returns no results
- **When** I click "Export as CSV"
- **Then** a CSV file is downloaded containing only the header row, and a notification informs me the export is empty

**Scenario 3: Large dataset**
- **Given** the filtered report contains more than 10,000 rows
- **When** I click "Export as CSV"
- **Then** the file is generated and download begins within 5 seconds

---

### Out of Scope
- Excel (.xlsx) / PDF export: deferred to a future story
- Scheduled or automated exports: separate feature
- Exporting data from non-report screens: out of scope per product decision

---

### Prerequisites
- Reporting module with filter functionality is implemented
- User authentication and role-based access control is in place
