# import os
# from git import Repo
#
#
# class GitManager:
#     @staticmethod
#     def clone_repo(github_url, dest_dir):
#         """
#         Clones a GitHub repository to the specified destination directory.
#
#         Parameters:
#         - github_url (str): The URL of the GitHub repository.
#         - dest_dir (str): The local directory where the repository will be cloned.
#
#         Returns:
#         - bool: True if cloning was successful, False otherwise.
#         """
#         try:
#             Repo.clone_from(github_url, dest_dir)
#             print(f"Repository cloned successfully to {dest_dir}")
#             return True
#         except Exception as e:
#             print(f"Error cloning repository: {e}")
#             return False

import os
import shutil
import boto3
from git import Repo

import stat

class GitManager:
    @staticmethod
    def clone_repo_to_s3(github_url, s3_bucket, s3_prefix):
        temp_dir = "./temp_repo"
        try:
            Repo.clone_from(github_url, temp_dir)
            print(f"Repository cloned successfully to {temp_dir}")

            s3_client = boto3.client('s3')
            for root, dirs, files in os.walk(temp_dir):
                for filename in files:
                    local_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(local_path, temp_dir)
                    s3_path = os.path.join(s3_prefix, relative_path)
                    s3_client.upload_file(local_path, s3_bucket, s3_path)
                    print(f"Uploaded {s3_path} to S3 bucket {s3_bucket}")

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            # Make sure all files and directories are writable before removing them
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for name in dirs:
                    os.chmod(os.path.join(root, name), stat.S_IWRITE)
                for name in files:
                    os.chmod(os.path.join(root, name), stat.S_IWRITE)
            shutil.rmtree(temp_dir)

import requests
import boto3

def download_repo_and_upload_to_s3(github_url, s3_bucket, s3_prefix):
    """
    Download a GitHub repository as a zip file and upload it to S3.

    :param github_url: URL of the GitHub repo (format: https://github.com/user/repo)
    :param s3_bucket: The name of the S3 bucket.
    :param s3_prefix: The prefix under which to store the repo contents in the bucket.
    """
    # Convert GitHub URL to ZIP download URL
    parts = github_url.rstrip("/").split("/")
    user, repo = parts[-2], parts[-1]
    zip_url = f"https://github.com/{user}/{repo}/archive/refs/heads/main.zip"

    # Download the ZIP file
    response = requests.get(zip_url)
    zip_content = response.content

    # Define the ZIP file path in S3
    s3_path = f"{s3_prefix}/{repo}.zip"

    # Upload the ZIP file to S3
    s3 = boto3.client('s3')
    s3.put_object(Bucket=s3_bucket, Key=s3_path, Body=zip_content)
    print(f"Uploaded {s3_path} to S3 bucket {s3_bucket}")

# Example usage
github_url = "https://github.com/mayank-vekariya/react-app"
s3_bucket = "my-ide-s3"
s3_prefix = "user/repo"
download_repo_and_upload_to_s3(github_url, s3_bucket, s3_prefix)

# Example usage
# if __name__ == "__main__":
#     github_url = "https://github.com/mayank-vekariya/react-app"
#     s3_bucket = "my-ide-s3"
#     s3_prefix = "user/repo"
#     GitManager.clone_repo_to_s3(github_url, s3_bucket, s3_prefix)
