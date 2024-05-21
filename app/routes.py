from flask import Blueprint, render_template, flash, redirect, url_for, request
from .models import User, Project, Task
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from datetime import datetime
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects, tasks=tasks)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main_bp.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        project = Project(name=name, description=description, user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('project_form.html')

@main_bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        priority = request.form['priority']
        project_id = request.form['project_id']
        task = Task(name=name, description=description, deadline=deadline, priority=priority, status='To Do', user_id=current_user.id, project_id=project_id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('task_form.html', projects=projects)

@main_bp.route('/timeline')
@login_required
def timeline():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.deadline).all()
    return render_template('timeline.html', projects=projects, tasks=tasks)