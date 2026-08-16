from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from database import execute_query, fetch_all
from routes.helpers import login_required
invoices_bp=Blueprint("invoices",__name__,url_prefix="/invoices")
@invoices_bp.route("/",methods=["GET","POST"])
@login_required
def index():
    if request.method=="POST":
        try:
            execute_query("INSERT INTO INVOICE (Amount,IssueDate,DueDate,Status,UserID) VALUES (%s,%s,%s,%s,%s)",(request.form["amount"],request.form["issue_date"],request.form["due_date"],request.form["status"],request.form["user_id"]))
            flash("Invoice created.","success");return redirect(url_for("invoices.index"))
        except Error as e: flash(f"Could not create invoice: {e.msg}","danger")
    invoices=fetch_all("SELECT i.*,u.FullName,COALESCE(SUM(p.Amount),0) AS PaidAmount FROM INVOICE i JOIN `USER` u ON u.UserID=i.UserID LEFT JOIN PAYMENT p ON p.InvoiceID=i.InvoiceID AND p.Status='Completed' GROUP BY i.InvoiceID ORDER BY i.InvoiceID DESC")
    return render_template("invoices.html",invoices=invoices,users=fetch_all("SELECT UserID,FullName FROM `USER` ORDER BY FullName"))
