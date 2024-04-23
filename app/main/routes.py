from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import Project, db  # Ensure Project model is defined in models.py

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id)  # Assuming user association
    return render_template('main/dashboard.html', projects=projects)

@main_bp.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        new_project = Project(name=project_name, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('main/create_project.html')
