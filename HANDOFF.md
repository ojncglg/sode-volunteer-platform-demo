# SODE Volunteer Platform Demo v1 Handoff

## Prototype Notice

This Flask application is a functional product prototype and demo.

It is not the production architecture. It should be treated as an executable specification of product behavior, stakeholder-approved screens, and demo workflows. A production team should rebuild and scale the product with proper architecture, security, persistence, testing, and operations.

## Project Purpose

The SODE Volunteer Platform demo models law-enforcement volunteer coordination for Special Olympics Delaware. It includes officer-facing workflows for finding opportunities, signing up, viewing assignments, acknowledging assignment changes, seeing volunteer history, and viewing leaderboards. It also includes coordinator-facing workflows for event staffing coverage, roster assignment management, volunteer-hours reporting, and demo role switching.

The prototype exists to support stakeholder demonstrations, collect feedback, and guide a later production rebuild.

## Current Stack

- Python Flask backend
- Jinja HTML templates
- CSS in `static/css/app.css`
- JavaScript in `static/js/auth.js` and `static/js/opportunities.js`
- JSON mock event data in `data/events.json`
- Python in-memory seed structures in `app.py`
- Flask session state for demo-only transient interactions
- No production database
- No real authentication, email, SMS, authorization, or notification backend

Python dependency:

- `Flask==3.1.2`

## Project Structure

```text
app.py
  Flask app, route definitions, mock data builders, session-backed demo workflow logic.

data/events.json
  Event and completed-history mock data used by opportunities, event detail, My Events, leaderboard, and reports.

templates/auth/login.html
  Officer access, account creation, and demo verification screen.

templates/officer/base.html
  Authenticated officer shell, navigation, notifications, user menu, demo controls.

templates/officer/opportunities.html
  Officer volunteer opportunities page.

templates/officer/event_detail.html
  Fall Festival event detail and signup workflow.

templates/officer/my_events.html
  Officer operational home, upcoming events, assignment update acknowledgment, completed history.

templates/officer/leaderboard.html
  Officer and department leaderboard.

templates/coordinator/base.html
  Coordinator shell, navigation, notifications, user menu, demo controls.

templates/coordinator/dashboard.html
  Coordinator Event Operations dashboard.

templates/coordinator/event_detail.html
  Coordinator event detail, Fall Festival staffing, roster, assignment management, demo messaging.

templates/coordinator/reports.html
  Coordinator Volunteer Hours report.

templates/coordinator/placeholder.html
  Placeholder for coordinator workflows not yet implemented.

templates/officer/*_placeholder.html
  Older placeholder templates retained in the repo but not used by the current main demo routes.

static/css/app.css
  Shared visual system and page-specific styles.

static/js/auth.js
  Login/account creation/verification panel interactions.

static/js/opportunities.js
  Authenticated shell behavior, officer filters/tabs, leaderboard toggle, coordinator panels, report filters, CSV export.
```

## Local Setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The app starts at `/`, redirects to `/login`, and uses demo login credentials. Any submitted credentials enter the officer demo.

## Route Inventory

| Method | Path | Role | Purpose |
| --- | --- | --- | --- |
| GET | `/` | Public | Redirects to login. |
| GET, POST | `/login` | Officer demo entry | Shows login. POST creates `demo_user` session and redirects to Opportunities. |
| POST | `/signup` | Officer account demo | Stores pending account info and returns to verification state. |
| GET | `/demo/verify` | Officer account demo | Simulates email verification. |
| GET | `/opportunities` | Officer | Lists volunteer opportunities with filters and signup state. |
| GET, POST | `/opportunities/<event_id>` | Officer | Shows event detail. POST records preferred/provisional assignment in session. |
| GET | `/my-events` | Officer | Shows upcoming assignments, assignment update state, completed history, and hours. |
| POST | `/my-events/fall-festival/acknowledge` | Officer | Marks the Fall Festival assignment change as acknowledged. |
| GET | `/leaderboard` | Officer | Shows officer and department leaderboard. |
| GET | `/demo/simulate-assignment-change` | Officer demo control | Simulates coordinator reassignment for Fall Festival after signup. |
| GET | `/demo/switch/coordinator` | Demo role switch | Switches presenter from officer shell to coordinator dashboard. |
| GET | `/demo/switch/officer` | Demo role switch | Switches presenter from coordinator shell to officer Opportunities. |
| GET | `/coordinator` | Coordinator | Event Operations dashboard. |
| GET | `/coordinator/events/<event_id>` | Coordinator | Coordinator event detail. Fall Festival is fully modeled; other events show staged detail. |
| POST | `/coordinator/events/<event_id>/reassign` | Coordinator | Updates officer assignment demo state. Alex reassignment drives officer notification workflow. |
| POST | `/coordinator/events/<event_id>/assign-volunteer` | Coordinator | Assigns an available demo volunteer to an assignment area. |
| GET | `/coordinator/volunteers` | Coordinator | Polished Volunteers placeholder. |
| GET | `/coordinator/reports` | Coordinator | Volunteer Hours report with filters and CSV export. |
| GET | `/demo/reset` | Demo control | Clears transient demo state and returns to Opportunities. |
| GET | `/logout` | Demo control | Clears session and returns to login. |
| GET | `/static/<path:filename>` | Flask static | Static file serving. |

## User Roles

### Officer

The officer role represents an authenticated law-enforcement volunteer. The demo officer is Alex Morgan from G3 Test Police Department.

There is no production authentication. The login form sets a Flask session object for demo use.

### Coordinator

The coordinator role represents an event operations user. The demo coordinator is Kyle Coordinator.

There is no production authorization. Coordinator view is reached through the demo role switch and shares session state with the officer view so a presenter can demonstrate cross-role effects.

### Demo Role Switching

Role switching is a presentation mechanism only. It lets a presenter:

1. Sign up as Alex.
2. Switch to Coordinator View.
3. Reassign Alex.
4. Switch back to Officer View.
5. See the notification and acknowledge it.
6. Switch back to Coordinator View and see the acknowledged state.

## Officer Features Implemented

- Login demo with any credentials.
- Account creation form.
- Official-email verification simulation.
- Volunteer Opportunities page.
- Opportunity filters: All, This Month, Weekends.
- Event cards with minimum staffing status.
- Fall Festival event detail.
- Preferred assignment selection.
- Demo signup.
- Provisional assignment state.
- My Events page with Next Up and upcoming events.
- Bowling Classic mocked signed-up state.
- Assignment change notification and update panel.
- Officer acknowledgment of assignment update.
- Acknowledgment changes assignment label from provisional to current.
- Completed volunteer history.
- Volunteer-hour total of 18.5 from completed history.
- Officer leaderboard.
- Department leaderboard.
- Header notification menu.
- Demo reset.

## Coordinator Features Implemented

- Coordinator shell with Events, Volunteers, Reports navigation.
- Event Operations dashboard.
- Operational summary metrics.
- Event list with staffing coverage and gap indicators.
- Fall Festival coordinator detail.
- Assignment-area staffing counts.
- Officer roster.
- Compact assignment management controls on roster rows.
- Alex reassignment connected to officer notification and acknowledgment state.
- Non-Alex assignment edits stored in coordinator demo session state.
- Assign Officers demo panel with available volunteers.
- Message Volunteers demo panel with recipient selection and demo toast.
- Assignment acknowledgment visibility for coordinator.
- Volunteer Hours report.
- Report range controls with visible active state.
- Officer search and department filter.
- CSV export of currently visible report rows.
- Volunteers placeholder.

## Mock Data

### JSON Data

`data/events.json` contains:

- Upcoming events.
- Fall Festival detail data.
- Assignment options for Fall Festival.
- Completed historical events used for Alex's volunteer-hour total.

### Python Seed Data

`app.py` contains seed structures for:

- Officer leaderboard.
- Department leaderboard.
- Coordinator user.
- Fall Festival staffing requirements.
- Fall Festival coordinator roster.
- Available volunteers for Assign Officers demo.
- Coordinator report summary metrics.
- Officer-hours report rows.

### Calculated Data

- Event staffing summaries are computed in `load_event_data`.
- Alex's completed volunteer hours are calculated from `completed_events`.
- Alex's event count in leaderboard and reports is calculated from completed history.
- Coordinator Fall Festival staffing counts are derived from the current roster plus session overrides.
- Pending acknowledgments are derived from assignment-change session state.

### Transient Session State

Flask session stores:

- `demo_user`
- `pending_account`
- `verified`
- `verified_email`
- `demo_signups`
- `demo_role`
- `coordinator_assignment_overrides`
- `coordinator_added_volunteers`

### Reset Behavior

`/demo/reset` clears:

- Fall Festival signup/session assignment state through `demo_signups`.
- Assignment changed state.
- Previous assignment.
- Acknowledgment state.
- Pending assignment-change notification state.
- Coordinator non-Alex assignment overrides.
- Coordinator added volunteers.

Reset preserves:

- Mock event data.
- Bowling Classic mocked signed-up state from JSON.
- Completed history and 18.5 credited hours.
- Leaderboard seed data.
- Coordinator report demo metrics.

## State Model

The prototype uses session-backed state to simulate user progress.

Officer signup writes a Fall Festival entry under `demo_signups` with:

- preferred assignment
- provisional assignment
- current assignment
- signup completion flag

Coordinator reassignment of Alex updates the same Fall Festival session entry:

- previous assignment
- current assignment
- provisional assignment
- assignment changed flag
- acknowledgment flag set to false

Officer acknowledgment sets the acknowledgment flag to true. That affects:

- Officer My Events display.
- Officer notification menu.
- Coordinator roster status.
- Coordinator pending acknowledgment count.

Coordinator edits for other officers use separate session override state because those officers are mocked and do not have an officer-facing session identity.

## Demo Assumptions

- Officer chooses a preferred assignment.
- In the demo, the selected preference becomes the provisional assignment.
- SODE coordinators may override an assignment.
- Officer acknowledgment means the officer saw the update.
- Acknowledgment is not acceptance or approval.
- Officers see simplified staffing need states.
- Coordinators see exact staffing counts.
- Shift-selection methodology remains unresolved.
- Check-in methodology remains unresolved.
- Checkout methodology remains unresolved.
- Volunteer-hour calculation remains unresolved.
- Volunteer-hour approval remains unresolved.
- Coordinator workflows require validation with actual SODE coordinators.

## Functional vs Simulated

| Area | Functional in prototype | Simulated or missing |
| --- | --- | --- |
| Navigation | Officer and coordinator navigation routes work. | No production route guard beyond session check. |
| Authentication | Login creates demo session. | No password validation, identity provider, MFA, or account security. |
| Account verification | Verification state and demo shortcut work. | No real email verification. |
| Opportunities | Filters and event detail work. | Event data is static JSON. |
| Signup | Session-backed signup works. | No database, no duplicate prevention beyond session, no production workflow. |
| Assignment selection | Preferred/provisional assignment works. | No final assignment rules or shift selection. |
| Reassignment | Coordinator can update Alex and notify officer flow. | No audit log, no real notification service. |
| Acknowledgment | Officer acknowledgment changes state. | Not a legal approval or acceptance workflow. |
| Notifications | Menus show state-sensitive items. | No notification backend, email, SMS, or push. |
| Role switching | Demo role switch works. | Not production authorization. |
| Reports | Search, department filter, and CSV export work. | Metrics are seeded demo figures, no reporting pipeline. |
| Reset | Restores demo state. | Not a production data operation. |

## Known Limitations

- Single-file Flask backend contains routes, data seeds, and business logic.
- No automated test suite is checked in.
- No production authentication or authorization.
- No database or persistence outside Flask session and JSON.
- No CSRF protection.
- No server-side form validation beyond simple route branching.
- No secrets management.
- `app.secret_key` is hard-coded for demo only.
- Report summary metrics are seeded demo numbers.
- Several product rules are intentionally unresolved.
- Some placeholder templates remain from earlier page scaffolding.
- `__pycache__` files are present locally but ignored by `.gitignore`.
- Mock data is split between JSON and Python seed structures.
- CSS and JS are shared files and have grown large during prototype development.

## Production Requirements

A production implementation needs:

- Identity/authentication.
- Role-based authorization.
- Persistent relational database.
- Proper event, assignment, and participation data model.
- Credited volunteer-hour records.
- Audit logging.
- Notification service.
- Email/SMS integration.
- Secure session/token management.
- Input validation.
- CSRF protection.
- Secrets management.
- Monitoring and logging.
- Automated tests.
- Backup and recovery strategy.
- Accessibility review.
- Security review.
- Data retention and privacy policies.

## AWS Direction for Discussion

The following is a candidate architecture for engineering validation, not an approved final design.

- AWS-hosted application/API.
- Managed relational database such as Amazon RDS.
- S3 for static or generated assets where appropriate.
- CloudFront for static delivery where appropriate.
- Managed identity/authentication approach, such as Cognito or integration with an approved identity provider.
- SES/SNS or equivalent services for email/SMS communication.
- CloudWatch for logs and metrics.
- Secrets Manager or Parameter Store for secrets/configuration.
- Infrastructure as code.
- CI/CD pipeline with automated tests and deployment gates.

## Candidate Production Data Model

Likely entities based on the prototype:

- User
- Agency
- Role
- Event
- AssignmentArea
- EventRegistration
- OfficerAssignment
- AssignmentChange
- AssignmentAcknowledgment
- VolunteerHourRecord
- Notification
- Message
- AuditLog

These are candidate entities only. They are not a finalized schema.

## Unresolved Product Questions

- Coordinator discovery still required.
- Do officers choose preferences, or do coordinators preassign officers?
- Do all events use shifts?
- What are shift selection rules?
- How does event-day check-in work?
- Is checkout required?
- How are volunteer hours calculated?
- Who approves credited hours?
- How are cancellations and no-shows handled?
- What assignment-change notifications are required?
- What coordinator permission levels exist?
- Is agency administration needed?
- What reporting outputs are required?
- What communication channels are required?
- What retention and audit requirements apply?
- What production identity requirements apply?

## Next Development Phase

Recommended next phase:

1. Conduct coordinator discovery interviews.
2. Validate officer assignment and shift-selection rules.
3. Define event-day check-in, checkout, and hour-credit rules.
4. Define production roles and permissions.
5. Draft production architecture and data model.
6. Build automated tests around the agreed workflows.
7. Rebuild production application using the prototype as executable product specification.

Do not blindly convert this Flask prototype into production code. Preserve the product learning, not the prototype shortcuts.
