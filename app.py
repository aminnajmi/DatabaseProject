import os
from flask import Flask
from database import ensure_default_admin


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-this-development-secret-key")
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.users import users_bp
    from routes.vps import vps_bp
    from routes.domains import domains_bp
    from routes.invoices import invoices_bp
    from routes.tickets import tickets_bp
    from routes.reports import reports_bp
    for blueprint in (auth_bp, dashboard_bp, users_bp, vps_bp, domains_bp, invoices_bp, tickets_bp, reports_bp):
        app.register_blueprint(blueprint)
    try:
        ensure_default_admin()
    except Exception as error:
        app.logger.warning("Default admin setup skipped: %s", error)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
