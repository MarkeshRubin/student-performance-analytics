# EduPulse | Student Performance Analytics Dashboard

A production-ready, full-stack Student Performance Analytics & Academic Intervention web application built with **Python (Flask)**, **SQLite**, **HTML5**, **Tailwind CSS**, **Chart.js**, and **Vanilla JavaScript**.

---

## 1. Project Folder Structure

```
student_performance_analytics/
├── app.py                     # Flask backend application & REST API endpoints
├── database.py                # SQLite schema definition, relational seeding & queries
├── requirements.txt           # Python dependency specifications
├── README.md                  # Comprehensive technical documentation & run guide
├── student_analytics.db       # Relational SQLite database (auto-generated)
└── templates/
    └── index.html             # Responsive Tailwind CSS + Chart.js dashboard UI
```

---

## 2. Database Schema & Architecture (`database.py`)

The application uses **SQLite** (`student_analytics.db`) with 4 relational tables:

1. **`students`**
   - `student_id` (`TEXT PRIMARY KEY`): Unique student identifier (e.g. `ST-1001`).
   - `full_name` (`TEXT NOT NULL`): Student's full name.
   - `email` (`TEXT NOT NULL`): Institutional email address.
   - `batch_class` (`TEXT NOT NULL`): Class batch (e.g. `CS-A`, `CS-B`, `IT-A`).
   - `semester` (`TEXT NOT NULL`): Academic semester (e.g. `Sem 1`, `Sem 2`, `Sem 3`).

2. **`subjects`**
   - `subject_id` (`INTEGER PRIMARY KEY AUTOINCREMENT`): Auto-incremented identifier.
   - `subject_name` (`TEXT NOT NULL`): Core subject title (e.g. `Data Structures`).
   - `semester` (`TEXT NOT NULL`): Associated semester.

3. **`assessments`**
   - `assessment_id` (`INTEGER PRIMARY KEY AUTOINCREMENT`): Auto-incremented identifier.
   - `subject_id` (`INTEGER FK`): References `subjects(subject_id)`.
   - `assessment_name` (`TEXT NOT NULL`): Milestone name (`Quiz 1`, `Assignment 1`, `Midterm`, etc.).
   - `max_marks` (`REAL NOT NULL`): Maximum possible assessment marks.

4. **`performance`**
   - `record_id` (`INTEGER PRIMARY KEY AUTOINCREMENT`): Unique performance entry ID.
   - `student_id` (`TEXT FK`): References `students(student_id)`.
   - `subject_id` (`INTEGER FK`): References `subjects(subject_id)`.
   - `marks_obtained` (`REAL NOT NULL`): Percentage score achieved (0–100).
   - `attendance_pct` (`REAL NOT NULL`): Class attendance percentage (0–100).
   - `risk_status` (`TEXT NOT NULL`): Computed institutional risk classification.

### Risk Status Classification Formula
Student risk classification is dynamically computed based on institutional thresholds:
- **High Risk**: `marks < 50` OR `attendance < 60`
- **Warning**: `marks < 70` OR `attendance < 75`
- **Safe**: Otherwise (`marks >= 70` AND `attendance >= 75`)

### Automatic Relational Seeding
When the database is empty, `database.init_db()` automatically seeds:
- 4 Core Subjects (`Data Structures`, `Mathematics III`, `Database Systems`, `Operating Systems`)
- 5 Standard Assessments per subject (`Quiz 1`, `Assignment 1`, `Midterm`, `Assignment 2`, `Final Exam`)
- 10 Realistic Student Performance records across batches (`CS-A`, `CS-B`, `IT-A`) and semesters (`Sem 1`, `Sem 2`, `Sem 3`).

---

## 3. Backend REST API Endpoints (`app.py`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main responsive HTML5 analytics dashboard. |
| `GET` | `/api/students` | Returns all joined student performance records as JSON. |
| `POST` | `/api/students` | Accepts a new student record, computes `risk_status`, saves to SQLite, and returns the record. |
| `GET` | `/api/export/csv` | Streams the full database dataset as a downloadable CSV file. |
| `GET` | `/api/summary` | Returns aggregated cohort KPIs and tier distributions. |

### Sample `POST /api/students` Request
```json
{
  "name": "Jordan Lee",
  "batch": "CS-A",
  "semester": "Sem 2",
  "subject": "Database Systems",
  "marks": 64.0,
  "attendance": 72.0
}
```

---

## 4. Frontend Dashboard Features (`templates/index.html`)

1. **Sidebar Dynamic Filters:**
   - Real-time dropdown filters for **Semester**, **Batch/Class**, **Core Subject**, and **Warning Status**.
   - Includes a **"Reset All Filters"** button that synchronizes all table rows, KPIs, and charts in real time.
2. **KPI Summary Cards:**
   - **Total Records:** Live count of currently displayed records.
   - **Average Score:** Average marks with academic letter grade badge (`A+`, `A`, `B`, `C`, `F`).
   - **Average Attendance:** Overall attendance with status range indicators.
   - **At-Risk Alerts:** Immediate count of students needing intervention (`High Risk` + `Warning`).
3. **Interactive Charts (Chart.js):**
   - **Grouped Bar Chart:** Subject-wise comparison between Average Marks and Average Attendance.
   - **Donut Chart:** Cohort risk distribution across `Safe`, `Warning`, and `High Risk` tiers.
   - **Trend Line Chart:** Cohort assessment trajectory from `Quiz 1` to `Final Exam`.
4. **"What-If" Student Success Simulator:**
   - Interactive sliders for Attendance Rate, Assignment Score, and Midterm Score.
   - Weighted predictive formula (`30% Attendance + 35% Assignment + 35% Midterm`) calculating real-time predicted final score, letter grade, and risk status.
5. **Drill-Down Student Roster Table:**
   - Live search input matching student name, ID, or subject.
   - Clicking any student row opens a detailed progress modal with avatar, contact info, assessment profile, and an interactive **Faculty Intervention Checklist**.
   - Includes a **"Print Report Card"** button styled with `@media print` rules.
6. **Add Record Modal & Live Backend Sync:**
   - Form modal with client-side & server-side validation.
   - Sends `POST /api/students` to Flask backend, writes to SQLite, and instantly updates all dashboard visuals without requiring a page reload.
7. **CSV Export:**
   - Generates and downloads a `.csv` file containing the currently filtered dataset.

---

## 5. Setup & Execution Instructions

### Step 1: Install Dependencies
Ensure Python 3.10+ is installed, then run:
```bash
pip install -r requirements.txt
```

### Step 2: Start the Flask Application
Run the backend server on port 5000:
```bash
python app.py
```

### Step 3: Access the Dashboard
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```
