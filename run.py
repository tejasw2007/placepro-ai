from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    from app.models import User, JobDrive

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # AUTO-INITIALIZE DATABASE TABLES ON STARTUP
    with app.app_context():
        db.create_all()

        # Seed default admin if missing
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
            print("[INFO] Database tables auto-created and seeded successfully.")

    return app