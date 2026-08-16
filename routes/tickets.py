from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error
from database import execute_query, fetch_all
from routes.helpers import login_required
tickets_bp=Blueprint("tickets",__name__,url_prefix="/tickets")
@tickets_bp.route("/",methods=["GET","POST"])
@login_required
def index():
    if request.method=="POST":
        try:
            execute_query("INSERT INTO TICKET (Subject,Message,Status,CreatedAt,UserID) VALUES (%s,%s,%s,NOW(),%s)",(request.form["subject"],request.form["message"],request.form["status"],request.form["user_id"]))
            flash("Ticket created.","success");return redirect(url_for("tickets.index"))
        except Error as e: flash(f"Could not create ticket: {e.msg}","danger")
    tickets=fetch_all("SELECT t.*,u.FullName FROM TICKET t JOIN `USER` u ON u.UserID=t.UserID ORDER BY t.TicketID DESC")
    return render_template("tickets.html",tickets=tickets,users=fetch_all("SELECT UserID,FullName FROM `USER` ORDER BY FullName"))
@tickets_bp.post("/<int:ticket_id>/status")
@login_required
def status(ticket_id):
    execute_query("UPDATE TICKET SET Status=%s WHERE TicketID=%s",(request.form["status"],ticket_id));flash("Ticket status updated.","success");return redirect(url_for("tickets.index"))
