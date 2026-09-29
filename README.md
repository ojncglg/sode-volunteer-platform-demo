# SODE Volunteer Platform Demo

Flask-based functional demo for the Special Olympics Delaware volunteer management platform, developed by G3 Industries.

## Current build status

**Page 1: Officer Access** is approved.

**Page 2: Volunteer Opportunities** is approved.

**Page 3: Fall Festival Event Detail and Signup Flow** is approved.

**Page 4: My Events** is approved.

Included demo flow:

- Officer login
- Create account
- Official email and agency selection
- Verification-email sent state
- Demo shortcut to simulate email verification
- Login with any credentials in demo mode
- Officer opportunities dashboard
- Working opportunity filters
- Mock staffing coverage data
- Fall Festival event detail
- One-page assignment preference signup
- Session-backed demo signup state
- My Events operational home
- Simulated assignment-change acknowledgment
- Mock completed-event history and volunteer hours

## Product assumptions for handoff

DEMO ASSUMPTION: For the current prototype, an officer's selected assignment preference becomes their provisional assignment upon signup. SODE coordinators will retain the ability to reassign officers before or during an event. Final assignment methodology requires validation with SODE event coordinators.

Exact assignment staffing numbers are intentionally coordinator-facing. Officers see simplified need statuses in the current prototype.

Shift selection and checkout/hour-credit rules remain unresolved and are intentionally not implemented.

ASSIGNMENT CHANGE DEMO ASSUMPTION: Coordinators may reassign officers after signup. The current prototype requires the officer to acknowledge that they have seen the updated assignment. Acknowledgment does not constitute acceptance or approval. Final reassignment and notification requirements require coordinator validation.

My Events is intended to become the officer's operational event-day hub, including future check-in and volunteer-hour history.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Demo rules

This repository is a functional product prototype, not production software. Authentication, email, SMS, persistence, and external integrations are simulated unless explicitly noted.

The demo will be built page by page. Each page is reviewed and approved before the next page is implemented.

## Brand

- Patrol Blue: `#2A638F`
- Service Gold: `#EACF65`
- Night Watch: `#171917`
- Charcoal: `#262724`
- Steel Slate: `#8B9293`
- Paper: `#F8F8F5`
- Headlines: Noto Sans Display
- Body: Noto Sans
