import os
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash


def get_connection():
    """Return a new MySQL connection using environment-based configuration."""
    return mysql.connector.connect(host=os.getenv("MYSQL_HOST", "localhost"), port=int(os.getenv("MYSQL_PORT", "3306")), user=os.getenv("MYSQL_USER", "root"), password=os.getenv("MYSQL_PASSWORD", ""), database=os.getenv("MYSQL_DATABASE", "VPSHostingDB"))


def fetch_all(query, params=()):
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params); return cursor.fetchall()
    finally:
        cursor.close(); connection.close()


def fetch_one(query, params=()):
    connection = get_connection(); cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params); return cursor.fetchone()
    finally:
        cursor.close(); connection.close()


def execute_query(query, params=()):
    connection = get_connection(); cursor = connection.cursor()
    try:
        cursor.execute(query, params); connection.commit(); return cursor.lastrowid
    except Error:
        connection.rollback(); raise
    finally:
        cursor.close(); connection.close()


def ensure_default_admin():
    email = "admin@vpshosting.local"
    if not fetch_one("SELECT UserID FROM `USER` WHERE Email=%s", (email,)):
        execute_query("INSERT INTO `USER` (FullName, Email, Phone, PasswordHash, CreatedAt) VALUES (%s,%s,%s,%s,NOW())", ("System Administrator", email, "0000000000", generate_password_hash("Admin@123")))
