from functools import wraps
from flask import flash, redirect, session, url_for

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.", "warning"); return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped

def missing_fields(form, fields):
    return [label for name, label in fields.items() if not form.get(name, "").strip()]
