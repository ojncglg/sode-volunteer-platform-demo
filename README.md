# SODE Volunteer Platform Demo

Flask-based functional demo for the Special Olympics Delaware volunteer management platform, developed by G3 Industries.

## Prototype Notice

This repository is a functional product prototype and stakeholder demo. It is not the production application or production architecture.

The prototype should be used as an executable specification for product behavior, workflow validation, and engineering handoff.

## Current Demo Scope

Implemented officer workflows:

- Officer access, account creation, and verification simulation
- Volunteer opportunities and filters
- Fall Festival event detail and signup
- Preferred assignment and provisional assignment
- My Events
- Assignment-change notification and acknowledgment
- Completed history and volunteer-hour total
- Officer leaderboard and department leaderboard

Implemented coordinator workflows:

- Event Operations dashboard
- Fall Festival staffing coverage and roster
- Assignment management and reassignment
- Assign Officers demo interaction
- Message Volunteers demo interaction
- Cross-role reassignment notification behavior
- Volunteer Hours report
- Officer search, department filter, and CSV export
- Volunteers placeholder

Simulated or not production-ready:

- Authentication and authorization
- Email verification
- Email, SMS, and notification delivery
- Persistent database
- Production reporting pipeline
- Event-day check-in, checkout, and hour-credit approval

## Documentation

Read these before production planning:

- [HANDOFF.md](HANDOFF.md): engineering handoff, route inventory, state model, assumptions, limitations, production requirements, and AWS discussion points.
- [WORKFLOWS.md](WORKFLOWS.md): current demo flows and future production workflow candidates using Mermaid diagrams.

## Run Locally

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

Any submitted login credentials enter the demo as Alex Morgan.

## Stack

- Python Flask
- Jinja templates
- HTML/CSS/JavaScript
- JSON and Python mock data
- Flask session state

## Demo Rules

- No production database
- No real authentication provider
- No real email or SMS service
- No cloud infrastructure
- Demo role switching is for presentation only
- Reset Demo State restores transient demo state while preserving seeded historical data

## Brand

- Patrol Blue: `#2A638F`
- Service Gold: `#EACF65`
- Night Watch: `#171917`
- Charcoal: `#262724`
- Steel Slate: `#8B9293`
- Paper: `#F8F8F5`
- Headlines: Noto Sans Display
- Body: Noto Sans
