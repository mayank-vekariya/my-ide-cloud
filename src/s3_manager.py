import boto3
import os

class S3Manager:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def upload_file(self, local_path, s3_key):
        """
        Uploads a file to an S3 bucket.

        :param local_path: Path to the local file to upload.
        :param s3_key: Key for the file in the S3 bucket.
        """
        try:
            self.s3_client.upload_file(local_path, self.bucket_name, s3_key)
            print(f"Uploaded {s3_key} to S3 bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error uploading file to S3: {e}")

    def upload_project_to_s3(self, local_dir, s3_prefix):
        """
        Uploads all files in a local directory to an S3 bucket, organized by the specified prefix.

        :param local_dir: Path to the local directory containing the project files.
        :param s3_prefix: Prefix for organizing the files in the S3 bucket.
        """
        for root, _, files in os.walk(local_dir):
            for filename in files:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, local_dir)
                s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")
                self.upload_file(local_path, s3_key)
