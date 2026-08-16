from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from database import fetch_one

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"): return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        email, password = request.form.get("email", "").strip().lower(), request.form.get("password", "")
        user = fetch_one("SELECT UserID, FullName, Email, PasswordHash FROM `USER` WHERE Email=%s", (email,))
        if user and check_password_hash(user["PasswordHash"], password):
            session.clear(); session.update(user_id=user["UserID"], user_name=user["FullName"]); return redirect(url_for("dashboard.index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear(); flash("You have been logged out.", "success"); return redirect(url_for("auth.login"))
