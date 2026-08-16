from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash
from mysql.connector import Error
from database import execute_query, fetch_all, fetch_one
from routes.helpers import login_required, missing_fields
users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        missing = missing_fields(request.form, {"full_name":"full name", "email":"email", "password":"password"})
        if missing: flash("Required: " + ", ".join(missing), "danger")
        else:
            try:
                execute_query("INSERT INTO `USER` (FullName,Email,Phone,PasswordHash,CreatedAt) VALUES (%s,%s,%s,%s,NOW())", (request.form["full_name"].strip(), request.form["email"].strip().lower(), request.form.get("phone", "").strip(), generate_password_hash(request.form["password"])))
                flash("User created.", "success"); return redirect(url_for("users.index"))
            except Error as e: flash(f"Could not create user: {e.msg}", "danger")
    search = request.args.get("email", "").strip()
    users = fetch_all("SELECT UserID,FullName,Email,Phone,CreatedAt FROM `USER` WHERE Email LIKE %s ORDER BY UserID DESC", (f"%{search}%",))
    return render_template("users.html", users=users, edit_user=None, search=search)

@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit(user_id):
    user = fetch_one("SELECT UserID,FullName,Email,Phone FROM `USER` WHERE UserID=%s", (user_id,))
    if not user: flash("User not found.", "warning"); return redirect(url_for("users.index"))
    if request.method == "POST":
        try:
            args = [request.form["full_name"].strip(),request.form["email"].strip().lower(),request.form.get("phone", "").strip()]
            query = "UPDATE `USER` SET FullName=%s,Email=%s,Phone=%s"
            if request.form.get("password"): query += ",PasswordHash=%s"; args.append(generate_password_hash(request.form["password"]))
            execute_query(query + " WHERE UserID=%s", tuple(args+[user_id])); flash("User updated.", "success"); return redirect(url_for("users.index"))
        except Error as e: flash(f"Could not update user: {e.msg}", "danger")
    return render_template("users.html", users=fetch_all("SELECT UserID,FullName,Email,Phone,CreatedAt FROM `USER` ORDER BY UserID DESC"), edit_user=user, search="")

@users_bp.post("/<int:user_id>/delete")
@login_required
def delete(user_id):
    try: execute_query("DELETE FROM `USER` WHERE UserID=%s", (user_id,)); flash("User deleted.", "success")
    except Error as e: flash(f"Cannot delete a user with related records: {e.msg}", "danger")
    return redirect(url_for("users.index"))
