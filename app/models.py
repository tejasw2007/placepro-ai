from datetime import datetime, timezone
from flask_login import UserMixin
from app import db

def utc_now():
    return datetime.now(timezone.utc)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now)

    degree = db.Column(db.String(80), nullable=True, default='BCA')
    passing_year = db.Column(db.Integer, nullable=True, default=2026)
    cgpa = db.Column(db.Float, nullable=True, default=0.0)
    skills = db.Column(db.Text, nullable=True, default='')
    resume_summary = db.Column(db.Text, nullable=True, default='')
    readiness_score = db.Column(db.Float, nullable=True, default=0.0)

    applications = db.relationship('Application', backref='applicant', lazy=True, cascade="all, delete-orphan")

class JobDrive(db.Model):
    __tablename__ = 'job_drives'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    role_title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text, nullable=False)
    min_cgpa = db.Column(db.Float, default=6.0)
    package_lpa = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now)

    applications = db.relationship('Application', backref='drive', lazy=True, cascade="all, delete-orphan")

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('job_drives.id'), nullable=False)
    applied_date = db.Column(db.DateTime(timezone=True), default=utc_now)
    match_percentage = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(30), default='Under Review')