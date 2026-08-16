from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import fetch_all, execute_query
from routes.helpers import login_required

domains_bp = Blueprint("domains", __name__, url_prefix="/domains")


@domains_bp.route("/")
@login_required
def index():

    expiry = request.args.get("expires_before", "").strip()

    if expiry:
        domains = fetch_all(
            """
            SELECT 
                d.*,
                u.FullName,
                GROUP_CONCAT(v.IPAddress SEPARATOR ', ') AS VPSIPs
            FROM DOMAIN d
            JOIN `USER` u 
                ON u.UserID = d.UserID
            LEFT JOIN VPS_DOMAIN vd 
                ON vd.DomainID = d.DomainID
            LEFT JOIN VPS v 
                ON v.VPSID = vd.VPSID
            WHERE d.ExpireDate <= %s
            GROUP BY d.DomainID
            ORDER BY d.ExpireDate
            """,
            (expiry,)
        )

    else:
        domains = fetch_all(
            """
            SELECT 
                d.*,
                u.FullName,
                GROUP_CONCAT(v.IPAddress SEPARATOR ', ') AS VPSIPs
            FROM DOMAIN d
            JOIN `USER` u 
                ON u.UserID = d.UserID
            LEFT JOIN VPS_DOMAIN vd 
                ON vd.DomainID = d.DomainID
            LEFT JOIN VPS v 
                ON v.VPSID = vd.VPSID
            GROUP BY d.DomainID
            ORDER BY d.ExpireDate
            """
        )


    users = fetch_all(
        """
        SELECT UserID, FullName
        FROM `USER`
        ORDER BY FullName
        """
    )


    vps_list = fetch_all(
        """
        SELECT VPSID, IPAddress
        FROM VPS
        ORDER BY IPAddress
        """
    )


    # آماده سازی VPS های متصل به هر Domain
    assigned_by_domain = {}

    assignments = fetch_all(
        """
        SELECT
            vd.DomainID,
            v.VPSID,
            v.IPAddress
        FROM VPS_DOMAIN vd
        JOIN VPS v
            ON v.VPSID = vd.VPSID
        """
    )


    for item in assignments:

        domain_id = item["DomainID"]

        if domain_id not in assigned_by_domain:
            assigned_by_domain[domain_id] = []

        assigned_by_domain[domain_id].append(item)


    return render_template(
        "domains.html",
        domains=domains,
        users=users,
        vps_list=vps_list,
        assigned_by_domain=assigned_by_domain,
        expires_before=expiry
    )



@domains_bp.route("/add", methods=["POST"])
@login_required
def add():

    execute_query(
        """
        INSERT INTO DOMAIN
        (
            DomainName,
            RegisterDate,
            ExpireDate,
            AutoRenew,
            Status,
            UserID
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            request.form.get("domain_name"),
            request.form.get("register_date"),
            request.form.get("expire_date"),
            1 if request.form.get("auto_renew") else 0,
            request.form.get("status"),
            request.form.get("user_id")
        )
    )

    flash("Domain added successfully", "success")

    return redirect(url_for("domains.index"))



@domains_bp.route("/assign/<int:domain_id>", methods=["POST"])
@login_required
def assign(domain_id):

    execute_query(
        """
        INSERT INTO VPS_DOMAIN
        (
            VPSID,
            DomainID,
            AssignDate
        )
        VALUES (%s,%s,CURDATE())
        """,
        (
            request.form.get("vps_id"),
            domain_id
        )
    )

    flash("VPS assigned successfully", "success")

    return redirect(url_for("domains.index"))



@domains_bp.route("/unassign/<int:domain_id>/<int:vps_id>", methods=["POST"])
@login_required
def unassign(domain_id, vps_id):

    execute_query(
        """
        DELETE FROM VPS_DOMAIN
        WHERE DomainID=%s
        AND VPSID=%s
        """,
        (
            domain_id,
            vps_id
        )
    )

    flash("VPS removed from domain", "success")

    return redirect(url_for("domains.index"))



@domains_bp.route("/delete/<int:domain_id>")
@login_required
def delete(domain_id):

    execute_query(
        """
        DELETE FROM VPS_DOMAIN
        WHERE DomainID=%s
        """,
        (domain_id,)
    )


    execute_query(
        """
        DELETE FROM DOMAIN
        WHERE DomainID=%s
        """,
        (domain_id,)
    )


    flash("Domain deleted successfully", "success")

    return redirect(url_for("domains.index"))