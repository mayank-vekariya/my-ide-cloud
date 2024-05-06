from google.cloud import run_v2
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPICallError

import subprocess
import json
import logging

PROJECT_ID = 'ide-cloud'
LOCATION = 'us-central1'  # or other location
IMAGE_URL = 'gcr.io/ide-cloud/my-code-server'
KEY_PATH = 'C:\\code\\my-ide-cloud\\app\\Gcloud-keys\\ide-cloud-638ae14ceb55.json'

# Authentication and client setup
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = run_v2.ServicesClient(credentials=credentials)

from google.cloud.run_v2 import EnvVar  # Ensure you import EnvVar



def run_command(command):
    """Execute a shell command and return the output, errors, and exit code."""
    logging.info(f"Executing command: {command}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    output, error = process.communicate()
    return output, error, process.returncode

def deploy_service_cli(service_name, github_repo):
    """Deploy a new service to Google Cloud Run using CLI and allow unauthenticated access."""
    image_url = "gcr.io/ide-cloud/my-code-server"  # Ensure this is set correctly
    region = "us-central1"
    project_id = "your-google-cloud-project-id"
    env_var = f"GITHUB_REPO={github_repo}"

    # Deploy the service
    deploy_command = f"gcloud run deploy {service_name} --image {image_url} --update-env-vars {env_var} " \
                     f"--platform managed --region {region} --allow-unauthenticated --format=json"
    output, error, exit_code = run_command(deploy_command)

    if exit_code != 0:
        logging.error(f"Deployment failed: {error}")
        return json.dumps({'error': error.strip()})

    # After successful deployment, retrieve service details
    get_service_command = f"gcloud run services describe {service_name} --format=json --region {region}"
    service_details, error, exit_code = run_command(get_service_command)

    if exit_code != 0:
        logging.error(f"Failed to retrieve service details: {error}")
        return json.dumps({'error': error.strip()})

    return service_details  # This already returns JSON formatted output from gcloud





def get_service_details(service_name):
    """Retrieve details about a specific service deployed on Google Cloud Run in JSON format."""
    service_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/services/{service_name}"
    try:
        service = client.get_service(name=service_path)
        return json.dumps(service._pb.SerializeToString().decode('utf-8'))  # Serialize protobuf to JSON
    except GoogleAPICallError as e:
        return json.dumps({'error': str(e)})

def delete_service(service_name):
    """Delete a service from Google Cloud Run and return the operation status in JSON format."""
    service_path = f"projects/{PROJECT_ID}/locations/{LOCATION}/services/{service_name}"
    try:
        operation = client.delete_service(name=service_path)
        result = operation.result()  # Waits for the delete operation to complete
        return json.dumps(result._pb.SerializeToString().decode('utf-8'))  # Serialize protobuf to JSON
    except GoogleAPICallError as e:
        return json.dumps({'error': str(e)})
