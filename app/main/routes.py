from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import current_user, login_required
from app.models import Project, db
import subprocess
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

main_bp = Blueprint('main', __name__, template_folder='templates/main')


@main_bp.route('/')
def home():
    return render_template('main/index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('main/dashboard.html', projects=projects)

def format_service_name(repo_url):
    """Simple helper to format GitHub repository URL into a service name compliant with Google Cloud Run constraints."""
    service_name = repo_url.split('/')[-1].replace('_', '-').lower()
    if not service_name[0].isalpha():
        service_name = 'a' + service_name
    return service_name[:49]  # Ensure service name is within the character limit

def run_command(command):
    """Execute a shell command and capture its output."""
    logging.info(f"Running command: {command}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    output, error = process.communicate()
    return output.strip(), error.strip(), process.returncode

def deploy_service_cli(service_name, github_repo):
    """Deploy a new service to Google Cloud Run using gcloud CLI commands."""
    image_url = "gcr.io/ide-cloud/my-code-server"
    project_id = "your-google-cloud-project-id"
    region = "us-central1"
    env_var = f"GITHUB_REPO={github_repo}"
    command = f"gcloud run deploy {service_name} --image {image_url} --update-env-vars {env_var} --platform managed --region {region} --allow-unauthenticated --format=json"
    output, error, exit_code = run_command(command)
    if exit_code == 0:
        return output  # JSON output from gcloud command
    else:
        logging.error(f"Error deploying service: {error}")
        return json.dumps({"error": error})

@main_bp.route('/deploy_git', methods=['POST'])
def deploy_from_git():
    github_repo = request.form.get('github_repo')
    service_name = format_service_name(github_repo)
    logging.info(f"Deploying GitHub repo {github_repo} as {service_name}")

    # Call the CLI deployment function
    result = deploy_service_cli(service_name, github_repo)
    print(result)

    # Process the result
    try:
        result_json = json.loads(result)
        if 'error' in result_json:
            flash(f"Deployment failed: {result_json['error']}", 'error')
        else:
            # Ensure that we are providing all necessary fields expected by the Project model
            new_project = Project(
                user_id=current_user.id,
                github_url=github_repo,
                s3_url=None,  # Assuming there is no S3 URL at this point
                status='deployed',  # Adjust based on actual deployment status
                url = result_json.get('status', {}).get('url'),  # Assuming the deployment result includes a URL; adjust as necessary
                project_name=service_name
            )
            db.session.add(new_project)
            db.session.commit()
            flash('Deployment initiated successfully!', 'success')
    except json.JSONDecodeError as e:
        flash(f"Failed to parse deployment results: {str(e)}", 'error')

    return redirect(url_for('main.dashboard'))



@main_bp.route('/view_container/<int:id>', methods=['GET'])
@login_required
def view_container(id):
    project = Project.query.get_or_404(id)
    return render_template('view_container.html', project=project)

@main_bp.route('/delete_container/<int:id>', methods=['POST'])
@login_required
def delete_container(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))
