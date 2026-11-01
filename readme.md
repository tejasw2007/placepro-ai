# PlacePro AI — Smart Placement Management System 🚀

An AI-powered campus recruitment and placement management web platform built with **Python (Flask)**, **PostgreSQL**, and a modern **Glassmorphism UI** with CSS animations. The platform automates campus drives, evaluates student placement readiness, analyzes resume summaries, and matches candidates with corporate openings.

---

## 🌟 Key Features

### 👨‍🎓 Student Portal
- **Profile & Readiness Prediction:** Dynamically calculates a 0–100% Placement Readiness score based on academic CGPA (40% weight) and technical skill density (60% weight).
- **AI Resume & Skill Analyzer:** Compares resume summary keywords against drive requirements, highlighting matched proficiencies and missing skills.
- **Drive Discovery & Direct Application:** Instant eligibility checks against minimum CGPA cutoffs with one-click drive applications.
- **Application Tracking:** Real-time visibility into application review status (*Under Review*, *Shortlisted*, *Rejected*).

### 🛡️ Admin Portal
- **Operations Dashboard:** Centralized tracking of registered students, published drives, submitted applications, and shortlisted candidates.
- **Placement Drive Management:** Publish recruitment openings with company details, role descriptions, required skills, package (LPA), minimum CGPA cutoffs, and application deadlines.
- **Applicant Screening:** Review candidate profiles, examine AI match percentages, and update candidate hiring status.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python 3.11+, Flask (Application Factory & Blueprints), Flask-Login, Werkzeug
- **Database & ORM:** PostgreSQL (Production) / SQLite (Fallback), Flask-SQLAlchemy, Psycopg2-binary
- **Frontend:** HTML5, CSS3 Glassmorphism, CSS Custom Properties, Vanilla JavaScript
- **Deployment:** Gunicorn WSGI, Render / Linux VPS (systemd + Nginx)

---

## 📂 Project Structure

```text
placepro-ai/
├── run.py                      # Application entry point & startup runner
├── config.py                   # Resilient database & environment configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
│
├── app/
│   ├── __init__.py             # App factory, database initialization, & blueprints
│   ├── models.py               # SQLAlchemy schemas (User, JobDrive, Application)
│   ├── utils.py                # AI keyword matching & readiness algorithms
│   │
│   ├── routes/
│   │   ├── auth.py             # Login, registration, & logout routes
│   │   ├── student.py          # Student portal & resume analysis routes
│   │   └── admin.py            # Drive posting & candidate screening routes
│   │
│   ├── static/
│   │   ├── css/style.css       # Glassmorphism design system & animations
│   │   └── js/main.js          # Dynamic frontend UI scripts
│   │
│   └── templates/
│       ├── base.html           # Shared layout with animated background blobs
│       ├── index.html          # Public landing page
│       ├── login.html          # Unified authentication page
│       ├── register.html       # Role-based registration page
│       ├── student/            # Student portal pages (Dashboard, Profile, Analyzer, Drives)
│       └── admin/              # Admin portal pages (Dashboard, New Drive, Applicants)