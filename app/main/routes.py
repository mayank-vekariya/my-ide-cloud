from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import current_user, login_required
from app.models import Project, db
import subprocess
import shlex

main_bp = Blueprint('main', __name__, template_folder='templates/main')

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('main/dashboard.html', projects=projects)

import subprocess
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO)

def run_command(command):
    """Run a shell command and yield output lines using a safer approach with detailed logging."""
    logging.info(f"Executing command: {command}")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        for line in process.stdout:
            logging.info(f"Output: {line.strip()}")
            yield line
        process.wait()
        if process.returncode != 0:
            # Log stderr if the process failed
            err = process.stderr.read()
            logging.error(f"Error: {err.strip()}")
            yield f"Error: {err.strip()}"
    except Exception as e:
        logging.error(f"Exception during command execution: {str(e)}")
        yield f"Exception: {str(e)}"

@main_bp.route('/deploy', methods=['POST'])
def deploy():
    github_repo = request.form.get('github_repo')
    command = f"gcloud run deploy my-service --image gcr.io/ide-cloud/my-code-server --update-env-vars GITHUB_REPO={github_repo} --platform managed --region us-central1 --allow-unauthenticated"
    def generate():
        for output in run_command(command):
            yield f"data:{output}\n\n"
        yield "data:Deployment completed successfully!\n\n"
    return Response(generate(), mimetype='text/event-stream')



@main_bp.route('/clone_project', methods=['GET', 'POST'])
@login_required
def clone_project():
    if request.method == 'POST':
        github_repo = request.form['github_repo']
        try:
            deploy_to_cloud_run(github_repo)
            flash('Deployment initiated successfully!', 'success')
        except subprocess.CalledProcessError as e:
            flash(f'Failed to initiate deployment: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))
    return render_template('main/clone_project.html')

def deploy_to_cloud_run(github_repo):
    gcloud_path = "C:\\Program Files (x86)\\Google\\Cloud SDK\\google-cloud-sdk\\bin"  # Full path to gcloud
    project_id = "ide-cloud"
    service_name = "my-code-server"
    image_url = f"gcr.io/{project_id}/{service_name}"
    region = "us-central1"
    command = [
        gcloud_path, "run", "deploy", service_name,
        "--image", image_url,
        "--update-env-vars", f"GITHUB_REPO={github_repo}",
        "--platform", "managed",
        "--region", region,
        "--allow-unauthenticated"
    ]
    subprocess.run(command, check=True)


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
import logging


