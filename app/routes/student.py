from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import JobDrive, Application, User
from app.utils import calculate_resume_match, calculate_readiness_score
from app import db

student_bp = Blueprint('student', __name__)

@student_bp.before_request
@login_required
def check_student_role():
    if current_user.role != 'student':
        flash('Access restricted to students.', 'danger')
        return redirect(url_for('auth.home'))

@student_bp.route('/dashboard')
def dashboard():
    applied_apps = Application.query.filter_by(user_id=current_user.id).all()
    open_drives = JobDrive.query.filter_by(status='Open').all()
    
    # Calculate match for open drives
    drives_with_match = []
    for d in open_drives:
        analysis = calculate_resume_match(current_user.skills, current_user.resume_summary, d.required_skills)
        drives_with_match.append({
            "drive": d,
            "match": analysis["match_score"]
        })
    drives_with_match.sort(key=lambda x: x['match'], reverse=True)

    return render_template(
        'student/dashboard.html',
        applications=applied_apps,
        recommended_drives=drives_with_match[:4]
    )

@student_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        current_user.degree = request.form.get('degree')
        current_user.passing_year = int(request.form.get('passing_year', 2026))
        current_user.cgpa = float(request.form.get('cgpa', 0.0))
        current_user.skills = request.form.get('skills', '').strip()
        current_user.resume_summary = request.form.get('resume_summary', '').strip()

        # Update readiness score
        current_user.readiness_score = calculate_readiness_score(
            current_user.cgpa, current_user.skills, current_user.resume_summary
        )

        db.session.commit()
        flash('Your academic profile and readiness score have been updated!', 'success')
        return redirect(url_for('student.profile'))

    return render_template('student/profile.html')

@student_bp.route('/analyzer', methods=['GET', 'POST'])
def analyzer():
    """AI Resume Analyzer and Company Recommendation Engine"""
    recommendations = []
    analysis_result = None

    if request.method == 'POST':
        custom_summary = request.form.get('resume_summary', '').strip()
        custom_skills = request.form.get('skills', '').strip()

        # Update if user wants to save to profile
        if request.form.get('save_to_profile'):
            current_user.resume_summary = custom_summary
            current_user.skills = custom_skills
            current_user.readiness_score = calculate_readiness_score(
                current_user.cgpa, custom_skills, custom_summary
            )
            db.session.commit()

        drives = JobDrive.query.filter_by(status='Open').all()
        for drive in drives:
            res = calculate_resume_match(custom_skills, custom_summary, drive.required_skills)
            recommendations.append({
                "drive": drive,
                "score": res["match_score"],
                "matched": res["matched"],
                "missing": res["missing"]
            })

        recommendations.sort(key=lambda x: x['score'], reverse=True)
        analysis_result = True

    return render_template('student/analyzer.html', recommendations=recommendations, analyzed=analysis_result)

@student_bp.route('/drives')
def drives():
    all_drives = JobDrive.query.filter_by(status='Open').all()
    applied_ids = [app.drive_id for app in current_user.applications]

    drive_list = []
    for d in all_drives:
        res = calculate_resume_match(current_user.skills, current_user.resume_summary, d.required_skills)
        drive_list.append({
            "drive": d,
            "match": res["match_score"],
            "has_applied": d.id in applied_ids,
            "eligible": current_user.cgpa >= d.min_cgpa
        })

    return render_template('student/drives.html', drives=drive_list)

@student_bp.route('/apply/<int:drive_id>', methods=['POST'])
def apply_drive(drive_id):
    existing = Application.query.filter_by(user_id=current_user.id, drive_id=drive_id).first()
    if existing:
        flash('You have already submitted an application for this drive.', 'warning')
        return redirect(url_for('student.drives'))

    drive = JobDrive.query.get_or_404(drive_id)
    if current_user.cgpa < drive.min_cgpa:
        flash(f'CGPA below requirement ({drive.min_cgpa}). Cannot apply.', 'danger')
        return redirect(url_for('student.drives'))

    match_res = calculate_resume_match(current_user.skills, current_user.resume_summary, drive.required_skills)
    new_app = Application(
        user_id=current_user.id,
        drive_id=drive.id,
        match_percentage=match_res['match_score'],
        status='Under Review'
    )
    db.session.add(new_app)
    db.session.commit()
    flash(f'Application successfully submitted for {drive.company_name}!', 'success')
    return redirect(url_for('student.dashboard'))