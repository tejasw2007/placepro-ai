import os
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

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Self-healing database initialization on launch
    with app.app_context():
        try:
            db.create_all()
            # Seed default admin if absent
            if not User.query.filter_by(email='admin@placepro.edu').first():
                admin_user = User(
                    full_name='Placement Officer',
                    email='admin@placepro.edu',
                    password_hash=generate_password_hash('Admin@123'),
                    role='admin'
                )
                db.session.add(admin_user)

                # Seed initial drive
                drive = JobDrive(
                    company_name='Nova Analytics & Tech',
                    role_title='Associate Data Analyst',
                    description='Analyzing data patterns, managing SQL databases, and building predictive reports.',
                    required_skills='python, sql, excel, data analysis, statistics',
                    min_cgpa=6.5,
                    package_lpa=6.5,
                    deadline='2026-11-30'
                )
                db.session.add(drive)
                db.session.commit()
                print("[INFO] Database successfully seeded.")
        except Exception as e:
            print(f"[WARNING] Database sync error caught: {e}")

    return app