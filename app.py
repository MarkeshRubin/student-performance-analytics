"""
app.py - Flask Web Application & REST API for Student Performance Analytics Dashboard
"""

import os
import io
import pandas as pd
from flask import Flask, render_template, request, jsonify, Response, send_file
import database

# Initialize Flask application
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'edu-pulse-analytics-secret-key-2026'

# Ensure database is initialized on startup
database.init_db()


@app.route('/')
def index():
    """Render and serve the interactive analytics dashboard."""
    return render_template('index.html')


@app.route('/api/students', methods=['GET'])
def get_students():
    """
    REST API endpoint: Returns all joined student performance records as JSON.
    """
    try:
        records = database.get_all_student_performance()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch student records", "details": str(e)}), 500


@app.route('/api/students', methods=['POST'])
def add_student():
    """
    REST API endpoint: Accepts new student performance submissions,
    inserts into SQLite with computed risk status, and returns the saved record.
    """
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({"error": "Invalid request body. Expected JSON or form data."}), 400

        name = data.get("name") or data.get("full_name")
        batch = data.get("batch") or data.get("batch_class")
        semester = data.get("semester")
        subject = data.get("subject") or data.get("subject_name")
        marks = data.get("marks") or data.get("marks_obtained")
        attendance = data.get("attendance") or data.get("attendance_pct")
        email = data.get("email")

        # Validation
        if not all([name, batch, semester, subject, marks is not None, attendance is not None]):
            return jsonify({
                "error": "Missing required fields: name, batch, semester, subject, marks, attendance"
            }), 400

        try:
            marks_val = float(marks)
            att_val = float(attendance)
            if not (0 <= marks_val <= 100) or not (0 <= att_val <= 100):
                return jsonify({"error": "Marks and attendance must be numbers between 0 and 100."}), 400
        except ValueError:
            return jsonify({"error": "Marks and attendance must be valid numeric values."}), 400

        new_record = database.add_student_performance(
            name=name,
            batch=batch,
            semester=semester,
            subject=subject,
            marks=marks_val,
            attendance=att_val,
            email=email
        )

        return jsonify({
            "message": "Student performance record created successfully",
            "record": new_record
        }), 201

    except Exception as e:
        return jsonify({"error": "Failed to create student record", "details": str(e)}), 500


@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """
    Export all current student performance records as a downloadable CSV using pandas.
    """
    try:
        records = database.get_all_student_performance()
        if not records:
            return Response("No student data available", mimetype="text/csv")

        df = pd.DataFrame(records)
        df.rename(columns={
            "id": "Student ID",
            "name": "Full Name",
            "email": "Email Address",
            "batch": "Batch / Class",
            "semester": "Semester",
            "subject": "Core Subject",
            "marks": "Marks Obtained (%)",
            "attendance": "Attendance (%)",
            "risk": "Risk Status"
        }, inplace=True)

        # Drop internal record_id if present
        if "record_id" in df.columns:
            df.drop(columns=["record_id"], inplace=True)

        output = io.BytesIO()
        df.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)

        return send_file(
            output,
            mimetype="text/csv",
            as_attachment=True,
            download_name="student_performance_analytics.csv"
        )
    except Exception as e:
        return jsonify({"error": "Failed to generate CSV export", "details": str(e)}), 500


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """
    Optional helper endpoint: Returns aggregate statistics across all records.
    """
    try:
        records = database.get_all_student_performance()
        if not records:
            return jsonify({
                "total": 0,
                "avg_marks": 0,
                "avg_attendance": 0,
                "risk_counts": {"Safe": 0, "Warning": 0, "High Risk": 0}
            }), 200

        total = len(records)
        avg_marks = round(sum(r['marks'] for r in records) / total, 1)
        avg_att = round(sum(r['attendance'] for r in records) / total, 1)
        risk_counts = {"Safe": 0, "Warning": 0, "High Risk": 0}
        for r in records:
            risk = r.get("risk", "Safe")
            risk_counts[risk] = risk_counts.get(risk, 0) + 1

        return jsonify({
            "total": total,
            "avg_marks": avg_marks,
            "avg_attendance": avg_att,
            "risk_counts": risk_counts
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to calculate summary", "details": str(e)}), 500


if __name__ == '__main__':
    # Initialize DB before starting server
    database.init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Student Performance Analytics Dashboard on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
