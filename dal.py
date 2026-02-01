# dal.py
"""
Simple Data Access Layer for homework_tracker using mysql-connector-python.
Place .env in the same folder with DB credentials.
"""

import os
import mysql.connector
from mysql.connector import errorcode
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', ''),
    'database': os.getenv('DB_NAME', 'homework_tracker'),
    'autocommit': True,
}

@contextmanager
def get_conn_cursor():
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)
        yield conn, cur
    except mysql.connector.Error as err:
        print("DB error:", err)
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# -------------------------
# Users CRUD
# -------------------------
def create_user(username, full_name=None, email=None, role='student'):
    sql = "INSERT INTO users (username, full_name, email, role) VALUES (%s,%s,%s,%s)"
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql, (username, full_name, email, role))
        return cur.lastrowid

def get_user(user_id):
    sql = "SELECT * FROM users WHERE id = %s"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (user_id,))
        return cur.fetchone()

def list_users():
    sql = "SELECT * FROM users ORDER BY id"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql)
        return cur.fetchall()

# -------------------------
# Courses CRUD
# -------------------------
def create_course(code, title, term=None):
    sql = "INSERT INTO courses (code, title, term) VALUES (%s,%s,%s)"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (code, title, term))
        return cur.lastrowid

def list_courses():
    sql = "SELECT * FROM courses ORDER BY id"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql)
        return cur.fetchall()

def get_course(course_id):
    sql = "SELECT * FROM courses WHERE id = %s"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (course_id,))
        return cur.fetchone()

# -------------------------
# Assignments CRUD
# -------------------------
def create_assignment(course_id, title, due_date=None, points=100):
    sql = "INSERT INTO assignments (course_id, title, due_date, points) VALUES (%s,%s,%s,%s)"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (course_id, title, due_date, points))
        return cur.lastrowid

def list_assignments_for_course(course_id):
    sql = "SELECT * FROM assignments WHERE course_id = %s ORDER BY due_date"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (course_id,))
        return cur.fetchall()

def get_assignment(assignment_id):
    sql = "SELECT * FROM assignments WHERE id = %s"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (assignment_id,))
        return cur.fetchone()

# -------------------------
# Submissions CRUD
# -------------------------
def create_submission(assignment_id, user_id, score=None, content=None):
    sql = "INSERT INTO submissions (assignment_id, user_id, submitted_at, content, score) VALUES (%s,%s,NOW(),%s,%s)"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (assignment_id, user_id, content, score))
        return cur.lastrowid

def list_submissions_for_assignment(assignment_id):
    sql = "SELECT s.*, u.username, u.full_name FROM submissions s JOIN users u ON u.id = s.user_id WHERE s.assignment_id = %s ORDER BY s.submitted_at DESC"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (assignment_id,))
        return cur.fetchall()

def update_submission_score(submission_id, new_score, feedback=None):
    sql = "UPDATE submissions SET score = %s, feedback = %s WHERE id = %s"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (new_score, feedback, submission_id))
        return cur.rowcount

def delete_submission(submission_id):
    sql = "DELETE FROM submissions WHERE id = %s"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql, (submission_id,))
        return cur.rowcount

# -------------------------
# Utility helpers
# -------------------------
def count_table_rows(table):
    sql = f"SELECT COUNT(*) AS cnt FROM {table}"
    with get_conn_cursor() as (_, cur):
        cur.execute(sql)
        return cur.fetchone().get('cnt')

if __name__ == "__main__":
    # quick smoke test (prints counts)
    try:
        print("Users:", count_table_rows("users"))
        print("Courses:", count_table_rows("courses"))
        print("Assignments:", count_table_rows("assignments"))
        print("Submissions:", count_table_rows("submissions"))
    except Exception as e:
        print("Error during DAL smoke test:", e)

