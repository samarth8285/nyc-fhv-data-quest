from botocore.exceptions import ClientError


def check_s3_bucket_exists(s3_client, bucket_name):
    """
    Check if an S3 bucket exists.
    Parameters:
        s3_client (boto3.client): An S3 client object.
        bucket_name (str): The name of the S3 bucket to check for existence.
    Returns:
        bool: True if the bucket exists, False otherwise.
    """
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        print(f"There is no {bucket_name} bucket in S3.")
        return False


def create_s3_bucket(s3_client, bucket_name):
    """
    Create an S3 bucket if it does not already exist.
    Parameters:
        s3_client (boto3.client): An S3 client object.
        bucket_name (str): The name of the S3 bucket to be created.
    Returns:
        None
    """
    if not check_s3_bucket_exists(s3_client, bucket_name):
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    else:
        print(f"Bucket {bucket_name} already exists.")
    return


def upload_file_to_s3(s3_client, bucket_name, file_name, data, content_type):
    """
    Upload a file to an S3 bucket.
    Parameters:
        s3_client (boto3.client): An S3 client object.
        bucket_name (str): The name of the S3 bucket.
        file_name (str): The name of the file to be uploaded.
        data (bytes): The content of the file to be uploaded.
        content_type (str): The MIME type of the file being uploaded.
    Returns:
        bool: True if the file was uploaded successfully, False otherwise.
    """
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=data,
            ContentType=content_type,
        )
        print(f"File {file_name} uploaded successfully to bucket {bucket_name}.")
        return True

    except ClientError as e:
        print(f"Failed to upload file {file_name} to bucket {bucket_name}. Error: {e}")
        return False
