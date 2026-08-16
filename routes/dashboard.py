from flask import Blueprint, render_template
from database import fetch_one
from routes.helpers import login_required
dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    def count(table, condition=""):
        return fetch_one(f"SELECT COUNT(*) AS total FROM {table} {condition}")["total"]
    stats = {"users":count("`USER`"), "vps":count("VPS"), "domains":count("DOMAIN"), "servers":count("SERVER"), "invoices":count("INVOICE"), "active_vps":count("VPS", "WHERE Status='Active'")}
    return render_template("dashboard.html", stats=stats)
