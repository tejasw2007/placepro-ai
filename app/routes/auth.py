from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/health')
def health_check():
    return "OK", 200

@auth_bp.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email is already registered. Please sign in.', 'warning')
            return redirect(url_for('auth.login'))

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=generate_password_hash(password),
            role='student'
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please sign in to your student portal.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email address or password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('auth.login'))