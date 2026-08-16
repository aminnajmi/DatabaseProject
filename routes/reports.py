from flask import Blueprint, render_template
from database import fetch_all
from routes.helpers import login_required
reports_bp=Blueprint("reports",__name__,url_prefix="/reports")
@reports_bp.route("/")
@login_required
def index():
    reports={
      "vps":fetch_all("SELECT u.FullName,u.Email,v.IPAddress,v.OS,v.RAM,v.CPU,v.Status,p.PlanName,p.Price,s.ServerName,d.Name AS Datacenter,d.Country,d.City FROM `USER` u JOIN VPS v ON v.UserID=u.UserID JOIN PLAN p ON p.PlanID=v.PlanID JOIN SERVER s ON s.ServerID=v.ServerID JOIN DATACENTER d ON d.DatacenterID=s.DatacenterID ORDER BY u.FullName"),
      "domains":fetch_all("SELECT u.FullName,dm.DomainName,dm.ExpireDate,v.IPAddress,s.ServerName,d.Name AS Datacenter FROM `USER` u JOIN DOMAIN dm ON dm.UserID=u.UserID JOIN VPS_DOMAIN vd ON vd.DomainID=dm.DomainID JOIN VPS v ON v.VPSID=vd.VPSID JOIN SERVER s ON s.ServerID=v.ServerID JOIN DATACENTER d ON d.DatacenterID=s.DatacenterID ORDER BY dm.ExpireDate"),
      "financial":fetch_all("SELECT u.FullName,i.InvoiceID,i.Amount AS InvoiceAmount,i.Status AS InvoiceStatus,pay.PaymentDate,pay.Amount AS PaymentAmount,pay.Status AS PaymentStatus,v.IPAddress,pl.PlanName FROM `USER` u JOIN INVOICE i ON i.UserID=u.UserID LEFT JOIN PAYMENT pay ON pay.InvoiceID=i.InvoiceID LEFT JOIN VPS v ON v.UserID=u.UserID LEFT JOIN PLAN pl ON pl.PlanID=v.PlanID ORDER BY i.InvoiceID DESC"),
      "tickets":fetch_all("SELECT u.FullName,t.TicketID,t.Subject,t.Status,t.CreatedAt,v.IPAddress,p.PlanName FROM `USER` u JOIN TICKET t ON t.UserID=u.UserID LEFT JOIN VPS v ON v.UserID=u.UserID LEFT JOIN PLAN p ON p.PlanID=v.PlanID ORDER BY t.TicketID DESC")}
    return render_template("reports.html",reports=reports)
