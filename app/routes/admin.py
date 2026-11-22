from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import JobDrive, Application, User
from app import db

admin_bp = Blueprint('admin', __name__)

def safe_float(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default

@admin_bp.before_request
@login_required
def check_admin_role():
    if current_user.role != 'admin':
        flash('Restricted area. Administrator credentials required.', 'danger')
        return redirect(url_for('auth.home'))

@admin_bp.route('/dashboard')
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_drives = JobDrive.query.count()
    total_applications = Application.query.count()
    shortlisted_count = Application.query.filter_by(status='Shortlisted').count()

    recent_drives = JobDrive.query.order_by(JobDrive.created_at.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_drives=total_drives,
        total_applications=total_applications,
        shortlisted_count=shortlisted_count,
        drives=recent_drives
    )

@admin_bp.route('/drives/new', methods=['GET', 'POST'])
def new_drive():
    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        role_title = request.form.get('role_title', '').strip()
        description = request.form.get('description', '').strip()
        required_skills = request.form.get('required_skills', '').strip()
        min_cgpa = safe_float(request.form.get('min_cgpa'), 6.0)
        package_lpa = safe_float(request.form.get('package_lpa'), 3.5)
        deadline = request.form.get('deadline', '').strip()

        if not company_name or not role_title or not required_skills or not deadline:
            flash('Please fill in all required drive fields.', 'danger')
            return render_template('admin/new_drive.html')

        drive = JobDrive(
            company_name=company_name,
            role_title=role_title,
            description=description,
            required_skills=required_skills,
            min_cgpa=min_cgpa,
            package_lpa=package_lpa,
            deadline=deadline
        )
        db.session.add(drive)
        db.session.commit()
        flash('New placement drive published successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/new_drive.html')

@admin_bp.route('/applicants')
def applicants():
    all_apps = Application.query.order_by(Application.applied_date.desc()).all()
    return render_template('admin/applicants.html', applications=all_apps)

@admin_bp.route('/application/<int:app_id>/status', methods=['POST'])
def update_status(app_id):
    app_record = db.get_or_404(Application, app_id)
    new_status = request.form.get('status')
    if new_status in ['Under Review', 'Shortlisted', 'Rejected']:
        app_record.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}.', 'success')
    return redirect(url_for('admin.applicants'))