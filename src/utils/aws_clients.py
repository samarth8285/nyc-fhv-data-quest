from dotenv import load_dotenv
import os
import boto3

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_ACCESS_SECRET")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def get_s3_client():
    s3_client = boto3.client("s3")
    return s3_client


def get_iam_client():
    iam_client = boto3.client("iam")
    return iam_client


def get_lambda_client():
    lambda_client = boto3.client("lambda")
    return lambda_client


def get_events_manager_client():
    events_manager_client = boto3.client("events")
    return events_manager_client


def get_secrets_manager_client():
    secrets_manager_client = boto3.client("secretsmanager")
    return secrets_manager_client


def get_ecr_client():
    ecr_client = boto3.client("ecr")
    return ecr_client
