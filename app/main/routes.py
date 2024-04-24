from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required  # Ensure login management is imported
from app.models import Project, db  # Assuming Project model is defined correctly

main_bp = Blueprint('main', __name__, template_folder='templates/main')

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required  # Ensure that only logged-in users can access the dashboard
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()  # Make sure to call `.all()`
    return render_template('main/dashboard.html', projects=projects)

@main_bp.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        new_project = Project(name=project_name, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('main/create_project.html')
