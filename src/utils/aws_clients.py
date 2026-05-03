import boto3

def get_s3_client():
    """
    Get an S3 client using boto3.
    Returns:
        boto3.client: An S3 client object.
    """
    s3_client = boto3.client("s3")
    return s3_client


def get_iam_client():
    """
    Get an IAM client using boto3.
    Returns:
        boto3.client: An IAM client object.
    """
    iam_client = boto3.client("iam")
    return iam_client


def get_lambda_client():
    """
    Get a Lambda client using boto3.
    Returns:
        boto3.client: A Lambda client object.
    """
    lambda_client = boto3.client("lambda")
    return lambda_client


def get_events_manager_client():
    """
    Get an Events Manager client using boto3.
    Returns:
        boto3.client: An Events Manager client object.
    """
    events_manager_client = boto3.client("events")
    return events_manager_client


def get_secrets_manager_client():
    """
    Get a Secrets Manager client using boto3.
    Returns:
        boto3.client: A Secrets Manager client object.
    """
    secrets_manager_client = boto3.client("secretsmanager")
    return secrets_manager_client


def get_ecr_client():
    """
    Get an ECR client using boto3.
    Returns:
        boto3.client: An ECR client object.
    """
    ecr_client = boto3.client("ecr")
    return ecr_client
