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
        if signed_up >= minimum_needed:
            event["staffing_status"] = "Minimum staffing met"
        else:
            event["staffing_status"] = f"{minimum_needed - signed_up} more needed"

    return {
        "demo_current_month": event_data["demo_current_month"],
        "events": events,
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
    return render_template(
        "officer/opportunities.html",
        demo_user=session["demo_user"],
        events=event_data["events"],
        demo_current_month=event_data["demo_current_month"],
    )


@app.route("/opportunities/<event_id>")
def opportunity_detail(event_id):
    if "demo_user" not in session:
        return redirect(url_for("login"))

    event_data = load_event_data()
    event = next(
        (event_item for event_item in event_data["events"] if event_item["id"] == event_id),
        None,
    )
    if event is None:
        abort(404)

    return render_template(
        "officer/event_detail_placeholder.html",
        demo_user=session["demo_user"],
        event=event,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
