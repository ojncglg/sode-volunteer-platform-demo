# SODE Volunteer Platform Demo

Flask-based functional demo for the Special Olympics Delaware volunteer management platform, developed by G3 Industries.

## Current build status

**Page 1: Officer Access** is ready for review.

Included demo flow:

- Officer login
- Create account
- Official email and agency selection
- Verification-email sent state
- Demo shortcut to simulate email verification
- Login with any credentials in demo mode
- Post-login placeholder that preserves the page-by-page approval process

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
