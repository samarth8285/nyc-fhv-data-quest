import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv


class S3Util:
    def __init__(self):
        load_dotenv()
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_ACCESS_SECRET")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_REGION,
        )

    def get_s3_client(self):
        return self.s3_client

    def check_s3_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.S3_BUCKET_NAME)
            return True
        except ClientError:
            print("There is no bucket with the name " + self.S3_BUCKET_NAME)
            return False

    def create_s3_bucket(self):

        if not self.check_s3_bucket_exists():
            self.s3_client.create_bucket(Bucket=self.S3_BUCKET_NAME)
            print("Bucket " + self.S3_BUCKET_NAME + " created successfully.")
        else:
            print("Bucket " + self.S3_BUCKET_NAME + " already exists.")

    def upload_file_to_s3(self, file_name, data, content_type):
        s3_response = self.s3_client.put_object(
            Bucket=self.S3_BUCKET_NAME,
            Key=file_name,
            Body=data,
            ContentType=content_type,
        )
        return s3_response
