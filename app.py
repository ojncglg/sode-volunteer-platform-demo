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

OFFICER_LEADERBOARD_SEEDS = [
    {
        "name": "Marcus Johnson",
        "agency": "Delaware State Police",
        "events_count": 14,
        "hours": 86,
        "streak": None,
    },
    {
        "name": "Emily Davis",
        "agency": "New Castle County PD",
        "events_count": 12,
        "hours": 74,
        "streak": "4-event streak",
    },
    {
        "name": "Robert Smith",
        "agency": "Wilmington PD",
        "events_count": 11,
        "hours": 68,
        "streak": None,
    },
    {
        "name": "Sarah Kim",
        "agency": "Dover PD",
        "events_count": 12,
        "hours": 59,
        "streak": "5-event streak",
    },
    {
        "name": "David Lee",
        "agency": "Newark PD",
        "events_count": 9,
        "hours": 55,
        "streak": None,
    },
    {
        "name": "Ava Martinez",
        "agency": "Middletown PD",
        "events_count": 9,
        "hours": 51,
        "streak": "3-event streak",
    },
    {
        "name": "Tyler Nguyen",
        "agency": "Smyrna PD",
        "events_count": 8,
        "hours": 47,
        "streak": None,
    },
]

DEPARTMENT_LEADERBOARD_SEEDS = [
    {
        "name": "Delaware State Police",
        "hours": 209,
        "officer_count": 31,
    },
    {
        "name": "New Castle County PD",
        "hours": 184,
        "officer_count": 28,
    },
    {
        "name": "Wilmington Police Department",
        "hours": 151,
        "officer_count": 22,
    },
    {
        "name": "Dover Police Department",
        "hours": 126,
        "officer_count": 18,
    },
    {
        "name": "Newark Police Department",
        "hours": 104,
        "officer_count": 16,
    },
    {
        "name": "Middletown Police Department",
        "hours": 88,
        "officer_count": 13,
    },
    {
        "name": "Smyrna Police Department",
        "hours": 71,
        "officer_count": 11,
    },
]

COORDINATOR_USER = {
    "name": "Kyle Coordinator",
    "agency": "G3 Test Police Department",
    "initials": "KC",
}

FALL_FESTIVAL_STAFFING_REQUIREMENTS = [
    {"id": "bocce-awards", "name": "Bocce Awards", "required": 3},
    {"id": "sports-arena", "name": "Sports Arena", "required": 4},
    {"id": "main-awards", "name": "Main Awards", "required": 3},
    {"id": "ldr-awards", "name": "LDR Awards", "required": 2},
    {"id": "cafeteria", "name": "Cafeteria", "required": 4},
]

FALL_FESTIVAL_ROSTER_SEEDS = [
    {
        "id": "alex-morgan",
        "name": "Alex Morgan",
        "agency": "G3 Test Police Department",
        "preferred_assignment": "Bocce Awards",
        "current_assignment": "Bocce Awards",
    },
    {
        "id": "emily-davis",
        "name": "Emily Davis",
        "agency": "New Castle County PD",
        "preferred_assignment": "No Preference",
        "current_assignment": "Cafeteria",
    },
    {
        "id": "marcus-johnson",
        "name": "Marcus Johnson",
        "agency": "Delaware State Police",
        "preferred_assignment": "Main Awards",
        "current_assignment": "Main Awards",
    },
    {
        "id": "robert-smith",
        "name": "Robert Smith",
        "agency": "Wilmington PD",
        "preferred_assignment": "Sports Arena",
        "current_assignment": "Sports Arena",
    },
    {
        "id": "sarah-kim",
        "name": "Sarah Kim",
        "agency": "Dover PD",
        "preferred_assignment": "LDR Awards",
        "current_assignment": "LDR Awards",
    },
    {
        "id": "david-lee",
        "name": "David Lee",
        "agency": "Newark PD",
        "preferred_assignment": "Bocce Awards",
        "current_assignment": "Bocce Awards",
    },
    {
        "id": "ava-martinez",
        "name": "Ava Martinez",
        "agency": "Middletown PD",
        "preferred_assignment": "Cafeteria",
        "current_assignment": "Cafeteria",
    },
    {
        "id": "tyler-nguyen",
        "name": "Tyler Nguyen",
        "agency": "Smyrna PD",
        "preferred_assignment": "Sports Arena",
        "current_assignment": "Sports Arena",
    },
    {
        "id": "olivia-brooks",
        "name": "Olivia Brooks",
        "agency": "Delaware State Police",
        "preferred_assignment": "Main Awards",
        "current_assignment": "Main Awards",
    },
    {
        "id": "james-wilson",
        "name": "James Wilson",
        "agency": "New Castle County PD",
        "preferred_assignment": "LDR Awards",
        "current_assignment": "LDR Awards",
    },
    {
        "id": "maya-patel",
        "name": "Maya Patel",
        "agency": "Wilmington PD",
        "preferred_assignment": "Bocce Awards",
        "current_assignment": "Bocce Awards",
    },
    {
        "id": "noah-reed",
        "name": "Noah Reed",
        "agency": "Dover PD",
        "preferred_assignment": "Main Awards",
        "current_assignment": "Main Awards",
    },
]

FALL_FESTIVAL_AVAILABLE_VOLUNTEERS = [
    {
        "id": "grace-turner",
        "name": "Grace Turner",
        "agency": "Delaware State Police",
        "preferred_assignment": "Sports Arena",
    },
    {
        "id": "logan-price",
        "name": "Logan Price",
        "agency": "New Castle County PD",
        "preferred_assignment": "Cafeteria",
    },
    {
        "id": "nina-carter",
        "name": "Nina Carter",
        "agency": "Wilmington PD",
        "preferred_assignment": "No Preference",
    },
]

REPORT_SUMMARY_METRICS = [
    {"label": "TOTAL HOURS", "value": "1,240"},
    {"label": "ACTIVE VOLUNTEERS", "value": "86"},
    {"label": "EVENTS HELD", "value": "24"},
    {"label": "AVG HOURS PER OFFICER", "value": "14.4"},
]

OFFICER_HOURS_REPORT_SEEDS = [
    {
        "name": "Marcus Johnson",
        "department": "Delaware State Police",
        "events": 14,
        "hours": 86,
        "cancellations": 1,
    },
    {
        "name": "Emily Davis",
        "department": "New Castle County PD",
        "events": 12,
        "hours": 74,
        "cancellations": 0,
    },
    {
        "name": "Robert Smith",
        "department": "Wilmington PD",
        "events": 11,
        "hours": 68,
        "cancellations": 2,
    },
    {
        "name": "Angela Torres",
        "department": "Dover PD",
        "events": 10,
        "hours": 61,
        "cancellations": 1,
    },
    {
        "name": "Kevin Brooks",
        "department": "Delaware State Police",
        "events": 9,
        "hours": 55,
        "cancellations": 3,
    },
    {
        "name": "Sarah Miller",
        "department": "Newark PD",
        "events": 8,
        "hours": 49,
        "cancellations": 0,
    },
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


def format_hours(hours):
    return f"{hours:g}"


def get_initials(name):
    return "".join(part[0] for part in name.split()[:2]).upper()


def rank_entries(entries):
    ranked_entries = sorted(entries, key=lambda entry: entry["hours"], reverse=True)
    for index, entry in enumerate(ranked_entries, start=1):
        entry["rank"] = index
        entry["hours_label"] = format_hours(entry["hours"])
    return ranked_entries


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


def build_leaderboard_context():
    event_data = load_event_data()
    completed_events = event_data["completed_events"]
    alex_hours = sum(event["hours"] for event in completed_events)
    alex_event_count = len(completed_events)

    officer_entries = [entry.copy() for entry in OFFICER_LEADERBOARD_SEEDS]
    officer_entries.append(
        {
            "name": "Alex Morgan",
            "agency": "G3 Test Police Department",
            "events_count": alex_event_count,
            "hours": alex_hours,
            "streak": None,
            "is_current_user": True,
        }
    )

    for officer in officer_entries:
        officer["initials"] = get_initials(officer["name"])
        officer.setdefault("is_current_user", False)

    ranked_officers = rank_entries(officer_entries)
    officer_podium = [ranked_officers[1], ranked_officers[0], ranked_officers[2]]

    department_entries = [entry.copy() for entry in DEPARTMENT_LEADERBOARD_SEEDS]
    department_entries.append(
        {
            "name": "G3 Test Police Department",
            "hours": alex_hours,
            "officer_count": 1,
            "is_current_user_department": True,
        }
    )

    for department in department_entries:
        department["initials"] = get_initials(department["name"])
        department.setdefault("is_current_user_department", False)

    ranked_departments = rank_entries(department_entries)
    department_podium = [ranked_departments[1], ranked_departments[0], ranked_departments[2]]

    return {
        "officer_podium": officer_podium,
        "officer_rows": ranked_officers[3:],
        "department_podium": department_podium,
        "department_rows": ranked_departments[3:],
        "alex_hours": alex_hours,
        "alex_event_count": alex_event_count,
    }


def build_coordinator_reports_context():
    event_data = load_event_data()
    completed_events = event_data["completed_events"]
    alex_hours = sum(event["hours"] for event in completed_events)
    alex_event_count = len(completed_events)

    officer_rows = [row.copy() for row in OFFICER_HOURS_REPORT_SEEDS]
    officer_rows.append(
        {
            "name": "Alex Morgan",
            "department": "G3 Test Police Department",
            "events": alex_event_count,
            "hours": alex_hours,
            "cancellations": 0,
        }
    )

    departments = sorted({row["department"] for row in officer_rows})
    for row in officer_rows:
        row["hours_label"] = format_hours(row["hours"])

    return {
        "coordinator_user": COORDINATOR_USER,
        "summary_metrics": REPORT_SUMMARY_METRICS,
        "officer_rows": officer_rows,
        "departments": departments,
    }


def get_fall_signup_for_coordinator():
    return get_event_signup("fall-festival") or {}


def get_assignment_options():
    return [
        {"id": requirement["id"], "name": requirement["name"]}
        for requirement in FALL_FESTIVAL_STAFFING_REQUIREMENTS
    ]


def get_assignment_area_name(assignment_id):
    return next(
        (
            requirement["name"]
            for requirement in FALL_FESTIVAL_STAFFING_REQUIREMENTS
            if requirement["id"] == assignment_id
        ),
        None,
    )


def get_coordinator_assignment_overrides():
    return session.get("coordinator_assignment_overrides", {})


def save_coordinator_assignment_override(officer_id, assignment_id):
    assignment_name = get_assignment_area_name(assignment_id)
    if assignment_name is None:
        return

    overrides = get_coordinator_assignment_overrides()
    overrides[officer_id] = {
        "current_assignment": assignment_name,
        "assignment_id": assignment_id,
        "status": "Assignment Updated",
    }
    session["coordinator_assignment_overrides"] = overrides
    session.modified = True


def get_added_volunteer_assignments():
    return session.get("coordinator_added_volunteers", {})


def assign_available_volunteer(volunteer_id, assignment_id):
    assignment_name = get_assignment_area_name(assignment_id)
    volunteer = next(
        (
            volunteer
            for volunteer in FALL_FESTIVAL_AVAILABLE_VOLUNTEERS
            if volunteer["id"] == volunteer_id
        ),
        None,
    )
    if volunteer is None or assignment_name is None:
        return

    added_volunteers = get_added_volunteer_assignments()
    added_volunteers[volunteer_id] = {
        "current_assignment": assignment_name,
        "assignment_id": assignment_id,
    }
    session["coordinator_added_volunteers"] = added_volunteers
    session.modified = True


def build_fall_festival_roster():
    fall_signup = get_fall_signup_for_coordinator()
    overrides = get_coordinator_assignment_overrides()
    added_volunteers = get_added_volunteer_assignments()
    roster = [officer.copy() for officer in FALL_FESTIVAL_ROSTER_SEEDS]

    for officer in roster:
        officer["initials"] = get_initials(officer["name"])
        officer["status"] = "Confirmed"
        override = overrides.get(officer["id"])
        if override:
            officer["current_assignment"] = override["current_assignment"]
            officer["status"] = override["status"]

    alex = next((officer for officer in roster if officer["id"] == "alex-morgan"), None)
    if alex and fall_signup.get("current_assignment_name"):
        alex["current_assignment"] = fall_signup["current_assignment_name"]
        alex["preferred_assignment"] = fall_signup.get(
            "preferred_assignment_name",
            alex["preferred_assignment"],
        )
        if fall_signup.get("assignment_changed") and fall_signup.get("assignment_change_acknowledged"):
            alex["status"] = "Acknowledged"
        elif fall_signup.get("assignment_changed"):
            alex["status"] = "Assignment Updated"

    for volunteer in FALL_FESTIVAL_AVAILABLE_VOLUNTEERS:
        assignment = added_volunteers.get(volunteer["id"])
        if not assignment:
            continue
        roster.append(
            {
                "id": volunteer["id"],
                "name": volunteer["name"],
                "agency": volunteer["agency"],
                "preferred_assignment": volunteer["preferred_assignment"],
                "current_assignment": assignment["current_assignment"],
                "initials": get_initials(volunteer["name"]),
                "status": "Confirmed",
            }
        )

    return roster


def build_fall_festival_staffing(roster):
    areas = []
    for requirement in FALL_FESTIVAL_STAFFING_REQUIREMENTS:
        assigned_count = sum(
            1 for officer in roster if officer["current_assignment"] == requirement["name"]
        )
        needed_count = max(requirement["required"] - assigned_count, 0)
        areas.append(
            {
                **requirement,
                "assigned": assigned_count,
                "needed": needed_count,
                "status": "FILLED" if needed_count == 0 else f"{needed_count} OFFICER NEEDED"
                if needed_count == 1
                else f"{needed_count} OFFICERS NEEDED",
                "status_class": "filled" if needed_count == 0 else "needs-officers",
            }
        )
    return areas


def get_fall_festival_operations():
    event = get_event("fall-festival")
    roster = build_fall_festival_roster()
    staffing_areas = build_fall_festival_staffing(roster)
    assigned_total = len(roster)
    required_total = sum(area["required"] for area in staffing_areas)
    needed_total = sum(area["needed"] for area in staffing_areas)
    added_volunteers = get_added_volunteer_assignments()
    available_volunteers = [
        {
            **volunteer,
            "initials": get_initials(volunteer["name"]),
        }
        for volunteer in FALL_FESTIVAL_AVAILABLE_VOLUNTEERS
        if volunteer["id"] not in added_volunteers
    ]
    return {
        "event": event,
        "roster": roster,
        "staffing_areas": staffing_areas,
        "assignment_options": get_assignment_options(),
        "available_volunteers": available_volunteers,
        "assigned_total": assigned_total,
        "required_total": required_total,
        "needed_total": needed_total,
        "needed_label": "FILLED"
        if needed_total == 0
        else f"{needed_total} OFFICER NEEDED"
        if needed_total == 1
        else f"{needed_total} OFFICERS NEEDED",
    }


def get_pending_assignment_acknowledgments():
    fall_signup = get_fall_signup_for_coordinator()
    if fall_signup.get("assignment_changed") and not fall_signup.get("assignment_change_acknowledged"):
        return 1
    return 0


def build_coordinator_dashboard_context():
    event_data = load_event_data()
    events = event_data["events"]
    fall_operations = get_fall_festival_operations()
    event_cards = []
    signed_up_total = 0
    staffing_gap_total = 0

    for event in events:
        if event["id"] == "fall-festival":
            assigned = fall_operations["assigned_total"]
            required = fall_operations["required_total"]
            needed = fall_operations["needed_total"]
            gap_areas = [
                area["name"] for area in fall_operations["staffing_areas"] if area["needed"] > 0
            ]
            detail_url = url_for("coordinator_event_detail", event_id=event["id"])
        else:
            assigned = event["signed_up"]
            required = event["minimum_needed"]
            needed = max(required - assigned, 0)
            gap_areas = event.get("assignment_areas", [])[:2] if needed else []
            detail_url = url_for("coordinator_event_detail", event_id=event["id"])

        signed_up_total += assigned
        staffing_gap_total += needed
        event_cards.append(
            {
                "event": event,
                "assigned": assigned,
                "required": required,
                "needed": needed,
                "status": "Minimum staffing met"
                if needed == 0
                else f"{needed} officer needed"
                if needed == 1
                else f"{needed} officers needed",
                "status_class": "filled" if needed == 0 else "needs-officers",
                "gap_areas": gap_areas,
                "detail_url": detail_url,
            }
        )

    return {
        "coordinator_user": COORDINATOR_USER,
        "event_cards": event_cards,
        "summary": {
            "upcoming_events": len(events),
            "signed_up": signed_up_total,
            "staffing_gaps": staffing_gap_total,
            "pending_acknowledgments": get_pending_assignment_acknowledgments(),
        },
    }


def build_coordinator_event_context(event_id):
    if event_id != "fall-festival":
        event = get_event(event_id)
        if event is None:
            abort(404)
        return {
            "coordinator_user": COORDINATOR_USER,
            "event": event,
            "is_fall_festival": False,
        }

    return {
        "coordinator_user": COORDINATOR_USER,
        "is_fall_festival": True,
        **get_fall_festival_operations(),
    }


def update_alex_assignment(assignment_id="sports-arena"):
    fall_event = get_event("fall-festival")
    if fall_event is None:
        return

    demo_signups = get_demo_signups()
    fall_signup = demo_signups.get("fall-festival", {})
    previous_assignment = fall_signup.get(
        "current_assignment_name",
        fall_signup.get("provisional_assignment_name", "Bocce Awards"),
    )
    new_assignment = resolve_assignment(fall_event, assignment_id)
    preferred_assignment = fall_signup.get("preferred_assignment", "bocce-awards")
    preferred_assignment_name = fall_signup.get("preferred_assignment_name", "Bocce Awards")

    if new_assignment is None:
        return

    fall_signup.update(
        {
            "event_id": "fall-festival",
            "signed_up": True,
            "preferred_assignment": preferred_assignment,
            "preferred_assignment_name": preferred_assignment_name,
            "previous_assignment": previous_assignment,
            "current_assignment": new_assignment["id"],
            "current_assignment_name": new_assignment["name"],
            "provisional_assignment": new_assignment["id"],
            "provisional_assignment_name": new_assignment["name"],
            "assignment_changed": True,
            "assignment_change_acknowledged": False,
            "signup_completed": True,
        }
    )
    demo_signups["fall-festival"] = fall_signup
    session["demo_signups"] = demo_signups
    session.modified = True


def update_alex_assignment_to_sports_arena():
    update_alex_assignment("sports-arena")


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


@app.route("/leaderboard")
def leaderboard():
    if "demo_user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "officer/leaderboard.html",
        demo_user=session["demo_user"],
        **build_leaderboard_context(),
    )


@app.route("/demo/switch/coordinator")
def switch_to_coordinator():
    if "demo_user" not in session:
        return redirect(url_for("login"))
    session["demo_role"] = "coordinator"
    return redirect(url_for("coordinator_dashboard"))


@app.route("/demo/switch/officer")
def switch_to_officer():
    if "demo_user" not in session:
        return redirect(url_for("login"))
    session["demo_role"] = "officer"
    return redirect(url_for("opportunities"))


@app.route("/coordinator")
def coordinator_dashboard():
    if "demo_user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "coordinator/dashboard.html",
        **build_coordinator_dashboard_context(),
    )


@app.route("/coordinator/events/<event_id>")
def coordinator_event_detail(event_id):
    if "demo_user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "coordinator/event_detail.html",
        **build_coordinator_event_context(event_id),
    )


@app.route("/coordinator/events/<event_id>/reassign", methods=["POST"])
def coordinator_reassign_officer(event_id):
    if "demo_user" not in session:
        return redirect(url_for("login"))

    if event_id != "fall-festival":
        abort(404)

    officer_id = request.form.get("officer_id")
    new_assignment = request.form.get("new_assignment")
    if officer_id == "alex-morgan":
        update_alex_assignment(new_assignment)
    elif officer_id:
        save_coordinator_assignment_override(officer_id, new_assignment)

    return redirect(url_for("coordinator_event_detail", event_id=event_id))


@app.route("/coordinator/events/<event_id>/assign-volunteer", methods=["POST"])
def coordinator_assign_volunteer(event_id):
    if "demo_user" not in session:
        return redirect(url_for("login"))

    if event_id != "fall-festival":
        abort(404)

    assign_available_volunteer(
        request.form.get("volunteer_id"),
        request.form.get("assignment_id"),
    )
    return redirect(url_for("coordinator_event_detail", event_id=event_id, assigned="1"))


@app.route("/coordinator/volunteers")
def coordinator_volunteers():
    if "demo_user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "coordinator/placeholder.html",
        coordinator_user=COORDINATOR_USER,
        active_section="volunteers",
        title="VOLUNTEERS",
        subtitle="Volunteer directory and participation management. Demo workflow coming in the next build phase.",
    )


@app.route("/coordinator/reports")
def coordinator_reports():
    if "demo_user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "coordinator/reports.html",
        **build_coordinator_reports_context(),
    )


@app.route("/demo/simulate-assignment-change")
def simulate_assignment_change():
    if "demo_user" not in session:
        return redirect(url_for("login"))

    fall_signup = get_event_signup("fall-festival")
    if not fall_signup or not fall_signup.get("signed_up"):
        return redirect(url_for("my_events"))

    update_alex_assignment_to_sports_arena()
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
    session.pop("coordinator_assignment_overrides", None)
    session.pop("coordinator_added_volunteers", None)
    session.modified = True
    return redirect(url_for("opportunities"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
