import json
from datetime import date
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "sode-demo-only-secret-key"

BASE_DIR = Path(__file__).resolve().parent
EVENT_DATA_PATH = BASE_DIR / "data" / "events.json"

AGENCIES = [
    "Delaware State Police",
    "New Castle County Police Department",
    "Wilmington Police Department",
    "Newark Police Department",
    "Middletown Police Department",
    "Dover Police Department",
    "University of Delaware Police Department",
    "Other Delaware Law Enforcement Agency",
]


def load_event_data():
    with EVENT_DATA_PATH.open() as event_file:
        event_data = json.load(event_file)

    events = sorted(
        event_data["events"],
        key=lambda event: date.fromisoformat(event["date"]),
    )
    for event in events:
        event_date = date.fromisoformat(event["date"])
        signed_up = event["signed_up"]
        minimum_needed = event["minimum_needed"]
        coverage_percent = round((signed_up / minimum_needed) * 100)

        event["month"] = event_date.strftime("%Y-%m")
        event["is_weekend"] = event_date.weekday() >= 5
        event["coverage_percent"] = min(coverage_percent, 100)
        event["staffing_summary"] = f"{signed_up} volunteers • {minimum_needed} needed"
        event.setdefault("detail_title", event["name"])
        event.setdefault("venue", event["location"])
        event.setdefault("city_state", "")
        event.setdefault(
            "description",
            "Support Special Olympics Delaware athletes, volunteers, families, and event operations.",
        )
        event.setdefault(
            "point_of_contact",
            {
                "name": "Special Olympics Delaware",
                "organization": "Event Operations",
            },
        )
        event.setdefault(
            "before_arrive",
            [
                {
                    "label": "REPORT TIME",
                    "value": event.get("time", "See event details"),
                },
                {
                    "label": "REPORT LOCATION",
                    "value": event["location"],
                },
                {
                    "label": "ATTIRE",
                    "value": "Department uniform or approved agency attire",
                },
            ],
        )
        event.setdefault(
            "assignments",
            [
                {
                    "id": "no-preference",
                    "name": "No Preference",
                    "description": "Put me where I'm needed most.",
                    "officer_status": "FLEXIBLE",
                },
            ],
        )
        if signed_up >= minimum_needed:
            event["staffing_status"] = "Minimum staffing met"
        else:
            event["staffing_status"] = f"{minimum_needed - signed_up} more needed"

    return {
        "demo_current_month": event_data["demo_current_month"],
        "events": events,
    }


def get_event(event_id):
    event_data = load_event_data()
    return next(
        (event_item for event_item in event_data["events"] if event_item["id"] == event_id),
        None,
    )


def get_demo_signups():
    return session.get("demo_signups", {})


def get_event_signup(event_id):
    return get_demo_signups().get(event_id)


def apply_session_signup_state(events):
    demo_signups = get_demo_signups()
    for event in events:
        signup = demo_signups.get(event["id"])
        if signup and signup.get("signed_up"):
            event["joined"] = True


def resolve_assignment(event, assignment_id):
    assignments = event.get("assignments", [])
    return next(
        (assignment for assignment in assignments if assignment["id"] == assignment_id),
        None,
    )


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["demo_user"] = {
            "name": "Alex Morgan",
            "agency": "G3 Test Police Department",
            "initials": "AM",
        }
        return redirect(url_for("opportunities"))
    return render_template("auth/login.html", agencies=AGENCIES)


@app.route("/signup", methods=["POST"])
def signup():
    session["pending_account"] = {
        "first_name": request.form.get("first_name", "Officer"),
        "last_name": request.form.get("last_name", "Demo"),
        "email": request.form.get("email", "officer@example.gov"),
        "agency": request.form.get("agency", "Delaware Law Enforcement Agency"),
    }
    session["verified"] = False
    return redirect(url_for("login", state="verification"))


@app.route("/demo/verify")
def demo_verify():
    session["verified"] = True
    account = session.get("pending_account", {})
    session["verified_email"] = account.get("email", "Demo account")
    return redirect(url_for("login", verified="1"))


@app.route("/opportunities")
def opportunities():
    if "demo_user" not in session:
        return redirect(url_for("login"))
    event_data = load_event_data()
    apply_session_signup_state(event_data["events"])
    return render_template(
        "officer/opportunities.html",
        demo_user=session["demo_user"],
        events=event_data["events"],
        demo_current_month=event_data["demo_current_month"],
    )


@app.route("/opportunities/<event_id>", methods=["GET", "POST"])
def opportunity_detail(event_id):
    if "demo_user" not in session:
        return redirect(url_for("login"))

    event = get_event(event_id)
    if event is None:
        abort(404)

    existing_signup = get_event_signup(event_id)
    if request.method == "POST":
        assignment_id = request.form.get("preferred_assignment", "no-preference")
        assignment = resolve_assignment(event, assignment_id)
        if assignment is None:
            assignment = resolve_assignment(event, "no-preference")

        if assignment is not None:
            demo_signups = get_demo_signups()
            demo_signups[event_id] = {
                "event_id": event_id,
                "signed_up": True,
                "preferred_assignment": assignment["id"],
                "preferred_assignment_name": assignment["name"],
                "provisional_assignment": assignment["id"],
                "provisional_assignment_name": assignment["name"],
                "signup_completed": True,
            }
            session["demo_signups"] = demo_signups
            session.modified = True
        return redirect(url_for("opportunity_detail", event_id=event_id))

    signup = existing_signup
    selected_assignment_id = "no-preference"
    selected_assignment = None
    if signup and signup.get("signed_up"):
        selected_assignment_id = signup.get("provisional_assignment", "no-preference")
        selected_assignment = resolve_assignment(event, selected_assignment_id)

    return render_template(
        "officer/event_detail.html",
        demo_user=session["demo_user"],
        event=event,
        signup=signup,
        selected_assignment_id=selected_assignment_id,
        selected_assignment=selected_assignment,
    )


@app.route("/demo/reset")
def demo_reset():
    session.pop("demo_signups", None)
    session.modified = True
    return redirect(url_for("opportunities"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
