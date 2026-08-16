from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from database import execute_query, fetch_all, fetch_one
from routes.helpers import login_required
vps_bp = Blueprint("vps", __name__, url_prefix="/vps")

def options():
    return (fetch_all("SELECT UserID,FullName FROM `USER` ORDER BY FullName"), fetch_all("SELECT PlanID,PlanName FROM PLAN ORDER BY PlanName"), fetch_all("SELECT ServerID,ServerName FROM SERVER ORDER BY ServerName"))

@vps_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        try:
            execute_query("INSERT INTO VPS (IPAddress,OS,RAM,CPU,Status,CreatedAt,ExpireDate,UserID,PlanID,ServerID) VALUES (%s,%s,%s,%s,%s,NOW(),%s,%s,%s,%s)", (request.form["ip_address"],request.form["os"],request.form["ram"],request.form["cpu"],request.form["status"],request.form["expire_date"],request.form["user_id"],request.form["plan_id"],request.form["server_id"]))
            flash("VPS created.", "success"); return redirect(url_for("vps.index"))
        except Error as e: flash(f"Could not create VPS: {e.msg}", "danger")
    search,status = request.args.get("ip", "").strip(),request.args.get("status", "")
    items = fetch_all("SELECT v.*,u.FullName,p.PlanName,s.ServerName FROM VPS v JOIN `USER` u ON u.UserID=v.UserID JOIN PLAN p ON p.PlanID=v.PlanID JOIN SERVER s ON s.ServerID=v.ServerID WHERE v.IPAddress LIKE %s AND (%s='' OR v.Status=%s) ORDER BY v.VPSID DESC", (f"%{search}%",status,status))
    users,plans,servers=options(); return render_template("vps.html", vps_list=items, users=users, plans=plans, servers=servers, edit_vps=None, search=search, selected_status=status)

@vps_bp.route("/<int:vps_id>/edit", methods=["GET", "POST"])
@login_required
def edit(vps_id):
    item=fetch_one("SELECT * FROM VPS WHERE VPSID=%s", (vps_id,))
    if not item: flash("VPS not found.", "warning"); return redirect(url_for("vps.index"))
    if request.method == "POST":
        try:
            execute_query("UPDATE VPS SET IPAddress=%s,OS=%s,RAM=%s,CPU=%s,Status=%s,ExpireDate=%s,UserID=%s,PlanID=%s,ServerID=%s WHERE VPSID=%s", (request.form["ip_address"],request.form["os"],request.form["ram"],request.form["cpu"],request.form["status"],request.form["expire_date"],request.form["user_id"],request.form["plan_id"],request.form["server_id"],vps_id)); flash("VPS updated.", "success"); return redirect(url_for("vps.index"))
        except Error as e: flash(f"Could not update VPS: {e.msg}", "danger")
    users,plans,servers=options(); return render_template("vps.html",vps_list=fetch_all("SELECT v.*,u.FullName,p.PlanName,s.ServerName FROM VPS v JOIN `USER` u ON u.UserID=v.UserID JOIN PLAN p ON p.PlanID=v.PlanID JOIN SERVER s ON s.ServerID=v.ServerID ORDER BY v.VPSID DESC"),users=users,plans=plans,servers=servers,edit_vps=item,search="",selected_status="")

@vps_bp.post("/<int:vps_id>/status")
@login_required
def status(vps_id):
    execute_query("UPDATE VPS SET Status=%s WHERE VPSID=%s", (request.form["status"],vps_id)); flash("VPS status updated.", "success"); return redirect(url_for("vps.index"))

@vps_bp.post("/<int:vps_id>/delete")
@login_required
def delete(vps_id):
    try: execute_query("DELETE FROM VPS WHERE VPSID=%s", (vps_id,)); flash("VPS deleted.", "success")
    except Error as e: flash(f"Cannot delete VPS with assignments: {e.msg}", "danger")
    return redirect(url_for("vps.index"))
