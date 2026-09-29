from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "sode-demo-only-secret-key"

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
    return render_template("officer/opportunities_placeholder.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
