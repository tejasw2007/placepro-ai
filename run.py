import os
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User, JobDrive

app = create_app()

def seed_initial_records():
    """Initializes tables and seeds a default admin and sample placement drive."""
    with app.app_context():
        db.create_all()

        # Check if an admin exists, otherwise seed
        if not User.query.filter_by(email='admin@placepro.edu').first():
            admin_user = User(
                full_name='Placement Administrator',
                email='admin@placepro.edu',
                password_hash=generate_password_hash('Admin@123'),
                role='admin'
            )
            db.session.add(admin_user)

            # Sample job drive
            sample_drive = JobDrive(
                company_name='Nova Analytics',
                role_title='Associate Data Analyst',
                description='Looking for candidates with strong Python, SQL, and data analysis fundamentals.',
                required_skills='python, sql, excel, data analysis, statistics',
                min_cgpa=7.0,
                package_lpa=6.5,
                deadline='2026-11-30'
            )
            db.session.add(sample_drive)
            db.session.commit()
            print("[INFO] Database initialized with default admin and sample drive.")

if __name__ == '__main__':
    seed_initial_records()
    app.run(host='0.0.0.0', port=5000, debug=True)