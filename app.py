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
        "completed_events": event_data.get("completed_events", []),
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


def get_assignment_name(event, assignment_id):
    assignment = resolve_assignment(event, assignment_id)
    if assignment is None:
        return "Assignment Pending"
    return assignment["name"]


def build_my_events_context():
    event_data = load_event_data()
    events = event_data["events"]
    fall_event = next((event for event in events if event["id"] == "fall-festival"), None)
    bowling_event = next((event for event in events if event["id"] == "bowling-classic"), None)
    fall_signup = get_event_signup("fall-festival")

    upcoming_events = []
    next_up = None
    if fall_event and fall_signup and fall_signup.get("signed_up"):
        current_assignment = fall_signup.get(
            "current_assignment_name",
            fall_signup.get("provisional_assignment_name", "Assignment Pending"),
        )
        fall_state = {
            "event": fall_event,
            "signup": fall_signup,
            "assignment_name": current_assignment,
            "report_time": "7:45 AM",
            "report_to": "Delaware Stadium Volunteer Check-In",
            "detail_url": url_for("opportunity_detail", event_id=fall_event["id"]),
        }
        event_date = date.fromisoformat(fall_event["date"])
        days_until = (event_date - date.today()).days
        if days_until >= 0:
            fall_state["days_until"] = days_until
        upcoming_events.append(fall_state)
        next_up = fall_state

    if bowling_event and bowling_event.get("joined"):
        bowling_state = {
            "event": bowling_event,
            "assignment_name": "Assignment Pending",
            "assignment_pending": True,
            "pending_copy": "Special Olympics Delaware will provide your event assignment before the event.",
            "report_time": "9:00 AM",
            "report_to": bowling_event["location"],
        }
        upcoming_events.append(bowling_state)
        if next_up is None:
            next_up = bowling_state

    completed_events = event_data["completed_events"]
    total_hours = sum(event["hours"] for event in completed_events)
    return {
        "next_up": next_up,
        "upcoming_events": upcoming_events,
        "completed_events": completed_events,
        "total_hours": total_hours,
        "fall_signup": fall_signup,
    }


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
                "current_assignment": assignment["id"],
                "current_assignment_name": assignment["name"],
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


@app.route("/my-events")
def my_events():
    if "demo_user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "officer/my_events.html",
        demo_user=session["demo_user"],
        **build_my_events_context(),
    )


@app.route("/demo/simulate-assignment-change")
def simulate_assignment_change():
    if "demo_user" not in session:
        return redirect(url_for("login"))

    fall_event = get_event("fall-festival")
    demo_signups = get_demo_signups()
    fall_signup = demo_signups.get("fall-festival")
    if not fall_event or not fall_signup or not fall_signup.get("signed_up"):
        return redirect(url_for("my_events"))

    previous_assignment = fall_signup.get(
        "current_assignment_name",
        fall_signup.get("provisional_assignment_name", "Assignment Pending"),
    )
    new_assignment = resolve_assignment(fall_event, "sports-arena")
    if new_assignment is None:
        return redirect(url_for("my_events"))

    fall_signup.update(
        {
            "previous_assignment": previous_assignment,
            "current_assignment": new_assignment["id"],
            "current_assignment_name": new_assignment["name"],
            "provisional_assignment": new_assignment["id"],
            "provisional_assignment_name": new_assignment["name"],
            "assignment_changed": True,
            "assignment_change_acknowledged": False,
        }
    )
    demo_signups["fall-festival"] = fall_signup
    session["demo_signups"] = demo_signups
    session.modified = True
    return redirect(url_for("my_events"))


@app.route("/my-events/fall-festival/acknowledge", methods=["POST"])
def acknowledge_assignment_change():
    if "demo_user" not in session:
        return redirect(url_for("login"))

    demo_signups = get_demo_signups()
    fall_signup = demo_signups.get("fall-festival")
    if fall_signup and fall_signup.get("assignment_changed"):
        fall_signup["assignment_change_acknowledged"] = True
        demo_signups["fall-festival"] = fall_signup
        session["demo_signups"] = demo_signups
        session.modified = True
    return redirect(url_for("my_events"))


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
