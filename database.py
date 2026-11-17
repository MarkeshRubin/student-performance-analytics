"""
database.py - Database Management & Seeding Module for Student Performance Analytics
Relational SQLite schema with 4 core tables:
1. students
2. subjects
3. assessments
4. performance
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'student_analytics.db')


def get_db_connection():
    """Establish and return a connection to the SQLite database with Row support."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def calculate_risk_status(marks: float, attendance: float) -> str:
    """
    Classify student risk status based on institutional criteria:
    - High Risk: marks < 50 or attendance < 60
    - Warning: marks < 70 or attendance < 75
    - Safe: otherwise
    """
    try:
        m = float(marks)
        a = float(attendance)
    except (ValueError, TypeError):
        return "Safe"

    if m < 50 or a < 60:
        return "High Risk"
    elif m < 70 or a < 75:
        return "Warning"
    else:
        return "Safe"


def init_db():
    """Initialize schema tables and seed data if database is empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            batch_class TEXT NOT NULL,
            semester TEXT NOT NULL
        );
    """)

    # 2. subjects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            semester TEXT NOT NULL,
            UNIQUE(subject_name, semester)
        );
    """)

    # 3. assessments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            assessment_name TEXT NOT NULL,
            max_marks REAL NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
        );
    """)

    # 4. performance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            marks_obtained REAL NOT NULL,
            attendance_pct REAL NOT NULL,
            risk_status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
        );
    """)

    conn.commit()

    # Check if performance table needs seeding
    cursor.execute("SELECT COUNT(*) FROM performance;")
    count = cursor.fetchone()[0]

    if count == 0:
        seed_database(cursor)
        conn.commit()

    conn.close()


def seed_database(cursor):
    """Seed initial realistic records across batches, semesters, and subjects."""
    # 1. Seed Subjects
    subject_catalog = [
        ("Data Structures", "Sem 3"),
        ("Mathematics III", "Sem 1"),
        ("Database Systems", "Sem 2"),
        ("Operating Systems", "Sem 3"),
    ]

    subject_ids = {}
    for name, sem in subject_catalog:
        cursor.execute(
            "INSERT OR IGNORE INTO subjects (subject_name, semester) VALUES (?, ?);",
            (name, sem)
        )
        cursor.execute(
            "SELECT subject_id FROM subjects WHERE subject_name = ? AND semester = ?;",
            (name, sem)
        )
        row = cursor.fetchone()
        subject_ids[name] = row["subject_id"]

    # 2. Seed Assessments for subjects
    assessment_types = [
        ("Quiz 1", 20.0),
        ("Assignment 1", 50.0),
        ("Midterm", 100.0),
        ("Assignment 2", 50.0),
        ("Final Exam", 100.0),
    ]

    for subj_name, s_id in subject_ids.items():
        for a_name, m_marks in assessment_types:
            cursor.execute(
                """
                INSERT OR IGNORE INTO assessments (subject_id, assessment_name, max_marks)
                VALUES (?, ?, ?);
                """,
                (s_id, a_name, m_marks)
            )

    # 3. Seed Students & Performance (10 realistic records across CS-A, CS-B, IT-A)
    seed_records = [
        {
            "id": "ST-1001",
            "name": "John Smith",
            "email": "john.smith@university.edu",
            "batch": "CS-A",
            "semester": "Sem 3",
            "subject": "Data Structures",
            "marks": 88.0,
            "attendance": 92.0
        },
        {
            "id": "ST-1002",
            "name": "Emily Davis",
            "email": "emily.davis@university.edu",
            "batch": "CS-A",
            "semester": "Sem 3",
            "subject": "Data Structures",
            "marks": 54.0,
            "attendance": 65.0
        },
        {
            "id": "ST-1003",
            "name": "Michael Brown",
            "email": "michael.brown@university.edu",
            "batch": "CS-B",
            "semester": "Sem 2",
            "subject": "Database Systems",
            "marks": 41.0,
            "attendance": 52.0
        },
        {
            "id": "ST-1004",
            "name": "Sarah Wilson",
            "email": "sarah.wilson@university.edu",
            "batch": "IT-A",
            "semester": "Sem 3",
            "subject": "Operating Systems",
            "marks": 92.0,
            "attendance": 96.0
        },
        {
            "id": "ST-1005",
            "name": "David Martinez",
            "email": "david.martinez@university.edu",
            "batch": "CS-B",
            "semester": "Sem 1",
            "subject": "Mathematics III",
            "marks": 58.0,
            "attendance": 70.0
        },
        {
            "id": "ST-1006",
            "name": "Jessica Taylor",
            "email": "jessica.taylor@university.edu",
            "batch": "IT-A",
            "semester": "Sem 2",
            "subject": "Database Systems",
            "marks": 35.0,
            "attendance": 48.0
        },
        {
            "id": "ST-1007",
            "name": "Robert Anderson",
            "email": "robert.anderson@university.edu",
            "batch": "CS-A",
            "semester": "Sem 1",
            "subject": "Mathematics III",
            "marks": 81.0,
            "attendance": 88.0
        },
        {
            "id": "ST-1008",
            "name": "Lisa Thomas",
            "email": "lisa.thomas@university.edu",
            "batch": "CS-B",
            "semester": "Sem 3",
            "subject": "Operating Systems",
            "marks": 74.0,
            "attendance": 82.0
        },
        {
            "id": "ST-1009",
            "name": "Kevin Chen",
            "email": "kevin.chen@university.edu",
            "batch": "IT-A",
            "semester": "Sem 1",
            "subject": "Mathematics III",
            "marks": 62.0,
            "attendance": 68.0
        },
        {
            "id": "ST-1010",
            "name": "Sophia Patel",
            "email": "sophia.patel@university.edu",
            "batch": "CS-B",
            "semester": "Sem 2",
            "subject": "Database Systems",
            "marks": 95.0,
            "attendance": 94.0
        }
    ]

    for item in seed_records:
        cursor.execute(
            """
            INSERT OR IGNORE INTO students (student_id, full_name, email, batch_class, semester)
            VALUES (?, ?, ?, ?, ?);
            """,
            (item["id"], item["name"], item["email"], item["batch"], item["semester"])
        )

        subj_id = subject_ids.get(item["subject"])
        if not subj_id:
            cursor.execute(
                "INSERT INTO subjects (subject_name, semester) VALUES (?, ?);",
                (item["subject"], item["semester"])
            )
            subj_id = cursor.lastrowid
            subject_ids[item["subject"]] = subj_id

        risk = calculate_risk_status(item["marks"], item["attendance"])

        cursor.execute(
            """
            INSERT INTO performance (student_id, subject_id, marks_obtained, attendance_pct, risk_status)
            VALUES (?, ?, ?, ?, ?);
            """,
            (item["id"], subj_id, item["marks"], item["attendance"], risk)
        )


def get_all_student_performance():
    """Retrieve joined student performance records ordered by record_id ascending."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            p.record_id,
            s.student_id AS id,
            s.full_name AS name,
            s.email,
            s.batch_class AS batch,
            s.semester,
            sub.subject_name AS subject,
            p.marks_obtained AS marks,
            p.attendance_pct AS attendance,
            p.risk_status AS risk
        FROM performance p
        JOIN students s ON p.student_id = s.student_id
        JOIN subjects sub ON p.subject_id = sub.subject_id
        ORDER BY p.record_id ASC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def add_student_performance(name: str, batch: str, semester: str, subject: str, marks: float, attendance: float, email: str = None, student_id: str = None):
    """
    Insert or reference student, subject, compute risk status, and save record.
    Returns the newly created joined record.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Determine or generate student ID
    if not student_id:
        cursor.execute("SELECT student_id FROM students WHERE student_id LIKE 'ST-%';")
        existing_ids = cursor.fetchall()
        max_num = 1000
        for row in existing_ids:
            sid = row["student_id"]
            try:
                num = int(sid.replace("ST-", ""))
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
        student_id = f"ST-{max_num + 1}"

    if not email:
        clean_name = name.strip().lower().replace(" ", ".")
        email = f"{clean_name}@university.edu"

    # Insert or update student
    cursor.execute(
        """
        INSERT INTO students (student_id, full_name, email, batch_class, semester)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            full_name = excluded.full_name,
            batch_class = excluded.batch_class,
            semester = excluded.semester;
        """,
        (student_id, name.strip(), email, batch.strip(), semester.strip())
    )

    # Check or insert subject
    cursor.execute(
        "SELECT subject_id FROM subjects WHERE subject_name = ? AND semester = ?;",
        (subject.strip(), semester.strip())
    )
    row = cursor.fetchone()
    if row:
        subj_id = row["subject_id"]
    else:
        cursor.execute(
            "INSERT INTO subjects (subject_name, semester) VALUES (?, ?);",
            (subject.strip(), semester.strip())
        )
        subj_id = cursor.lastrowid

    # Compute risk status
    marks_val = float(marks)
    att_val = float(attendance)
    risk = calculate_risk_status(marks_val, att_val)

    # Insert into performance
    cursor.execute(
        """
        INSERT INTO performance (student_id, subject_id, marks_obtained, attendance_pct, risk_status)
        VALUES (?, ?, ?, ?, ?);
        """,
        (student_id, subj_id, marks_val, att_val, risk)
    )
    new_record_id = cursor.lastrowid
    conn.commit()

    # Fetch and return the newly saved record
    cursor.execute(
        """
        SELECT 
            p.record_id,
            s.student_id AS id,
            s.full_name AS name,
            s.email,
            s.batch_class AS batch,
            s.semester,
            sub.subject_name AS subject,
            p.marks_obtained AS marks,
            p.attendance_pct AS attendance,
            p.risk_status AS risk
        FROM performance p
        JOIN students s ON p.student_id = s.student_id
        JOIN subjects sub ON p.subject_id = sub.subject_id
        WHERE p.record_id = ?;
        """,
        (new_record_id,)
    )
    new_record = dict(cursor.fetchone())
    conn.close()

    return new_record
