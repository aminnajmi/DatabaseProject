from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from database import execute_query, fetch_all
from routes.helpers import login_required
domains_bp=Blueprint("domains",__name__,url_prefix="/domains")

@domains_bp.route("/",methods=["GET","POST"])
@login_required
def index():
    if request.method=="POST":
        try:
            execute_query("INSERT INTO DOMAIN (DomainName,RegisterDate,ExpireDate,AutoRenew,Status,UserID) VALUES (%s,%s,%s,%s,%s,%s)",(request.form["domain_name"],request.form["register_date"],request.form["expire_date"],request.form.get("auto_renew",0),request.form["status"],request.form["user_id"]))
            flash("Domain created.","success");return redirect(url_for("domains.index"))
        except Error as e: flash(f"Could not create domain: {e.msg}","danger")
    expiry=request.args.get("expires_before","")
    domains=fetch_all("SELECT d.*,u.FullName,GROUP_CONCAT(v.IPAddress SEPARATOR ', ') AS VPSIPs FROM DOMAIN d JOIN `USER` u ON u.UserID=d.UserID LEFT JOIN VPS_DOMAIN vd ON vd.DomainID=d.DomainID LEFT JOIN VPS v ON v.VPSID=vd.VPSID WHERE (%s='' OR d.ExpireDate<=%s) GROUP BY d.DomainID ORDER BY d.ExpireDate",(expiry,expiry))
    assignments=fetch_all("SELECT vd.DomainID,v.VPSID,v.IPAddress FROM VPS_DOMAIN vd JOIN VPS v ON v.VPSID=vd.VPSID")
    assigned_by_domain={}
    for assignment in assignments: assigned_by_domain.setdefault(assignment["DomainID"], []).append(assignment)
    return render_template("domains.html",domains=domains,users=fetch_all("SELECT UserID,FullName FROM `USER` ORDER BY FullName"),vps_list=fetch_all("SELECT VPSID,IPAddress FROM VPS ORDER BY IPAddress"),expires_before=expiry,assigned_by_domain=assigned_by_domain)

@domains_bp.post("/<int:domain_id>/assign")
@login_required
def assign(domain_id):
    try: execute_query("INSERT INTO VPS_DOMAIN (VPSID,DomainID,AssignDate) VALUES (%s,%s,NOW())",(request.form["vps_id"],domain_id));flash("Domain assigned to VPS.","success")
    except Error as e: flash(f"Could not assign domain: {e.msg}","danger")
    return redirect(url_for("domains.index"))

@domains_bp.post("/<int:domain_id>/unassign/<int:vps_id>")
@login_required
def unassign(domain_id,vps_id):
    execute_query("DELETE FROM VPS_DOMAIN WHERE VPSID=%s AND DomainID=%s",(vps_id,domain_id));flash("Domain assignment removed.","success");return redirect(url_for("domains.index"))
