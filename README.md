# VPS Hosting Management System

A Flask and MySQL university project demonstrating raw SQL CRUD operations, many-to-many domain assignment, authentication, dashboard metrics, and multi-table reports.

## Install and run

1. Ensure MySQL is running and the existing `VPSHostingDB` schema/tables listed in the project brief have been created.
2. From this directory, create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Configure MySQL credentials (defaults are host `localhost`, port `3306`, user `root`, empty password):
   ```bash
   export MYSQL_HOST=localhost MYSQL_PORT=3306 MYSQL_USER=root MYSQL_PASSWORD='your-password' MYSQL_DATABASE=VPSHostingDB
   ```
5. Run: `python app.py`
6. Open http://127.0.0.1:5000.

The app creates a default administrator when it first connects successfully:

- Email: `admin@vpshosting.local`
- Password: `Admin@123`

Change the Flask secret in production with `FLASK_SECRET_KEY`. All database values are passed through parameterized MySQL connector queries; no ORM is used.

## Powered by Graphyfy for easier development
<img width="1009" height="866" alt="Screenshot 2026-09-25 at 23 30 27" src="https://github.com/user-attachments/assets/6a59d5ab-31b1-44ea-b53f-9caa207e78fa" />
